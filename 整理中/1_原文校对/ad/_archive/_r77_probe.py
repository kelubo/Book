# -*- coding: utf-8 -*-
"""r77 探针：查看 book.tex 旧区"性爱相关"巨块的内部结构。"""
import io, re, collections

H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{(.*)\}\s*$")

lines = [x.rstrip("\r") for x in io.open("book.tex", encoding="utf-8", newline="").read().split("\n")]

for a, b, label in ((53683, 67115, "part{性爱与亲密关系} > 性爱技巧与沟通"),
                    (27245, 27842, "第四篇：性交体位与姿势艺术"),
                    (73725, 73876, "初学者的SM指导 + 文化与性")):
    seg = lines[a - 1:b]
    c = collections.Counter()
    for l in seg:
        m = H.match(l)
        if m:
            c[m.group(1)] += 1
    print("=" * 96)
    print("L%d~L%d  %s  共 %d 行  标题计数 %s" % (a, b, label, len(seg), dict(c)))

print("=" * 96)
print("--- 53683~53780 原文 ---")
for i in range(53682, 53780):
    print("  %-6d| %s" % (i + 1, lines[i][:114]))

print("=" * 96)
print("--- 53683~67115 的 section/subsection 标题 ---")
for i in range(53682, 67115):
    m = H.match(lines[i])
    if m and m.group(1) in ("section", "subsection"):
        print("  L%-6d %-11s %s" % (i + 1, m.group(1), m.group(2)[:86]))
