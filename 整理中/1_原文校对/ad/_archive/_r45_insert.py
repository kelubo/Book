# -*- coding: utf-8 -*-
"""r45 执行器：薄条增写（插入到条目内容之后、下一标题之前）
用法：python _r45_insert.py          -> dry-run
      python _r45_insert.py apply   -> 正式写盘
"""
import io, os, sys, importlib.util

BASE = os.path.dirname(os.path.abspath(__file__))
FILES = ("book.tex", "female.tex", "male.tex")
HEADS = ("\\chapter{", "\\section{", "\\subsection{", "\\subsubsection{")
APPLY = "apply" in sys.argv

def load_mod(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(BASE, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.C

C = {}
for mod in ("_r45_c1", "_r45_c2", "_r45_c3"):
    C.update(load_mod(mod))

PLAN = [
    ("book.tex",   539,  "b539"),
    ("book.tex",   616,  "b616"),
    ("book.tex",   628,  "b628"),
    ("book.tex",   652,  "b652"),
    ("book.tex",  1134,  "b1134"),
    ("book.tex",  1549,  "b1549"),
    ("book.tex",  2997,  "b2997"),
    ("book.tex",  3021,  "b3021"),
    ("book.tex",  3057,  "b3057"),
    ("book.tex",  3349,  "b3349"),
    ("book.tex",  3517,  "b3517"),
    ("book.tex",  7639,  "b7639"),
    ("book.tex",  8231,  "b8231"),
    ("book.tex",  8280,  "b8280"),
    ("book.tex", 21028,  "b21028"),
    ("book.tex", 21052,  "b21052"),
    ("book.tex", 21308,  "b21308"),
    ("book.tex", 24692,  "b24692"),
    ("book.tex", 25416,  "b25416"),
    ("book.tex", 25653,  "b25653"),
    ("book.tex", 26055,  "b26055"),
    ("book.tex", 30181,  "b30181"),
    ("book.tex", 46508,  "b46508"),
    ("book.tex", 53968,  "b53968"),
    ("female.tex",  3207,  "f3207"),
    ("female.tex",  3404,  "f3404"),
    ("female.tex",  3436,  "f3436"),
    ("female.tex",  4865,  "f4865"),
    ("female.tex", 11725,  "f11725"),
    ("female.tex", 12341,  "f12341"),
    ("male.tex",    561,  "m561"),
    ("male.tex",   1078,  "m1078"),
    ("male.tex",   1108,  "m1108"),
    ("male.tex",   2702,  "m2702"),
    ("male.tex",   5338,  "m5338"),
    ("male.tex",   7816,  "m7816"),
]

data = {}
for fn in FILES:
    with io.open(os.path.join(BASE, fn), "r", encoding="utf-8", newline="") as f:
        raw = f.read().replace("\r\n", "\n").replace("\r", "\n")
    data[fn] = raw.split("\n")

def is_head(s):
    t = s.strip()
    return any(t.startswith(h) for h in HEADS)

ins = {}
pos_seen = {}
before_counts = {fn: len(data[fn]) for fn in FILES}
for fn, ln, key in PLAN:
    assert key in C, "缺内容key: %s" % key
    L = data[fn]
    title = L[ln - 1].strip()
    assert is_head(title), "%s L%d 不是标题行: %r" % (fn, ln, title[:60])
    nxt = None
    for j in range(ln, len(L)):
        if is_head(L[j]):
            nxt = j
            break
    assert nxt is not None, "%s L%d 找不到下一标题" % (fn, ln)
    pos = (fn, nxt)
    assert pos not in pos_seen, "插入位置重复: %s L%d (来自 L%d 与 L%d)" % (
        fn, nxt + 1, pos_seen[pos], ln)
    pos_seen[pos] = ln
    content = C[key].replace("\r\n", "\n").replace("\r", "\n")
    clines = [x.rstrip() for x in content.rstrip("\n").split("\n") if x.strip()]
    ins[pos] = [""] + clines + [""]

for fn in FILES:
    positions = sorted([n for f2, n in ins if f2 == fn], reverse=True)
    L = data[fn]
    added = 0
    for n in positions:
        L[n:n] = ins[(fn, n)]
        added += len(ins[(fn, n)])
    out = "\r\n".join(L)
    print("%-12s %6d -> %6d 行 (+%d)" % (fn, before_counts[fn], len(L), added))
    if APPLY:
        with io.open(os.path.join(BASE, fn), "w", encoding="utf-8", newline="") as f:
            f.write(out)

mode = "APPLY 已写盘" if APPLY else "dry-run（未写盘，通过后加参数 apply）"
print("PLAN %d 条全部校验通过。" % len(PLAN), mode)
