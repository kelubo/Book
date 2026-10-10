# -*- coding: utf-8 -*-
"""列出两卷新骨架结构（preview 文件）。"""
import io
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
T = re.compile(r"\\(part|chapter|section)\*?\{([^{}]*)\}")
IND = {"part": "", "chapter": "  ", "section": "    "}

for fn in ("_r72_preview_female.txt", "_r72_preview_male.txt"):
    print("=" * 26, fn)
    for l in io.open(os.path.join(BASE, fn), encoding="utf-8").read().split("\n"):
        s = l.strip()
        if s.startswith("%"):
            continue
        m = T.match(s)
        if m:
            print(IND[m.group(1)] + s)
