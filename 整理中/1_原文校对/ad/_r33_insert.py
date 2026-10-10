# -*- coding: utf-8 -*-
"""第三十三轮：插入 2 个新块到 book.tex"""
import io, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FNAME = os.path.join(BASE, "book.tex")
CR = "\r\n"

JOBS = [
    # 女同就医障碍：插在《医疗服务障碍》小节之后（即《性健康知识缺乏》之前）
    ("_r33_blk1.tex", r"\subsubsection{性健康知识缺乏}"),
    # 社群资源清单：插在《性健康知识缺乏》之前 → 后插者更近锚点，须排在 blk1 之后
    ("_r33_blk2.tex", r"\subsubsection{性健康知识缺乏}"),
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
