# -*- coding: utf-8 -*-
"""r34 锚点核验 + 落位结构确认"""
import io, os, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
text = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read()
lines = text.split("\r\n")

anchors = [
    r"\subsubsection{性别确认医疗服务}",
    r"\section{性健康资源与支持}",
    r"\subsection{性侵犯与性暴力的法律应对}",
    r"\subsubsection{肛交的技巧与安全}",
    r"\subsection{性犯罪与法律责任}",
    r"\section{性创伤与心理康复}",
]
print("== 锚点计数 ==")
for a in anchors:
    print(lines.count(a), "|", a)

print()
print("== L14748-14800（跨性别医疗落位）==")
for i in range(14748, 14801):
    s = lines[i - 1].strip()
    if s:
        print("L%-6d %s" % (i, s[:120]))

print()
print("== 扫描 肛交/性病风险 相关节标题 ==")
pat = re.compile(r"\\(section|subsection|subsubsection)\{([^{}]*)\}")
for i, l in enumerate(lines, 1):
    m = pat.match(l.strip())
    if m and any(k in m.group(2) for k in ["肛", "口交", "乳交", "性病风险", "性传播感染", "伴侣告知"]):
        print("L%-6d %s %s" % (i, m.group(1), m.group(2)[:70]))
