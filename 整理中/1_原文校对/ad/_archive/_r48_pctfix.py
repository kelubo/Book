# -*- coding: utf-8 -*-
"""r48 修复：r44-r48 新增 3 行中的未转义 % → \\%"""
import io, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
TARGETS = {3186, 3355, 3853}

p = os.path.join(BASE, "book.tex")
raw = io.open(p, encoding="utf-8", newline="").read()
lines = raw.replace("\r\n", "\n").split("\n")
fixed = 0
for ln_no in TARGETS:
    ln = lines[ln_no - 1]
    out = []
    j = 0
    while j < len(ln):
        if ln[j] == "%":
            k = j - 1; nb = 0
            while k >= 0 and ln[k] == "\\":
                nb += 1; k -= 1
            if nb % 2 == 0:
                out.append("\\%")
                fixed += 1
                j += 1
                continue
        out.append(ln[j]); j += 1
    lines[ln_no - 1] = "".join(out)

new_raw = "\r\n".join(lines)
with io.open(p, "w", encoding="utf-8", newline="") as f:
    f.write(new_raw)
print("转义 %d 处  bare-LF=%d" % (fixed, new_raw.count("\n") - new_raw.count("\r\n")))
