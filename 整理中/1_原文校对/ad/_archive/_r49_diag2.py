# -*- coding: utf-8 -*-
"""排查 missing-item 错误根因"""
import io, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
raw = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read().replace("\r\n", "\n")
L = raw.split("\n")

out = io.open(os.path.join(BASE, "_r49_diag2.txt"), "w", encoding="utf-8", newline="")

# 1. preamble 宏包
out.write("=== \\usepackage 行 ===\n")
for i, ln in enumerate(L[:200], 1):
    if "\\usepackage" in ln or "enumitem" in ln:
        out.write("L%d: %s\n" % (i, ln.strip()[:110]))

# 2. 统计
out.write("\n=== 统计 ===\n")
out.write("begin{itemize}[ 总数: %d\n" % raw.count("\\begin{itemize}["))
out.write("begin{itemize} 总数: %d\n" % raw.count("\\begin{itemize}"))
out.write("begin{enumerate}[ 总数: %d\n" % raw.count("\\begin{enumerate}["))
# \item 后紧跟非空格非[ 的
pat = re.compile(r"\\item([^\s\[\{])")
hits2 = [(i, ln.strip()[:90]) for i, ln in enumerate(L, 1) if pat.search(ln)]
out.write("\\item 后紧跟其他字符: %d\n" % len(hits2))
for i, s in hits2[:15]:
    out.write("  L%d: %s\n" % (i, s))

# 3. tab 缩进 \item 且上一行不是 begin/begin 内的:检查日志中报错的行,看其所在环境的 begin 行
ERR = [3914,3923,3944,3987,4023,4035,4043,4053,4080,4088,4111,4119,4128,4145,4160,4174,4196,4212,4227,4252,
       5085,5097,5108,5139,5151,5163,5177,5193,5202,5211,6011,6039,6051,7676,7688,7702,7713,7725,7734,7747,
       7756,7773,7783,7814,7823,17431,17444,17463,17472,17525,24627,24653,24681,27118,27127,27147,27159,
       27178,27188,27215,27228,27306,48508,48534,48549]
out.write("\n=== 报错行所在 itemize 的 begin 参数分布 ===\n")
from collections import Counter
c = Counter()
for t in ERR:
    # 向上找最近的 \begin{itemize/enumerate/description}
    for j in range(t-1, 0, -1):
        s = L[j-1].strip()
        if s.startswith("\\begin{itemize}") or s.startswith("\\begin{enumerate}") or s.startswith("\\begin{description}"):
            c[s[:40]] += 1
            break
        if s.startswith("\\chapter{") or s.startswith("\\section{"):
            c["<未找到环境:" + s[:30] + ">"] += 1
            break
for k, v in c.most_common():
    out.write("%4d  %s\n" % (v, k))

# 4. 是否所有报错行都紧跟 begin{itemize}[leftmargin=2cm]
out.write("\n=== 报错行前 3 行是否含 begin{itemize}[ ===\n")
n_near = sum(1 for t in ERR if any("\\begin{itemize}[" in L[k] for k in range(max(0,t-4), t-1)))
out.write("附近有 begin{itemize}[: %d / %d\n" % (n_near, len(ERR)))
out.close()
print("diag2 written")
print(io.open(os.path.join(BASE, "_r49_diag2.txt"), encoding="utf-8").read()[:4000])
