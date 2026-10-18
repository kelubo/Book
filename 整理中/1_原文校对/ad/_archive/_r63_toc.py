# -*- coding: utf-8 -*-
"""r63：解析编译产出的 book.toc，看真实目录结构"""
import io, re, collections, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
s = io.open(os.path.join(BASE, "book.toc"), encoding="utf-8", errors="replace").read()
pat = re.compile(r"\\contentsline\s*\{(part|chapter|section|subsection|subsubsection)\}\{[^}]*?(?:\{[^}]*\}[^}]*?)*?")
rows = re.findall(r"\\contentsline\s*\{(part|chapter|section|subsection|subsubsection)\}", s)
c = collections.Counter(rows)
print("book.toc 条目统计：", dict(c))

# 打印 part 与 chapter 序列
cur = []
for m in re.finditer(r"\\contentsline\s*\{(part|chapter)\}\{(.*?)\}\{(\d+)\}", s):
    lv, t, page = m.group(1), m.group(2), m.group(3)
    t = re.sub(r"\\[a-zA-Z]+\s*|\\numberline\s*\{[^}]*\}", "", t).strip()
    if lv == "part":
        print("\n[PART] %s   (p.%s)" % (t, page))
    else:
        print("   ch  %-40s p.%s" % (t[:40], page))
print("\n总页数（book.log）:")
log = io.open(os.path.join(BASE, "book.log"), encoding="utf-8", errors="replace").read()
m = re.findall(r"Output written on book\.pdf \((\d+) pages", log)
print("  ", m[-1] if m else "?")
print("  ! 错误行:", sum(1 for l in log.split("\n") if l.startswith("!")))
