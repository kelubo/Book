# -*- coding: utf-8 -*-
"""检查 book.tex 骨架区（\begin{document} .. \part{old}）里是否存在带缩进的标题行。"""
import io
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
raw = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read().replace("\r\n", "\n")
lines = raw.split("\n")
si = next(i for i, l in enumerate(lines) if l.strip() == "\\begin{document}")
ei = next(i for i, l in enumerate(lines) if l.strip() == "\\part{old}")
pat = re.compile(r"^\s+\\(part|chapter|section|subsection)\*?\{")
bad = [(i + 1, lines[i]) for i in range(si, ei) if pat.match(lines[i])]
print("缩进标题行数：", len(bad))
for ln, txt in bad[:40]:
    print("  L%d %r" % (ln, txt[:90]))

# 另外统计骨架区标题行总数
for k in ("part", "chapter", "section", "subsection"):
    n = sum(1 for i in range(si, ei) if re.match(r"^\\%s\*?\{" % k, lines[i].strip())
            and lines[i].startswith("\\"))
    print("%-12s %d" % (k, n))
print("骨架区 L%d..L%d（1-based）" % (si + 1, ei))
