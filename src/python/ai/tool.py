from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from langchain_community.utilities.sql_database import SQLDatabase
from crewai.tools import tool
from dotenv import load_dotenv
from crewai import LLM
import os

def get_llm(model: str):
    load_dotenv()
    return LLM(model=model,
               api_base=os.getenv("AZURE_API_ENDPOINT"),
               api_key=os.getenv("AZURE_API_KEY"),
               api_version=os.getenv("AZURE_API_VERSION"))

def get_db():
    db_path = os.path.join(os.path.dirname(
                            os.path.dirname(
                                os.path.dirname(
                                    os.path.dirname(
                                        os.path.abspath(__file__)
                                                    )
                                                )
                                            )
                                        ),
                            "data" , "ddl","debug.db")
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")
    return SQLDatabase.from_uri(f"sqlite:///{db_path}")

@tool("list_tables")
def list_tables() -> str:
    """List the available tables in the database"""
    return ListSQLDatabaseTool(db=get_db()).invoke("")

@tool("tables_schema")
def tables_schema(tables: str) -> str:
    """
    Input is a comma-separated list of tables, output is the schema and sample rows
    for those tables. Be sure that the tables actually exist by calling `list_tables` first!
    Example Input: table1, table2, table3
    """
    tool = InfoSQLDatabaseTool(db=get_db())
    return tool.invoke(tables)

@tool("execute_sql")
def execute_sql(sql_query: str) -> str:
    """Execute a SQL query against the database. Returns the result"""
    return QuerySQLDataBaseTool(db=get_db()).invoke(sql_query)

@tool("check_sql")
def check_sql(sql_query: str) -> str:
    """
    Use this tool to double check if your query is correct before executing it. Always use this
    tool before executing a query with `execute_sql`.
    """
    return QuerySQLCheckerTool(db=get_db(), llm=get_llm()).invoke({"query": sql_query})