# -*- coding: utf-8 -*-
"""r67：从 book.tex 骨架区导出「新目录清单」Markdown。"""
import io, os, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
lines = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8").read().split("\n")
old = next(i for i, l in enumerate(lines) if l.strip() == "\\part{old}")
body = lines[:old]

out = []
out.append("# 全书目录（2026-09-21 重构版）")
out.append("")
out.append("> 来源：`book.tex` 前置骨架区（`\\part{old}` 之前，L1–L%d）。旧区未动。" % old)
out.append("> 每章/节的来源锚写在 `book.tex` 的注释里（`% 移入：\"旧区标题\"`），搜标题即可定位原块。")
out.append("")

npart = nch = nsec = 0
cur_is_appendix = False
for i, l in enumerate(body):
    s = l.strip()
    if not s or s.startswith("%"):
        continue
    if s.startswith("\\part"):
        t = s[s.index("{") + 1:s.rindex("}")] if "}" in s else s
        npart += 1
        out.append("")
        out.append("## %s" % t)
        out.append("")
        continue
    m = re.match(r"^\\chapter\{(.*)\}$", s)
    if m:
        nch += 1
        if s.startswith("\\chapter") and "前言" in m.group(1):
            out.append("## %s" % m.group(1))
        else:
            out.append("### %s" % m.group(1))
        continue
    m = re.match(r"^\\section\{(.*)\}$", s)
    if m:
        nsec += 1
        out.append("- %s" % m.group(1))
        continue
    m = re.match(r"^\\subsection\{(.*)\}$", s)
    if m:
        out.append("    - %s" % m.group(1))

out.append("")
out.append("---")
out.append("")
out.append("合计：part %d 个（含 `\\part*{附录}`）、chapter %d 个、section %d 个。" % (npart, nch, nsec))
io.open(os.path.join(BASE, "_r67_新目录清单_2026-09-21.md"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
print("written，行数", len(out), "｜ part", npart, "chapter", nch, "section", nsec)
