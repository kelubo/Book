# -*- coding: utf-8 -*-
"""r61d 候选清单：中文主体宽度 >= 30 的标题，三卷分层输出。
同时给出"剥离全部括号后"的宽度，便于识别"仅需剥离括号"的条目。
"""
import os, re, unicodedata
import importlib.util

spec = importlib.util.spec_from_file_location(
    "p", r"D:\Git\Book\整理中\1_原文校对\ad\_r61b_probe.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FILES = ["book.tex", "female.tex", "male.tex"]
LV = ["chapter", "section", "subsection", "subsubsection"]
ALLPAREN = re.compile(r"[（(][^（）()]*[）)]")

out = []
tot = 0
for f in FILES:
    rows = m.scan(os.path.join(BASE, f))
    cand = [r for r in rows if r["bw"] >= 30]
    cand.sort(key=lambda x: (LV.index(x["lv"]), -x["bw"]))
    out.append("\n## %s（%d 条）\n" % (f, len(cand)))
    tot += len(cand)
    cur = None
    for r in cand:
        if r["lv"] != cur:
            cur = r["lv"]
            out.append("\n### %s\n" % cur)
        nop = ALLPAREN.sub("", r["txt"])
        nop = re.sub(r"\s+", "", nop)
        nw = m.width(nop)
        kind = []
        if "（" in r["txt"] or "(" in r["txt"]:
            kind.append("括号")
        if "：" in r["txt"]:
            kind.append("冒号")
        if "姿势" in r["txt"] and "：" in r["txt"]:
            kind.append("姿势系列")
        out.append("- L%d bw=%d 裸=%d %s | %s" % (
            r["ln"], r["bw"], nw, "/".join(kind) or "-", r["raw"]))

with open(os.path.join(BASE, "_r61d_list.md"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("# r61 候选清单：中文主体宽度 >= 30\n")
    fh.write("\n合计 %d 条（bw=含中文括号主体宽，裸=剥离全部括号后宽）\n" % tot)
    fh.write("\n".join(out))
print("WROTE", tot)
