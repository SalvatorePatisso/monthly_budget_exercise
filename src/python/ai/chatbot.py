from .azure_gpt import AzureGPT4O
from typing import Iterable, Mapping

class ChatBot():
    def __init__(self, model: str = 'gpt_4o_mini', history : Iterable[Mapping[str,str]] = [], system_message: str = ""):
        """
        
        """

        #init system message to tell the llm how to behave
        self.system_prompt = system_message

        #init chat history
        if len(history) == 0:
            self.history = [ {'role': 'system', 'content': system_message} ]
        elif history[0]['role'] == 'system':
            self.history = [ {'role': 'system', 'content': system_message} ] + history
        else: 
            self.history = history
            self.system_prompt = self.history[0]['content']
        
        #initialize model
        if model == 'gpt_4o_mini':
            self.llm  = AzureGPT4O()
            
    def response(self, input: str):
        """Get the response of the llm to an input based on the chat history.
         Add this input to the history
        Args: 
            input (str): The name of the category to add.
        Returns:
            response(strs): The response of the model."""
        
        #add last input to history 
        self.history = self.history + [{'role': 'user', 'content': input}]
        #get response
        response = self.llm.chat_completion(messages = self.history)

        #add response to chat history 
        self.history = self.history + [{'role': 'assistant', 'content': response}] 

        return response
    
    def change_system_behaviour(self,new_system_prompt:str):
        """Change the system message of the history to another system prompt to modify the behavhiour
        Args:
            system_prompt (str) :The system prompt to substitute"""
        self.system_prompt = new_system_prompt
        self.history[0]['content'] = self.system_prompt
   
    def reset_history(self):
        """Reset history to an empty list, without affecting the system prompt"""
        self.history = [self.history[0]]
