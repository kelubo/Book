# -*- coding: utf-8 -*-
"""r66a：探测 book.tex 当前骨架（\part{old} 之前）的结构。"""
import io, re, os, time

P = r"D:\Git\Book\整理中\1_原文校对\ad\book.tex"
raw = io.open(P, "rb").read()
txt = raw.decode("utf-8", errors="replace")
lines = txt.replace("\r\n", "\n").split("\n")
print("mtime", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(P).st_mtime)))
print("总行数", len(lines), "CRLF", raw.count(b"\r\n"), "裸LF", raw.count(b"\n") - raw.count(b"\r\n"))

PART = re.compile(r"^\\part\*?\{")
HDR = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{")

# 找 \part{old}
old_ln = None
for i, l in enumerate(lines):
    if PART.match(l.strip()) and "old" in l:
        old_ln = i + 1
        break
print("\\part{old} 在 L", old_ln)

print()
print("=== \\part{old} 之前的所有 part ===")
for i, l in enumerate(lines[:old_ln - 1]):
    s = l.strip()
    if PART.match(s):
        print("L%6d| %s" % (i + 1, s[:80]))

print()
print("=== 骨架区 篇/章 骨架 ===")
cur_part = None
n_ch = 0
for i, l in enumerate(lines[:old_ln - 1]):
    s = l.strip()
    if s.startswith("%"):
        continue
    m = PART.match(s)
    if m:
        cur_part = s
        print()
        print("--- L%d %s" % (i + 1, s[:70]))
        continue
    m = HDR.match(s)
    if m and m.group(1) == "chapter":
        n_ch += 1
        print("   L%6d  %s" % (i + 1, s[:74]))
print()
print("骨架章总数", n_ch)
