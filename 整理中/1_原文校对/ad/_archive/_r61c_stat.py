# -*- coding: utf-8 -*-
"""r61c 分层分布统计：各层级在不同阈值下的标题数量（中文主体宽度）。"""
import os, re, unicodedata
import importlib.util

spec = importlib.util.spec_from_file_location(
    "p", r"D:\Git\Book\整理中\1_原文校对\ad\_r61b_probe.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FILES = ["book.tex", "female.tex", "male.tex"]
LV = ["chapter", "section", "subsection", "subsubsection"]

for f in FILES:
    rows = m.scan(os.path.join(BASE, f))
    print("=" * 66)
    print(f)
    print("%-14s %6s %6s %6s %6s %6s %6s" % ("层级", "n", ">=24", ">=26", ">=28", ">=30", ">=32"))
    for lv in LV:
        sub = [r for r in rows if r["lv"] == lv]
        if not sub:
            continue
        c = lambda t: sum(1 for r in sub if r["bw"] >= t)
        print("%-14s %6d %6d %6d %6d %6d %6d" % (lv, len(sub), c(24), c(26), c(28), c(30), c(32)))
    # 冒号式（含全角冒号）统计
    for lv in LV:
        sub = [r for r in rows if r["lv"] == lv]
        colon = [r for r in sub if "：" in r["txt"]]
        print("   %s 冒号式：%d" % (lv, len(colon)))
