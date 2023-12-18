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

        return rows
    
    except: 
        logging.warning("Query execution failed")

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

