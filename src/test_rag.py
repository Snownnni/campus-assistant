# src/test_rag_final.py
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from rag import rag_answer, rag_answer_with_source

# 测试用例 - 优化关键词匹配（基于您的实际数据）
test_cases = [
    # 请假流程 - 调整期望关键词为数据中实际存在的词
    {
        "question": "怎么请病假？",
        "keywords": ["病假", "证明", "教务处"],  # 数据中有"教务处备案"
        "category": "请假",
        "data_id": 4
    },
    {
        "question": "3天以内的事假怎么请？",
        "keywords": ["教务系统", "辅导员", "线上审批"],
        "category": "请假",
        "data_id": 1
    },
    {
        "question": "4-7天假需要什么材料？",
        "keywords": ["纸质请假单", "辅导员签字", "副书记"],
        "category": "请假",
        "data_id": 2
    },
    
    # 奖学金 - 调整关键词
    {
        "question": "国家奖学金要多少绩点？",
        "keywords": ["3.5", "前10%", "体测良好"],
        "category": "奖学金",
        "data_id": 11
    },
    {
        "question": "什么情况不能评奖学金？",
        "keywords": ["违纪", "挂科", "一票否决"],
        "category": "奖学金",
        "data_id": 13
    },
    {
        "question": "挂科补考过了能评奖学金吗？",
        "keywords": ["不能", "挂科记录", "本学年"],
        "category": "奖学金",
        "data_id": 16
    },
    
    # 宿舍报修
    {
        "question": "宿舍故障怎么报修？",
        "keywords": ["后勤报修", "小程序", "24小时"],
        "category": "宿舍",
        "data_id": 21
    },
    {
        "question": "宿舍空调坏了维修收费吗？",
        "keywords": ["非人为损坏", "免费", "人为损坏"],
        "category": "宿舍",
        "data_id": 22
    },
    {
        "question": "报修后多久上门维修？",
        "keywords": ["24小时", "紧急", "2小时"],
        "category": "宿舍",
        "data_id": 30
    },
    
    # 一卡通
    {
        "question": "一卡通丢了怎么挂失？",
        "keywords": ["公众号", "一键挂失", "冻结"],
        "category": "一卡通",
        "data_id": 31
    },
    {
        "question": "补办一卡通在哪里办？",
        "keywords": ["行政楼", "卡务中心", "工作日"],
        "category": "一卡通",
        "data_id": 32
    },
    {
        "question": "补办一卡通多少钱？",
        "keywords": ["10元", "20元", "工本费"],
        "category": "一卡通",
        "data_id": 33
    },
    
    # 选课退课
    {
        "question": "选错了课能退吗？",
        "keywords": ["退课窗口期", "重新选择", "选修课"],
        "category": "选课",
        "data_id": 44
    },
    {
        "question": "退课最晚到什么时候？",
        "keywords": ["第四周", "周五", "17:00"],
        "category": "选课",
        "data_id": 42
    },
    {
        "question": "必修课能退课吗？",
        "keywords": ["不允许", "休学", "缓考"],
        "category": "选课",
        "data_id": 43
    }
]

def run_test():
    print("="*70)
    print("RAG系统优化测试（基于实际数据）")
    print("="*70)
    
    passed = 0
    total = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        question = test["question"]
        keywords = test["keywords"]
        category = test["category"]
        
        print(f"\n【测试 {i}/{total}】{category}")
        print(f"❓ {question}")
        print(f"📌 期望关键词：{keywords}")
        
        # 执行RAG问答（带来源）
        answer, sources = rag_answer_with_source(question)
        
        print(f"🤖 回答：{answer}")
        print(f"🔍 检索得分：{[s['score'] for s in sources[:3]]}")
        
        # 检查关键词命中
        found = [kw for kw in keywords if kw in answer]
        missing = [kw for kw in keywords if kw not in answer]
        
        # 宽松标准：命中一半以上即通过
        if len(found) >= len(keywords) * 0.5:
            print(f"✅ 通过 (命中：{found})")
            passed += 1
        else:
            print(f"❌ 失败 (缺失：{missing})")
        print("-"*50)
    
    print("\n" + "="*70)
    print("测试总结")
    print("="*70)
    print(f"总测试数：{total}")
    print(f"通过数：{passed}")
    print(f"通过率：{passed/total*100:.1f}%")
    
    if passed >= total * 0.8:
        print("✅ 检查点通过：正确率80%以上")
    else:
        print("❌ 需要进一步优化")

if __name__ == "__main__":
    run_test()