# -*- coding: utf-8 -*-
"""r44：抽查选定薄条的上下文（标题行到下一标题）"""
import io, os

BASE = os.path.dirname(os.path.abspath(__file__))
PICKS = {
    "book.tex": [577, 1188, 1301, 3087, 5013, 5221, 21682, 21703, 23548, 24556,
                 27361, 28877, 28941, 29616, 29690, 30158, 30416],
    "female.tex": [1057, 11351, 13930, 14438, 15586, 20662],
    "male.tex": [1325, 1526, 1744, 3796, 5057, 7656, 7684],
}
HEADS = ("\\chapter{", "\\section{", "\\subsection{", "\\subsubsection{")

def is_head(s):
    t = s.strip()
    return any(t.startswith(h) for h in HEADS)

for fn, lns in PICKS.items():
    L = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
    print("\n" + "#" * 74)
    print("### " + fn)
    for ln in lns:
        # 找下一个标题行
        nxt = None
        for j in range(ln, len(L)):
            if is_head(L[j]):
                nxt = j + 1
                break
        print("\n--- L%d 起（下一标题 L%s）---" % (ln, nxt))
        print("标题: " + L[ln - 1].strip()[:90])
        end = (nxt - 1) if nxt else min(ln + 8, len(L))
        for j in range(ln, end):
            print("%6d | %s" % (j + 1, L[j][:104]))
