# -*- coding: utf-8 -*-
"""第十六轮：新方向候选主题探测"""
import re, os

BASE = r"D:/Git/Book/整理中/1_原文校对/ad"
files = {"book": "book.tex", "female": "female.tex", "male": "male.tex"}
texts = {}
for k, f in files.items():
    with open(os.path.join(BASE, f), encoding="utf-8") as fp:
        texts[k] = fp.read()

candidates = [
    # 单身/无性/节制
    "单身", "独居", "长期无性生活", "无性婚姻", "性节制", "戒色", "NoFap",
    "性欲管理", "禁欲", "性欲周期", "性欲节律",
    # 性心理/行为
    "性幻想", "性梦", "恋物", "性偏好", "性成瘾", "强迫性性行为",
    "网络色情", "色情成瘾", "交友软件", "线上约会",
    # 感染
    "生殖器疱疹", "尖锐湿疣", "HPV疫苗", "衣原体", "支原体", "滴虫",
    "阴虱", "疥疮", "梅毒", "乙肝与性", "猴痘", "mpox",
    # 药物/物质
    "SSRI", "抗抑郁药与性", "抗精神病药", "降压药与性", "非那雄胺",
    "壮阳药", "保健品", "西地那非", "达泊西汀",
    # 生活因素
    "桑拿", "骑行", "久坐", "手机辐射", "电子烟", "大麻", "咖啡因",
    "睡眠与性", "熬夜", "时差",
    # 身体/手术
    "子宫切除", "乳房切除", "造口", "器官移植", "癫痫与性",
    "多发性硬化", "脊髓损伤", "甲状腺", "肝病与性",
    # 多元群体
    "性取向", "跨性别", "无性恋", "双性恋", "出柜", "性别肯定激素",
    "残疾与性", "自闭症", "智力障碍",
    # 性玩具/用品
    "性玩具", "情趣用品", "跳蛋", "按摩棒", "润滑剂选择", "乳胶过敏", "避孕套过敏",
    # 服务/咨询
    "性治疗师", "性咨询", "性教育课程", "性健康App",
]

print("主题".ljust(20), "book".rjust(6), "female".rjust(8), "male".rjust(6), sep="")
print("-" * 52)
blank = []
thin = []
for c in candidates:
    counts = [len(re.findall(re.escape(c), texts[k])) for k in ["book", "female", "male"]]
    total = sum(counts)
    flag = ""
    if total == 0:
        flag = "  <== 空白"; blank.append(c)
    elif total <= 3:
        flag = "  <- 极薄"; thin.append(c)
    print(c.ljust(20), str(counts[0]).rjust(6), str(counts[1]).rjust(8), str(counts[2]).rjust(6), flag, sep="")
print()
print("【全空白】", "、".join(blank))
print("【极薄】", "、".join(thin))
