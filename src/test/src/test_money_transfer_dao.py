import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from python.dao.money_transfer_dao import MoneyTransferDAO
import pytest


@pytest.fixture
def dao_connection():
    """Fixture to connect to debug.db in data folder under test and maintain that connection"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "debug.db")

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file does not exist: {db_path}")
    dao = MoneyTransferDAO(db_path=db_path,env=None)
    yield dao

def test_create_transfer(dao_connection):
    """Test creating a money transfer."""
    date = "2023-10-01"
    amount = 100.0
    category_id = 1
    user_id = 1
    description = "Test transfer"
    incoming = False

    result = dao_connection.create_transfer(date, amount, category_id, user_id, description, incoming)
    assert result == 1, "Transfer should be created successfully"

def test_get_all_transfers(dao_connection):
    """Test retrieving all money transfers."""
    transfers = dao_connection.get_all_transfers()
    assert isinstance(transfers, list), "Should return a list of transfers"

def test_delete_transfer(dao_connection):
    """Test deleting a money transfer."""
    # First, create a transfer to delete
    date = "2023-10-01"
    amount = 100.0
    category_id = 1
    user_id = 1
    description = "Test transfer for deletion"
    incoming = False

    rows_affected = dao_connection.create_transfer(date, amount, category_id, user_id, description, incoming)

    #select last id inserted
    last_id_inserted = dao_connection.get_all_transfers()[-1][0]
    
    assert rows_affected == 1, "Transfer should be created successfully"
    print("Last id: ",last_id_inserted)
    # Now delete the transfer
    result = dao_connection.delete_transfer(last_id_inserted)
    assert result == 1, "Transfer should be deleted successfully"

def test_get_transfer_by_id(dao_connection):
    
    transfer = dao_connection.get_transfer_by_id(1)
    assert transfer is not None, "Transfer should be found by ID"


if __name__ == "__main__":
    pytest.main([__file__])
