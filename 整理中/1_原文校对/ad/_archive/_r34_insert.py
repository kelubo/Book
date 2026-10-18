# -*- coding: utf-8 -*-
"""第三十四轮：插入 5 个新块到 book.tex"""
import io, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FNAME = os.path.join(BASE, "book.tex")
CR = "\r\n"

JOBS = [
    # 跨性别就医流程：插在《性别确认医疗服务》之后
    ("_r34_blk1.tex", r"\subsubsection{中国的现状}"),
    # 伴侣法律事务：插在《性健康资源与支持》之前（即《色情内容的法律监管与伦理》之后）
    ("_r34_blk2.tex", r"\section{性健康资源与支持}"),
    # 三方式安全补遗：插在《肛交》小节之后（即下一个 subsection「性爱技巧进阶」之前）
    ("_r34_blk3.tex", r"\section{性交姿势}"),
    # 强奸创伤综合征：插在《性侵犯与性暴力的法律应对》之后
    ("_r34_blk4.tex", r"\subsection{色情内容的法律监管与伦理}"),
    # 熟人强奸与迷思：插在《色情内容的法律监管与伦理》之前 → 后插者更近锚点，排在 blk4 之后
    ("_r34_blk5.tex", r"\subsection{色情内容的法律监管与伦理}"),
]

text = io.open(FNAME, encoding="utf-8", newline="").read()
for blk, anchor in JOBS:
    core = io.open(os.path.join(BASE, blk), encoding="utf-8", newline="").read()
    core = core.replace("\r\n", "\n").replace("\n", CR).rstrip(CR)
    ikey = core.split(CR)[0].strip()
    if ikey in text:
        print("SKIP (idempotent):", blk)
        continue
    n = text.count(anchor)
    if n != 1:
        raise SystemExit("ANCHOR FAIL (%d): %s <- %s" % (n, anchor, blk))
    text = text.replace(anchor, core + CR + CR + anchor, 1)
    print("OK:", blk, "<-", anchor)

with io.open(FNAME, "w", encoding="utf-8", newline="") as f:
    f.write(text)
print("saved:", len(text.split(CR)), "lines")
