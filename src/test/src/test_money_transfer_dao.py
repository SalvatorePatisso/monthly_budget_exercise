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

def test_create_multiple_transfers(dao_connection):
    """Test creating multiple money transfers."""
    transfers = [
        ("2023-10-02", 200.0, 1, 1, "Bulk transfer 1", True),
        ("2023-10-03", 300.0, 2, 1, "Bulk transfer 2", False),
    ]
    # Flatten the list of tuples for the query parameters
    flattened_transfers = [item for transfer in transfers for item in transfer]
    print("Flattened transfers: ",flattened_transfers)
    print("flattened_length: ", len(flattened_transfers))
    result = dao_connection.create_multiple_transfers(transfers)
    assert result == len(transfers), "Should insert all transfers successfully"



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

def test_search_transaction_for_attributes(dao_connection):
    """Test searching for transactions with specific attributes."""
    attributes = {
        "start_date": "2023-10-01",
        "end_date": "2023-10-31",
        "amount": 100.0,
        "category_id": 1,
    }
    # Assuming the attributes are valid and exist in the database
    # This will depend on the actual data in your database
    results = dao_connection.search_transaction_for_attributes(attributes)
    assert isinstance(results, list), "Should return a list of transactions"
    assert len(results) > 0, "Should find at least one transaction matching the criteria"

if __name__ == "__main__":
    pytest.main([__file__])
