# src/preload.py
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

print("🔄 正在预加载模型...")

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("📥 加载嵌入模型...")
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh",
    model_kwargs={'device': 'cpu'}
)

print("📂 加载向量数据库...")
vector_db = Chroma(
    persist_directory="./vector_db",
    embedding_function=embeddings
)

print("✅ 模型预加载完成！")