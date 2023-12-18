#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Quickly add new solution from the euler project list and create the barebone
python main.py file for it.
Also adds a new item to the list in the repositories README.md
"""
import logging

import requests
from bs4 import BeautifulSoup

from db_utils import execute_query, check_if_table_exists, init_expected_answers_table


MAX_PROBLEM_ID = 20  # 841
EULER_URL = "https://projecteuler.net/problem={}"


def fetch_problem_from_euler_platform(pid):
    logging.info(f"Attempting to fetch Euler problem {pid}")

    url = EULER_URL.format(pid)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    # Grab problem title and body from project euler website
    title = soup.h2.string
    title = title.replace("$", "")
    assignment = []
    for i in soup.findAll("div", {"class": "problem_content"}):
        for k in i.contents:
            try:
                for s in k.stripped_strings:
                    assignment += repr(s)
            except:
                pass
    assignment = "".join(assignment)
    assignment = assignment.replace("u'", "").replace("'", " ").replace("\n", " ").replace("\\n", " ").strip()
    assignment = assignment.replace("  ", " ")
    logging.info("Euler problem title and assignment fetched")

    # get expected answer for pid
    try:
        response = execute_query(f"SELECT expected_answer FROM expected_answers WHERE problem_id = {pid}")
        expected_answer = response[0][0]
    except: 
        logging.critical(f"No expected answer found in db for problem {pid}")

    # write problem assignment to db
    execute_query(
        "INSERT INTO problems (title, assignment, expected_answer) VALUES (?, ?, ?)", 
        (title, assignment, expected_answer)
    )

def fetch_all_euler_problems_from_platform(reset_table=False):
    if reset_table:
        execute_query("DROP TABLE IF EXISTS problems;")

    # Check if expected answers are loaded
    if check_if_table_exists(table_name="expected_answers") == False:
        init_expected_answers_table()

    # Create table if not exists
    execute_query("""
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            title TEXT NOT NULL,
            assignment TEXT NOT NULL,
            expected_answer REAL
        )
        """
    )

    # Fetch all problems
    for pid in range(1, MAX_PROBLEM_ID + 1):
        # Check if entry for problem already exists in db, otherwise start fetching
        result = execute_query(f"SELECT id FROM problems WHERE id = {pid}")
        if len(result) > 0:
            logging.debug(f"Skipping fetching problem {pid}")
            continue
        else:
            fetch_problem_from_euler_platform(pid)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fetch_all_euler_problems_from_platform(reset_table=False)

    # create_solutions_table_query = """
    #     CREATE TABLE IF NOT EXISTS solutions (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    #         problem_id INTEGER NOT NULL,
    #         engine TEXT NOT NULL,
    #         code_solution TEXT NOT NULL,
    #         is_executable INTEGER,
    #         is_correct INTEGER
    #     )
    # """



