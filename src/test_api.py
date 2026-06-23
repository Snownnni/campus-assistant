# src/app.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from chat_memory import ConversationMemory, chat_with_memory

# 页面配置
st.set_page_config(
    page_title="校园百事通 - 安徽交通职业技术学院",
    page_icon="🏫",
    layout="wide"
)

# 自定义CSS样式
st.markdown("""
<style>
    .stApp {
        background: #f0f2f5 !important;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a73e8;
        text-align: center;
        padding: 20px 0 5px 0;
    }
    .sub-header {
        text-align: center;
        color: #5f6368;
        font-size: 1rem;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 2px solid #a4dee1;
    }
    .welcome-banner {
        background: linear-gradient(135deg, #3aaeff, #59bcf6);
        color: white;
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .welcome-banner h3 {
        margin: 0;
        font-weight: 600;
    }
    .welcome-banner p {
        margin: 5px 0 0 0;
        opacity: 0.9;
        font-size: 0.95rem;
    }
    /* 用户消息 */
    .stChatMessage[data-testid="user"] {
        background: linear-gradient(135deg, #3aaeff, #59bcf6) !important;
        color: white !important;
        border-radius: 15px !important;
        padding: 12px 16px !important;
    }
    /* 助手消息 */
    .stChatMessage[data-testid="assistant"] {
        background: #ffffff !important;
        border: 1px solid #c2ecd6 !important;
        border-radius: 15px !important;
        padding: 12px 16px !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== 侧边栏 ==========
with st.sidebar:
    st.markdown("### 🏫 安徽交通职业技术学院")
    st.markdown("#### AI 校园智能助手")
    st.markdown("---")
    st.markdown("### ✨ 功能")
    st.markdown("""
    - 📅 查询校历周数
    - 📊 计算平均绩点
    - 📈 学期进度查询
    - ❓ 校园规则问答
    """)
    st.markdown("---")
    st.markdown("### 🚀 快捷提问")
    
    quick_questions = [
        "现在第几周？",
        "绩点计算85,90,78",
        "学期进度多少？",
        "怎么请病假？",
        "奖学金要多少绩点？"
    ]
    
    for q in quick_questions:
        if st.button(q, use_container_width=True):
            st.session_state.quick_input = q
    
    st.markdown("---")
    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.messages = []
        st.session_state.memory = ConversationMemory()
        welcome_msg = "👋 你好！我是校园百事通助手，可以帮你查询校历、计算绩点、解答校园规则问题。有什么可以帮你的吗？"
        st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]
        st.rerun()

# ========== 主界面 ==========

# 标题
st.markdown('<div class="main-header">🏫 校园生活百事通助手</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">🤖 AI驱动的校园智能问答系统 · 基于RAG技术</div>', unsafe_allow_html=True)

# 欢迎横幅
st.markdown("""
<div class="welcome-banner">
    <h3>👋 欢迎使用校园百事通！</h3>
    <p>我可以帮你查询校历周数、计算绩点、了解校园规则。试试在下方输入你的问题吧！</p>
</div>
""", unsafe_allow_html=True)

# ========== 初始化会话状态 ==========
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.memory = ConversationMemory()
    welcome_msg = "👋 你好！我是校园百事通助手，可以帮你查询校历、计算绩点、解答校园规则问题。有什么可以帮你的吗？"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

if "quick_input" not in st.session_state:
    st.session_state.quick_input = None

# ========== 处理快捷输入 ==========
if st.session_state.quick_input:
    prompt = st.session_state.quick_input
    st.session_state.quick_input = None
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        response, st.session_state.memory = chat_with_memory(prompt, st.session_state.memory)
    except Exception as e:
        response = f"❌ 发生错误：{e}"
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# ========== 显示聊天历史 ==========
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ========== 输入框 ==========
prompt = st.chat_input("💬 输入你的问题...")

if prompt:
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 显示用户消息
    with st.chat_message("user"):
        st.write(prompt)
    
    # 调用智能体
    with st.chat_message("assistant"):
        with st.spinner("🤔 正在思考..."):
            try:
                response, st.session_state.memory = chat_with_memory(prompt, st.session_state.memory)
            except Exception as e:
                response = f"❌ 发生错误：{e}"
        st.write(response)
    
    # 添加助手消息
    st.session_state.messages.append({"role": "assistant", "content": response})