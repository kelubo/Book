# -*- coding: utf-8 -*-
"""三卷目录查重：跨卷重名 + 卷内重名。读 _r72_preview_*.txt。"""
import io
import os
import re
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
T = re.compile(r"\\(part|chapter|section|subsection)\*?\{([^{}]*)\}")

vols = {}
for tag, fn in (("book", "_r72_preview_book.txt"),
                ("female", "_r72_preview_female.txt"),
                ("male", "_r72_preview_male.txt")):
    ents = []
    for i, l in enumerate(io.open(os.path.join(BASE, fn), encoding="utf-8").read().split("\n"), 1):
        s = l.strip()
        if s.startswith("%"):
            continue
        m = T.match(s)
        if m:
            ents.append((m.group(1), m.group(2).strip(), i))
    vols[tag] = ents

# 卷内重名（章 / 节 分别看）
for tag, ents in vols.items():
    print("── %s：章 %d / 节 %d / 小节 %d"
          % (tag, sum(1 for k, _, _ in ents if k == "chapter"),
             sum(1 for k, _, _ in ents if k == "section"),
             sum(1 for k, _, _ in ents if k == "subsection")))
    for lv in ("chapter", "section"):
        c = Counter(t for k, t, _ in ents if k == lv)
        d = {t: n for t, n in c.items() if n > 1}
        if d and lv == "chapter":
            print("   卷内重名章：", d)
    # 小节重名（同章内）
    cur = None
    seendupe = []
    for k, t, _ in ents:
        if k == "chapter":
            cur = t
            seen = Counter()
        elif k == "subsection":
            seen[t] += 1
    print()

# 跨卷重名（章级）
print("── 跨卷重名（章级）")
idx = defaultdict(dict)
for tag, ents in vols.items():
    for k, t, _ in ents:
        if k == "chapter":
            idx[t][tag] = 1
hits = {t: v for t, v in idx.items() if len(v) > 1}
print("   ", hits if hits else "无")

print("── 跨卷重名（节级）")
idx2 = defaultdict(dict)
for tag, ents in vols.items():
    for k, t, _ in ents:
        if k == "section":
            idx2[t][tag] = 1
hits2 = {t: list(v) for t, v in idx2.items() if len(v) > 1}
if not hits2:
    print("    无")
for t, v in sorted(hits2.items()):
    print("    %-30s %s" % (t, v))
