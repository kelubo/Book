# -*- coding: utf-8 -*-
"""r61f 打印指定行的上级标题链（chapter/section/subsection）。"""
import os, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
TARGETS = {
    "female.tex": [1524, 4487, 5875, 2233, 1520, 4898],
    "male.tex": [782, 1083, 1213, 1612, 755, 1468, 1541, 5704, 5691, 661, 818],
    "book.tex": [47504, 47513, 47521, 48078],
}
HEAD_RE = re.compile(r"^\\(chapter|section|subsection|subsubsection)\*?\{")


def load(fn):
    with open(os.path.join(BASE, fn), encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n").replace("\r", "\n").split("\n")


for fn, tls in TARGETS.items():
    lines = load(fn)
    print("=" * 70)
    print(fn)
    for t in sorted(tls):
        chain = []
        for i in range(t - 1, 0, -1):
            ln = lines[i - 1].strip() if i - 1 < len(lines) else ""
            if HEAD_RE.match(ln) and not ln.startswith("%"):
                lv = ln[1:ln.index("{")]
                chain.append((lv, ln))
                if lv == "chapter":
                    break
        print("  L%-6d %s" % (t, lines[t - 1].strip()[:80]))
        for lv, s in reversed(chain):
            print("        <- %-14s %s" % (lv, s[:80]))
