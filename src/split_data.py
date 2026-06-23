import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. 读取校园问答CSV数据集
def load_campus_csv(file_path="./data/campus_data.csv"):
    # Windows中文文件用gbk编码
    df = pd.read_csv(file_path, encoding="gbk")
    all_text = ""
    # 把每条问答拼接成完整长文本
    for idx, row in df.iterrows():
        single_text = f"分类：{row['category']}\n问题：{row['question']}\n答案：{row['answer']}\n资料来源：{row['source']}\n------\n"
        all_text += single_text
    return all_text

# 2. 文本切分函数
def split_long_text(long_text):
    # 递归字符文本分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,    # 单块文本最大200字符
        chunk_overlap=20,  # 块之间重叠20字符，保证上下文不丢失
        separators=["\n------\n", "\n", "，", "。", "、"]  # 优先按问答分隔线切割
    )
    chunks = text_splitter.split_text(long_text)
    return chunks

if __name__ == "__main__":
    # 加载完整问答文本
    full_text = load_campus_csv()
    # 执行切分
    text_chunks = split_long_text(full_text)
    
    print(f"文本切分完成，总块数：{len(text_chunks)}")
    print("=" * 50)
    # 打印前3块预览效果
    for i, chunk in enumerate(text_chunks[:3]):
        print(f"【文本块{i+1}】\n{chunk}\n")