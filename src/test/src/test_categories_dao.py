import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from python.dao.categories_dao import CategoriesDAO
import pytest


@pytest.fixture
def dao_connection():
    """Fixture to connecto to debug.db in data folder under test and maintain that connection"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"data" , "debug.db")

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file does not exist: {db_path}")
    dao = CategoriesDAO(db_path=db_path)
    yield dao
    
def test_add_category(dao_connection):
    """Test adding a new category."""
    result = dao_connection.add_category("Test Category","Test description")
    assert result == 1

def test_get_all_categories(dao_connection):
    """Test retrieving all categories."""
    categories = dao_connection.get_all_categories()
    assert isinstance(categories, list)


if __name__ == "__main__":
    pytest.main([__file__])