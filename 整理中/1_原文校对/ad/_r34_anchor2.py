# -*- coding: utf-8 -*-
"""r34 精确锚点核验"""
import io, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
text = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read()
lines = text.split("\r\n")

for a in [r"\subsection{性与亲密关系的维护}", r"\subsubsection{肛交}",
          r"\subsection{性侵犯与性暴力的法律应对}", r"\subsubsection{中国的现状}",
          r"\section{性创伤与心理康复}"]:
    print(lines.count(a), "|", a)

print()
print("== L28615-28640（肛交小节周边）==")
for i in range(28615, 28641):
    s = lines[i - 1].strip()
    if s:
        print("L%-6d %s" % (i, s[:115]))
print()
print("== L39350-39375（性侵犯法律应对周边）==")
for i in range(39350, 39376):
    s = lines[i - 1].strip()
    if s:
        print("L%-6d %s" % (i, s[:115]))
