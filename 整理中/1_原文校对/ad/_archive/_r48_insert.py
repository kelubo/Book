# -*- coding: utf-8 -*-
"""r48 执行器：清空全部存量薄条（PLAN 由 _r48_cand.json ∩ 内容模块 key 自动生成）
用法：python _r48_insert.py          -> dry-run
      python _r48_insert.py apply   -> 正式写盘
"""
import io, os, sys, json, importlib.util

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
for mod in ("_r48_c1", "_r48_c2", "_r48_c3", "_r48_c4", "_r48_c5",
            "_r48_c6", "_r48_c7", "_r48_c8", "_r48_c9"):
    C.update(load_mod(mod))
print("内容模块条目数：%d" % len(C))

with io.open(os.path.join(BASE, "_r48_cand.json"), "r", encoding="utf-8", newline="") as f:
    CAND = json.load(f)

data = {}
for fn in FILES:
    with io.open(os.path.join(BASE, fn), "r", encoding="utf-8", newline="") as f:
        raw = f.read().replace("\r\n", "\n").replace("\r", "\n")
    data[fn] = raw.split("\n")

def is_head(s):
    t = s.strip()
    return any(t.startswith(h) for h in HEADS)

PLAN = []
missing = []
for fn in FILES:
    for ln, lv, t, ch, cl in CAND[fn]:
        key = (fn, ln)
        if key in C:
            PLAN.append((fn, ln, lv, t, key))
        else:
            missing.append((fn, ln, lv, t, ch))

print("清单条目数：%d；已覆盖：%d；未覆盖：%d" % (
    sum(len(CAND[fn]) for fn in FILES), len(PLAN), len(missing)))
for fn, ln, lv, t, ch in missing:
    print("  [未覆盖] %s L%d %s %s (%d字)" % (fn, ln, lv, t[:30], ch))

ins = {}
pos_seen = {}
before_counts = {fn: len(data[fn]) for fn in FILES}
for fn, ln, lv, t, key in PLAN:
    L = data[fn]
    title = L[ln - 1].strip()
    assert title == "\\" + lv + "{" + t + "}", \
        "%s L%d 标题不匹配: %r != %r" % (fn, ln, title[:60], ("\\" + lv + "{" + t + "}")[:60])
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
