import os
# 强制使用hf国内镜像站，解决10060连接超时
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
# src/test_retrieve.py
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 1. 加载和构建向量库时完全一致的嵌入模型
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh"
)

# 2. 加载本地持久化向量库
vector_db = Chroma(
    persist_directory=r"./vector_db",
    embedding_function=embeddings
)

# 3. 课件检索函数
def search_knowledge(query):
    # k=3 检索相似度最高3条数据
    results = vector_db.similarity_search(query, k=3)
    for r in results:
        print(f"元数据信息：{r.metadata}")
        print(f"问答内容：{r.page_content}\n")
    return results

# 测试提问
if __name__ == "__main__":
    search_knowledge("3 天内的事假需要走什么审批流程？")