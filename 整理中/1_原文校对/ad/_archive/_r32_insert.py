# -*- coding: utf-8 -*-
"""第三十二轮：插入 4 个新块到 book.tex（before 型锚点）"""
import io, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FNAME = os.path.join(BASE, "book.tex")
CR = "\r\n"

JOBS = [
    # 女同行为实践：插在《女同性恋者的亲密关系》小节之后（即下一个 subsubsection 之前）
    ("_r32_blk1.tex", r"\subsubsection{男同性恋者的亲密关系}"),
    # 药物辅助性侵：插在《约会软件安全使用指南》之前
    ("_r32_blk2.tex", r"\subsection{约会软件安全使用指南}"),
    # 捡尸与旁观者：插在《约会软件安全使用指南》之前（后插者更靠近锚点，故 3 在 2 之前）
    ("_r32_blk3.tex", r"\subsection{约会软件安全使用指南}"),
    # 体位补遗：插在《传教士体位（男上女下）》之前
    ("_r32_blk4.tex", r"\section{传教士体位（男上女下）}"),
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
