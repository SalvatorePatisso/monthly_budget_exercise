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

def get_db():
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"data" , "ddl","debug.db")
    return SQLDatabase.from_uri("sqlite:///"+db_path)

def get_llm(model: str):
    load_dotenv()
    return LLM(model=model,
               api_base=os.getenv("AZURE_API_BASE"),
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

@CrewBase
class MoneyTransferOperator(): 
    agents_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config','agents.yaml')
    tasks_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config','task.yaml')

    @agent
    def sql_expert(self) -> Agent:
        load_dotenv()
        return Agent(
            config=self.agents_config['sql_expert'],
            tools=[list_tables,tables_schema,execute_sql,check_sql],
            llm=get_llm(model = "azure/o4-mini"),
            allow_delegation=True
        )    
 
    @agent
    def descriptor(self) -> Agent:
        return Agent(
        config=self.agents_config['descriptor'],
        llm=get_llm(model="azure/gpt-4o")
        )    
 
    @task
    def create_sql(self) -> Agent:
        return  Task(
            config = self.tasks_config['create_sql_task']
        )
 
    @task
    def describe(self) -> Agent:
        return  Task(
            config = self.tasks_config['describe_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MoneyTransferOperator crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
            )
    
if __name__ == "__main__":
    json  = {
                "invoice_number": 1,
                "invoice_total": 22,
                "items":[
                    {
                        "description": "Mele Melinda",
                        "quantity": 2,
                        "total": 22
                    }
                ]
            }
    crew = MoneyTransferOperator()
    result = crew.crew().kickoff(inputs=json)
    print(result)
