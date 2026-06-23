# src/rag.py
import os

# 强制使用国内镜像
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings  # 使用OpenAI嵌入
from prompt_templates import RAG_PROMPT

load_dotenv()

# 初始化DeepSeek客户端
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

# 使用在线嵌入模型（OpenAI兼容格式）
# 注意：DeepSeek不支持嵌入，所以这里使用智谱AI或OpenAI的嵌入
# 如果没有其他API，可以使用模拟嵌入
def get_embeddings():
    """获取嵌入模型"""
    try:
        # 尝试使用智谱AI嵌入（需要额外API Key）
        # 或者使用OpenAI嵌入（需要OpenAI API Key）
        # 由于DeepSeek不支持嵌入，我们使用模拟嵌入
        from langchain_community.embeddings import FakeEmbeddings
        return FakeEmbeddings(size=384)
    except:
        # 如果上面都失败，使用本地模型（但会慢一些）
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

# 加载嵌入模型
embeddings = get_embeddings()

def load_vector_db():
    """加载向量数据库"""
    try:
        vector_db = Chroma(
            persist_directory="./vector_db",
            embedding_function=embeddings
        )
        return vector_db
    except Exception as e:
        print(f"⚠️ 向量数据库加载失败：{e}")
        # 创建空向量库
        from langchain_community.vectorstores import Chroma
        vector_db = Chroma.from_texts(
            texts=["暂无数据"],
            embedding=embeddings,
            persist_directory="./vector_db"
        )
        vector_db.persist()
        return vector_db

# 加载向量数据库
vector_db = load_vector_db()

def rag_answer(question, k=5):
    """RAG问答函数"""
    try:
        # 1. 检索
        docs = vector_db.similarity_search(question, k=k)
        
        # 2. 构建上下文
        context_parts = []
        for i, doc in enumerate(docs, 1):
            q = doc.metadata.get('question', '')
            answer = doc.page_content
            category = doc.metadata.get('category', '')
            context_parts.append(f"【{category}】问题：{q}\n答案：{answer}")
        
        context = "\n\n".join(context_parts)
        
        # 3. 构建提示词
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
        
        # 4. 调用DeepSeek API
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
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=500
        )
        return response.choices[0].message.content, sources
    
    except Exception as e:
        return f"❌ 处理失败：{e}", []