# -*- coding: utf-8 -*-
"""r33 语境核查：现有服务可及性节的覆盖范围"""
import io, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
text = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read()
lines = text.split("\r\n")


def dump(a, b, label):
    print("========== %s (L%d-%d) ==========" % (label, a, b))
    for i in range(a, b + 1):
        s = lines[i - 1].rstrip()
        if s.strip():
            print("L%-6d %s" % (i, s[:135]))
    print()


dump(43205, 43300, "女同性恋者的性健康需求 / 医疗服务障碍")
dump(39389, 39470, "性健康资源与支持（含资源清单？）")
