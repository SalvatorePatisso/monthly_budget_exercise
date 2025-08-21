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
        sql = "SELECT * FROM categories WHERE category_id = (?)"
        result = self.db_connection.execute_query(sql, (category_id,))
        return result[0] if result else None
    
    def update_category(
        self,
        category_id: int,
        name: str | None = None,
        description: str | None = None
    ) -> bool:
        """Update an existing category. Returns ``True`` if at least one field was updated."""
        fields = []
        params = []
        if name is not None:
            fields.append("name=?")
            params.append(name)
        if description is not None:
            fields.append("description=?")
            params.append(description)
        if not fields:
            return False
        params.append(category_id)
        query = f"UPDATE categories SET {', '.join(fields)} WHERE category_id=(?)"
        self.db_connection.execute_ddl(query, tuple(params))
        return True
    
    def delete_category(self, category_id: int):
        """Delete a category by its ID."""
        sql = "DELETE FROM categories WHERE category_id = ?"
        return self.db_connection.execute_ddl(sql, (category_id,))


if __name__== "__main__":
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
    print("project_root",PROJECT_ROOT)
    DB_PATH = os.getenv("DB_PATH") or str(PROJECT_ROOT / "data" / "ddl" / "debug.db")

    dao = CategoriesDAO(db_path=DB_PATH)
    print(dao.get_all_categories()[0][1])