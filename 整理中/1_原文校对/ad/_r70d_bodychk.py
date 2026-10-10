# -*- coding: utf-8 -*-
"""r70d：核对骨架各章正文行数（只读）。"""
import re

lines = open("book.tex", encoding="utf-8").read().split("\n")
i_old = next(i for i, l in enumerate(lines) if l.strip() == r"\part{old}")
T = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection|paragraph)\*?\s*\{")

cur = None
res = []
for i in range(140, i_old):
    ln = lines[i]
    m = T.match(ln)
    if m and m.group(1) == "chapter":
        cur = [ln.strip(), 0, i + 1]
        res.append(cur)
        continue
    if m:
        continue
    t = ln.strip()
    if cur and t and not t.startswith("%"):
        cur[1] += 1

for nm, n, ln in res:
    if n:
        print("L%-6d %-24s 正文行 %d" % (ln, nm, n))
print("总章数", len(res), "有正文", sum(1 for _, n, _ in res if n))
