import logging
import sqlite3
import traceback
import sys

DB_NAME = 'euler.sqlite'

def execute_query(query, parameters=None):
    """
    Execute an SQL query and handle opening/closing the connection.

    Parameters:
    - query (str): The SQL query to execute.
    - parameters (tuple, optional): Parameters to be used in the query (default is None).

    Returns:
    - list: A list of rows resulting from the query.
    """
    logging.debug("Attempting to executing query")

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    try:
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)

        rows = cursor.fetchall()

        conn.commit()

        logging.debug("Query executed successfully")
        logging.debug(query)

        return rows
    
    except sqlite3.Error as error:
        logging.warning("Query execution failed")
        logging.debug(query)
        logging.warning('SQLite error: %s' % (' '.join(error.args)))
        logging.warning("Exception class is: ", error.__class__)
        logging.warning('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        logging.warning(traceback.format_exception(exc_type, exc_value, exc_tb))



    finally:
        cursor.close()
        conn.close()


def check_if_table_exists(table_name:str):
    try: 
        result = execute_query(f"SELECT FROM {table_name} LIMIT 1")
        if len(result) > 0:
            return True
        else:
            return False
    except:
        return False


def init_expected_answers_table(reset_table=False):
    # Recreate table if reset_table flag is enabled
    if reset_table:
        execute_query("DROP TABLE IF EXISTS expected_answers;")

    # Create the table if it doesn't exist
    execute_query("""
        CREATE TABLE IF NOT EXISTS expected_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id INTEGER NOT NULL,
            expected_answer TEXT NOT NULL
        )
    """)

    # Open expected answers file and write it's contents into the db
    with open('./data/expected_answers.txt', 'r') as file:
        for line in file:
            values = line.strip().split(' ')
            if len(values) == 2:
                problem_id, expected_answer = map(str, values)

                # check if row exists, then skip, otherwise write
                result = execute_query(f"SELECT problem_id FROM expected_answers WHERE problem_id = {problem_id}")
                logging.debug(result)

                if len(result) > 0:
                    logging.debug(f"Skipped writing expected answer for problem {problem_id} as it already exists in db")
                    continue
                else:
                    execute_query(
                        "INSERT INTO expected_answers (problem_id, expected_answer) VALUES (?, ?)", 
                        (problem_id, expected_answer)
                    )
                    logging.info(f"Successfully wrote expected value for problem {problem_id} into db")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    init_expected_answers_table(reset_table=True)

