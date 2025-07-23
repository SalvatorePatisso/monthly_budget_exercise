from db_connection import ConnectionBB
import os


class MoneyTransferDAO:
    def __init__(self,db_path: str = None, env: str = None):
        """Initialize the TransactionDAO with a database connection."""
        self.db_connection = ConnectionBB(db_path, env)

    def add_transaction(self, amount: float,
                         category_id: None int,
                         description: str,
                         user_id: int,
                         ):
        """Add a new transaction to the database."""
        sql = "INSERT INTO transactions (amount, category_id, description) VALUES (?, ?, ?)"
        return self.db_connection.execute_ddl(sql, (amount, category_id, description))