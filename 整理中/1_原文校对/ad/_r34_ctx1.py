# -*- coding: utf-8 -*-
"""r34 语境核查：排除词组误配 + 定位现有结构"""
import io, os, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
T = {}
for fn in ["book.tex", "female.tex", "male.tex"]:
    T[fn] = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read()

print("== 口交 误配检查（抽前 12 处上下文）==")
n = 0
for fn in ["book.tex"]:
    for i, l in enumerate(T[fn].split("\n"), 1):
        s = l.strip()
        if "口交" in s:
            idx = s.find("口交")
            print("L%-6d ...%s..." % (i, s[max(0, idx-12):idx+14]))
            n += 1
            if n >= 12: break
print()

print("== 乳交 误配检查 ==")
n = 0
for fn in ["book.tex"]:
    for i, l in enumerate(T[fn].split("\n"), 1):
        s = l.strip()
        if "乳交" in s:
            idx = s.find("乳交")
            print("L%-6d ...%s..." % (i, s[max(0, idx-12):idx+14]))
            n += 1
            if n >= 10: break
print()

print("== 相关标题扫描 ==")
pat = re.compile(r"\\(chapter|section|subsection|subsubsection)\{([^{}]*)\}")
kw = ["口交", "肛交", "乳交", "乳房", "性强暴", "强奸", "性侵", "创伤", "跨性别", "法律", "婚姻", "权利",
      "伴侣", "关系"]
for fn in ["book.tex", "female.tex"]:
    for i, l in enumerate(T[fn].split("\n"), 1):
        m = pat.match(l.strip())
        if m and any(k in m.group(2) for k in kw):
            print("%-11s L%-6d %s %s" % (fn, i, m.group(1), m.group(2)[:60]))
