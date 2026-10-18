# -*- coding: utf-8 -*-
"""r40: A2 皮肤可见病锚点探测——住院康复节结构与身体意象相关位置"""
import io, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
with io.open(BASE + r"\book.tex", "r", encoding="utf-8", newline="") as f:
    lines = f.read().split("\r\n")

HDR = re.compile(r"\\(chapter|section|subsection|subsubsection)\{([^{}]*)\}")
lv = {"chapter": 0, "section": 1, "subsection": 2, "subsubsection": 3}

def title_of(lineno):
    best = None
    for i in range(lineno, 0, -1):
        st = lines[i - 1].strip()
        if st.startswith("%"):
            continue
        m = HDR.match(st)
        if m:
            return "L%d \\%s{%s}" % (i, m.group(1), m.group(2)[:50])
    return "?"

print("---- L28054 所属上下文 ----")
print("所属:", title_of(28054))
for i in range(28040, 28075):
    print("%5d| %s" % (i, lines[i - 1].strip()[:105]))

print("\n---- 皮肤/慢病语境的 section/subsection 标题 ----")
for i, ln in enumerate(lines, 1):
    st = ln.strip()
    if st.startswith("%"):
        continue
    m = HDR.match(st)
    if m and any(k in m.group(2) for k in ("皮肤", "慢性病", "慢性疾病", "康复", "住院", "外貌", "形象", "自信")):
        print("L%d \\%s{%s}" % (i, m.group(1), m.group(2)[:80]))

print("\n---- 身体意象 命中行（前12处 + 所属节） ----")
n = 0
for i, ln in enumerate(lines, 1):
    st = ln.strip()
    if st.startswith("%"):
        continue
    if "身体意象" in st:
        n += 1
        if n <= 12:
            print("L%d (%s): %s" % (i, title_of(i), st[:70]))
print("total:", n)
