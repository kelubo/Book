# -*- coding: utf-8 -*-
"""r32 锚点核验"""
import io, os, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
P = os.path.join(BASE, "book.tex")
text = io.open(P, encoding="utf-8", newline="").read()
lines = text.split("\r\n")

anchors = [
    r"\subsection{性行为中的伦理与法律问题}",
    r"\subsection{约会软件安全使用指南}",
    r"\subsubsection{女女性行为}",  # 预期不存在
    r"\section{传教士体位（男上女下）}",
]
for a in anchors:
    print(lines.count(a), "|", a)

print()
print("== 搜索女同/性少数相关结构 ==")
pat = re.compile(r"\\(section|subsection|subsubsection)\{([^{}]*)\}")
for i, l in enumerate(lines, 1):
    m = pat.match(l.strip())
    if not m:
        continue
    t = m.group(2)
    if any(k in t for k in ["女同", "同性", "LGBTQ", "性取向", "性少数", "蕾丝"]):
        print("L%-6d %s %s" % (i, m.group(1), t))
