# -*- coding: utf-8 -*-
"""r70 状态快照：确认 r69 落盘后的骨架规模与关键分界。只读，不改文件。"""
import re

P = "book.tex"
s = open(P, encoding="utf-8").read()
lines = s.split("\n")

print("== 换行 ==")
print("CRLF", s.count("\r\n"), " LF", s.count("\n"), " -> ",
      "纯LF" if s.count("\r\n") == 0 else "含CRLF")

stripped = re.sub(r"\\iffalse[\s\S]*?\\fi", "", s)
i_old = stripped.find(r"\part{old}")
head = stripped[:i_old]


def cnt(t, cmd):
    return len(re.findall(r"\\" + re.escape(cmd) + r"\{", t))


print("\n== 骨架区（\\part{old} 之前，已剔除 iffalse 区间） ==")
for c in ("part", "part*", "chapter", "section", "subsection"):
    print("  %-12s %d" % (c, cnt(head, c)))

print("\n== 关键分界（原文行号） ==")
for key in (r"\part{结语}", r"\backmatter", r"\part*{附录}", r"\part{old}"):
    for idx, ln in enumerate(lines, 1):
        if key in ln:
            print("  %-16s L%d" % (key, idx))
            break

print("\n== 骨架内的 part 行 ==")
old_line = next(k for k, l in enumerate(lines, 1) if r"\part{old}" in l)
for idx in range(1, old_line):
    if re.match(r"\s*\\part\*?\{", lines[idx - 1]):
        print("  L%d: %s" % (idx, lines[idx - 1].strip()))

print("\n== 骨架区非标题/非注释文本行 ==")
body = []
for l in lines[: old_line - 1]:
    t = l.strip()
    if not t or t.startswith("%"):
        continue
    if re.match(r"\\[a-zA-Z]+\*?(\[|\{)", t):
        continue
    body.append(l)
print("  计数：", len(body))
for l in body[:5]:
    print("   ", l.strip()[:100])
print("\n总行数：", len(lines))
