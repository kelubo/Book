# -*- coding: utf-8 -*-
"""找出 r44-r48 新增的行内未转义 % 行（当前 vs _backup_r43 按行文本对比）"""
import io, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
def scan(p):
    raw = io.open(p, encoding="utf-8", newline="").read().replace("\r\n", "\n")
    hits = {}
    for i, ln in enumerate(raw.split("\n"), 1):
        s = ln.strip()
        if s.startswith("%") or not s:
            continue
        for m in re.finditer(r"%", ln):
            j = m.start(); k = j - 1; nb = 0
            while k >= 0 and ln[k] == "\\":
                nb += 1; k -= 1
            if nb % 2 == 0:
                hits[ln.strip()] = (i, ln)
                break
    return hits

for fn in ("book.tex", "female.tex", "male.tex"):
    cur = scan(os.path.join(BASE, fn))
    old = scan(os.path.join(BASE, "_backup_r43", fn))
    added = [v for k, v in cur.items() if k not in old]
    print("%-12s 新增未转义%%行=%d" % (fn, len(added)))
    for i, ln in added:
        print("  L%d: %s" % (i, ln[:130]))
