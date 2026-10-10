# -*- coding: utf-8 -*-
"""第三十一轮：插入 10 个新块（ABC 全做）到 book.tex，全部 before 型锚点插入"""
import io, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FNAME = os.path.join(BASE, "book.tex")
CR = "\r\n"

# (块文件, 锚点) 顺序决定相邻关系：后插的靠近锚点
JOBS = [
    ("_r31_blk_c1.tex", r"\subsubsection{新兴数字性文化术语的社会影响}"),
    ("_r31_blk_c2.tex", r"\subsection{人工智能(AI)与性健康}"),
    ("_r31_blk_c3.tex", r"\subsection{LGBTQ+人群的性健康促进策略}"),
    ("_r31_blk_b3.tex", r"\subsubsection{针灸治疗}"),
    ("_r31_blk_b2.tex", r"\subsubsection{针灸治疗}"),
    ("_r31_blk_b4.tex", r"\subsection{中医对常见性问题的认识与治疗}"),
    ("_r31_blk_b1.tex", r"\subsection{中医对常见性问题的认识与治疗}"),
    ("_r31_blk_a2.tex", r"\subsection{SM与心理健康}"),
    ("_r31_blk_a3.tex", r"\subsection{SM与心理健康}"),
    ("_r31_blk_a1.tex", r"\subsection{SM与心理健康}"),
]

text = io.open(FNAME, encoding="utf-8", newline="").read()
for blk, anchor in JOBS:
    core = io.open(os.path.join(BASE, blk), encoding="utf-8", newline="").read()
    core = core.replace("\r\n", "\n").replace("\n", CR).rstrip(CR)
    ikey = core.split(CR)[0].strip()  # 块首行 = 标题行，幂等键
    if ikey in text:
        print("SKIP (idempotent):", blk)
        continue
    n = text.count(anchor)
    if n != 1:
        raise SystemExit("ANCHOR FAIL (%d): %s <- %s" % (n, anchor, blk))
    text = text.replace(anchor, core + CR + CR + anchor, 1)
    print("OK:", blk, "<-", anchor.strip("\\").split("{")[0], anchor)

with io.open(FNAME, "w", encoding="utf-8", newline="") as f:
    f.write(text)
print("saved:", FNAME, len(text.split(CR)), "lines")
