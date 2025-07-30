import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pytest
from python.ai.chatbot import ChatBot

@pytest.fixture
def init_bot():
    history = [
        {'role': 'system', 'content': 'Act like a good assistant'},
        {'role': 'user', 'content': 'Hello, can you help me with my budget?'},
        {'role': 'assistant', 'content': 'Of course! I can help you manage your budget. What would you like to focus on?'}
    ]
    chatbot = ChatBot(history=history)
    yield chatbot

def  test_chatbot_response(init_bot):
    input = "Say hello to me"
    response = init_bot.response(input)
    assert response is not None
    assert isinstance(response,str)

    assert init_bot.history[-1] == {'role':'assistant',
                                    'content':response}
    assert init_bot.history[-2] == {'role':'user',
                                    'content':input}
    
def test_change_system_behaviour(init_bot):
    new_system_prompt = "Comportati in maniera diversa"
    init_bot.change_system_behaviour(new_system_prompt=new_system_prompt)

    assert init_bot.system_prompt == new_system_prompt
    assert init_bot.history[0]  ==  {'role':'system','content':new_system_prompt}

def test_reset_history(init_bot):
    init_bot.reset_history()
    assert len(init_bot.history) == 1
    assert init_bot.history[0] == {'role':'system','content':init_bot.system_prompt}

if __name__ == "__main__":
    pytest.main([__file__])