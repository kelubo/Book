# -*- coding: utf-8 -*-
"""r68d：把 book.tex 骨架区渲染成 Markdown 完整目录（学习框架版）
输出：_r68_目录框架_完整版_2026-09-21.md
标注：◆ 零节章 / ⚠ 跨章重名 / ○ 建议新增位（由 r68e 追加）
"""
import io, os, re, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
OUT = os.path.join(BASE, "_r68_目录框架_完整版_2026-09-21.md")
lines = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
N = len(lines)
H = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection)\*?\{")
LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}


def gt(s):
    r = s[s.index("{"):]
    d = 0
    for j, c in enumerate(r):
        if c == "{":
            d += 1
        elif c == "}":
            d -= 1
            if d == 0:
                return r[1:j]
    return r[1:]


# \iffalse 区间（含行内注释）
off = set()
depth = 0
start = None
for i, l in enumerate(lines):
    s = l.strip()
    if re.match(r"^\\iffalse\b", s):
        if depth == 0:
            start = i + 1
        depth += 1
    elif s == "\\fi" and depth > 0:
        depth -= 1
        if depth == 0:
            for k in range(start, i + 2):
                off.add(k)

T = []
for i, l in enumerate(lines):
    s = l.strip()
    if not s or s.startswith("%"):
        continue
    m = H.match(s)
    if m:
        T.append((i + 1, m.group(1), gt(s)))
OLD = next(ln for ln, lv, t in T if lv == "part" and t == "old")
SK = [(ln, lv, t) for ln, lv, t in T if ln < OLD]

# 每章：节数 / 每节：小节数
sec_cnt = {}
sub_cnt = {}
for i, (ln, lv, t) in enumerate(SK):
    if lv == "chapter":
        n = 0
        for ln2, lv2, _ in SK[i + 1:]:
            if LV[lv2] <= 1:
                break
            if lv2 == "section":
                n += 1
        sec_cnt[ln] = n
    if lv == "section":
        n = 0
        for ln2, lv2, _ in SK[i + 1:]:
            if LV[lv2] <= 2:
                break
            if lv2 == "subsection":
                n += 1
        sub_cnt[ln] = n

# 跨章重名节
name2 = collections.defaultdict(list)
for ln, lv, t in SK:
    if lv in ("section", "subsection"):
        name2[t].append(ln)
dup = {k for k, v in name2.items() if len(v) > 1}

out = []
A = out.append
A("# 《性健康与性爱指南》综合卷 · 目录框架（完整版）")
A("")
A("> 生成日期：2026-09-21 ｜ 源文件：`book.tex` 骨架区（L170–L1260）")
A("> 说明：本文件是骨架的**可读渲染**，用于审读与迁移导航；改目录请改 `book.tex`。")
A("> 图例：`◆` 该章尚无节（需补）｜`⚠` 与其他章重名｜`★` 已有正文｜括号内为小节数")
A("")
A("---")
A("")

cur_part = "（前置）"
cur_ch = None
pch = collections.OrderedDict()
pch[cur_part] = {"ch": 0, "sec": 0, "sub": 0, "line": 0}
A("## 前置（frontmatter）")
A("")
for ln, lv, t in SK:
    if ln in off:
        continue
    if lv == "part":
        cur_part = t
        pch[t] = {"ch": 0, "sec": 0, "sub": 0, "line": ln}
        A("")
        A("---")
        A("")
        A("## %s" % t)
        A("")
    elif lv == "chapter":
        cur_ch = t
        pch[cur_part]["ch"] += 1
        mark = ""
        if sec_cnt.get(ln, 0) == 0:
            mark = " `◆`"
        if "两性研究导论" in t:
            mark = " `★`"
        A("")
        A("### %s%s" % (t, mark))
        A("")
    elif lv == "section":
        pch[cur_part]["sec"] += 1
        m = ""
        if t in dup:
            m = " `⚠`"
        n = sub_cnt.get(ln, 0)
        A("- **%s**%s%s" % (t, m, ("（%d 小节）" % n) if n else ""))
    elif lv == "subsection":
        pch[cur_part]["sub"] += 1
        A("    - %s" % t)
    else:
        A("        - %s" % t)

A("")
A("---")
A("")
A("## 规模一览")
A("")
A("| 篇 | 章 | 节 | 小节 |")
A("|---|---:|---:|---:|")
tc = ts = tu = 0
for k, v in pch.items():
    A("| %s | %d | %d | %d |" % (k, v["ch"], v["sec"], v["sub"]))
    tc += v["ch"]
    ts += v["sec"]
    tu += v["sub"]
A("| **合计** | **%d** | **%d** | **%d** |" % (tc, ts, tu))

io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("written", OUT, len("\n".join(out)), "chars")
print("篇 %d 章 %d 节 %d 小节 %d" % (len(pch), tc, ts, tu))
