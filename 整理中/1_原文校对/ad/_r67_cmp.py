# -*- coding: utf-8 -*-
"""对比改动前后骨架区的 part/chapter/section/subsection 数，以及各篇新增节数。"""
import io, os, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
H = re.compile(r"^[ \t]*\\(part|chapter|section|subsection)\*?\{")


def stat(p):
    ls = io.open(p, encoding="utf-8").read().split("\n")
    oi = next(i for i, l in enumerate(ls) if l.strip() == "\\part{old}")
    body = ls[:oi]
    d = {"part": 0, "chapter": 0, "section": 0, "subsection": 0}
    for l in body:
        m = H.match(l)
        if m:
            d[m.group(1)] += 1
    return d


a = stat(os.path.join(BASE, "_backup_r67", "book.tex"))
b = stat(os.path.join(BASE, "book.tex"))
print("%-12s %6s %6s" % ("层级", "改前", "改后"))
for k in ("part", "chapter", "section", "subsection"):
    print("%-12s %6d %6d  (%+d)" % (k, a[k], b[k], b[k] - a[k]))

# 各篇新增节数（对骨架逐章统计）
cur = None
cnt = {}
part = None
ls = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8").read().split("\n")
oi = next(i for i, l in enumerate(ls) if l.strip() == "\\part{old}")
for l in ls[:oi]:
    s = l.strip()
    if s.startswith("\\part"):
        part = s[s.index("{") + 1:s.rindex("}")]
        cnt.setdefault(part, {"ch": 0, "sec": 0})
    elif s.startswith("\\chapter"):
        if part:
            cnt[part]["ch"] += 1
    elif re.match(r"^\\section\{", s):
        if part:
            cnt[part]["sec"] += 1
print()
for k, v in cnt.items():
    print("  %-24s 章 %2d  节 %3d" % (k[:24], v["ch"], v["sec"]))
