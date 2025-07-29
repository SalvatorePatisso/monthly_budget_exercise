from .db_connection import ConnectionDB
import os
from enum import Enum

class MoneyTransferAttribute(Enum):
    START_AMOUNT = "start_amount"
    END_AMOUNT = "end_amount"
    MONEY_TRANSFER_START_DATE = "start_date"
    MONEY_TRANSFER_END_DATE = "end_date"
    MONEY_TRANSFER_AMOUNT = "amount"
    CATEGORY_ID = "category_id"
    DESCRIPTION = "description"
    TRANSACTION_ID = "transaction_id"
    INCOMING = "incoming"

class MoneyTransferDAO:

    def __init__(self,db_path: str = None, env: str = None):
        """Initialize the TransactionDAO with a database connection."""
        self.db_connection = ConnectionDB(db_path, env)

    def _insert_amount_range(self, attributes: list,query: str):
    # Check if the attributes contain amount range conditions
        if (MoneyTransferAttribute.START_AMOUNT.value in attributes) and (MoneyTransferAttribute.END_AMOUNT.value in attributes):
        
            #query must be BETWEEN
            query += " AND amount BETWEEN ? AND ?"
            
            attributes.remove(MoneyTransferAttribute.START_AMOUNT.value)
            attributes.remove(MoneyTransferAttribute.END_AMOUNT.value)

        elif MoneyTransferAttribute.START_AMOUNT.value in attributes:

            query += " AND amount >= ?"
            attributes.remove(MoneyTransferAttribute.START_AMOUNT.value)

        elif MoneyTransferAttribute.END_AMOUNT.value in attributes:

            query += " AND amount <= ?"
            attributes.remove(MoneyTransferAttribute.END_AMOUNT.value)

        return attributes, query
    
    def _insert_date_range(self, attributes: list, query: str):     
    # Check if the attributes contain date range conditions
        if (MoneyTransferAttribute.MONEY_TRANSFER_START_DATE.value in attributes) and (MoneyTransferAttribute.MONEY_TRANSFER_END_DATE.value in attributes):
            print("Both start and end date attributes found.")
            #query must be BETWEEN
            query += " date BETWEEN ? AND ?"

            attributes.remove(MoneyTransferAttribute.MONEY_TRANSFER_START_DATE.value)
            attributes.remove(MoneyTransferAttribute.MONEY_TRANSFER_END_DATE.value)

        elif MoneyTransferAttribute.MONEY_TRANSFER_START_DATE.value in attributes:

            query += " date >= ?"
            attributes.remove(MoneyTransferAttribute.MONEY_TRANSFER_START_DATE.value)

        elif MoneyTransferAttribute.MONEY_TRANSFER_END_DATE.value in attributes:

            query += " date <= ?"
            attributes.remove(MoneyTransferAttribute.MONEY_TRANSFER_END_DATE.value)

        print("ATTRIBUTES: ",attributes) #TODO: remove this print statement
        
        return attributes, query

    def search_transaction_for_attributes(self, dict_attributes: dict) -> list: 
        """
        Build a query based on the provided attributes and return the results.
        :param attributes: A dictionary of MoneyTransferAttribute as key.
        :return: A list of transactions matching the query.
        """

        attributes = list(dict_attributes.keys())
        values = dict_attributes.values()
        self.params_accepted =  [attr.value for attr in MoneyTransferAttribute]
    
        for attr in attributes:
            if attr not in self.params_accepted:
                raise ValueError(f"Invalid attribute: {attr}. Accepted attributes are: {self.params_accepted}")
        query = "SELECT * FROM money_transfer WHERE"
        
        attributes,query = self._insert_date_range(attributes, query)
        attributes,query = self._insert_amount_range(attributes, query)

        if MoneyTransferAttribute.DESCRIPTION in attributes:
            query += " AND description LIKE ?"
            attributes.remove(MoneyTransferAttribute.DESCRIPTION)
            
        # Add the remaining attributes to the query
        for attr in attributes: 
            #do not put OR in the beginning
            if query.endswith("WHERE"):
                query += f" {attr} = ?"
            else:
                query += f" AND {attr} = ?"

        return self.db_connection.execute_query(query, tuple(values))

    def _add_values_to_query_string(self,transfers):
        values = ""
        for i,transfer in enumerate(transfers):
            question_mark = ""
            for j, elem in enumerate(transfer):
                if j == len(transfer)-1:
                    question_mark += "?"
                else:
                    question_mark += "?,"

            if i == len(transfers)-1:
                value = "("+question_mark+"); "
            else:
                value = "("+question_mark+"), "
            values += value
        return values
    
    def create_multiple_transfers(self, transfers: list[tuple]) -> int:
        """Insert multiple money transfers and return the number of rows inserted."""
        insert_query = (
            "INSERT INTO money_transfer (date, amount, category_id, user_id, description, incoming) VALUES "
        )
        insert_query += self._add_values_to_query_string(transfers)

        print(insert_query)#TODO REMOVE
        
        flattened_transfers = [item for transfer in transfers for item in transfer]
        return self.db_connection.execute_ddl(insert_query, flattened_transfers)
    
    def create_transfer(self, 
                         date: str, 
                         amount: float, 
                         category_id: int,
                         user_id: int, 
                         description: str = None, 
                         incoming: bool = False) -> int:
        """Insert a new money transfer and return the number of rows inserted."""
        insert_query = (
            "INSERT INTO money_transfer (date, amount, category_id, user_id, description, incoming) VALUES (?, ?, ?, ?, ?, ?)"
        )
        return self.db_connection.execute_ddl(
            insert_query, (date, amount, category_id, user_id, description, incoming)
        )
    
    def get_all_transfers(self):
        """Return a list of all money transfers."""
        query = "SELECT * FROM money_transfer"
        return self.db_connection.execute_query(query)
    
    def get_transfer_by_id(self, transfer_id: int):
        """Return a single money transfer matching ``transfer_id`` or ``None`` if not found."""
        query = (
            "SELECT * FROM money_transfer WHERE transaction_id= (?)"
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
        query = f"UPDATE money_transfer SET {', '.join(fields)} WHERE transaction_id= (?)"
        
        return self.db_connection.execute_ddl(query, tuple(params))

    def delete_transfer(self, transfer_id: int) -> int:
        """Remove a money transfer from the database. Returns number of rows deleted."""
        return self.db_connection.execute_ddl("DELETE FROM money_transfer WHERE transaction_id= (?)", (transfer_id,))  
    