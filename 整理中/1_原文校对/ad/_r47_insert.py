# -*- coding: utf-8 -*-
"""r47 执行器：薄条增写（插入到条目内容之后、下一标题之前）
用法：python _r47_insert.py          -> dry-run
      python _r47_insert.py apply   -> 正式写盘
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
for mod in ("_r47_c1", "_r47_c2"):
    C.update(load_mod(mod))

PLAN = [
    ("book.tex",    623,  "b623"),
    ("book.tex",    649,  "b649"),
    ("book.tex",    655,  "b655"),
    ("book.tex",    926,  "b926"),
    ("book.tex",   3024,  "b3024"),
    ("book.tex",   3525,  "b3525"),
    ("book.tex",   3529,  "b3529"),
    ("book.tex",   3626,  "b3626"),
    ("book.tex",   3663,  "b3663"),
    ("book.tex",   5113,  "b5113"),
    ("book.tex",   5166,  "b5166"),
    ("book.tex",   5248,  "b5248"),
    ("book.tex",   5439,  "b5439"),
    ("book.tex",   5444,  "b5444"),
    ("book.tex",   5449,  "b5449"),
    ("book.tex",   6262,  "b6262"),
    ("book.tex",   6266,  "b6266"),
    ("book.tex",   8131,  "b8131"),
    ("book.tex",  11516,  "b11516"),
    ("book.tex",  16425,  "b16425"),
    ("book.tex",  21328,  "b21328"),
    ("book.tex",  24643,  "b24643"),
    ("book.tex",  25390,  "b25390"),
    ("book.tex",  50440,  "b50440"),
    ("female.tex",  3040,  "f3040"),
    ("female.tex",  3786,  "f3786"),
    ("female.tex",  3867,  "f3867"),
    ("female.tex",  3936,  "f3936"),
    ("female.tex", 18972,  "f18972"),
    ("female.tex", 19914,  "f19914"),
    ("male.tex",     526,  "m526"),
    ("male.tex",     905,  "m905"),
    ("male.tex",    1125,  "m1125"),
    ("male.tex",    1131,  "m1131"),
    ("male.tex",    7719,  "m7719"),
    ("male.tex",    7750,  "m7750"),
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
    # 保留内容内部的空行（段间空行 = LaTeX 分段），只去掉首尾空行
    clines = [x.rstrip() for x in content.split("\n")]
    while clines and not clines[0].strip():
        clines.pop(0)
    while clines and not clines[-1].strip():
        clines.pop()
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
