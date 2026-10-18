# -*- coding: utf-8 -*-
"""Find the first point where cumulative brace balance goes negative."""
BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FILES = [BASE + r"\book.tex", BASE + r"\male.tex"]

for p in FILES:
    raw = open(p, "rb").read()
    s = raw.decode("utf-8")
    crlf = "\r\n" if b"\r\n" in raw else "\n"
    lines = s.split(crlf)
    bal = 0
    hits = []
    for i, line in enumerate(lines, 1):
        # ignore verbatim/verb content lines coarsely: report anyway but mark
        d = line.count("{") - line.count("}")
        prev = bal
        bal += d
        if bal < 0:
            hits.append((i, prev, bal, line))
            bal = 0  # reset to keep scanning for further anomalies
    print("====", p.split("\\")[-1], " negative-balance hits:", len(hits))
    for i, prev, bal, line in hits[:5]:
        print("  L%-6d %d->%d | %s" % (i, prev, bal, line.strip()[:90]))
