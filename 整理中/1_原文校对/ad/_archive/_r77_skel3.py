# -*- coding: utf-8 -*-
"""r77: 导出 book.tex 骨架第三篇（亲密关系与性实践）8 个实践章的内部结构。"""
import io, re

H = re.compile(r"^\\(chapter|section|subsection|subsubsection)\*?\{(.*)\}\s*$")
lines = [x.rstrip("\r") for x in io.open("book.tex", encoding="utf-8", newline="").read().split("\n")]

RANGES = [(3867, 4221, "第15章 新婚首夜"),
          (4221, 4618, "第16章 自慰"),
          (4618, 4906, "第17章 情感亲密与沟通"),
          (4906, 5582, "第18章 前戏与爱抚"),
          (5582, 5871, "第19章 性技巧与性辅助"),
          (5871, 6264, "第20章 体位与姿势"),
          (6264, 6797, "第21章 性爱的多样实践"),
          (6797, 7110, "第22章 家庭形态的多样性"),
          (7110, 7440, "第23章 性爱中的意外与处理")]

out = []
for a, b, lab in RANGES:
    out.append("=" * 88)
    out.append("%s   L%d~L%d  共 %d 行" % (lab, a, b, b - a))
    for i in range(a - 1, b):
        m = H.match(lines[i])
        if m:
            out.append("  L%-6d %-13s %s" % (i + 1, m.group(1), ("  " * {"chapter": 0, "section": 1, "subsection": 2, "subsubsection": 3}[m.group(1)]) + m.group(2)))
io.open("_r77_skel3.txt", "w", encoding="utf-8", newline="").write("\n".join(out) + "\n")
print("写出 _r77_skel3.txt：%d 行" % len(out))
