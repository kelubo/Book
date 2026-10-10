# -*- coding: utf-8 -*-
"""r77: 抽查巨块若干小节的真实正文，判断"凑数"程度。"""
import io, re, collections

lines = [x.rstrip("\r") for x in io.open("book.tex", encoding="utf-8", newline="").read().split("\n")]

def stat(a, b, label):
    seg = lines[a - 1:b]
    nonempty = [x for x in seg if x.strip()]
    comments = [x for x in seg if x.strip().startswith("%")]
    print("-" * 92)
    print("%s  L%d~L%d  行 %d ｜非空 %d ｜注释 %d" % (label, a, b, len(seg), len(nonempty), len(comments)))

print("### 一、54269 口交技巧 ~ 54687 吟叫与扭动 之间到底是什么")
stat(54269, 54687, "区间")
for i in range(54268, 54290):
    print("   %-6d| %s" % (i + 1, lines[i][:116]))
print("   ...")
for i in range(54680, 54700):
    print("   %-6d| %s" % (i + 1, lines[i][:116]))

print()
print("### 二、姿势小节抽样（好例 vs 凑数例）")
for a, b, lab in ((59379, 59412, "男上女下姿势（传教士姿势）"),
                  (62682, 62715, "办公室安全姿势"),
                  (62275, 62306, "未来式姿势"),
                  (62306, 62337, "复古式姿势"),
                  (62619, 62650, "庆祝式姿势"),
                  (65915, 65989, "特殊技巧姿势")):
    print("=" * 92)
    print(lab, "L%d~L%d" % (a, b))
    for i in range(a - 1, b):
        print("   %-6d| %s" % (i + 1, lines[i][:116]))
