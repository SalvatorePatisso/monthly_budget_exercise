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

def test_get_category_by_id(dao_connection):
    """Test retrieving a category by ID."""
    category = dao_connection.get_category_by_id(1)
    assert category is not None

def test_update_category(dao_connection):
    """Test updating a category name."""
    result = dao_connection.update_category(1, "Updated Category Name")
    assert result == 1

def test_delete_category(dao_connection):
    """Test deleting a category."""
    #create a category to delete
    dao_connection.add_category("Category to Delete", "This category will be deleted")

    #retrieve last category_id added
    categories = dao_connection.get_all_categories()
    last_category_id = categories[-1][0] 

    # Now delete it
    result = dao_connection.delete_category(last_category_id)
    assert result == 1

if __name__ == "__main__":
    pytest.main([__file__])