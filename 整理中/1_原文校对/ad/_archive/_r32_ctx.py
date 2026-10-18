# -*- coding: utf-8 -*-
"""r32 语境核查：迷奸/捡尸/女同/姿势 的现有覆盖位置"""
import io, os, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
T = {}
for fn in ["book.tex", "female.tex", "male.tex"]:
    T[fn] = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read()


def show(word, fns=("book.tex",), limit=8, width=110):
    print("----- %s -----" % word)
    n = 0
    for fn in fns:
        for i, l in enumerate(T[fn].split("\n"), 1):
            s = l.strip()
            if s.startswith("%"):
                continue
            if word.lower() in s.lower():
                print("%-10s L%-6d %s" % (fn, i, s[:width]))
                n += 1
                if n >= limit:
                    return
    if n == 0:
        print("(无)")
    print()


show("迷奸")
show("约会强奸")
show("GHB")
show("失能")
show("旁观者")
show("酒吧", ("book.tex",), 6)
show("女同", ("book.tex",), 8)
show("女女性行为")
show("阴蒂", ("book.tex",), 4)
show("传教士", ("book.tex",), 4)
