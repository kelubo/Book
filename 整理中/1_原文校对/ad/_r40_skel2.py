# -*- coding: utf-8 -*-
"""r40 探测第 4 轮：骨架空壳宽松口径（<150 字符），对齐历轮 570"""
import re, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FILES = ["book.tex", "female.tex", "male.tex"]

HDR = re.compile(r"\\(chapter|section|subsection|subsubsection|subparagraph)\{([^{}]*)\}")
lv_order = {"chapter": 0, "section": 1, "subsection": 2, "subsubsection": 3, "subparagraph": 4}

for fn in FILES:
    raw = open(os.path.join(BASE, fn), "rb").read()
    crlf = "\r\n" if b"\r\n" in raw else "\n"
    lines = raw.decode("utf-8").split(crlf)
    ents = []
    for i, ln in enumerate(lines, 1):
        st = ln.strip()
        if st.startswith("%"):
            continue
        m = HDR.match(st)
        if m:
            ents.append((m.group(1), i, m.group(2).strip()))
    for TH in (150,):
        hollow = []
        for idx, (lv, i, t) in enumerate(ents):
            if not t:
                hollow.append((lv, i, "(空花括号)"))
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
            if chars < TH:
                hollow.append((lv, i, t))
        print("== %s == 阈值 %d 字符：%d 处" % (fn, TH, len(hollow)))
        bych = {}
        cur_ch = "(卷首)"
        chents = []
        for lv, i, t in ents:
            if lv == "chapter":
                cur_ch = t if t else "(未命名章)"
        for lv, i, t in hollow:
            # 找所属章
            ch = "(卷首)"
            for lv2, j, t2 in ents:
                if j >= i:
                    break
                if lv2 == "chapter":
                    ch = t2 if t2 else "(未命名章)"
            bych.setdefault(ch, []).append((lv, i, t))
        for ch, items in sorted(bych.items(), key=lambda x: -len(x[1]))[:15]:
            lvls = {}
            for lv, i, t in items:
                lvls[lv] = lvls.get(lv, 0) + 1
            print("   [%3d 处] %s  %s" % (len(items), ch[:50], lvls))
        print()
