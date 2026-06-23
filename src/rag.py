# src/rag.py
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from prompt_templates import RAG_PROMPT

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

vector_db = Chroma(
    persist_directory="./vector_db",
    embedding_function=embeddings
)

def rag_answer(question, k=5):  # k从3增加到5
    """RAG问答函数"""
    # 1. 检索更多文档（k=5）
    docs = vector_db.similarity_search(question, k=k)
    
    # 2. 构建上下文（包含问题和答案）
    context_parts = []
    for i, doc in enumerate(docs, 1):
        q = doc.metadata.get('question', '')
        answer = doc.page_content
        category = doc.metadata.get('category', '')
        context_parts.append(f"【{category}】问题：{q}\n答案：{answer}")
    
    context = "\n\n".join(context_parts)
    
    # 3. 构建提示词（增强版）
    prompt = f"""你是一个安徽交通职业技术学院的校园生活助手。请根据以下校园规则回答问题。

【校园规则参考】
{context}

【学生问题】
{question}

【回答要求】
1. **严格基于上述规则回答**，不要编造
2. 如果规则中有相关信息，**直接回答**，不要说"我不确定"
3. 如果规则中没有相关信息，才说"建议咨询辅导员"
4. 回答要**具体、完整**，包含时间、地点、流程等关键信息
5. 涉及数字（绩点、天数、金额）必须准确引用

【回答】
"""
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"调用API失败：{e}"

def rag_answer_with_source(question, k=5):
    """带检索来源的RAG问答"""
    docs = vector_db.similarity_search_with_score(question, k=k)
    
    context_parts = []
    sources = []
    for i, (doc, score) in enumerate(docs, 1):
        q = doc.metadata.get('question', '')
        answer = doc.page_content
        category = doc.metadata.get('category', '')
        context_parts.append(f"【{category}】问题：{q}\n答案：{answer}")
        sources.append({
            'question': q,
            'answer': answer,
            'score': score,
            'category': category
        })
    
    context = "\n\n".join(context_parts)
    
    prompt = f"""你是一个安徽交通职业技术学院的校园生活助手。请根据以下校园规则回答问题。

【校园规则参考】
{context}

【学生问题】
{question}

【回答要求】
1. **严格基于上述规则回答**，不要编造
2. 如果规则中有相关信息，**直接回答**，不要说"我不确定"
3. 如果规则中没有相关信息，才说"建议咨询辅导员"
4. 回答要**具体、完整**，包含时间、地点、流程等关键信息

【回答】
"""
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=500
        )
        return response.choices[0].message.content, sources
    except Exception as e:
        return f"调用API失败：{e}", []