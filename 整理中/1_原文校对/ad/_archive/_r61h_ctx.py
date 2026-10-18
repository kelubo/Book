# -*- coding: utf-8 -*-
"""r61h 查看重名既有出处上下文 + 裸名是否已被占用。"""
import os, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
HEAD_RE = re.compile(r"^\\(chapter|section|subsection|subsubsection)\*?\{")


def load(fn):
    with open(os.path.join(BASE, fn), encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n").replace("\r", "\n").split("\n")


def ctx(fn, ln, back=3, fwd=2):
    lines = load(fn)
    print("--- %s L%d ---" % (fn, ln))
    for i in range(max(1, ln - back), min(len(lines), ln + fwd) + 1):
        print("  %6d| %s" % (i, lines[i - 1].strip()[:100]))


def find_title(fn, name):
    lines = load(fn)
    out = []
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if HEAD_RE.match(s) and s.endswith("{%s}" % name):
            out.append(i)
    print("%s  标题正好为 %r 的行：%s" % (fn, name, out))
    return out


for fn, lns in [("book.tex", [7555, 47260, 24217, 45793, 52384, 1833, 53402, 53440]),
                ("female.tex", [8785, 9178, 8815, 8844, 11287, 8825, 11104])]:
    for l in lns:
        ctx(fn, l)
print("=" * 60)
for nm in ["尖锐湿疣", "激素避孕法", "私处整容", "二级预防", "一级预防", "三级预防"]:
    find_title("book.tex", nm)
for nm in ["阴道", "子宫", "卵巢", "G点", "G 点"]:
    find_title("female.tex", nm)
