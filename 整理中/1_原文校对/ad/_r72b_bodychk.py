# -*- coding: utf-8 -*-
"""统计 book.tex 骨架区各章的实际正文行数（判断哪些章是纯占位）。"""
import io
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
raw = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read()
raw = raw.replace("\r\n", "\n")
lines = raw.split("\n")
si = next(i for i, l in enumerate(lines) if l.strip() == "\\begin{document}")
ei = next(i for i, l in enumerate(lines) if l.strip() == "\\part{old}")
T = re.compile(r"^\\(part|chapter|section|subsection)\*?\{")

cur = None
body = {}
order = []
for i in range(si, ei):
    s = lines[i].strip()
    m = T.match(s)
    if m and m.group(1) == "chapter":
        e = s.index("}", m.end())
        cur = s[m.end():e].strip()
        order.append(cur)
        body[cur] = 0
        continue
    if not s or s.startswith("%"):
        continue
    if T.match(s):
        continue
    if cur:
        body[cur] += 1

for c in order:
    print("%-30s %d" % (c, body[c]))
