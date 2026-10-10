# -*- coding: utf-8 -*-
"""r46 执行器：薄条增写（插入到条目内容之后、下一标题之前）
用法：python _r46_insert.py          -> dry-run
      python _r46_insert.py apply   -> 正式写盘
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
for mod in ("_r46_c1", "_r46_c2"):
    C.update(load_mod(mod))

PLAN = [
    ("book.tex",    428,  "b428"),
    ("book.tex",    509,  "b509"),
    ("book.tex",    869,  "b869"),
    ("book.tex",   1019,  "b1019"),
    ("book.tex",   1432,  "b1432"),
    ("book.tex",   1604,  "b1604"),
    ("book.tex",   3011,  "b3011"),
    ("book.tex",   3483,  "b3483"),
    ("book.tex",   3832,  "b3832"),
    ("book.tex",  21234,  "b21234"),
    ("book.tex",  21280,  "b21280"),
    ("book.tex",  21392,  "b21392"),
    ("book.tex",  22612,  "b22612"),
    ("book.tex",  22771,  "b22771"),
    ("book.tex",  23032,  "b23032"),
    ("book.tex",  23390,  "b23390"),
    ("book.tex",  24700,  "b24700"),
    ("book.tex",  24913,  "b24913"),
    ("book.tex",  24983,  "b24983"),
    ("book.tex",  26272,  "b26272"),
    ("book.tex",  26319,  "b26319"),
    ("book.tex",  26373,  "b26373"),
    ("book.tex",  27517,  "b27517"),
    ("book.tex",  27690,  "b27690"),
    ("female.tex",   587,  "f587"),
    ("female.tex",  3255,  "f3255"),
    ("female.tex",  3497,  "f3497"),
    ("female.tex",  6594,  "f6594"),
    ("female.tex",  8719,  "f8719"),
    ("female.tex", 19764,  "f19764"),
    ("male.tex",     622,  "m622"),
    ("male.tex",    2166,  "m2166"),
    ("male.tex",    2223,  "m2223"),
    ("male.tex",    4107,  "m4107"),
    ("male.tex",    5259,  "m5259"),
    ("male.tex",    6644,  "m6644"),
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
