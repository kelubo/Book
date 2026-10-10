# -*- coding: utf-8 -*-
"""r74 进度报告：统计已完成 / 剩余的空小节。只读。"""
import io, re, sys, os
sys.stdout.reconfigure(encoding="utf-8")

F = "book.tex"
raw = io.open(F, encoding="utf-8", newline="").read()
lines = raw.replace("\r\n", "\n").split("\n")

H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{(.*)\}\s*(%.*)?$")
LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}
heads = [(i, H.match(l).group(1), H.match(l).group(2)) for i, l in enumerate(lines) if H.match(l)]
OLD = next(i for i, lv, t in heads if lv == "part" and t == "old")
off = set()
d = 0; st = None
for i, l in enumerate(lines):
    s = l.strip()
    if re.match(r"^\\iffalse\b", s):
        if d == 0: st = i
        d += 1
    elif s == "\\fi" and d > 0:
        d -= 1
        if d == 0:
            for k in range(st, i + 1): off.add(k)
sk = [(i, lv, t) for i, lv, t in heads if i < OLD and i not in off]

def has_body(idx):
    ln, lv, t = sk[idx]
    end = len(lines)
    for j in range(idx + 1, len(sk)):
        if LV[sk[j][1]] <= LV[lv]:
            end = sk[j][0]; break
    for k in range(ln + 1, end):
        s = lines[k].strip()
        if s and not s.startswith("%"): return True
    return False

order = []
cur_part = "（前置）"
for idx, (ln, lv, t) in enumerate(sk):
    if lv == "part":
        cur_part = t
    elif lv == "chapter":
        order.append([cur_part, ln + 1, t, 0, 0])   # part, line, title, total, empty
    elif lv == "subsection":
        if order:
            order[-1][3] += 1
            if not has_body(idx): order[-1][4] += 1

print("| 篇 | 章 | 总小节 | 已完成 | 剩余 |")
print("|---|---|---:|---:|---:|")
tot_t = tot_e = 0
for p, ln, t, u, e in order:
    done = u - e
    tot_t += u; tot_e += e
    mark = " ✅" if u and e == 0 else (" ⬜" if e == u else " 🔶")
    print("| %s | %s%s | %d | %d | %d |" % (p, t, mark, u, done, e))
print("| **合计** | **%d 章** | **%d** | **%d** | **%d** |" % (len(order), tot_t, tot_t - tot_e, tot_e))
print()
print("完成率: %.1f%%" % (100.0 * (tot_t - tot_e) / tot_t))
