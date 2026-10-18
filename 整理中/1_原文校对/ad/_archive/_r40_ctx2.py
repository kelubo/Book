# -*- coding: utf-8 -*-
"""r40 探测第 3 轮：补充词面 + 定点上下文抽查"""
import re, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FILES = ["book.tex", "female.tex", "male.tex"]

texts = {}
for fn in FILES:
    raw = open(os.path.join(BASE, fn), "rb").read()
    crlf = "\r\n" if b"\r\n" in raw else "\n"
    texts[fn] = raw.decode("utf-8").split(crlf)

# (A) 补充词面
KWS = ["大麻", "毒品", "摇头丸", "GHB", "性瘾", "强迫性性行为", "隆胸", "阴茎增大",
       "纹身", "穿环", "罕见病", "男性更年期", "迟发性", "健身", "力量训练", "吸烟",
       "职场", "同事", "上司", "情趣娃娃", "娃娃", "白癜风", "银屑", "单身", "进食障碍",
       "丧偶", "创伤后", "PTSD", "早泄", "阴道痉挛", "性欲低下", "润滑", "夜店", "酒吧",
       "游戏", "网瘾", "月经杯", "棉条", "卫生棉", "母乳", "遗精", "手淫", "自慰"]

print("==== (A) 补充词面 ====")
for kw in KWS:
    total = 0
    samples = []
    for fn in FILES:
        for i, ln in enumerate(texts[fn], 1):
            st = ln.strip()
            if st.startswith("%"):
                continue
            if kw in st:
                total += 1
                if len(samples) < 3:
                    samples.append("%s L%d: %s" % (fn, i, st[:80]))
    tag = "BLANK" if total == 0 else ("THIN" if total <= 5 else "")
    print("[%3d]%s %s" % (total, (" " + tag) if tag else "", kw))
    if total <= 5:
        for s in samples:
            print("     " + s)

# (B) 定点上下文
SPOTS = [
    ("book.tex", 25500, 25560, "AI伴侣/VR 节结构"),
    ("book.tex", 24670, 24715, "多元关系节"),
    ("book.tex", 20000, 20040, "性伤害分级上下文"),
    ("book.tex", 1315, 1345, "独身节"),
    ("book.tex", 27970, 28000, "特殊职业节"),
    ("book.tex", 18200, 18225, "性短信/隐私（青少年）"),
]
print("\n==== (B) 定点上下文 ====")
for fn, a, b, label in SPOTS:
    print("--- %s (%s L%d-L%d) ---" % (label, fn, a, b))
    # 先打印该范围内的标题结构
    for i in range(a, min(b, len(texts[fn]))):
        st = texts[fn][i - 1].strip()
        if st.startswith("\\chapter") or st.startswith("\\section") or st.startswith("\\subsection") or st.startswith("\\subsubsection") or st.startswith("\\subparagraph"):
            print("  HDR L%d: %s" % (i, st[:100]))
    print()
