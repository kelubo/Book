# -*- coding: utf-8 -*-
"""r69b：列出所有需要补小节的骨架节（part / chapter / section），供人工设计小节名。
输出：_r69b_todo.txt
"""
import io, os, re, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
lines = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
N = len(lines)
H = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection)\*?\{")
LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}


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


off = set()
d = 0
st = None
for i, l in enumerate(lines):
    s = l.strip()
    if re.match(r"^\\iffalse\b", s):
        if d == 0:
            st = i + 1
        d += 1
    elif s == "\\fi" and d > 0:
        d -= 1
        if d == 0:
            for k in range(st, i + 2):
                off.add(k)

T = []
for i, l in enumerate(lines):
    s = l.strip()
    if not s or s.startswith("%"):
        continue
    m = H.match(s)
    if m:
        T.append((i + 1, m.group(1), gt(s)))
OLD = next(ln for ln, lv, t in T if lv == "part" and t == "old")
SK = [(ln, lv, t) for ln, lv, t in T if ln < OLD and ln not in off]

out = []
A = out.append
cp = cc = None
n = 0
for i, (ln, lv, t) in enumerate(SK):
    if lv == "part":
        cp = t
        if t == "附录":
            break
        A("")
        A("=" * 60)
        A("篇 %s" % t)
        A("=" * 60)
    elif lv == "chapter":
        cc = t
        A("")
        A("【章】%s" % t)
    elif lv == "section":
        has = [x for x in SK[i + 1:] if True]
        m = 0
        for ln2, lv2, _ in SK[i + 1:]:
            if LV[lv2] <= 2:
                break
            if lv2 == "subsection":
                m += 1
        if m == 0:
            n += 1
            A("   %2d. %s" % (n, t))
            print("%-14s| %-22s| %s" % (cp, cc, t))
print()
print("合计需补小节的节：", n)
io.open(os.path.join(BASE, "_r69b_todo.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
