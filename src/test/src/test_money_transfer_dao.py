import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from python.dao.money_transfer_dao import MoneyTransferDAO
from python.dao.db_connection import ConnectionDB
import pytest
@pytest.fixture

def setup(dao_connection):
    """Fixture to set up user and return relevant data, including inserted ID."""
    
    # Define the parameters for the money transfer
    date = "2023-10-01"
    amount = 100.0
    category_id = 1
    description = "Test Transfer"

    # Clean up any previous transfers
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "debug.db")
    db_connection = ConnectionDB(db_path)
    db_connection.execute_ddl("DELETE FROM users WHERE username LIKE 'Nome Test%' OR email LIKE 'test.%'")
    
    # Insert new transfer and return ID
    inserted = dao_connection.create_transfer(date=date, 
                                              amount=amount, 
                                              category_id=category_id, 
                                              user_id=user_id, 
                                              description=description)
    assert inserted == 1, "User should be added successfully"
    
    # Retrieve the user ID for the transfer
    user = dao_connection.get_user_by_username()
    user_id = user[0]
    yield date, amount, category_id, user_id,description


@pytest.fixture
def dao_connection():
    """Fixture to connect to debug.db in data folder under test and maintain that connection"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "debug.db")

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file does not exist: {db_path}")
    dao = MoneyTransferDAO(db_path=db_path,env=None)
    yield dao


    
    result = dao_connection.create_transfer(date, amount, category_id, user_id, description)
    assert result == 1, "Transfer should be created successfully"

if __name__ == "__main__":
    pytest.main([__file__])