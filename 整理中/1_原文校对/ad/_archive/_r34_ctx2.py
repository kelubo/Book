# -*- coding: utf-8 -*-
"""r34 深查：强奸应对 / 三类方式安全细节 / 跨性别就医实操"""
import io, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
T = {}
for fn in ["book.tex", "female.tex"]:
    T[fn] = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read()

lines = T["book.tex"].split("\n")


def dump(a, b, label, fname="book.tex"):
    ls = T[fname].split("\n")
    print("========== %s (%s L%d-%d) ==========" % (label, fname, a, b))
    for i in range(a, min(b, len(ls)) + 1):
        s = ls[i - 1].rstrip()
        if s.strip():
            print("L%-6d %s" % (i, s[:130]))
    print()


# 强奸罪 / 性侵犯法律应对
dump(22704, 22760, "性犯罪与法律责任")
dump(39357, 39400, "性侵犯与性暴力的法律应对")
# 性创伤康复
dump(17922, 17960, "性创伤与心理康复")
# 肛交技巧（female 与 book）
dump(8650, 8700, "female 肛交技巧与体验", "female.tex")
