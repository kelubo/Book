# -*- coding: utf-8 -*-
import re, os

base = r"D:/Git/Book/整理中/1_原文校对/ad"
files = {"book": "book.tex", "female": "female.tex", "male": "male.tex"}
texts = {}
for k, f in files.items():
    with open(os.path.join(base, f), "r", encoding="utf-8") as fp:
        texts[k] = fp.read()

candidates = [
    "性交后头痛", "交配后头痛", "性交后悲伤", "性交后烦躁", "性交后忧郁",
    "性交后不适", "性交后出血", "性交后尿痛", "性交后尿路", "性交后护理", "性交后清洁",
    "青少年性健康", "青少年性咨询", "青少年性教育", "青春期性健康",
    "阴毛修剪", "阴毛剃", "剃毛", "比基尼线", "激光脱毛", "毛囊炎",
    "私处美白", "私处漂白", "私处香氛", "私处护理品", "嫩红",
    "性交恐惧", "性交疼痛恐惧", "coitophobia", "初夜", "处子",
    "小阴唇", "阴唇肥大", "阴唇外观", "外阴外观焦虑", "私处外观",
    "多重高潮", "连续高潮", "不应期", "性交后不应期",
    "阴道痉挛", "初夜出血", "处女膜",
]

print("主题".ljust(20), "book".rjust(6), "female".rjust(8), "male".rjust(6), sep="")
print("-" * 50)
for c in candidates:
    counts = []
    for k in ["book", "female", "male"]:
        counts.append(len(re.findall(re.escape(c), texts[k])))
    flag = ""
    total = sum(counts)
    if total == 0:
        flag = "  <== 全空白"
    elif total <= 3:
        flag = "  <- 极薄"
    print(c.ljust(20), str(counts[0]).rjust(6), str(counts[1]).rjust(8), str(counts[2]).rjust(6), flag, sep="")
