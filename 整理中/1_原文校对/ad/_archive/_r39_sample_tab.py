# -*- coding: utf-8 -*-
"""r39: 抽样验证 book.tex 3 处 tabular 转换结果"""
import io

FN = r"D:\Git\Book\整理中\1_原文校对\ad\book.tex"

with io.open(FN, "r", encoding="utf-8", newline="") as f:
    lines = f.read().split("\r\n")

def show(start, before=6, after=22):
    s = max(0, start - 1 - before)
    e = min(len(lines), start - 1 + after)
    for i in range(s, e):
        print("%6d| %s" % (i + 1, lines[i][:150]))
    print("-" * 70)

for ln in (25817, 25998, 44754):
    print("=== tabular @ L%d ===" % ln)
    show(ln)
