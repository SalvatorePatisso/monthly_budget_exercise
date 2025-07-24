from db_connection import ConnectionBB
import os


class MoneyTransferDAO:
    def __init__(self,db_path: str = None, env: str = None):
        """Initialize the TransactionDAO with a database connection."""
        self.db_connection = ConnectionBB(db_path, env)

    def create_transfer(self, 
                         date: str, 
                         amount: float, 
                         category_id: int,
                         user_id: int, 
                         description: str = None, 
                         incoming: bool = False) -> int:
        """Insert a new money transfer and return the number of rows inserted."""
        insert_query = (
            "INSERT INTO money_transfers (date, amount, category_id, user_id, description, incoming) VALUES (?, ?, ?, ?, ?, ?)"
        )
        return self.db_connection.execute_ddl(
            insert_query, (date, amount, category_id, user_id, description, incoming)
        )
    
    def get_all_transfers(self):
        """Return a list of all money transfers."""
        query = "SELECT * FROM money_transfers"
        return self.db_connection.execute_query(query)
    
    def get_transfer_by_id(self, transfer_id: int):
        """Return a single money transfer matching ``transfer_id`` or ``None`` if not found."""
        query = (
            "SELECT * FROM money_transfers WHERE transfer_id= (?)"
        )
        rows = self.db_connection.execute_query(query, (transfer_id,))
        return rows[0] if rows else None
 
    def update_transfer(
        self,
        transfer_id: int,
        *,
        date: str | None = None,
        amount: float | None = None,
        category_id: int | None = None,
        user_id: int | None = None,
        description: str | None = None,
        incoming: bool | None = None
    ) -> bool:
        """Update an existing money transfer. Returns ``True`` if at least one field was updated."""
        fields = []
        params = []
        
        if date is not None:
            fields.append("date=?")
            params.append(date)
        if amount is not None:
            fields.append("amount=?")
            params.append(amount)
        if category_id is not None:
            fields.append("category_id=?")
            params.append(category_id)
        if user_id is not None:
            fields.append("user_id=?")
            params.append(user_id)
        if description is not None:
            fields.append("description=?")
            params.append(description)
        if incoming is not None:
            fields.append("incoming=?")
            params.append(incoming)

        if not fields:
            return False
        
        params.append(transfer_id)
        query = f"UPDATE money_transfers SET {', '.join(fields)} WHERE transfer_id= (?)"
        
        return self.db_connection.execute_ddl(query, tuple(params))

    def delete_transfer(self, transfer_id: int) -> int:
        """Remove a money transfer from the database. Returns number of rows deleted."""
        return self.db_connection.execute_ddl("DELETE FROM money_transfers WHERE transfer_id= (?)", (transfer_id,))  
    
