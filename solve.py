#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a Solution wrapper that orchestrates fetching the problems, generating, and running solutions 
either self-written, or generated via one of OpenAI, Gemini, or Claude's APIs. Handles repeated attempts
with suggestions to refine generated solutions if wrong or less efficient. Stores all solutions in the DB
and handles creating the solution subfolders for each problem.
"""
import logging

from db_utils import execute_query


class Solution:
    def __init__(self, pid):
        self.pid = pid

    def get_pid(self):
        return self.pid


def create_solutions_table(reset_table=False):
    if reset_table:
        execute_query("DROP TABLE IF EXISTS solutions;")
    
    execute_query("""
        CREATE TABLE IF NOT EXISTS solutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            problem_id INTEGER NOT NULL,
            engine TEXT NOT NULL,
            code_solution TEXT NOT NULL,
            is_executable INTEGER,
            is_correct INTEGER,
            walltime INTEGER,
            memory INTEGER
        )
    """)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Create solutions table
    create_solutions_table(reset_table=True)
                  