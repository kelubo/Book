# -*- coding: utf-8 -*-
"""r41: 统一执行器——132 处 0 字空标题填充（行级倒序插入，CRLF 重建）"""
import io, os, json, importlib.util

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"

def load_mod(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(BASE, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.C

CONT = {}
CONT["female.tex"] = {**load_mod("_r41_fa1"), **load_mod("_r41_fa2")}
CONT["book.tex"] = {**load_mod("_r41_bk1"), **load_mod("_r41_bk2")}
CONT["male.tex"] = load_mod("_r41_ma")

ZERO = json.load(io.open(BASE + r"\_r41_zero.json", encoding="utf-8"))

for fn in ("book.tex", "female.tex", "male.tex"):
    path = os.path.join(BASE, fn)
    raw = io.open(path, "r", encoding="utf-8", newline="").read()
    lines = raw.split("\r\n")
    zero = ZERO[fn]
    cdict = CONT[fn]
    todo = [z for z in zero if z[0] in cdict]
    missing = [z for z in zero if z[0] not in cdict]
    print("== %s == zero=%d, content=%d, missing=%d" % (fn, len(zero), len(todo), len(missing)))
    if missing:
        for z in missing[:5]:
            print("   MISSING L%d %s" % (z[0], z[2][:40]))
    # 倒序插入
    n_ins = 0
    for lineno, lv, title in sorted(todo, key=lambda x: -x[0]):
        # 校验标题行仍匹配（防漂移）
        ln = lines[lineno - 1].strip()
        if not ln.startswith("\\" + lv + "{" + title + "}"):
            raise RuntimeError("line drift %s L%d: %r vs %r" % (fn, lineno, ln[:50], title[:40]))
        content = cdict[lineno].replace("\r\n", "\n").replace("\r", "\n")
        clines = [x.rstrip() for x in content.rstrip("\n").split("\n")]
        lines[lineno:lineno] = [""] + clines + [""]
        n_ins += 1
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(lines))
    print("   inserted %d blocks -> %d lines total" % (n_ins, len(lines)))

# 残留检查
for fn in ("book.tex", "female.tex", "male.tex"):
    raw = io.open(os.path.join(BASE, fn), "r", encoding="utf-8", newline="").read()
    lns = raw.split("\r\n")
    star = sum(1 for x in lns if "**" in x)
    pipe = sum(1 for x in lns if x.strip().startswith("|"))
    md = sum(1 for x in lns if x.strip().startswith(("- ", "* ")))
    bare_lf = sum(1 for i, ch in enumerate(raw) if ch == "\n" and (i == 0 or raw[i-1] != "\r"))
    print("%s: **=%d pipe=%d md=%d bareLF=%d lines=%d" % (fn, star, pipe, md, bare_lf, len(lns)))
