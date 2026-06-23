import os
import sys
from dotenv import load_dotenv
import hashlib
import struct
import json
import time

# 尽量避免在模块导入时执行网络请求；仅在 __main__ 做自测
load_dotenv()

# 环境变量（可选）
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def _hash_to_vector(text: str, dim: int = 8):
    """简单、无外部依赖的确定性向量回退（基于 SHA256）。"""
    h = hashlib.sha256(text.encode("utf-8")).digest()
    # 将字节切片为 dim 个 8-byte 区块并转换为 float
    vec = []
    for i in range(dim):
        start = (i * 4) % len(h)
        chunk = h[start:start + 4]
        # 保证长度为4
        if len(chunk) < 4:
            chunk = (chunk + b"\x00\x00\x00\x00")[:4]
        val = struct.unpack("I", chunk)[0]
        vec.append((val % 10000) / 10000.0)
    return vec


def get_embedding(text: str, provider: str = "auto") -> list:
    """获取文本嵌入：
    优先顺序：
      1. DeepSeek OpenAI-compatible 接口（若设置了 DEEPSEEK_* 环境变量 并且可用）
      2. OpenAI API（若设置了 OPENAI_API_KEY）
      3. 本地确定性哈希回退（无需网络）

    返回一个浮点列表作为嵌入向量。
    """
    text = text or ""

    # 延迟导入以避免导入时失败
    if provider in ("auto", "deepseek") and DEEPSEEK_API_KEY and DEEPSEEK_BASE_URL:
        try:
            # 尝试使用 requests 调用 DeepSeek 风格的 OpenAI 兼容 embeddings 接口
            import requests

            url = DEEPSEEK_BASE_URL.rstrip("/") + "/v1/embeddings"
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {"model": "deepseek-embedding", "input": text}
            resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
            if resp.status_code == 200:
                j = resp.json()
                # 兼容 OpenAI 返回结构或自定义结构
                if "data" in j and isinstance(j["data"], list) and "embedding" in j["data"][0]:
                    return j["data"][0]["embedding"]
                if "embedding" in j:
                    return j["embedding"]
                # 未识别结构，回退
            else:
                # 明确告诉用户 404/401 等问题
                print(f"DeepSeek 返回状态码 {resp.status_code}：{resp.text}")
        except requests.exceptions.Timeout:
            print("请求 DeepSeek 时发生超时（timeout）。将回退到其他提供者。")
        except Exception as e:
            print(f"DeepSeek 嵌入调用失败：{e}")

    if provider in ("auto", "openai") and OPENAI_API_KEY:
        try:
            # 使用 openai 包的嵌入（若已安装并配置）
            import openai

            openai.api_key = OPENAI_API_KEY
            # 如果需要自定义 base，可通过 OPENAI_API_BASE 环境变量支持
            resp = openai.Embedding.create(model="text-embedding-3-small", input=text)
            if resp and "data" in resp and len(resp["data"]) > 0:
                return resp["data"][0]["embedding"]
        except Exception as e:
            print(f"OpenAI 嵌入调用失败：{e}")

    # 最后回退：本地哈希向量（保证脚本在离线或网络受限时可运行）
    print("使用本地哈希回退生成嵌入（无网络依赖）。")
    return _hash_to_vector(text, dim=8)


if __name__ == "__main__":
    # 简单自测：从命令行读取文本并打印嵌入长度与示例
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--text", "-t", default="测试文本：你好世界", help="待嵌入的文本")
    args = parser.parse_args()
    t0 = time.time()
    emb = get_embedding(args.text)
    t1 = time.time()
    print(f"嵌入向量长度：{len(emb)}，前8个元素：{emb[:8]}")
    print(f"耗时：{t1-t0:.3f}s")