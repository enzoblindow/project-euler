import logging
import sqlite3

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
    logging.info("Executing query")

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    try:
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)

        rows = cursor.fetchall()

        conn.commit()

        logging.info("Query executed successfully")
        logging.debug(query)

        return rows
    
    except: 
        logging.warning("Query execution failed")
        logging.debug(query)

    finally:
        cursor.close()
        conn.close()


def init_expected_answers_table(reset_table=False):
    # Recreate table if reset_table flag is enabled
    if reset_table:
        execute_query("DROP TABLE IF EXISTS expected_answers;")

    # Create the table if it doesn't exist
    execute_query("""
        CREATE TABLE IF NOT EXISTS expected_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id INTEGER NOT NULL,
            expected_value TEXT NOT NULL
        )
    """)

    # Open expected answers file and write it's contents into the db
    with open('./data/expected_answers.txt', 'r') as file:
        for line in file:
            values = line.strip().split(' ')
            if len(values) == 2:
                problem_id, expected_value = map(str, values)

                # check if row exists, then skip, otherwise write
                result = execute_query(f"SELECT problem_id FROM expected_answers WHERE problem_id = {problem_id}")
                logging.debug(result)

                if len(result) > 0:
                    logging.debug(f"Skipped writing expected value for problem {problem_id} as it already exists in db")
                    continue
                else:
                    execute_query(
                        "INSERT INTO expected_answers (problem_id, expected_value) VALUES (?, ?)", 
                        (problem_id, expected_value)
                    )
                    logging.info(f"Successfully wrote expected value for problem {problem_id} into db")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    init_expected_answers_table(reset_table=False)

