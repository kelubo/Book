# -*- coding: utf-8 -*-
import re, os

base = r"D:/Git/Book/整理中/1_原文校对/ad"
files = {"book": "book.tex", "female": "female.tex", "male": "male.tex"}
texts = {}
for k, f in files.items():
    with open(os.path.join(base, f), "r", encoding="utf-8") as fp:
        texts[k] = fp.read()

candidates = [
    "遗精", "梦遗", "滑精", "晨勃", "夜间勃起",
    "男性乳房发育", "男性乳腺增生", "gynecomastia",
    "包皮环切", "包皮术后", "术后护理",
    "青春期性咨询", "遗精焦虑", "手淫焦虑", "手淫负罪",
    "男性性交后", "射精后", "射精痛", "射精后疼痛", "射精后头痛",
    "男性尿路感染", "尿道炎", "前列腺按摩",
    "男性盆底肌", "凯格尔（男性）", "会阴", "骑跨伤",
    "精索", "睾丸自检", "阴囊潮湿", "阴囊湿疹",
    "男性性欲周期", "男性更年期",
    "单身男性", "长期禁欲", "性节制", "戒色",
    "固定伴侣", "性生活频率", "性生活和谐",
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
