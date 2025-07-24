import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from python.dao.user_dao import UserDAO
from python.dao.db_connection import ConnectionDB
import pytest

@pytest.fixture
def setup(dao_connection):
    """Fixture to set up user and return relevant data, including inserted ID."""
    username = "Nome Test"
    email = "test.email@gmail.com"
    password = "password_test"

    # Pulisce eventuali utenti precedenti
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "debug.db")
    db_connection = ConnectionDB(db_path)
    db_connection.execute_ddl("DELETE FROM users WHERE username LIKE 'Nome Test%' OR email LIKE 'test.%'")
    
    # Inserisce nuovo utente e restituisce ID
    inserted = dao_connection.create_user(username=username, email=email, password=password)
    assert inserted == 1, "User should be added successfully"
    
    # Recupera l'utente appena inserito
    user = dao_connection.get_user_by_username(username)
    user_id = user[0]  # id viene prima
    yield username, email, password, user_id




@pytest.fixture
def dao_connection():
    """Fixture to connect to debug.db in data folder under test and maintain that connection"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "debug.db")

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file does not exist: {db_path}")
    dao = UserDAO(db_path=db_path,env=None)
    yield dao



@pytest.mark.order(1)
def test_get_user_by_id(dao_connection, setup):
    _, _, _, user_id = setup
    user = dao_connection.get_user_by_id(user_id)
    assert user is not None, "User should be found"
    assert user[0] == user_id, "User ID should match"

@pytest.mark.order(2)
def test_update_user(dao_connection, setup):
    _, _, _, user_id = setup
    updated = dao_connection.update_user(user_id, username="Nome Test Updated")
    assert updated == 1, "User should be updated successfully"

@pytest.mark.order(3)
def test_get_user_by_username(dao_connection):
    user = dao_connection.get_user_by_username("Nome Test Updated")
    assert user is not None, "User should be found"
    assert user[1] == "Nome Test Updated", "Username should match"

@pytest.mark.order(4)
def test_delete_user(dao_connection, setup):
    _, _, _, user_id = setup
    user_before = dao_connection.get_user_by_id(user_id)
    assert user_before is not None, "User should exist before deletion"

    print(user_id)
    deleted = dao_connection.delete_user(user_id)
    assert deleted == 1, "User should be deleted successfully"

    user_after = dao_connection.get_user_by_id(user_id)
    assert user_after is None, "User should no longer exist"

def test_get_all_users(dao_connection):
    """Test retrieving all users."""
    users = dao_connection.get_all_users()
    assert isinstance(users, list), "Should retur\n a list of users"
    assert len(users) > 0, "Should return at least one user"

if __name__ == "__main__":
    pytest.main([__file__]) 