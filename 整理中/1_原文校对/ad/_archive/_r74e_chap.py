# -*- coding: utf-8 -*-
"""r74e: 按章节标题打印骨架。用法: python _r74e_chap.py "性心理与情感层面" [下一章标题]"""
import io, sys, re
sys.stdout.reconfigure(encoding="utf-8")
F = "book.tex"
lines = io.open(F, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
H = re.compile(r"^\\(part|chapter)\*?\{(.*)\}\s*(%.*)?$")
start = sys.argv[1]
a = b = None
for i, l in enumerate(lines):
    m = H.match(l)
    if m and m.group(2) == start and a is None:
        a = i
        continue
    if a is not None and m and i > a:
        b = i
        break
print("区间 L%d - L%d" % (a + 1, b + 1))
for i in range(a, b):
    l = lines[i]
    if l.startswith(("\\section", "\\subsection", "\\subsubsection", "\\chapter", "%")):
        print("%d|%s" % (i + 1, l))
