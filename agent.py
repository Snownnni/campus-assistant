# src/agent.py
import os
import re
from datetime import datetime

from tools import get_current_week, calculate_gpa, get_semester_progress

# 学期结束日期
SEMESTER_END_DATE = datetime(2026, 7, 15)

def extract_week_from_context(context):
    """从上下文中提取周数"""
    if not context:
        return None
    for msg in context:
        content = msg.get("content", "")
        week_match = re.search(r'第\s*(\d+)\s*周', content)
        if week_match:
            return int(week_match.group(1))
    return None

def extract_gpa_from_context(context):
    """从上下文中提取绩点"""
    if not context:
        return None
    for msg in context:
        content = msg.get("content", "")
        gpa_match = re.search(r'绩点.*?(\d+\.?\d*)', content)
        if gpa_match:
            return float(gpa_match.group(1))
    return None

def get_remaining_weeks_from_date(today=None):
    """计算距离学期结束还有几周"""
    if today is None:
        today = datetime.now()
    
    if today > SEMESTER_END_DATE:
        return 0, 0, "本学期已结束"
    
    total_days = (SEMESTER_END_DATE - today).days
    weeks_left = total_days // 7
    days_left = total_days % 7
    
    return weeks_left, days_left, None

def get_weeks_until_end():
    """计算距离学期结束还有几周"""
    if datetime.now() > SEMESTER_END_DATE:
        return "本学期已结束"
    
    weeks_left, days_left, _ = get_remaining_weeks_from_date()
    
    if weeks_left <= 0:
        return "本学期即将结束！"
    
    return f"距离学期结束还有 {weeks_left} 周 {days_left} 天"

def detect_intent(user_input, context=None):
    """意图识别"""
    user_lower = user_input.lower()
    
    # 检查是否是追问
    if user_input.startswith("那") or user_input.startswith("那么"):
        week = extract_week_from_context(context)
        if week:
            return "query_week_with_context"
        gpa = extract_gpa_from_context(context)
        if gpa:
            return "query_gpa_with_context"
    
    # 查询周数
    if ("周" in user_input and ("几" in user_input or "校历" in user_input or "第几" in user_input)):
        return "get_week"
    
    # 距离期末
    if "期末" in user_input and ("几周" in user_input or "多久" in user_input):
        return "weeks_until_end"
    
    # 计算绩点
    if "绩点" in user_input or "GPA" in user_input or "gpa" in user_input:
        if re.search(r'\d+', user_input):
            return "calc_gpa"
        else:
            return "ask_gpa_score"
    
    # 学期进度
    if "学期进度" in user_input or "学期过了" in user_input:
        return "semester_progress"
    
    return "rag_qa"

def extract_scores(text):
    """从文本中提取分数"""
    scores = re.findall(r'\d+', text)
    return scores

def agent_chat(user_input, context=None):
    """智能体对话函数"""
    intent = detect_intent(user_input, context)
    
    if intent == "get_week":
        return get_current_week()
    
    elif intent == "query_week_with_context":
        week = extract_week_from_context(context)
        if week:
            weeks_left, days_left, status = get_remaining_weeks_from_date()
            if status == "本学期已结束":
                return f"现在是第 {week} 周，本学期已结束"
            if weeks_left <= 0:
                return f"现在是第 {week} 周，本学期即将结束！"
            return f"现在是第 {week} 周，距离学期结束还有 {weeks_left} 周"
        else:
            return get_current_week()
    
    elif intent == "weeks_until_end":
        return get_weeks_until_end()
    
    elif intent == "query_gpa_with_context":
        gpa = extract_gpa_from_context(context)
        if gpa:
            return f"您之前的绩点是 {gpa:.2f}，需要我帮您重新计算吗？"
        return "请告诉我您的各科分数，例如：85,90,78"
    
    elif intent == "calc_gpa":
        scores = extract_scores(user_input)
        if scores:
            return calculate_gpa(','.join(scores))
        else:
            return "请提供您的各科分数，例如：85,90,78"
    
    elif intent == "ask_gpa_score":
        return "请提供您的各科分数，例如：85,90,78，我来帮您计算绩点"
    
    elif intent == "semester_progress":
        return get_semester_progress()
    
    else:
        # 默认走RAG问答
        from rag import rag_answer
        return rag_answer(user_input)