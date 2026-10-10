# -*- coding: utf-8 -*-
"""r74d: 打印指定行区间的完整骨架（含注释）。用法: python _r74d_dump.py 311 340"""
import io, sys
sys.stdout.reconfigure(encoding="utf-8")
F = "book.tex"
a = int(sys.argv[1]); b = int(sys.argv[2])
lines = io.open(F, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
for i in range(a - 1, min(b, len(lines))):
    print("%d|%s" % (i + 1, lines[i]))
