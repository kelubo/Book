# -*- coding: utf-8 -*-
"""r32 结构细查：L38700-38770 与选址"""
import io, os, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
text = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read()
lines = text.split("\r\n")

# 锚点计数
for a in [r"\subsubsection{男同性恋者的亲密关系}", r"\subsection{不同性偏好的亲密关系指导}",
          r"\subsection{约会软件安全使用指南}", r"\section{传教士体位（男上女下）}"]:
    print(lines.count(a), "|", a)
print()

print("== L38696-38770 ==")
for i in range(38696, 38771):
    s = lines[i-1].strip()
    if s:
        print("L%-6d %s" % (i, s[:120]))
