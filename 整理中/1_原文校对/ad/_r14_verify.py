# -*- coding: utf-8 -*-
"""Verify TOC line numbers for the six new sections."""
import re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
toc = open(BASE + r"\_全书导览_三卷目录总览_2026-09-08.md", "rb").read().decode("utf-8")
checks = [
    ("book.tex", "第一次就诊：流程、如何开口与费用参考"),
    ("book.tex", "年度性健康自查清单"),
    ("book.tex", "分手之后：协商删除与隐私重建"),
    ("book.tex", "出差、旅行与酒店：路上的性健康"),
    ("male.tex", "赛前禁欲与运动表现：迷思与真相"),
    ("male.tex", "捐精者视角：报名、流程与责任"),
]
ok = True
BS = chr(92)
for fn, title in checks:
    lines = open(BASE + "\\" + fn, "rb").read().decode("utf-8").split(chr(13) + chr(10))
    real = []
    for i, l in enumerate(lines):
        st = l.strip()
        if title in l and any(st.startswith(BS + w + "{") for w in
                              ("section", "subsection", "subsubsection", "subparagraph", "chapter")):
            real.append(i + 1)
    m = re.search(r"(\d+)｜" + re.escape(title), toc)
    tocno = int(m.group(1)) if m else None
    match = bool(real) and tocno in real
    ok = ok and match
    print(fn[:5], title[:18], "real=", real, "toc=", tocno, "OK" if match else "MISMATCH")
print("ALL LINE NUMBERS OK" if ok else "PROBLEM FOUND")
