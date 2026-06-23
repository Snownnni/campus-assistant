# src/tools.py
from datetime import datetime
import re

def get_current_week():
    start_date = datetime(2025, 9, 1)
    today = datetime.now()
    delta = today - start_date
    if delta.days < 0:
        return "新学期还未开始，请耐心等待开学！"
    week_num = delta.days // 7 + 1
    return f"📅 现在是第 {week_num} 周"

def calculate_gpa(scores_str):
    try:
        scores = re.findall(r'\d+', scores_str)
        if not scores:
            return "请提供具体的分数，例如：85,90,78"
        scores = [int(s) for s in scores]
        total = 0
        for s in scores:
            if s >= 90:
                total += 4.0
            elif s >= 80:
                total += 3.0
            elif s >= 70:
                total += 2.0
            elif s >= 60:
                total += 1.0
            else:
                total += 0
        gpa = total / len(scores)
        return f"📊 您的平均绩点（GPA）是：{gpa:.2f}"
    except Exception as e:
        return f"计算失败：{e}，请检查输入格式"

def get_semester_progress():
    start_date = datetime(2025, 9, 1)
    end_date = datetime(2026, 1, 15)
    today = datetime.now()
    total_days = (end_date - start_date).days
    passed_days = (today - start_date).days
    if passed_days < 0:
        return "学期还未开始"
    elif passed_days > total_days:
        return "本学期已结束"
    progress = passed_days / total_days * 100
    return f"📈 学期进度：{progress:.1f}%"
