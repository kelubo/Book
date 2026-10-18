# -*- coding: utf-8 -*-
"""r45：补查三个缺失标题的行号"""
import io, os

BASE = os.path.dirname(os.path.abspath(__file__))
JOBS = [
    ("book.tex", ["肛门括约肌和盆腔耻尾肌联合收缩法", "兴奋期", "平台期", "高潮期", "消退期"]),
    ("male.tex", ["男性的性反应", "兴奋期"]),
]
for fn, pats in JOBS:
    with io.open(os.path.join(BASE, fn), encoding="utf-8", newline="") as f:
        L = f.read().replace("\r\n", "\n").split("\n")
    for i, ln in enumerate(L, 1):
        s = ln.strip()
        for lv in ("section", "subsection", "subsubsection"):
            pre = "\\" + lv + "{"
            if s.startswith(pre):
                inner = s[len(pre):-1] if s.endswith("}") else ""
                if any(inner == p or inner.startswith(p) for p in pats):
                    print(fn, i, lv, inner[:52])
