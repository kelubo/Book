# -*- coding: utf-8 -*-
"""r77: 量化 female.tex 旧区中与性爱实践相关的块，并抽样。"""
import io, re

H = re.compile(r"^\\(part|chapter|section|subsection)\*?\{(.*)\}\s*$")
LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3}
lines = [x.rstrip("\r") for x in io.open("female.tex", encoding="utf-8", newline="").read().split("\n")]
N = len(lines)

toks = []
for i, l in enumerate(lines):
    m = H.match(l)
    if m:
        toks.append((i, m.group(1), m.group(2).strip()))
toks.append((N, None, None))

TARGETS = ["阴交技巧与体验", "肛交技巧与体验", "性生活的准备与技巧", "口交与性健康",
           "第一次性交的感受与体验", "性交后的身体护理与清洁", "安全体位与技巧", "润滑剂选择"]
print("=== female.tex 目标块体量 ===")
found = {}
for k in range(len(toks) - 1):
    i, lvl, t = toks[k]
    if t in TARGETS:
        a, b = i + 1, toks[k + 1][0]
        nb = len([x for x in lines[a - 1:b] if x.strip()])
        found.setdefault(t, []).append((a, b, nb))
        print("  %-24s %-11s L%-6d~L%-6d  %5d 行（非空 %d）" % (t, lvl, a, b, b - a + 1, nb))
print("未找到：", [t for t in TARGETS if t not in found])

print()
print("=== 抽样：阴交技巧与体验 L10433 ===")
for i in range(10432, 10460):
    print("  %-6d| %s" % (i + 1, lines[i][:114]))
print("=== 抽样：性生活的准备与技巧 L15098 ===")
for i in range(15097, 15130):
    print("  %-6d| %s" % (i + 1, lines[i][:114]))
