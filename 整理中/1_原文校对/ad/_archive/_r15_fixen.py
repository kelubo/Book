# -*- coding: utf-8 -*-
"""修复 female.tex 历史遗留环境错配：L2357 \\begin{enumerate} 被 \\end{itemize} 关闭"""
import os
BASE = r"D:/Git/Book/整理中/1_原文校对/ad"

def load(n):
    with open(os.path.join(BASE, n), encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\r\n")

def save(n, t):
    with open(os.path.join(BASE, n), "w", encoding="utf-8", newline="") as f:
        f.write(t)

anchor = ("\t\\item 日后一提到性交，可能反射性地出现阴部灼痛、阴道痉挛、阴茎难以插入等心身反应\r\n"
          "\\end{itemize}")
fixup = ("\t\\item 日后一提到性交，可能反射性地出现阴部灼痛、阴道痉挛、阴茎难以插入等心身反应\r\n"
         "\\end{enumerate}")

t = load("female.tex")
n = t.count(anchor)
print("锚点命中:", n)
if n == 1:
    t = t.replace(anchor, fixup, 1)
    save("female.tex", t)
    print("已修复 female.tex")
else:
    print("未命中，未改动")
