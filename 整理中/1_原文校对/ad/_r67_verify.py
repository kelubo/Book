# -*- coding: utf-8 -*-
"""r67 落盘后验证：换行、改动边界、旧区一致、骨架统计。"""
import io, os, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
raw = io.open(os.path.join(BASE, "book.tex"), "rb").read()
print("换行：CRLF %d，裸 LF %d，字节 %d" % (raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n"), len(raw)))
b = raw.decode("utf-8").split("\n")
a = io.open(os.path.join(BASE, "_backup_r67", "book.tex"), encoding="utf-8").read().split("\n")
print("行数：%d -> %d (%+d)" % (len(a), len(b), len(b) - len(a)))

p = 0
while p < min(len(a), len(b)) and a[p] == b[p]:
    p += 1
print("公共前缀 %d 行（L%d 起不同）" % (p, p + 1))
i = next(i for i, l in enumerate(b) if l.strip() == "\\part{old}")
j = next(i for i, l in enumerate(a) if l.strip() == "\\part{old}")
print("\\part{old}: L%d -> L%d" % (j + 1, i + 1))
print("旧区逐字一致：%s" % (a[j:] == b[i:]))

# 未闭合的 \if 检查
t = "\n".join(b)
print("\\iffalse 数 %d，\\fi 数 %d" % (t.count("\\iffalse"), len(re.findall(r"^\\fi$", t, re.M))))

# 骨架统计
body = b[:i]
print("\n骨架区：part %d / chapter %d / section %d / subsection %d" % (
    sum(1 for l in body if l.strip().startswith("\\part")),
    sum(1 for l in body if l.strip().startswith("\\chapter")),
    sum(1 for l in body if re.match(r"^\\section\*?\{", l.strip())),
    sum(1 for l in body if re.match(r"^\\subsection\*?\{", l.strip()))))

# 标题宽度审计（沿用 r61 口径：中文主体宽，剥英文对照括号）
import unicodedata
PAREN = re.compile(r"[（(]([^（）()]*)[）)]")
CMD_RE = re.compile(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?(\{[^{}]*\})?")


def cjk(s):
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


def W(s):
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def clean(raw_):
    t = raw_
    for _ in range(6):
        n = CMD_RE.sub(lambda m: m.group(2) or "", t)
        if n == t:
            break
        t = n
    t = t.replace("\\", "")

    def rep(m):
        return "" if cjk(m.group(1)) == 0 else m.group(0)
    return W(PAREN.sub(rep, t).strip())


bad = []
for i2, l in enumerate(body):
    s = l.strip()
    m = re.match(r"^\\(chapter|section|subsection|subsubsection)\*?\{(.*)\}$", s)
    if not m:
        continue
    w = clean(m.group(2))
    if w >= 30:
        bad.append((i2 + 1, m.group(1), m.group(2), w))
print("\n骨架区中文主体宽 >=30 的标题：%d 处" % len(bad))
for x in bad:
    print("   L%-6d %-12s %-40s 宽 %d" % x)

# 重复节名检查（同章内）
from collections import Counter
cur = None
dups = []
for i2, l in enumerate(body):
    s = l.strip()
    if s.startswith("\\chapter"):
        cur = s
        seen = set()
        continue
    m = re.match(r"^\\section\{(.*)\}$", s)
    if m:
        if m.group(1) in seen:
            dups.append((cur, m.group(1), i2 + 1))
        seen.add(m.group(1))
print("\n同章内重复节名：%d 处" % len(dups))
for d in dups:
    print("   ", d)
