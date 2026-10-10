# -*- coding: utf-8 -*-
"""扫描三卷行内未转义 % （LaTeX 注释符泄漏），并对比 r43 备份确认来源"""
import io, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
def scan(p):
    raw = io.open(p, encoding="utf-8", newline="").read().replace("\r\n", "\n")
    hits = []
    for i, ln in enumerate(raw.split("\n"), 1):
        s = ln.strip()
        if s.startswith("%") or not s:
            continue
        # 未转义 %：前面没有反斜杠（处理 \\ 与 \%）
        for m in re.finditer(r"%", ln):
            j = m.start()
            # 数前面连续反斜杠数
            k = j - 1; nb = 0
            while k >= 0 and ln[k] == "\\":
                nb += 1; k -= 1
            if nb % 2 == 0:
                hits.append((i, ln[:120]))
                break
    return hits

for fn in ("book.tex", "female.tex", "male.tex"):
    cur = scan(os.path.join(BASE, fn))
    old = scan(os.path.join(BASE, "_backup_r43", fn))
    print("%-12s 当前未转义%%行=%d  (r43前=%d)" % (fn, len(cur), len(old)))
    for i, s in cur:
        print("  L%d: %s" % (i, s))
