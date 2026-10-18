# -*- coding: utf-8 -*-
"""Locate unbalanced itemize/enumerate in male.tex; compare with backup if present."""
import re, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
MALE = BASE + r"\male.tex"
BK   = BASE + r"\_backup_术语替换" + r"\male.tex"

def scan(path):
    if not os.path.exists(path):
        return None
    s = open(path, "rb").read().decode("utf-8")
    out = {}
    for env in ("itemize", "enumerate"):
        bal = 0
        events = []
        for i, line in enumerate(s.split("\n"), 1):
            if re.search(r"\\begin\{" + env + r"\}", line):
                bal += 1
            if re.search(r"\\end\{" + env + r"\}", line):
                bal -= 1
                if bal < 0:
                    events.append((i, "END without BEGIN, bal=%d" % bal))
                    bal = 0  # reset to continue scanning
        if bal != 0:
            events.append(("EOF", "unclosed balance=%d" % bal))
        out[env] = events
    return out

for label, p in (("current", MALE), ("backup", BK)):
    r = scan(p)
    print("==== %s: %s" % (label, p))
    if r is None:
        print("   (not found)")
        continue
    for env, evs in r.items():
        print("  %s: %s" % (env, evs if evs else "balanced"))
