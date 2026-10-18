# -*- coding: utf-8 -*-
"""r77: 扫描 female.tex / male.tex 中与「性爱实践」相关的标题。"""
import io, re

H = re.compile(r"^\\(part|chapter|section|subsection)\*?\{(.*)\}\s*$")
LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3}
KEY = ("技巧", "体位", "姿势", "前戏", "爱抚", "性交", "口交", "自慰", "手淫", "做爱", "性爱",
       "频率", "注意事项", "润滑", "插入", "高潮技", "辅助", "情趣", "按摩")

for f in ("female.tex", "male.tex"):
    lines = [x.rstrip("\r") for x in io.open(f, encoding="utf-8", newline="").read().split("\n")]
    print("=" * 96)
    print(f, "总行", len(lines))
    stack = []
    for i, l in enumerate(lines):
        m = H.match(l)
        if not m:
            continue
        lvl, t = m.group(1), m.group(2).strip()
        while stack and LV[stack[-1][0]] >= LV[lvl]:
            stack.pop()
        path = " > ".join(x[1] for x in stack)
        stack.append((lvl, t))
        if any(k in t for k in KEY):
            print("  L%-6d %-11s %s" % (i + 1, lvl, (path + " > " if path else "") + t))
