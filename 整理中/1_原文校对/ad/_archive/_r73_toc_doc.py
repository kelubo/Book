# -*- coding: utf-8 -*-
"""r69d：把 book.tex 骨架区渲染成 Markdown 完整目录（学习框架 · 四层版）
输出：_r73_目录框架_完整版_2026-09-22.md
"""
import io, os, re, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
OUT = os.path.join(BASE, "_r73_目录框架_完整版_2026-09-22.md")
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


off = set()
d = 0
st = None
for i, l in enumerate(lines):
    s = l.strip()
    if re.match(r"^\\iffalse\b", s):
        if d == 0:
            st = i + 1
        d += 1
    elif s == "\\fi" and d > 0:
        d -= 1
        if d == 0:
            for k in range(st, i + 2):
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
SK = [(ln, lv, t) for ln, lv, t in T if ln < OLD and ln not in off]

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

out = []
A = out.append
A("# 《性健康与性爱指南》综合卷 · 目录框架（完整版 · 四层）")
A("")
A("> 生成日期：2026-09-22 ｜ 源文件：`book.tex` 骨架区")
A("> 结构：八篇 53 章 ＋ 结语 1 章 ＋ 附录 5 章 ＝ **60 章 / 257 节 / 892 小节**。")
A("> 说明：本文件是骨架的**可读渲染**，用于审读、学习与迁移导航；改目录请改 `book.tex`。")
A("> 图例：`★` 已有正文｜括号内为该节的学习要点条数")
A(">")
A("> 2026-09-22 本轮改动（r73）：《求助与资源导航 · 求助渠道》四小节正文撰写完成")
A("> （医疗机构 / 心理咨询机构 / 公益热线与社群 / 网络求助的注意事项）。")
A("> 全书唯一的「待写」标注已撤销并替换为来源锚——该标注系误标：旧区有同名章现成内容。")
A("> 上一轮（r72）：三卷目录按读者性别分工、互不重复（共通 / 女性专属 / 男性专属）。")
A("")
A("---")

cur_part = "（前置）"
pch = collections.OrderedDict()
pch[cur_part] = {"ch": 0, "sec": 0, "sub": 0, "line": 0}
A("")
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
        pch[cur_part]["ch"] += 1
        mark = " `★`" if "两性研究导论" in t else ""
        A("")
        A("### %s%s" % (t, mark))
        A("")
    elif lv == "section":
        pch[cur_part]["sec"] += 1
        n = sub_cnt.get(ln, 0)
        A("- **%s**%s" % (t, ("　（%d）" % n) if n else ""))
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
print("written", OUT)
print("篇 %d 章 %d 节 %d 小节 %d" % (len(pch), tc, ts, tu))
