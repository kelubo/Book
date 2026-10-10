# -*- coding: utf-8 -*-
"""r48 尾批执行器：剩余 41 处薄条增写（book 40 + male 1）
机制：PLAN 由 _r48_cand2.json 自动生成；锚位运行时推导下一标题行；
倒序插入；dry-run 校验 / apply 写盘双模式。
"""
import io, json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
CAND = json.load(io.open(os.path.join(BASE, "_r48_cand2.json"), encoding="utf-8"))

import importlib.util
def load_mod(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(BASE, name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.D

C = {}
C["book.tex"] = {**load_mod("_r48_d1"), **load_mod("_r48_d2"), **load_mod("_r48_d3")}
C["male.tex"] = load_mod("_r48_d3")  # d3 内含 m6744；book 取不含 m 前缀的条目
# 修正：book 只用非 m 条目（d3 的 D 同时含 book 与 male 条目，用 key 前缀区分）
BOOK_KEYS = [k for k in C["book.tex"] if k.startswith("b")]
C["book.tex"] = {k: C["book.tex"][k] for k in BOOK_KEYS}
C["male.tex"] = {k: v for k, v in load_mod("_r48_d3").items() if k.startswith("m")}

HEADS = ("\\chapter{", "\\section{", "\\subsection{", "\\subsubsection{")
def is_heading(s):
    st = s.strip()
    if st.startswith("%"):
        return False
    return any(st.startswith(h) for h in HEADS)

def norm(c):
    content = c.replace("\r\n", "\n").replace("\r", "\n")
    return [x.rstrip() for x in content.strip("\n").split("\n")]

apply_mode = len(sys.argv) > 1 and sys.argv[1] == "apply"

plan = {}   # fn -> [(pos, key, title)]
for fn, es in CAND.items():
    L = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
    todo = sorted(es, key=lambda x: -x[0])
    cdict = C.get(fn, {})
    missing = [e[0] for e in todo if "b%d" % e[0] not in cdict and "m%d" % e[0] not in cdict]
    if missing:
        raise SystemExit("%s 缺内容块: %s" % (fn, missing))
    ins = {}
    seen_pos = set()
    for ln, lv, t, ch, cl in todo:
        key = ("m" if fn == "male.tex" else "b") + str(ln)
        # 锚校验：标题行全等
        expect = "\\" + lv + "{" + t + "}"
        assert L[ln-1].strip() == expect, "%s L%d 锚不符: %r" % (fn, ln, L[ln-1].strip()[:60])
        # 运行时推导下一标题行（0-based nh）
        nh = None
        for j in range(ln, len(L)):
            if is_heading(L[j]):
                nh = j; break
        assert nh is not None, "%s L%d 找不到下一标题" % (fn, ln)
        # 插入点：下一标题之前，回退跳过尾部空行
        pos = nh
        while pos > ln and L[pos-1].strip() == "":
            pos -= 1
        assert pos > ln, "%s L%d 条目无实体内容？" % (fn, ln)
        assert pos not in seen_pos, "%s 插入位置重复 pos=%d" % (fn, pos)
        seen_pos.add(pos)
        ins[pos] = [""] + norm(cdict[key]) + [""]
    plan[fn] = ins
    if apply_mode:
        for pos in sorted(ins, reverse=True):
            L[pos:pos] = ins[pos]
        with io.open(os.path.join(BASE, fn), "w", encoding="utf-8", newline="") as f:
            f.write("\r\n".join(L))
    add = sum(len(v) for v in ins.values())
    print("%-12s %s 处数=%d 预计+%d 行" % (fn, "APPLY" if apply_mode else "DRY-RUN", len(ins), add))

total = sum(sum(len(v) for v in p.values()) for p in plan.values())
print("合计预计 +", total, "行")
if not apply_mode:
    print("（dry-run 通过，未写盘；带 apply 参数执行写盘）")
else:
    print("已写盘完成")
