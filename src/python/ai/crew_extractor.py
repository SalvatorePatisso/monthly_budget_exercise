from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from langchain_community.utilities.sql_database import SQLDatabase
import sqlite3 
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.tools import tool
from textwrap import dedent
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel



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

def get_llm(model: str):
    load_dotenv()
    return LLM(model=model,
               api_base=os.getenv("AZURE_API_ENDPOINT"),
               api_key=os.getenv("AZURE_API_KEY"),
               api_version=os.getenv("AZURE_API_VERSION"))

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

class QueryValuesModel(BaseModel):
    query: str
    date: str
    amount: float
    description: str
    category_id: int
    category_description: str
    is_incoming: bool

@CrewBase
class MoneyTransferOperator(): 
    agents_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config','agents.yaml')
    tasks_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config','tasks.yaml')

    @agent
    def sql_expert(self) -> Agent:
        load_dotenv()
        return Agent(
            config=self.agents_config['sql_expert'],
            tools=[list_tables,tables_schema,execute_sql,check_sql],
            llm=get_llm(model="azure/gpt-4o-mini"),
            allow_delegation=True
        )    
 
    @agent
    def descriptor(self) -> Agent:
        return Agent(
        config=self.agents_config['descriptor'],
        llm=get_llm(model="azure/gpt-4o-mini")
        )    
 
    @task
    def create_sql(self) -> Agent:
        return  Task(
            config = self.tasks_config['create_sql_task'],
            context=[self.describe()],
            agent=self.sql_expert(),
            output_json = QueryValuesModel
        )
 
    @task
    def describe(self) -> Agent:
        return  Task(
            config=self.tasks_config['describe_task'],
            agent=self.descriptor()
        )
    @crew
    def crew(self) -> Crew:
        """Creates the CrewDocumentProcessor crew"""
        return Crew(
            agents=[self.descriptor(),self.sql_expert()],
            tasks =[self.describe(),self.create_sql()], 
            process=Process.sequential
            )
    
if __name__ == "__main__":
        inputs = {
            "json": """
            {
                "name" : "Da Giovanni Eletric",
                "items": [
                    {
                        "description": "lampadine"
                        "quantity":4
                        "cost" : 22
                    },
                    {
                        "description": "citofoni",
                        "quantity": 2,
                        "cost": 22
                    }
                ]
            }
            """
        }

        print(inputs)
        processor = MoneyTransferOperator()
        result = processor.crew().kickoff(inputs=inputs)
        print(result['description']) 