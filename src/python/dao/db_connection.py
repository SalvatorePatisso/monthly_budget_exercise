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
            try:
                load_dotenv(env_path=env)
                self.db_path = os.getenv("DB_PATH")
            except Exception as e:
                raise ValueError(f"Error loading environment file: {e}")
        else:
            if not db_path:
                raise ValueError("Database path must be provided if env is not set.")
            elif not os.path.exists(db_path):
                raise ValueError(f"Database file does not exist: {db_path}")
            else: 
                self.db_path = db_path
    def query(self, query, params=None):
        """Execute a query on the database.
        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to pass to the query.
        Returns:
            list: A list of rows returned by the query.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # interact with database
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                rows = cursor.fetchall()
                return rows
        except sqlite3.OperationalError as e:
            print("Failed to open database:", e)
