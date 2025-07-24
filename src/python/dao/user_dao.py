from .db_connection import ConnectionDB

class UserDAO:
    """Data access object for the ``users`` table."""

    def __init__(self,db_path: str = None, env: str = None):
        """Initialize the UserDAO with a database connection."""
        self.connection = ConnectionDB(db_path, env)

    def get_all_users(self):
        """Return a list of all users."""
        query = "SELECT user_id, username, email, password FROM users"
        return self.connection.execute_query(query)

    def get_user_by_id(self, user_id: int):
        """Return a single user matching ``user_id`` or ``None`` if not found."""
        query = (
            "SELECT user_id, username, email, password FROM users WHERE user_id=?"
        )
        rows = self.connection.execute_query(query, (user_id,))
        return rows[0] if rows else None

    def get_user_by_username(self, username: str):
        """Return a user by username or ``None`` if not found."""
        query = (
            "SELECT user_id, username, email, password FROM users WHERE username=?"
        )
        rows = self.connection.execute_query(query, (username,))
        return rows[0] if rows else None

    def create_user(self, username: str, email: str, password: str) -> int:
        """Insert a new user and return number of row inserted"""
        insert_q = (
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
        )
        return self.connection.execute_ddl(insert_q, (username, email, password))
        

    def update_user(
        self,
        user_id: int,
        *,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
    ) -> bool:
        """Update an existing user. Returns ``True`` if at least one field was updated."""
        fields = []
        params = []
        if username is not None:
            fields.append("username=?")
            params.append(username)
        if email is not None:
            fields.append("email=?")
            params.append(email)
        if password is not None:
            fields.append("password=?")
            params.append(password)
        if not fields:
            return False
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE user_id=(?)"
        self.connection.execute_ddl(query, tuple(params))
        return True

    def delete_user(self, user_id: int) -> int:
        """Remove a user from the database. Returns number of rows deleted."""
        return self.connection.execute_ddl("DELETE FROM users WHERE user_id=?", (user_id,))
