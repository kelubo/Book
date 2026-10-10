# -*- coding: utf-8 -*-
"""r44 执行器：薄条增写（插入到每个条目内容之后、下一标题之前）
用法：python _r44_insert.py          -> dry-run（全量校验，不写盘）
      python _r44_insert.py apply   -> 正式写盘
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
for mod in ("_r44_c1", "_r44_c2", "_r44_c3"):
    C.update(load_mod(mod))

# PLAN: (文件, 条目标题行号, 内容key)
PLAN = [
    ("book.tex",   577,  "b577"),
    ("book.tex",  1188,  "b1188"),
    ("book.tex",  1192,  "b1192"),
    ("book.tex",  1301,  "b1301"),
    ("book.tex",  3087,  "b3087"),
    ("book.tex",  3363,  "b3363"),
    ("book.tex",  3392,  "b3392"),
    ("book.tex",  3516,  "b3516"),
    ("book.tex",  3554,  "b3554"),
    ("book.tex",  5013,  "b5013"),
    ("book.tex",  5221,  "b5221"),
    ("book.tex",  5226,  "b5226"),
    ("book.tex",  5231,  "b5231"),
    ("book.tex", 21682,  "b21682"),
    ("book.tex", 21703,  "b21703"),
    ("book.tex", 23548,  "b23548"),
    ("book.tex", 27361,  "b27361"),
    ("book.tex", 28877,  "b28877"),
    ("book.tex", 28941,  "b28941"),
    ("book.tex", 29616,  "b29616"),
    ("book.tex", 29690,  "b29690"),
    ("book.tex", 30158,  "b30158"),
    ("book.tex", 30416,  "b30416"),
    ("female.tex", 1057,  "f1057"),
    ("female.tex", 11351, "f11351"),
    ("female.tex", 13930, "f13930"),
    ("female.tex", 14438, "f14438"),
    ("female.tex", 15586, "f15586"),
    ("female.tex", 20662, "f20662"),
    ("male.tex",  1325,  "m1325"),
    ("male.tex",  1526,  "m1526"),
    ("male.tex",  1744,  "m1744"),
    ("male.tex",  3796,  "m3796"),
    ("male.tex",  5057,  "m5057"),
    ("male.tex",  7656,  "m7656"),
    ("male.tex",  7684,  "m7684"),
]

# 读入
data = {}
for fn in FILES:
    with io.open(os.path.join(BASE, fn), "r", encoding="utf-8", newline="") as f:
        raw = f.read().replace("\r\n", "\n").replace("\r", "\n")
    data[fn] = raw.split("\n")

def is_head(s):
    t = s.strip()
    return any(t.startswith(h) for h in HEADS)

# 校验 + 组装插入（位置去重检查）
ins = {}          # (fn, lineno) -> [lines to insert]
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
            nxt = j  # 0-based 下一标题行下标
            break
    assert nxt is not None, "%s L%d 找不到下一标题" % (fn, ln)
    pos = (fn, nxt)
    assert pos not in pos_seen, "插入位置重复: %s L%d (来自 L%d 与 L%d)" % (
        fn, nxt + 1, pos_seen[pos], ln)
    pos_seen[pos] = ln
    content = C[key].replace("\r\n", "\n").replace("\r", "\n")
    clines = [x.rstrip() for x in content.rstrip("\n").split("\n") if x.strip()]
    ins[pos] = [""] + clines + [""]

# 倒序插入
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
