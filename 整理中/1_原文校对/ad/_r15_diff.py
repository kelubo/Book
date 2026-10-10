# -*- coding: utf-8 -*-
import os, re
from collections import Counter
BASE = r"D:/Git/Book/整理中/1_原文校对/ad"
for tag, d in [("备份", "_backup_r15"), ("当前", ".")]:
    for f in ["book.tex", "female.tex", "male.tex"]:
        p = os.path.join(BASE, d, f)
        with open(p, encoding="utf-8", newline="") as fp:
            t = fp.read()
        ob, cb = t.count("{"), t.count("}")
        b = Counter(re.findall(r"\\begin\{([^}]+)\}", t))
        e = Counter(re.findall(r"\\end\{([^}]+)\}", t))
        bad = {k: (b[k], e.get(k, 0)) for k in set(list(b)+list(e)) if b[k] != e.get(k, 0)}
        print(f"[{tag}] {f:11s} delta={ob-cb:3d}  env_bad={bad}")
