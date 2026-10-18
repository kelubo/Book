# -*- coding: utf-8 -*-
"""r74 剩余空小节清单：按篇/章/节列出骨架区仍无正文的 \subsection。

用法: python _r74_empty.py [篇关键词]   不带参数则列出全部
"""

import re
import io
import sys

lines = io.open("book.tex", encoding="utf-8", newline="").read().split("\n")
old = next(i for i, l in enumerate(lines) if l.startswith("\\part{old}"))
H = re.compile(r"^\\(part|chapter|section|subsection)\*?\{(.*)\}\s*(%.*)?$")
BS = chr(92)  # 反斜杠，避免转义困扰
title_re = re.compile("^" + BS + BS + r"(part|chapter|section|subsection|subsubsection)\*?\{")

cur = []
out = []
for i in range(old):
    m = H.match(lines[i])
    if not m:
        continue
    k, t = m.group(1), m.group(2).strip()
    if k == "part":
        cur = [t]
    elif k == "chapter":
        cur = cur[:1] + [t]
    elif k == "section":
        cur = cur[:2] + [t]
    else:
        j = i + 1
        while j < old and (not lines[j].strip() or lines[j].strip().startswith("%")):
            j += 1
        # 修正（r74）：\begin{itemize}/\begin{enumerate}/\begin{tcolorbox} 等也是正文，
        # 只有「下一个标题行」才说明该小节为空。
        empty = True
        if j < old and not title_re.match(lines[j]):
            empty = False
        if empty:
            out.append(" > ".join(cur + [t]))

kw = sys.argv[1] if len(sys.argv) > 1 else None
shown = [x for x in out if (kw is None or kw in x)]
print("剩余空小节 %d 个（筛选后 %d）" % (len(out), len(shown)))
for x in shown:
    print("   ", x)
