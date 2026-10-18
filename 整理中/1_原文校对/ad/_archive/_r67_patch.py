# -*- coding: utf-8 -*-
import io
p = r"D:\Git\Book\整理中\1_原文校对\ad\_r67_rebuild.py"
s = io.open(p, encoding="utf-8").read()
old = '        ("性玩具与器具的使用安全", \'% 移入："性玩具的使用与安全"（与"性技巧与辅助"章分工：本节收使用安全与卫生）\'),\n'
assert s.count(old) == 1, s.count(old)
s = s.replace(old, "")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("removed")
