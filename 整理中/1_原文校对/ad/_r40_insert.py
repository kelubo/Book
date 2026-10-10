# -*- coding: utf-8 -*-
"""r40: 三个新节 before 型插入 book.tex（严格不删改现有内容）"""
import io

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FN = BASE + r"\book.tex"

JOBS = [
    ("_r40_blk_a.tex", r"\section{性与多元关系}"),          # A1 年龄差伴侣
    ("_r40_blk_b.tex", r"\section{性创伤与心理康复}"),      # A2 皮肤可见疾病（身体形象章末）
    ("_r40_blk_c.tex", r"\section{特殊职业人群的性健康}"),  # A3 职场恋情与权力不对等
]

with io.open(FN, "r", encoding="utf-8", newline="") as f:
    text = f.read()

CR = "\r\n"
for blk, anchor in JOBS:
    core = io.open(BASE + "\\" + blk, "r", encoding="utf-8", newline="").read().rstrip("\r\n")
    # 行首非注释锚命中（排除 % 目录树注释行）
    hits = [i for i, ln in enumerate(text.split(CR), 1)
            if ln.strip().startswith(anchor)]
    assert len(hits) == 1, "anchor not unique: %s -> %s" % (anchor, hits)
    if core in text:
        print("skip (already inserted): %s" % blk)
        continue
    text = text.replace(anchor, core + CR + CR + anchor, 1)
    print("inserted %-18s before %s @L%d (core %d chars)" % (blk, anchor, hits[0], len(core)))

with io.open(FN, "w", encoding="utf-8", newline="") as f:
    f.write(text)

n = text.count(CR) + 1
print("book.tex now %d lines" % n)

# 快速残留检查：新引入的 markdown 迹象
bad_star = sum(1 for ln in text.split(CR) if "**" in ln)
bad_pipe = sum(1 for ln in text.split(CR) if ln.strip().startswith("|"))
bad_md = sum(1 for ln in text.split(CR) if ln.strip().startswith(("- ", "* ")))
print("residual ** =%d, leading-pipe =%d, md-bullet =%d" % (bad_star, bad_pipe, bad_md))
