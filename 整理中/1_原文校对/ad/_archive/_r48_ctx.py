# -*- coding: utf-8 -*-
"""r48 上下文抽查：female/male 候选条目的实际结构（确认是否为列表项）"""
import io, os

BASE = os.path.dirname(os.path.abspath(__file__))

def show(fn, ln, before=1, after=6):
    L = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
    print("--- %s @%d ---" % (fn, ln))
    for i in range(max(1, ln - before), min(len(L), ln + after) + 1):
        print("%6d| %s" % (i, L[i - 1][:120]))
    print()

for ln in (3679, 3853, 4662, 5003, 8073, 13760, 16113, 17777, 18240, 19523, 20365):
    show("female.tex", ln)
for ln in (550, 906, 921, 1112, 1791, 1811, 3567, 3750, 4003, 4669, 4737, 4933, 4987, 5183, 5915, 6692, 6696):
    show("male.tex", ln)
