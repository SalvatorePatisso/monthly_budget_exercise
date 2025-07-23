from .db_connection import ConnectionDB
import os

class CategoriesDAO:
    def __init__(self, db_path: str = None, env: str = None):
        """Initialize the CategoriesDAO with a database connection."""
        self.db_connection = ConnectionDB(db_path, env)

    def add_category(self, name: str, descr: str,) -> int:
        """Add a new category to the database.
        Args: 
            name (str): The name of the category to add.
            descr (str): The description of the category to add.
        Returns:
            int: The number of affected rows."""
        sql = "INSERT INTO categories (name, description) VALUES (?, ?);"
        return self.db_connection.execute_ddl(sql, (name,descr))

    def get_all_categories(self):
        """Retrieve all categories from the database."""
        sql = "SELECT * FROM categories"
        return self.db_connection.execute_query(sql)
    
    def get_category_by_id(self, category_id: int):
        """Retrieve a category by its ID."""
        sql = "SELECT * FROM categories WHERE id = ?"
        result = self.db_connection.execute_query(sql, (category_id,))
        return result[0] if result else None
    
    def update_category_name(self, category_id: int, name: str):
        """Update the name of an existing category."""
        sql = "UPDATE categories SET name = ? WHERE id = ?"
        return self.db_connection.execute_ddl(sql, (name, category_id))

    def update_category_descr(self, category_id: int, descr: str):    
        """Update the details of an existing category."""
        sql = "UPDATE categories SET name = ? WHERE id = ?"
        return self.db_connection.execute_ddl(sql, (name, category_id))
    
    def delete_category(self, category_id: int):
        """Delete a category by its ID."""
        sql = "DELETE FROM categories WHERE id = ?"
        return self.db_connection.execute_ddl(sql, (category_id,))