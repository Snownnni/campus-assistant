# src/app.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from datetime import datetime
from chat_memory import ConversationMemory, chat_with_memory
from agent import agent_chat
from rag import rag_answer

# 页面配置
st.set_page_config(
    page_title="校园百事通 - 安徽交通职业技术学院",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== 自定义CSS样式 ==========
st.markdown("""
<style>
    /* 全局样式 - 右侧主区域淡灰色背景 */
    .stApp {
        background: #f0f2f5 !important;  /* 主区域淡灰色 */
    }
    
    /* 主内容区域 - 淡灰色 */
    .main > div {
        background: #f0f2f5 !important;
    }
    
    /* 块容器 - 淡灰色 */
    .block-container {
        background: #f0f2f5 !important;
        padding-top: 2rem !important;
    }
    
    /* 主标题 - 使用 #3aaeff */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #3aaeff, #59bcf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px 0 5px 0;
        letter-spacing: 2px;
    }
    
    .main-header-icon {
        font-size: 3rem;
        -webkit-text-fill-color: initial;
    }
    
    /* 副标题 - 使用 #7ccbed */
    .sub-header {
        text-align: center;
        color: #7ccbed;
        font-size: 1.1rem;
        margin-bottom: 30px;
        padding-bottom: 20px;
        border-bottom: 3px solid #a4dee1;
    }
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background: linear-gradient(180deg, #e7ffc9 0%, #c2ecd6 100%) !important;
    }
    
    /* 侧边栏标题 */
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #3aaeff;
        text-align: center;
        margin: 10px 0;
    }
    
    .sidebar-subtitle {
        text-align: center;
        color: #7ccbed;
        font-size: 0.9rem;
        margin-bottom: 20px;
    }
    
    /* 功能项 */
    .feature-item {
        background: linear-gradient(135deg, #c2ecd6, #a4dee1);
        border-radius: 10px;
        padding: 10px 15px;
        margin: 8px 0;
        border-left: 4px solid #3aaeff;
        color: #2c3e50;
    }
    
    .feature-item:hover {
        transform: translateX(5px);
        transition: 0.3s;
        box-shadow: 0 2px 8px rgba(58, 174, 255, 0.3);
    }
    
    /* 快捷按钮样式 */
    .quick-btn {
        background: linear-gradient(135deg, #c2ecd6, #a4dee1) !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 8px 16px !important;
        margin: 4px 0 !important;
        color: #2c3e50 !important;
        font-weight: 500 !important;
        transition: all 0.3s !important;
        width: 100% !important;
        text-align: left !important;
    }
    
    .quick-btn:hover {
        background: linear-gradient(135deg, #3aaeff, #59bcf6) !important;
        color: white !important;
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(58, 174, 255, 0.4);
    }
    
    /* 消息气泡样式 */
    .stChatMessage {
        border-radius: 15px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* 用户消息 - 使用 #3aaeff 渐变 */
    .stChatMessage[data-testid="user"] {
        background: linear-gradient(135deg, #3aaeff, #59bcf6) !important;
        color: white !important;
        border-bottom-right-radius: 5px !important;
    }
    
    /* 助手消息 - 白色背景 */
    .stChatMessage[data-testid="assistant"] {
        background: #ffffff !important;
        border: 1px solid #c2ecd6 !important;
        border-bottom-left-radius: 5px !important;
        color: #2c3e50 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    }
    
    /* 统计卡片 */
    .stat-card {
        background: #e7ffc9;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: 10px 0;
        border: 1px solid #c2ecd6;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #3aaeff;
    }
    
    .stat-label {
        color: #7ccbed;
        font-size: 0.85rem;
    }
    
    /* 清空按钮 */
    .clear-btn {
        background: linear-gradient(135deg, #3aaeff, #59bcf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 8px 20px !important;
        font-weight: 500 !important;
        transition: all 0.3s !important;
    }
    
    .clear-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(58, 174, 255, 0.4);
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        border: 2px solid #c2ecd6 !important;
        padding: 12px 20px !important;
        font-size: 1rem !important;
        transition: all 0.3s !important;
        background: #ffffff !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3aaeff !important;
        box-shadow: 0 0 0 3px rgba(58, 174, 255, 0.2) !important;
    }
    
    /* 聊天输入框 */
    .stChatInput > div > div > textarea {
        background: #ffffff !important;
        border-radius: 25px !important;
        border: 2px solid #c2ecd6 !important;
    }
    
    .stChatInput > div > div > textarea:focus {
        border-color: #3aaeff !important;
        box-shadow: 0 0 0 3px rgba(58, 174, 255, 0.2) !important;
    }
    
    /* 底部 */
    .footer {
        text-align: center;
        color: #7ccbed;
        font-size: 0.8rem;
        padding: 20px 0;
        border-top: 2px solid #a4dee1;
        margin-top: 30px;
    }
    
    /* 欢迎横幅 */
    .welcome-banner {
        background: linear-gradient(135deg, #3aaeff, #59bcf6);
        color: white;
        padding: 20px 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(58, 174, 255, 0.3);
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
    
    /* Streamlit 默认按钮覆盖 */
    .stButton > button {
        background: linear-gradient(135deg, #c2ecd6, #a4dee1) !important;
        color: #2c3e50 !important;
        border: 1px solid #a4dee1 !important;
        border-radius: 20px !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3aaeff, #59bcf6) !important;
        color: white !important;
        border-color: #3aaeff !important;
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(58, 174, 255, 0.4);
    }
    
    /* 侧边栏标题分隔线 */
    hr {
        border-color: #a4dee1 !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== 侧边栏 ==========
with st.sidebar:
    # 学校标识
    st.markdown("""
    <div style="text-align: center; padding: 10px 0;">
        <div style="font-size: 4rem;">🏫</div>
        <div class="sidebar-title">安徽交通职业技术学院</div>
        <div class="sidebar-subtitle">AI 校园智能助手</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 功能介绍
    st.markdown("### ✨ 功能")
    st.markdown("""
    <div class="feature-item">📅 查询校历周数</div>
    <div class="feature-item">📊 计算平均绩点</div>
    <div class="feature-item">📈 学期进度查询</div>
    <div class="feature-item">❓ 校园规则问答</div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 快捷提问
    st.markdown("### 🚀 快捷提问")
    quick_questions = [
        ("📅 现在第几周？", "现在第几周？"),
        ("📊 绩点计算85,90,78", "绩点计算85,90,78"),
        ("📈 学期进度多少？", "学期进度多少？"),
        ("💊 怎么请病假？", "怎么请病假？"),
        ("🏆 奖学金要多少绩点？", "奖学金要多少绩点？"),
        ("🛠️ 宿舍灯坏了找谁？", "宿舍灯坏了找谁？"),
        ("💳 一卡通丢了怎么办？", "一卡通丢了怎么办？"),
        ("📚 选错了课能退吗？", "选错了课能退吗？")
    ]
    
    for label, value in quick_questions:
        if st.button(label, key=value, use_container_width=True):
            st.session_state.quick_input = value
    
    st.markdown("---")
    
    # 统计信息
    st.markdown("### 📊 对话统计")
    if "messages" in st.session_state:
        msg_count = len(st.session_state.messages)
        user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user") if msg_count > 0 else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{msg_count}</div>
                <div class="stat-label">总消息</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{user_msgs}</div>
                <div class="stat-label">提问数</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 清空对话
    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.messages = []
        st.session_state.memory = ConversationMemory()
        welcome_msg = "👋 你好！我是校园百事通助手，可以帮你查询校历、计算绩点、解答校园规则问题。有什么可以帮你的吗？"
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
        st.rerun()
    
    # 版本信息
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7ccbed; font-size: 0.75rem;">
        v2.0 | 基于 RAG 技术<br>
        © 2026 安徽交通职业技术学院
    </div>
    """, unsafe_allow_html=True)

# ========== 主界面 ==========

# 主标题
st.markdown(
    """
    <div style="text-align: center;">
        <span style="font-size: 3rem;">🏫</span>
        <span style="font-size: 3rem; font-weight: 800; background: linear-gradient(135deg, #3aaeff, #59bcf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">校园生活百事通助手</span>
    </div>
    <div style="text-align: center; color: #7ccbed; font-size: 1.1rem; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 3px solid #a4dee1;">
        🤖 AI驱动的校园智能问答系统 · 基于检索增强生成（RAG）技术
    </div>
    """,
    unsafe_allow_html=True
)

# 欢迎横幅
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #3aaeff, #59bcf6); color: white; padding: 20px 25px; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(58, 174, 255, 0.3);">
        <h3 style="margin: 0; font-weight: 600;">👋 欢迎使用校园百事通！</h3>
        <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 0.95rem;">我可以帮你查询校历周数、计算绩点、了解校园规则。试试在下方输入你的问题吧！</p>
    </div>
    """,
    unsafe_allow_html=True
)

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
    
    with st.spinner("🤔 思考中..."):
        response, st.session_state.memory = chat_with_memory(prompt, st.session_state.memory)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()

# ========== 显示聊天历史 ==========
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========== 输入框 ==========
if prompt := st.chat_input("💬 输入你的问题..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 调用智能体
    with st.chat_message("assistant"):
        with st.spinner("🤔 正在思考..."):
            try:
                response, st.session_state.memory = chat_with_memory(prompt, st.session_state.memory)
            except Exception as e:
                response = f"❌ 发生错误：{e}"
        
        st.markdown(response)
    
    # 添加助手消息
    st.session_state.messages.append({"role": "assistant", "content": response})

# ========== 底部 ==========
st.markdown(
    """
    <div style="text-align: center; color: #7ccbed; font-size: 0.8rem; padding: 20px 0; border-top: 2px solid #a4dee1; margin-top: 30px;">
        💡 提示：本系统基于校园规则数据生成回答，如有疑问请咨询辅导员
    </div>
    """,
    unsafe_allow_html=True
)