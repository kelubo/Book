# -*- coding: utf-8 -*-
"""r32 收尾检查：笔误增量、英文词、新标题行号"""
import io, re, os, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
new = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read()
old = io.open(os.path.join(BASE, "_backup_r32", "book.tex"), encoding="utf-8", newline="").read()

pat = re.compile(r"\\\\(?:textbf|textit|item|begin|end|noindent|section|subsection|subsubsection|par|title)\b")
print("双反斜杠 插入前=%d 插入后=%d 增量=%d" % (len(pat.findall(old)), len(pat.findall(new)),
                                        len(pat.findall(new)) - len(pat.findall(old))))

blocks = ["_r32_blk1.tex", "_r32_blk2.tex", "_r32_blk3.tex", "_r32_blk4.tex"]
words = collections.Counter()
for blk in blocks:
    t = io.open(os.path.join(BASE, blk), encoding="utf-8", newline="").read()
    body = re.sub(r"\\[A-Za-z]+", " ", t)
    for w in re.findall(r"[A-Za-z][A-Za-z/-]{2,}", body):
        words[w] += 1
print("新块英文词：", dict(sorted(words.items())))

lines = new.split("\r\n")
print()
print("== 新标题行号 ==")
for t in ["女女性行为实践", "药物辅助性侵", '"捡尸"与酒后失能', "体位补遗"]:
    hit = [i for i, l in enumerate(lines, 1) if t in l]
    print((hit[0] if hit else "MISS"), "|", t)
print("book.tex 行数:", len(lines))
