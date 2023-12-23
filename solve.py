#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a Solution wrapper that orchestrates fetching the problems, generating, and running solutions 
either self-written, or generated via one of OpenAI, Gemini, or Claude's APIs. Handles repeated attempts
with suggestions to refine generated solutions if wrong or less efficient. Stores all solutions in the DB
and handles creating the solution subfolders for each problem.
"""
import logging
import time
import importlib
import sys
from enum import Enum

from db_utils import execute_query
from utils import transform_time_to_string, OpenAIClient

import click


MAX_ANSWER_CODE_CHAR_LENGTH = 2 * 1000 * 1000

class Engine(Enum):
    SELF = 1
    OPENAI = 2
    GEMINI = 3
    CLAUDE = 4
    MISTRAL = 5

    def __str__(self):
        return str(self.name.lower())
    
class SolutionMode(Enum):
    MANUAL = 1
    EULER = 2

class Solution:
    def __init__(self, mode:SolutionMode = SolutionMode.MANUAL, problem_id:int = None, engine:Engine = Engine.SELF):
        self.mode = mode
        self.engine = engine
        self.start_client()

        # init values
        if mode == SolutionMode.MANUAL:
            self.add_new_problem()
            self.problem_id = execute_query(f"SELECT id FROM problems ORDER BY id DESC LIMIT 1;")[0][0]
            logging.info(f"Creating problem with ID: {self.problem_id}")
        elif mode == SolutionMode.EULER:
            self.problem_id = problem_id
            self.expected_answer = self.get_expected_answer()
            self.assignment_text = self.get_assignment_text()

        # defaults
        self.answer_code = None
        self.is_executable = 0
        self.is_correct = 0
        self.walltime = None
        self.walltime_string = None
        self.memory = None

        # run
        self.generate_answer_code()
        self.run_solution()

    def get_problem_id(self):
        return self.problem_id
    
    def get_engine(self):
        return self.engine
    
    def start_client(self):
        if self.engine == Engine.SELF:
            self.engine_client = None
        elif self.engine == Engine.OPENAI:
            self.engine_client = OpenAIClient()
        else:
            logging.critical("Unsupported engine type used")
        
        logging.debug(f"{self.engine} client started")

    def generate_answer_code(self):
        logging.debug(f"Attempting to generate code for assignment: \n{self.assignment_text}")

        self.answer_code = self.engine_client.get_answer_code(
            assignment_text = self.assignment_text
        )
        self.clean_answer_code()
        logging.debug(f"Received following answer code back: \n{self.answer_code}")
        click.echo(f"Generated the following code: \n{self.answer_code}")

        if len(self.answer_code) > MAX_ANSWER_CODE_CHAR_LENGTH:
            logging.critical("Max answer code character length exceeded")
            raise Exception()
        
        # write to file
        self.write_answer_code_to_file()

    def write_answer_code_to_file(self):
        self.answer_code_module_path = "FIXME_temp_solution_path"
        logging.debug(f"Writing answer code to file {self.answer_code_module_path}")
        with open(f"{self.answer_code_module_path}.py", "w") as file:
            file.write(self.answer_code)

    def run_solution(self):
        click.confirm('Do you want to execute the proposed code solution?', abort=True)
        # enable_run_solution()

        # load answer code from module
        answer_code_module = importlib.import_module(f"{self.answer_code_module_path}")

        # run with runtime logger
        logging.debug("Attempting to run answer code")
        try:
            start = time.time()
            self.answer = answer_code_module.solve()
            self.walltime = time.time() - start
            self.walltime_string = transform_time_to_string(self.walltime)
            self.is_executable = 1

            # check answer if provided
            if self.expected_answer is not None:
                self.is_correct = 1 if str(self.answer) == str(self.expected_answer) else 0
                is_correct_string = 'Correct' if self.is_correct else 'Incorrect'
            else:
                is_correct_string = 'Unknown'
            
            # print answers
            click.echo('=======================')
            click.echo(f'Solution: {self.answer}')
            if self.expected_answer is not None:
                click.echo('{is_correct_string}, expected answer: {self.expected_answer}')
            click.echo(u'Walltime: {}'.format(self.walltime_string))
        
        except:
            logging.critical("Answer code failed to execute properly. Aborting.")
            self.answer = None

        # wrap up
        self.write_to_db()

    def clean_answer_code(self):
        logging.debug("Cleaning answer code string from artifacts")

        if self.answer_code[:11] == "```python\n":
            self.answer_code = self.answer_code[11:]
        elif self.answer_code[:9] == "```python":
            self.answer_code = self.answer_code[9:]
        elif self.answer_code[:3] == "```":
            self.answer_code = self.answer_code[3:]

        if self.answer_code[-3:] == "```":
            self.answer_code = self.answer_code[:-3]

    def add_new_problem(self):
        problem_title = click.prompt('Enter title', default="", type=str)
        self.assignment_text = click.prompt('Enter assignment', default="", type=str)
        self.expected_answer = click.prompt('Enter expected answer if known', default="", type=str)

        execute_query(
            "INSERT INTO problems (problem_type, title, assignment, expected_answer) VALUES (?, ?, ?, ?)", 
            ("manual", problem_title, self.assignment_text, self.expected_answer)
        )

    def get_assignment_text(self):
        return execute_query(f"SELECT assignment FROM problems WHERE id = {self.problem_id} ORDER BY id DESC LIMIT 1;")[0][0]
    
    def get_expected_answer(self):
        return execute_query(f"SELECT expected_answer FROM expected_answers WHERE problem_id = {self.problem_id} ORDER BY id DESC LIMIT 1;")[0][0]
    
    def write_to_db(self):
        execute_query(
            "INSERT INTO solutions (problem_id, engine, code, answer, is_executable, is_correct, walltime, walltime_string, memory, memory_string) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
            (self.problem_id, str(self.engine), str(self.answer_code), str(self.answer), int(self.is_executable), int(self.is_correct), self.walltime, str(self.walltime_string), self.memory, None)
        )


def create_solutions_table(reset_table=False):
    if reset_table:
        execute_query("DROP TABLE IF EXISTS solutions;")
    
    execute_query("""
        CREATE TABLE IF NOT EXISTS solutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            problem_id INTEGER NOT NULL,
            engine TEXT NOT NULL,
            code TEXT,
            answer TEXT,
            is_executable INTEGER,
            is_correct INTEGER,
            walltime REAL,
            walltime_string TEXT,
            memory REAL,
            memory_string TEXT
        )
    """)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Create solutions table
    create_solutions_table(reset_table=False)
    solution = Solution(mode=SolutionMode.MANUAL, engine=Engine.OPENAI)

    # client = OpenAIClient()
    # answer = client.get_answer_code("Solve x: $5 = 3 + 2$")
    # print(answer)
    