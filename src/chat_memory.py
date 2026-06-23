# src/chat_memory.py
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from agent import agent_chat

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
        return self.history[-n*2:] if self.history else []
    
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
    response = agent_chat(user_input, context=context)
    memory.add_assistant_message(response)
    
    return response, memory

if __name__ == "__main__":
    memory = ConversationMemory()
    
    print("="*60)
    print("带记忆的智能体对话测试")
    print("输入 'exit' 退出")
    print("="*60)
    
    while True:
        user_input = input("\n用户：")
        if user_input.lower() in ['exit', 'quit', '退出']:
            print("再见！")
            break
        
        response, memory = chat_with_memory(user_input, memory)
        print(f"助手：{response}")
        print(f"\n[当前对话轮数：{len(memory.history)//2}]")