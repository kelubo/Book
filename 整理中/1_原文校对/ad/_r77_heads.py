# -*- coding: utf-8 -*-
"""r77: 导出巨块全部标题的有序清单（含行号），供精选。"""
import io, re

H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{(.*)\}\s*$")
lines = [x.rstrip("\r") for x in io.open("book.tex", encoding="utf-8", newline="").read().split("\n")]
A, B = 53683, 67498
out = []
for i in range(A - 1, min(B, len(lines))):
    m = H.match(lines[i])
    if m:
        out.append("%-6d %-13s %s" % (i + 1, m.group(1), ("  " * {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}[m.group(1)]) + m.group(2)))
io.open("_r77_heads.txt", "w", encoding="utf-8", newline="").write("\n".join(out) + "\n")
print("写出 _r77_heads.txt：%d 条" % len(out))
