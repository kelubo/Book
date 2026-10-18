# -*- coding: utf-8 -*-
"""排查编译错误：L72 全文、missing-item 样本行、itemitem 搜索"""
import io, os

BASE = os.path.dirname(os.path.abspath(__file__))
L = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")

out = io.open(os.path.join(BASE, "_r49_diag.txt"), "w", encoding="utf-8", newline="")
out.write("L72 长度=%d 末尾: %r\n\n" % (len(L[71]), L[71][-80:]))

for target in (3914, 4035, 5085, 17431, 24627, 27118, 48508):
    out.write("=== L%d 前后 ===\n" % target)
    for i in range(max(1, target - 6), target + 3):
        out.write("%6d| %s\n" % (i, L[i-1][:130]))
    out.write("\n")
out.close()

# 全文搜 itemitem
for fn in ("book.tex", "female.tex", "male.tex"):
    raw = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n")
    hits = [(i, ln.strip()[:100]) for i, ln in enumerate(raw.split("\n"), 1) if "itemitem" in ln]
    with io.open(os.path.join(BASE, "_r49_diag.txt"), "a", encoding="utf-8", newline="") as f:
        f.write("### %s itemitem 命中 %d\n" % (fn, len(hits)))
        for i, s in hits:
            f.write("  L%d: %s\n" % (i, s))
        f.write("\n")
print("diag written")
