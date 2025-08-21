from crewai import Agent, Task, Crew,Process
from tool import *
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class ChatBot():
    
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
    def chatbot(self) -> Agent: 
        return Agent(
            config=self.agents_config['descriptor'],
            llm=get_llm(model="azure/gpt-4o-mini")
        )
    
    @task
    def answer_user(self) -> Task:
        return Task(
            config = self.tasks_config['answer_user'],
            agent = self.chatbot(),
            context = [self.query_db()]
        )
    
    @task
    def query_db(self) -> Task:
        return Task(
            config = self.tasks_config['query_db'],
            agent = self.sql_expert(),
        )
    
    @crew
    def chatCrew(self) -> Crew:
        return Crew(
            agents = [self.sql_expert(),self.chatbot()],
            tasks= [self.query_db(),self.answer_user()],
            process = Process.sequential
        )
    

if __name__ == "__main__":
    chatbot = ChatBot()
    while True:
        print("You: ")
        user_input = input()
        if(user_input == "quit"):
            break
        inputs = {"user_input": user_input}
        result = chatbot.chatCrew().kickoff(inputs=inputs)
        print("Chat: "+str(result)+"\n")

