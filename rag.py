# src/rag.py
import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 初始化DeepSeek客户端
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

# 加载CSV数据作为知识库
def load_knowledge_base():
    """从CSV加载知识库"""
    try:
        df = pd.read_csv('data/campus_data.csv', encoding='gbk')
        print(f"✅ 加载了 {len(df)} 条数据")
        return df
    except:
        try:
            df = pd.read_csv('data/campus_data.csv', encoding='utf-8')
            print(f"✅ 加载了 {len(df)} 条数据")
            return df
        except Exception as e:
            print(f"❌ 加载数据失败：{e}")
            return None

# 加载知识库
knowledge_df = load_knowledge_base()

def search_knowledge(question, k=5):
    """简单的关键词检索"""
    if knowledge_df is None:
        print("⚠️ 知识库未加载")
        return []
    
    results = []
    question_lower = question.lower()
    
    for _, row in knowledge_df.iterrows():
        score = 0
        text = str(row['question']) + str(row['answer'])
        text_lower = text.lower()
        
        # 关键词匹配
        keywords = question_lower.split()
        for kw in keywords:
            if len(kw) > 1 and kw in text_lower:
                score += 1
        
        # 类别匹配
        if str(row['category']) in question_lower:
            score += 2
        
        if score > 0:
            results.append({
                'question': row['question'],
                'answer': row['answer'],
                'category': row['category'],
                'source': row.get('source', ''),
                'score': score
            })
    
    # 按分数排序
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:k]

def rag_answer(question, k=5):
    """RAG问答函数"""
    try:
        docs = search_knowledge(question, k=k)
        
        if not docs:
            return "抱歉，我没有找到相关信息。建议你咨询辅导员或查看学生手册。"
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            context_parts.append(f"【{doc['category']}】问题：{doc['question']}\n答案：{doc['answer']}")
        
        context = "\n\n".join(context_parts)
        
        prompt = f"""你是一个安徽交通职业技术学院的校园生活助手。请根据以下校园规则回答问题。

【校园规则参考】
{context}

【学生问题】
{question}

【回答要求】
1. 严格基于上述规则回答，不要编造
2. 如果规则中有相关信息，直接回答
3. 如果规则中没有相关信息，说"建议咨询辅导员"
4. 回答要具体、完整

【回答】
"""
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=500
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return f"❌ 处理失败：{e}"

def rag_answer_with_source(question, k=5):
    """带检索来源的RAG问答"""
    try:
        docs = search_knowledge(question, k=k)
        
        if not docs:
            return "抱歉，我没有找到相关信息。建议你咨询辅导员或查看学生手册。", []
        
        context_parts = []
        sources = []
        for i, doc in enumerate(docs, 1):
            context_parts.append(f"【{doc['category']}】问题：{doc['question']}\n答案：{doc['answer']}")
            sources.append({
                'question': doc['question'],
                'answer': doc['answer'],
                'score': doc['score'],
                'category': doc['category']
            })
        
        context = "\n\n".join(context_parts)
        
        prompt = f"""你是一个安徽交通职业技术学院的校园生活助手。请根据以下校园规则回答问题。

【校园规则参考】
{context}

【学生问题】
{question}

【回答要求】
1. 严格基于上述规则回答，不要编造
2. 如果规则中有相关信息，直接回答
3. 如果规则中没有相关信息，说"建议咨询辅导员"
4. 回答要具体、完整

【回答】
"""
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=500
        )
        return response.choices[0].message.content, sources
    
    except Exception as e:
        return f"❌ 处理失败：{e}", []
