# src/test_memory_final.py
from chat_memory import ConversationMemory, chat_with_memory

def test_memory():
    memory = ConversationMemory()
    
    print("="*60)
    print("记忆功能测试")
    print("="*60)
    
    test_conversation = [
        "现在第几周？",
        "那距离期末还有几周？",
        "绩点计算85,90,78",
        "那我的平均绩点是多少？"
    ]
    
    for user_input in test_conversation:
        print(f"\n用户：{user_input}")
        response, memory = chat_with_memory(user_input, memory)
        print(f"助手：{response}")
        print("-"*40)

if __name__ == "__main__":
    test_memory()