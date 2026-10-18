# -*- coding: utf-8 -*-
"""r63c：骨架各篇章数 + toc/appendix 命令位置"""
import io, os, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
lines = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")

for cmd in ("\\tableofcontents", "\\appendix", "\\frontmatter", "\\mainmatter", "\\backmatter", "\\listoffigures"):
    print("%-18s %s" % (cmd, [i + 1 for i, l in enumerate(lines) if l.strip() == cmd]))

S = re.compile(r"^\\(part|chapter)\*?\{")
sk = []
for i, l in enumerate(lines[:753]):
    s = l.strip()
    if s.startswith("%"):
        continue
    m = S.match(s)
    if m:
        t = s[s.index("{") + 1:]
        t = t[:t.rindex("}")] if "}" in t else t
        sk.append((i + 1, m.group(1), t))

cur, cnt, order = None, {}, []
for ln, lv, t in sk:
    if lv == "part":
        cur = t
        order.append(cur)
        cnt[cur] = []
    elif cur:
        cnt[cur].append(t)
print()
for k in order:
    v = cnt[k]
    print("%-26s %2d 章 | %s" % (k[:26], len(v), "、".join(x[:12] for x in v)))
