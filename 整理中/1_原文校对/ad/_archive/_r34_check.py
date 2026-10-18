# -*- coding: utf-8 -*-
"""r34 收尾检查"""
import io, re, os, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
new = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read()
old = io.open(os.path.join(BASE, "_backup_r34", "book.tex"), encoding="utf-8", newline="").read()

pat = re.compile(r"\\\\(textbf|textit|item|begin|end|noindent|section|subsection|subsubsection|par|title|chapter)\b")
print("真双反斜杠笔误：前=%d 后=%d 增量=%d" % (len(pat.findall(old)), len(pat.findall(new)),
                                     len(pat.findall(new)) - len(pat.findall(old))))

others = re.compile(r"\\[0-9]|\\%|\\&(?![a-zA-Z])")
print("反斜杠+数字/%%：前=%d 后=%d" % (len(re.findall(r"\\[0-9]", old)), len(re.findall(r"\\[0-9]", new))))

blocks = ["_r34_blk1.tex", "_r34_blk2.tex", "_r34_blk3.tex", "_r34_blk4.tex", "_r34_blk5.tex"]
words = collections.Counter()
for blk in blocks:
    t = io.open(os.path.join(BASE, blk), encoding="utf-8", newline="").read()
    hits = re.findall(r"\\\\.", t)
    print("%s: 双反斜杠 %d 次" % (blk, len(hits)))
    for w in re.findall(r"[A-Za-z][A-Za-z/-]{2,}", re.sub(r"\\[A-Za-z]+", " ", t)):
        words[w] += 1
print("新块英文词：", dict(sorted(words.items())))

lines = new.split("\r\n")
print("book.tex 行数:", len(lines))
print()
for t in ["跨性别者就医流程实务", "同性伴侣的法律事务", "安全细节补遗", "强奸创伤综合征", "熟人强奸"]:
    hit = [i for i, l in enumerate(lines, 1) if t in l]
    print((hit[0] if hit else "MISS"), "|", t)
