# -*- coding: utf-8 -*-
"""r46 探测：备份三卷 + 重扫薄条清单（r45 增写后行号已变）"""
import io, os, shutil, json

BASE = os.path.dirname(os.path.abspath(__file__))
FILES = ("book.tex", "female.tex", "male.tex")

bk = os.path.join(BASE, "_backup_r46")
os.makedirs(bk, exist_ok=True)
for fn in FILES:
    dst = os.path.join(bk, fn)
    if not os.path.exists(dst):
        shutil.copy2(os.path.join(BASE, fn), dst)
print("备份完成 ->", bk)

def head_of(line):
    s = line.strip()
    for lv in ("chapter", "section", "subsection", "subsubsection"):
        if s.startswith("\\" + lv + "{") and s.endswith("}"):
            return lv, s[len("\\" + lv + "{"):-1]
    return None, None

result = {}
for fn in FILES:
    with io.open(os.path.join(BASE, fn), "r", encoding="utf-8", newline="") as f:
        L = f.read().replace("\r\n", "\n").replace("\r", "\n").split("\n")
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
    result[fn] = (entries, L)
    print("%s: 薄条 %d 处" % (fn, len(entries)))

with io.open(os.path.join(BASE, "_r46_cand.json"), "w", encoding="utf-8", newline="") as f:
    json.dump({fn: result[fn][0] for fn in FILES}, f, ensure_ascii=False)

out = io.open(os.path.join(BASE, "_r46_thin.txt"), "w", encoding="utf-8", newline="")
for fn in FILES:
    es, L = result[fn]
    out.write("=" * 70 + "\n### " + fn + "\n")
    cur = "?"
    for ln, lv, t, ch, cl in es:
        for j in range(ln - 1, -1, -1):
            lv2, t2 = head_of(L[j])
            if lv2 == "chapter":
                cur = t2
                break
        out.write("%6d %-13s [%4d/%d行] %s  <<%s>>\n" % (ln, lv, ch, cl, t[:46], cur[:22]))
out.close()
print("清单已写出 _r46_thin.txt")
