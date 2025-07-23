import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import sqlite3
import tempfile
from python.dao.db_connection import ConnectionDB
import pytest


@pytest.fixture
def temp_db_file():
    # Create a temporary SQLite database file
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    # Initialize the database with a table
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)")
    conn.execute("INSERT INTO test (value) VALUES ('foo'), ('bar')")
    conn.commit()
    conn.close()
    yield path
    os.remove(path)

def test_init_with_db_path(temp_db_file):
    db = ConnectionDB(db_path=temp_db_file)
    assert db.db_path == temp_db_file

def test_init_with_missing_db_path():
    with pytest.raises(ValueError):
        ConnectionDB(db_path=None)

def test_init_with_nonexistent_db_path():
    with pytest.raises(ValueError):
        ConnectionDB(db_path="nonexistent.db")

def test_query_returns_rows(temp_db_file):
    db = ConnectionDB(db_path=temp_db_file)
    rows = db.query("SELECT * FROM test")
    assert len(rows) == 2
    assert rows[0][1] == 'foo'
    assert rows[1][1] == 'bar'

def test_query_with_params(temp_db_file):
    db = ConnectionDB(db_path=temp_db_file)
    rows = db.query("SELECT * FROM test WHERE value=?", ("foo",))
    assert len(rows) == 1
    assert rows[0][1] == 'foo'

def test_query_invalid_sql(temp_db_file, capsys):
    db = ConnectionDB(db_path=temp_db_file)
    db.query("SELECT * FROM non_existing_table")
    captured = capsys.readouterr()
    assert "Failed to open database:" in captured.out

def test_init_with_env(temp_db_file,tmp_path):
    # Create a .env file
    env_file = tmp_path / ".env"
    db_file = temp_db_file
    sqlite3.connect(db_file).close()
    env_file.write_text(f"DB_PATH={db_file}\n")
    db = ConnectionDB(env=str(env_file))
    assert db.db_path == str(db_file)

def test_init_with_env_file_error(tmp_path):
    # Pass a non-existent .env file
    with pytest.raises(ValueError):
        ConnectionDB(env=str(tmp_path / "nonexistent.env"))

if __name__ == "__main__":
    pytest.main([__file__])