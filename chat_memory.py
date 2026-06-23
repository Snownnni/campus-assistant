# src/chat_memory.py
from agent import agent_chat

class ConversationMemory:
    def __init__(self, max_history=10):
        self.history = []
        self.max_history = max_history
    
    def add_user_message(self, content):
        self.history.append({"role": "user", "content": content})
        self._trim_history()
    
    def add_assistant_message(self, content):
        self.history.append({"role": "assistant", "content": content})
        self._trim_history()
    
    def get_recent(self, n=5):
        return self.history[-n*2:] if self.history else []
    
    def _trim_history(self):
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-self.max_history * 2:]
    
    def clear(self):
        self.history = []

def chat_with_memory(user_input, memory=None):
    if memory is None:
        memory = ConversationMemory()
    memory.add_user_message(user_input)
    context = memory.get_recent(5)
    response = agent_chat(user_input, context=context)
    memory.add_assistant_message(response)
    return response, memory