# -*- coding: utf-8 -*-
"""r43 补充探测：特殊职业节内部 + 三卷章列表 + 丧偶"""
import io, os
BASE = os.path.dirname(os.path.abspath(__file__))
def load(fn):
    with io.open(os.path.join(BASE, fn), "r", encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n").replace("\r", "\n").split("\n")
P = {fn: load(fn) for fn in ("book.tex", "female.tex", "male.tex")}

print("=" * 74)
print("### book 特殊职业人群节内部 L28728-28860")
print("=" * 74)
for i in range(28728, 28870):
    s = P["book.tex"][i - 1]
    if s.strip().startswith("\\") or s.strip():
        print("%6d | %s" % (i, s[:100]))

print("\n" + "=" * 74)
print("### book 丧偶/再婚/空巢 相关 L28080-28110")
print("=" * 74)
for i in range(28080, 28115):
    print("%6d | %s" % (i, P["book.tex"][i - 1][:100]))

for fn in ("female.tex", "male.tex"):
    print("\n" + "=" * 74)
    print("### %s 章/节清单（chapter + section）" % fn)
    print("=" * 74)
    for i, ln in enumerate(P[fn], 1):
        s = ln.strip()
        if s.startswith("\\chapter{") or s.startswith("\\section{"):
            print("%6d %s" % (i, s[:100]))
