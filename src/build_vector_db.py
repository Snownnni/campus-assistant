# src/build_vector_db.py
import os
# 强制使用国内镜像站
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

import pandas as pd
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 原有代码不变
df = pd.read_csv(r"data/campus_data.csv", encoding="gbk")
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh"
)
texts = df['answer'].tolist()
metadatas = df[['id', 'category', 'question']].to_dict('records')
vector_db = Chroma.from_texts(
    texts=texts,
    embedding=embeddings,
    metadatas=metadatas,
    persist_directory='./vector_db'
)
vector_db.persist()
print(f"已存入{len(texts)}条问答记录到向量库")