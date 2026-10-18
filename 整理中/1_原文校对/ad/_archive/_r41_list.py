# -*- coding: utf-8 -*-
"""r41: 备份三卷 + 提取全部空壳节清单（<150 字符口径），按 (文件,章) 分组输出"""
import io, os, re, shutil

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
BK = BASE + r"\_backup_r41"
FILES = ["book.tex", "female.tex", "male.tex"]

os.makedirs(BK, exist_ok=True)
for fn in FILES:
    shutil.copy2(os.path.join(BASE, fn), os.path.join(BK, fn))
print("backup ok ->", BK)

HDR = re.compile(r"\\(chapter|section|subsection|subsubsection|subparagraph)\{([^{}]*)\}")
lv_order = {"chapter": 0, "section": 1, "subsection": 2, "subsubsection": 3, "subparagraph": 4}

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
    hollow = []
    for idx, (lv, i, t) in enumerate(ents):
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
        if chars < 150:
            hollow.append((lv, i, t, chars))
    # 按章分组输出
    bych = {}
    cur = "(卷首)"
    for lv, i, t in ents:
        if lv == "chapter":
            cur = t if t else "(未命名章)"
    for lv, i, t, ch in hollow:
        ch2 = "(卷首)"
        for lv2, j, t2 in ents:
            if j >= i:
                break
            if lv2 == "chapter":
                ch2 = t2 if t2 else "(未命名章)"
        bych.setdefault(ch2, []).append((lv, i, t, ch))
    print("=" * 20, fn, "空壳 %d 处" % len(hollow))
    for ch, items in bych.items():
        print("-- [%s] %d 处" % (ch, len(items)))
        for lv, i, t, ch_ in items:
            print("   L%-6d %-12s %s  (%d字)" % (i, lv, t[:46], ch_))
