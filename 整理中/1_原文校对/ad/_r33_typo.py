# -*- coding: utf-8 -*-
"""r33 精确笔误扫描：仅查真正的双反斜杠笔误"""
import io, os, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
new = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read()
old = io.open(os.path.join(BASE, "_backup_r33", "book.tex"), encoding="utf-8", newline="").read()

# 真笔误 = 源码中有两个连续反斜杠且后面跟命令名（源码层面）
pat = re.compile(r"\\\\(textbf|textit|item|begin|end|noindent|section|subsection|subsubsection|subparagraph|par|title|chapter)\b")
print("真双反斜杠笔误：前=%d 后=%d 增量=%d" % (len(pat.findall(old)), len(pat.findall(new)),
                                     len(pat.findall(new)) - len(pat.findall(old))))

# 另一种笔误：单个反斜杠+数字/中文，或 \& 误用
pat2 = re.compile(r"\\[0-9]")
print("反斜杠+数字：前=%d 后=%d" % (len(pat2.findall(old)), len(pat2.findall(new))))

# 本轮新块内容是否引入 \\ 
for blk in ["_r33_blk1.tex", "_r33_blk2.tex"]:
    t = io.open(os.path.join(BASE, blk), encoding="utf-8", newline="").read()
    hits = [m.group(0) for m in re.finditer(r"\\\\.", t)]
    print("%s: 双反斜杠出现 %d 次 %s" % (blk, len(hits), hits[:5]))
