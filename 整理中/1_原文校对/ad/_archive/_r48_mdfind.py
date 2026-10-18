# -*- coding: utf-8 -*-
"""定位 mdfix 后 book.tex delta=1 的来源行"""
import io, os

BASE = os.path.dirname(os.path.abspath(__file__))
def load(p):
    return io.open(p, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")

old = load(os.path.join(BASE, "_backup_r48_md", "book.tex"))
new = load(os.path.join(BASE, "book.tex"))
print("行数 old=%d new=%d" % (len(old), len(new)))

total_delta = 0
for i, (a, b) in enumerate(zip(old, new), 1):
    if a != b:
        da = a.count("{") - a.count("}")
        db = b.count("{") - b.count("}")
        if da != db:
            total_delta += db - da
            print("L%d brace delta %d -> %d" % (i, da, db))
            print("  OLD:", a[:150])
            print("  NEW:", b[:150])
print("delta 变化合计:", total_delta)
