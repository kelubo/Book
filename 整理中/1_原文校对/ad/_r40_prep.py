# -*- coding: utf-8 -*-
"""r40: 备份三卷 + 探测三个新节锚点候选"""
import io, os, re, shutil

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
BK = BASE + r"\_backup_r40"

# 1) 备份
os.makedirs(BK, exist_ok=True)
for fn in ("book.tex", "female.tex", "male.tex"):
    shutil.copy2(os.path.join(BASE, fn), os.path.join(BK, fn))
print("backup ok ->", BK)

# 2) 锚点候选 count 检查
with io.open(os.path.join(BASE, "book.tex"), "r", encoding="utf-8", newline="") as f:
    lines = f.read().split("\r\n")

CANDS = [
    # A1 年龄差伴侣：性与多元关系前（关系模式群）
    r"\section{性与多元关系}",
    r"\subsection{多元关系的类型}",
    # A2 皮肤可见病：身体意象/慢性病语境
    r"\section{身体意象与性自信}",
    r"\subsection{身体意象与性}",
    r"\section{住院与康复期的性}",
    r"\subsection{住院与康复期的性}",
    # A3 职场恋情：特殊职业人群前
    r"\section{特殊职业人群的性健康}",
    r"\subsection{共同处境}",
]
for c in CANDS:
    n = sum(1 for ln in lines if ln.strip().startswith(c))
    print("count=%d  %s" % (n, c))

# 3) 相关节结构：身体意象 / 多元关系前后 / 慢性病章
HDR = re.compile(r"\\(section|subsection)\{([^{}]*)\}")
print("\n---- 身体意象相关节 ----")
for i, ln in enumerate(lines, 1):
    st = ln.strip()
    if st.startswith("%"):
        continue
    if "身体意象" in st and HDR.match(st):
        print("L%d %s" % (i, st[:90]))

print("\n---- L24690-L24715 (多元关系节头) ----")
for i in range(24690, 24716):
    print("%5d| %s" % (i, lines[i - 1].strip()[:100]))

print("\n---- L27960-L27980 (特殊职业节头) ----")
for i in range(27960, 27981):
    print("%5d| %s" % (i, lines[i - 1].strip()[:100]))
