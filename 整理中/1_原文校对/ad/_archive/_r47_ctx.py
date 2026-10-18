# -*- coding: utf-8 -*-
"""r47 抽查候选薄条上下文（行号取自 _r47_scan.py 的当前文件）"""
import io, os

BASE = os.path.dirname(os.path.abspath(__file__))

CAND = {
"book.tex": [623, 649, 655, 926, 3024, 3525, 3529, 3626, 3663, 4087,
             5113, 5166, 5208, 5248, 5434, 5439, 5444, 5449, 5454,
             6262, 6266, 7300, 7662, 8131, 11516, 16425, 21286, 21328,
             24218, 24643, 24705, 25191, 25390, 26501, 27050, 28033,
             29205, 29358, 29660, 30007, 30282, 30430, 30673, 46754, 50440],
"female.tex": [3040, 3786, 3867, 3936, 18972, 19914, 20335],
"male.tex":   [526, 1125, 1131, 3547, 7719, 7750],
}

for fn, nums in CAND.items():
    with io.open(os.path.join(BASE, fn), "r", encoding="utf-8", newline="") as f:
        L = f.read().replace("\r\n", "\n").replace("\r", "\n").split("\n")
    print("\n" + "=" * 78)
    print("### " + fn + "  总行数 %d" % len(L))
    print("=" * 78)
    for n in nums:
        lo, hi = n, min(n + 7, len(L))
        print("-" * 74)
        for i in range(lo, hi + 1):
            print("%6d| %s" % (i, L[i - 1][:150]))
