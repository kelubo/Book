# -*- coding: utf-8 -*-
"""r67：输出指定行区间所在块的二级/三级标题结构。"""
import io, os, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
lines = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
N = len(lines)
H = re.compile(r"^[ \t]*\\(part|chapter|section|subsection|subsubsection)\*?\{")
LVN = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}


def gt(s):
    r = s[s.index("{"):]
    d = 0
    for j, c in enumerate(r):
        if c == "{":
            d += 1
        elif c == "}":
            d -= 1
            if d == 0:
                return r[1:j]
    return r[1:]


T = []
for i, l in enumerate(lines):
    s = l.strip()
    if not s or s.startswith("%"):
        continue
    m = H.match(s)
    if m:
        T.append((i + 1, m.group(1), gt(s)))

ENDMAP = {}
for k, (ln, lv, t) in enumerate(T):
    lvl = LVN[lv]
    e = N + 1
    for ln2, lv2, _ in T[k + 1:]:
        if LVN[lv2] <= lvl:
            e = ln2
            break
    ENDMAP[ln] = e


def nb(ln, e):
    return sum(1 for x in lines[ln:e - 1] if x.strip() and not x.strip().startswith("%"))


TARGETS = [32098, 10005, 12988, 17184, 44487, 8301, 23094, 23667, 8649, 50757, 4739, 4801, 1828, 51269, 21850, 22399]
out = []
for tg in TARGETS:
    key = [x for x in T if x[0] == tg]
    if not key:
        out.append("\n@@ L%d 不是标题行" % tg)
        continue
    ln, lv, t = key[0]
    e = ENDMAP[ln]
    out.append("\n@@ L%d [%s] %s   块 %d行" % (ln, lv, t[:50], nb(ln, e)))
    lv2max = 4 if lv == "section" else 3
    for ln2, lv2, t2 in T:
        if ln < ln2 < e and LVN[lv2] <= lv2max:
            ind = "  " * (LVN[lv2] - LVN[lv])
            out.append("   %s%-12s %-46s L%-6d %d行" % (ind, lv2, t2[:46], ln2, nb(ln2, ENDMAP[ln2])))

io.open(os.path.join(BASE, "_r67d_sub.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
print("written", len(out))
