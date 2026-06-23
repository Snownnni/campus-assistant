# src/chat_memory.py

class ConversationMemory:
    """对话记忆管理器"""
    
    def __init__(self, max_history=10):
        self.history = []
        self.max_history = max_history
    
    def add_user_message(self, content):
        """添加用户消息"""
        self.history.append({"role": "user", "content": content})
        self._trim_history()
    
    def add_assistant_message(self, content):
        """添加助手消息"""
        self.history.append({"role": "assistant", "content": content})
        self._trim_history()
    
    def get_recent(self, n=5):
        """获取最近n轮对话"""
        if not self.history:
            return []
        return self.history[-n*2:]
    
    def _trim_history(self):
        """修剪历史记录"""
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-self.max_history * 2:]
    
    def clear(self):
        """清空对话历史"""
        self.history = []
    
    def get_full_history(self):
        """获取完整历史"""
        return self.history


def chat_with_memory(user_input, memory=None):
    """带记忆的对话"""
    if memory is None:
        memory = ConversationMemory()
    
    memory.add_user_message(user_input)
    context = memory.get_recent(5)
    
    # 延迟导入，避免循环依赖
    from agent import agent_chat
    response = agent_chat(user_input, context=context)
    memory.add_assistant_message(response)
    
    return response, memory
