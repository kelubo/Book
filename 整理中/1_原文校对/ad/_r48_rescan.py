# -*- coding: utf-8 -*-
"""r48b 复扫：导出剩余薄条清单（口径同 _r48_scan）"""
import io, os, json

BASE = os.path.dirname(os.path.abspath(__file__))
FILES = ("book.tex", "female.tex", "male.tex")

def head_of(line):
    s = line.strip()
    for lv in ("chapter", "section", "subsection", "subsubsection"):
        if s.startswith("\\" + lv + "{") and s.endswith("}"):
            return lv, s[len("\\" + lv + "{"):-1]
    return None, None

result = {}
for fn in FILES:
    L = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
    n = len(L)
    heads = []
    for i, ln in enumerate(L):
        lv, t = head_of(ln)
        if lv:
            heads.append((i + 1, lv, t))
    entries = []
    for k, (ln, lv, t) in enumerate(heads):
        if lv == "chapter":
            continue
        end = heads[k + 1][0] - 1 if k + 1 < len(heads) else n
        chars, clines = 0, 0
        for j in range(ln, end):
            s = L[j].strip()
            if not s or s.startswith("%"):
                continue
            chars += len(s)
            clines += 1
        if (clines <= 1 and 40 <= chars <= 400) or (clines == 2 and chars <= 250):
            entries.append([ln, lv, t, chars, clines])
    result[fn] = entries
    print("%s 剩余 %d 处" % (fn, len(entries)))
    for e in entries:
        print("   %6d %-13s [%4d/%d行] %s" % (e[0], e[1], e[3], e[4], e[2][:44]))

with io.open(os.path.join(BASE, "_r48_cand2.json"), "w", encoding="utf-8", newline="") as f:
    json.dump(result, f, ensure_ascii=False)
print("已写出 _r48_cand2.json")
