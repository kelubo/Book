# -*- coding: utf-8 -*-
"""r41: 导出三卷 0 字纯空标题清单为 JSON（行号 + 层级 + 标题）"""
import io, os, re, json

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FILES = ["book.tex", "female.tex", "male.tex"]
HDR = re.compile(r"\\(chapter|section|subsection|subsubsection|subparagraph)\{([^{}]*)\}")
lv_order = {"chapter": 0, "section": 1, "subsection": 2, "subsubsection": 3, "subparagraph": 4}

out = {}
for fn in FILES:
    raw = io.open(os.path.join(BASE, fn), "r", encoding="utf-8", newline="").read()
    lines = raw.split("\r\n")
    ents = []
    for i, ln in enumerate(lines, 1):
        st = ln.strip()
        if st.startswith("%"):
            continue
        m = HDR.match(st)
        if m:
            ents.append((m.group(1), i, m.group(2).strip()))
    zero = []
    for idx, (lv, i, t) in enumerate(ents):
        if not t:
            continue
        end = len(lines)
        for lv2, j, _ in ents[idx + 1:]:
            if lv_order[lv2] <= lv_order[lv]:
                end = j - 1
                break
        chars = 0
        for ln in lines[i:end]:
            st = ln.strip()
            if not st or st.startswith("%"):
                continue
            chars += len(st)
        if chars == 0:
            zero.append([i, lv, t])
    out[fn] = zero
    print(fn, "0字空标题:", len(zero))

with io.open(BASE + r"\_r41_zero.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("saved _r41_zero.json")
for fn in FILES:
    for i, lv, t in out[fn]:
        print("%s L%-6d %-12s %s" % (fn[:2], i, lv, t[:60]))
