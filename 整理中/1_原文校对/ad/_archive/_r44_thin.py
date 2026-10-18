# -*- coding: utf-8 -*-
"""r44：从候选中过滤单行/双行薄条，输出 _r44_thin.txt"""
import io, json, os

BASE = os.path.dirname(os.path.abspath(__file__))
D = json.load(io.open(os.path.join(BASE, "_r44_cand.json"), encoding="utf-8"))

def head_of(line):
    s = line.strip()
    for lv in ("chapter", "section", "subsection", "subsubsection"):
        if s.startswith("\\" + lv + "{") and s.endswith("}"):
            return lv, s[len("\\" + lv + "{"):-1]
    return None, None

out = io.open(os.path.join(BASE, "_r44_thin.txt"), "w", encoding="utf-8", newline="")
total = 0
for fn, es in D.items():
    L = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
    out.write("=" * 70 + "\n### " + fn + "\n")
    cur = "?"
    for ln, lv, t, ch, cl in es:
        sel = (cl <= 1 and 40 <= ch <= 400) or (cl == 2 and ch <= 250)
        if not sel:
            continue
        for j in range(ln - 1, -1, -1):
            lv2, t2 = head_of(L[j])
            if lv2 == "chapter":
                cur = t2
                break
        out.write("%6d %-13s [%4d] %s  <<%s>>\n" % (ln, lv, ch, t[:46], cur[:22]))
        total += 1
out.close()
print("written, total =", total)
