# -*- coding: utf-8 -*-
r"""r75 female 旧区逐节体检：列出原始内容区每个 section 的行跨度、体量，
并判断框架区是否有同名/近似 section，以及该节内容是否在框架中以其他名目覆盖。

用法: python _r75_femsec.py
"""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection|paragraph)\*?\{(.*?)\}")


def norm(t):
    t = re.sub(r"（[^）]*）", "", t)
    t = re.sub(r"\([^)]*\)", "", t)
    t = re.sub(r"[\s、，,。·・\-—–：:；;／/]+", "", t)
    return t.strip()


f = "female.tex"
lines = io.open(f, encoding="utf-8", newline="").read().split("\n")
oi = next(i for i, l in enumerate(lines) if l.rstrip("\r").strip().startswith("\\part*{原始内容}"))

# 框架区标题集合（含 subsection）
fw = []
for i in range(284, 6481):
    m = H.match(lines[i].rstrip("\r"))
    if m:
        fw.append((m.group(1), m.group(2).strip(), i + 1, norm(m.group(2))))
fw_n = set(x[3] for x in fw)

# 旧区 section 列表（含跨度）
secs = []
for i in range(oi, len(lines)):
    m = H.match(lines[i].rstrip("\r"))
    if m and m.group(1) in ("chapter", "section"):
        secs.append((m.group(1), m.group(2).strip(), i))
secs.append(("END", "", len(lines) - 1))

print("female.tex 原始内容区逐节体检（L%d 起，共 %d 行）" % (oi + 1, len(lines) - oi))
print("=" * 92)
tot_miss = 0
for k in range(len(secs) - 1):
    lvl, t, i0 = secs[k]
    i1 = secs[k + 1][2]
    n = norm(t)
    exact = n in fw_n
    loose = exact or any(n and (n in k2 or k2 in n) for k2 in fw_n)
    # 该节下 subsection 与框架的重合率
    subs = [norm(H.match(lines[j].rstrip("\r")).group(2)) for j in range(i0 + 1, i1)
            if H.match(lines[j].rstrip("\r")) and H.match(lines[j].rstrip("\r")).group(1) in ("subsection", "subsubsection")]
    hit = sum(1 for s in subs if s in fw_n)
    flag = "OK " if loose else "缺失"
    if not loose:
        tot_miss += i1 - i0
    print("%-6s L%-6d~%-6d %5d行  %-10s %s" % (flag, i0 + 1, i1, i1 - i0, lvl, t[:52]))
    print("            %d/%d 个子标题在框架中命中 %s" % (hit, len(subs), ("(精确)" if exact else "")))
print("=" * 92)
print("宽松缺失节的合计行数 =", tot_miss)
