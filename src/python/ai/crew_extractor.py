
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
from pydantic import BaseModel
from tool import *


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
            llm=get_llm(model="azure/gpt-4o-mini")
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