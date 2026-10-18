# -*- coding: utf-8 -*-
"""r72 终检：直接读三个 tex 文件的「新目录骨架区」，输出规模、卷内重名、跨卷重名。
骨架区边界：book = \\mainmatter .. \\part{old}；female = \\mainmatter .. \\part*{原始内容}；
            male = \\listoftables .. \\part*{原始内容}。
"""
import io
import os
import re
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
T = re.compile(r"\\(part|chapter|section|subsection)\*?\{([^{}]*)\}")


def skel(fn, anchor, endkw):
    raw = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n")
    lines = raw.split("\n")
    si = next(i for i, l in enumerate(lines) if l.strip() == anchor)
    ei = next(i for i, l in enumerate(lines) if endkw in l and l.strip().startswith("\\part"))
    ents, dead = [], False
    for i in range(si + 1, ei):
        s = lines[i].strip()
        if s.startswith("\\iffalse"):
            dead = True
        if s.startswith("%") or not s:
            continue
        m = T.match(s) if lines[i].startswith("\\") else None
        if m:
            ents.append((m.group(1), m.group(2).strip(), dead))
    return ents


V = {"book": skel("book.tex", "\\mainmatter", "\\part{old}"),
     "female": skel("female.tex", "\\mainmatter", "原始内容"),
     "male": skel("male.tex", "\\listoftables", "原始内容")}

print("══ 规模（只计生效区，排除 \\iffalse）══")
for k, ents in V.items():
    c = Counter(lv for lv, _, d in ents if not d)
    print("  %-7s 篇 %d / 章 %d / 节 %d / 小节 %d" % (k, c["part"], c["chapter"], c["section"], c["subsection"]))

print("\n══ 卷内重名章 ══")
bad = 0
for k, ents in V.items():
    c = Counter(t for lv, t, d in ents if lv == "chapter" and not d)
    d = {t: n for t, n in c.items() if n > 1}
    if d:
        print("  %s: %s" % (k, d))
        bad += len(d)
print("  无" if not bad else "")

print("\n══ 卷内重名节（同章内，排除医学体例同名）══")
BODY = {"分类", "病因", "诊断与评估", "治疗方法", "预防措施", "症状", "检查项目", "概述"}
bad2 = 0
for k, ents in V.items():
    cur, seen = None, Counter()
    for lv, t, d in ents:
        if d:
            continue
        if lv == "chapter":
            cur, seen = t, Counter()
        elif lv == "section":
            seen[t] += 1
            if seen[t] == 2 and t not in BODY:
                print("  %s / %s -> 《%s》" % (k, cur, t))
                bad2 += 1
print("  无" if not bad2 else "")

print("\n══ 跨卷重名（章级）══")
idx = defaultdict(set)
for k, ents in V.items():
    for lv, t, d in ents:
        if lv == "chapter" and not d:
            idx[t].add(k)
h = {t: sorted(v) for t, v in idx.items() if len(v) > 1}
print("  ", h if h else "无")

print("\n══ 跨卷重名（节级）══")
idx2 = defaultdict(set)
for k, ents in V.items():
    for lv, t, d in ents:
        if lv == "section" and not d:
            idx2[t].add(k)
h2 = {t: sorted(v) for t, v in idx2.items() if len(v) > 1}
if not h2:
    print("   无")
for t, v in sorted(h2.items()):
    print("   %-32s %s" % (t, v))
