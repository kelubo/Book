# -*- coding: utf-8 -*-
"""r44 探测：备份三卷 + 重扫短词条（标题块后续实体内容量），行号基于 r43 后现状。"""
import io, os, shutil, json

BASE = os.path.dirname(os.path.abspath(__file__))
FILES = ("book.tex", "female.tex", "male.tex")

# 1) 备份
bk = os.path.join(BASE, "_backup_r44")
os.makedirs(bk, exist_ok=True)
for fn in FILES:
    dst = os.path.join(bk, fn)
    if not os.path.exists(dst):
        shutil.copy2(os.path.join(BASE, fn), dst)
print("备份完成 ->", bk)

HEADS = ("\\chapter{", "\\section{", "\\subsection{", "\\subsubsection{")

def load_lines(fn):
    with io.open(os.path.join(BASE, fn), "r", encoding="utf-8", newline="") as f:
        raw = f.read().replace("\r\n", "\n").replace("\r", "\n")
    return raw.split("\n")

def head_of(line):
    s = line.strip()
    for lv in ("chapter", "section", "subsection", "subsubsection"):
        if s.startswith("\\" + lv + "{") and s.endswith("}"):
            return lv, s[len("\\" + lv + "{"):-1]
    return None, None

result = {}
for fn in FILES:
    L = load_lines(fn)
    n = len(L)
    heads = []  # (lineno, lv, title)
    for i, ln in enumerate(L):
        lv, t = head_of(ln)
        if lv:
            heads.append((i + 1, lv, t))
    entries = []
    for k, (ln, lv, t) in enumerate(heads):
        if lv in ("chapter",):
            continue
        end = heads[k + 1][0] - 1 if k + 1 < len(heads) else n
        chars = 0
        clines = 0
        for j in range(ln, end):  # 正文区段 = 标题行之后到下一标题之前
            s = L[j].strip()
            if not s or s.startswith("%"):
                continue
            chars += len(s)
            clines += 1
        # 短词条口径：实体内容 40~500 字；浅小节口径：实体行 < 6
        if 40 <= chars <= 500 or (clines < 6 and chars < 1500):
            entries.append([ln, lv, t, chars, clines])
    result[fn] = entries
    print("%s: 标题 %d 个, 候选短条 %d 处" % (fn, len(heads), len(entries)))

with io.open(os.path.join(BASE, "_r44_cand.json"), "w", encoding="utf-8", newline="") as f:
    json.dump(result, f, ensure_ascii=False)

# 按章分组打印概览（book 只打印 section/subsection 层）
for fn in FILES:
    L = load_lines(fn)
    print("\n" + "=" * 80)
    print("### " + fn)
    cur_ch = "?"
    for ln, lv, t, ch, cl in result[fn]:
        # 找所属章
        for j in range(ln - 1, -1, -1):
            lv2, t2 = head_of(L[j])
            if lv2 == "chapter":
                cur_ch = t2
                break
        print("%6d %-12s [%4d字/%2d行] %s  <<%s>>" % (ln, lv, ch, cl, t[:44], cur_ch[:20]))
