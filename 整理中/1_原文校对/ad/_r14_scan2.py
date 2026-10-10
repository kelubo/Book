# -*- coding: utf-8 -*-
"""Show all enumerate begin/end lines + context around stray end{itemize} at 2280."""
import re

MALE = r"D:\Git\Book\整理中\1_原文校对\ad\male.tex"
s = open(MALE, "rb").read().decode("utf-8")
lines = s.split("\n")

print("== enumerate events ==")
bal = 0
for i, line in enumerate(lines, 1):
    if re.search(r"\\begin\{enumerate\}", line):
        bal += 1
        print("  L%-6d BEGIN (bal=%d)  %s" % (i, bal, line.strip()[:70]))
    if re.search(r"\\end\{enumerate\}", line):
        print("  L%-6d END   (bal=%d)  %s" % (i, bal - 1, line.strip()[:70]))
        bal -= 1

print()
print("== context around L2280 ==")
for i in range(2260, 2296):
    print("%5d| %s" % (i, lines[i - 1][:100]))
