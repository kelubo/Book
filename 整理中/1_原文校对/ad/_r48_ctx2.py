# -*- coding: utf-8 -*-
"""r48 尾批：抽查剩余 41 处薄条上下文"""
import io, json, os

BASE = os.path.dirname(os.path.abspath(__file__))
CAND = json.load(io.open(os.path.join(BASE, "_r48_cand2.json"), encoding="utf-8"))

def show(fn, a, b):
    L = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
    print("--- %s L%d-%d ---" % (fn, a, b))
    for i in range(a, b + 1):
        if 1 <= i <= len(L):
            print("%6d| %s" % (i, L[i-1][:130]))
    print()

# 每条展示 标题行+后 4 行
for fn, es in CAND.items():
    L = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
    print("=" * 70, fn)
    for ln, lv, t, ch, cl in es:
        print(">>> [%d] %s %s (%d字)" % (ln, lv, t, ch))
        for i in range(ln, min(ln + 5, len(L) + 1)):
            print("%6d| %s" % (i, L[i-1][:120]))
        print()
