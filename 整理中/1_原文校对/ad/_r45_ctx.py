# -*- coding: utf-8 -*-
"""r45：抽查含义不明的候选条目上下文"""
import io, os

BASE = os.path.dirname(os.path.abspath(__file__))
PICKS = {
    "male.tex": [1078, 1108, 561, 2702, 7816],
    "book.tex": [3021, 1549, 1134, 46508],
    "female.tex": [3436, 11725],
}
HEADS = ("\\chapter{", "\\section{", "\\subsection{", "\\subsubsection{")

def is_head(s):
    t = s.strip()
    return any(t.startswith(h) for h in HEADS)

for fn, lns in PICKS.items():
    L = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
    print("\n" + "#" * 70)
    print("### " + fn)
    for ln in lns:
        nxt = None
        for j in range(ln, len(L)):
            if is_head(L[j]):
                nxt = j + 1
                break
        print("\n--- L%d（下一标题 L%s）---" % (ln, nxt))
        print("标题: " + L[ln - 1].strip()[:88])
        end = (nxt - 1) if nxt else min(ln + 6, len(L))
        for j in range(ln, end):
            print("%6d | %s" % (j + 1, L[j][:100]))
