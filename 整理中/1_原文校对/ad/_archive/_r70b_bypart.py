# -*- coding: utf-8 -*-
"""r70b：按篇分组统计章/节/小节数，核对 r69 交付文档的 64 章口径。只读。"""
import re

s = open("book.tex", encoding="utf-8").read()
s = re.sub(r"\\iffalse[\s\S]*?\\fi", "", s)
head = s[: s.find(r"\part{old}")]
lines = head.split("\n")

cur = "（前置）"
stat = {}
order = ["（前置）"]
stat[cur] = [0, 0, 0]

for ln in lines:
    t = ln.rstrip()
    m = re.match(r"\s*\\part\*?\{(.+?)\}", t)
    if m:
        cur = m.group(1)
        if cur not in stat:
            stat[cur] = [0, 0, 0]
            order.append(cur)
        continue
    if re.match(r"\s*\\chapter\*?\{", t):
        stat[cur][0] += 1
    elif re.match(r"\s*\\section\*?\{", t):
        stat[cur][1] += 1
    elif re.match(r"\s*\\subsection\*?\{", t):
        stat[cur][2] += 1

tot = [0, 0, 0]
print("%-22s %5s %6s %8s" % ("篇", "章", "节", "小节"))
print("-" * 46)
n = 0
for k in order:
    v = stat[k]
    if k != "（前置）":
        n += 1
    label = k if k != "（前置）" else "（前置：序/导言）"
    print("%-22s %5d %6d %8d" % (label, v[0], v[1], v[2]))
    for i in range(3):
        tot[i] += v[i]
print("-" * 46)
print("%-22s %5d %6d %8d" % ("合计", tot[0], tot[1], tot[2]))
print("\n编号篇数（不含前置）：", n - 1 if "（前置）" in order else n)
print("正文八篇章数：", tot[0] - stat["（前置）"][0] - stat.get("结语", [0])[0] - stat.get("附录", [0])[0])
