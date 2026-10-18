# -*- coding: utf-8 -*-
"""r48 校验：内容块唯一性 + markdown 残留 + 结构统计 + 存量复扫"""
import io, os, json, re, importlib.util

BASE = os.path.dirname(os.path.abspath(__file__))
FILES = ("book.tex", "female.tex", "male.tex")
HEADS = ("\\chapter{", "\\section{", "\\subsection{", "\\subsubsection{")

def load_mod(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(BASE, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.C

C = {}
for mod in ("_r48_c1", "_r48_c2", "_r48_c3", "_r48_c4", "_r48_c5",
            "_r48_c6", "_r48_c7", "_r48_c8", "_r48_c9"):
    C.update(load_mod(mod))

RAW = {}
for fn in FILES:
    RAW[fn] = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read()

# 1) 内容块唯一性
bad = []
for (fn, ln), body in C.items():
    content = body.replace("\r\n", "\n").replace("\r", "\n")
    clines = [x.rstrip() for x in content.split("\n")]
    while clines and not clines[0].strip():
        clines.pop(0)
    while clines and not clines[-1].strip():
        clines.pop()
    needle = "\r\n".join(clines)
    n = RAW[fn].count(needle)
    if n != 1:
        bad.append((fn, ln, n))
print("1) 内容块唯一性：%d 条检查，异常 %d 条" % (len(C), len(bad)))
for fn, ln, n in bad[:20]:
    print("   [异常] %s L%d x%d" % (fn, ln, n))

# 2) markdown 残留（行首）
pat = re.compile(r"^\s*(#{1,4}\s|\*\*|\|.*\|)")
md = {fn: 0 for fn in FILES}
for fn in FILES:
    for ln in RAW[fn].replace("\r\n", "\n").split("\n"):
        if pat.match(ln):
            md[fn] += 1
print("2) markdown 残留：", md)

# 3) 行尾
for fn in FILES:
    bare = RAW[fn].count("\n") - RAW[fn].count("\r\n")
    print("   %-12s 行数 %6d  bare-LF %d" % (
        fn, len(RAW[fn].replace("\r\n", "\n").split("\n")), bare))

# 4) 结构统计 + 标题唯一性
def head_of(line):
    s = line.strip()
    for lv in ("chapter", "section", "subsection", "subsubsection"):
        if s.startswith("\\" + lv + "{") and s.endswith("}"):
            return lv, s[len("\\" + lv + "{"):-1]
    return None, None

stat = {}
for fn in FILES:
    L = RAW[fn].replace("\r\n", "\n").split("\n")
    c = {"chapter": 0, "section": 0, "subsection": 0, "subsubsection": 0}
    for ln in L:
        lv, t = head_of(ln)
        if lv:
            c[lv] += 1
    stat[fn] = c
print("3) 结构统计：")
for fn in FILES:
    print("   %-12s 章%3d 节%4d 子节%5d 子子节%5d" % (
        fn, stat[fn]["chapter"], stat[fn]["section"],
        stat[fn]["subsection"], stat[fn]["subsubsection"]))

# 5) 存量复扫（同 _r48_scan 口径）
tot = 0
for fn in FILES:
    L = RAW[fn].replace("\r\n", "\n").split("\n")
    n = len(L)
    heads = []
    for i, ln in enumerate(L):
        lv, t = head_of(ln)
        if lv:
            heads.append((i + 1, lv, t))
    left = []
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
            left.append((ln, lv, t, chars, clines))
    tot += len(left)
    print("4) %-12s 剩余薄条 %d 处" % (fn, len(left)))
    for e in left[:15]:
        print("     %6d %-13s [%4d/%d行] %s" % (e[0], e[1], e[3], e[4], e[2][:40]))
print("剩余合计：%d" % tot)
