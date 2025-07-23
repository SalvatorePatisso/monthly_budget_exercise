import sqlite3 
from dotenv import load_dotenv
import os
class ConnectionDB(): 
    def __init__(self,db_path: str = None, env: str = None):
        """Initialize the database connection. If env is provided, 
        it will load the DB_PATH from the .env file specified. Otherwise if 
        it is not provided, it will use the db_path parameter and it must be not None
        Args:
            db_path (str): Path to the database file. 
            env (str): Path to the .env file containing the DB_PATH variable.
        Raises: 
            ValueError: If neither db_path nor env is provided.
        """

        if env is not None:
                if not os.path.exists(env):
                    raise ValueError(f"Environment file does not exist: {env}")
                else:
                    load_dotenv(dotenv_path=env)
                    self.db_path = os.getenv("DB_PATH")
        else:
            if not db_path:
                raise ValueError("Database path must be provided if env is not set.")
            elif not os.path.exists(db_path):
                raise ValueError(f"Database file does not exist: {db_path}")
            else: 
                self.db_path = db_path
                
    def execute_ddl(self, sql, params=None):
        """Execute an SQL statement (INSERT, UPDATE, DELETE, etc.) on the database.
        Args:
            sql (str): The SQL statement to execute.
            params (tuple, optional): Parameters to pass to the statement.
        Returns:
            int: Number of affected rows.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params or ())
                conn.commit()
                return cursor.rowcount
        except sqlite3.OperationalError as e:
            print("Failed to execute SQL:", e)
            return 0

    def execute_query(self, sql, params=None):
        """Execute a SELECT SQL statement and return the results.
        Args:
            sql (str): The SQL SELECT statement to execute.
            params (tuple, optional): Parameters to pass to the statement.
        Returns:
            list: List of rows returned by the query.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params or ())
                return cursor.fetchall()
        except sqlite3.OperationalError as e:
            print("Failed to execute SQL:", e)
            return []
