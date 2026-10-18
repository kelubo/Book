# -*- coding: utf-8 -*-
"""r63b：keyword 宏 / matter 边界 / 空壳节统计"""
import io, re, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
lines = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")

kw = [i + 1 for i, l in enumerate(lines) if "\\keyword" in l]
print("\\keyword 出现 %d 行：L%d ~ L%d" % (len(kw), kw[0], kw[-1]) if kw else "无")

DEF = re.compile(r"(newcommand|renewcommand|providecommand|def|DeclareRobustCommand|NewDocumentCommand|newtcolorbox|newenvironment)\b")
found = False
for i, l in enumerate(lines):
    if DEF.search(l) and "keyword" in l:
        print("  定义候选 L%d: %s" % (i + 1, l.strip()[:120]))
        found = True
if not found:
    print("  !! 全文未见 \\keyword 的定义")

# 其它可疑宏：骨架章用到但可能未定义的
susp = {}
for i, l in enumerate(lines[:760]):
    for m in re.finditer(r"\\([a-zA-Z@]+)", l):
        n = m.group(1)
        if n in ("part", "chapter", "section", "subsection", "subsubsection", "item", "begin", "end",
                 "textbf", "textit", "emph", "label", "ref", "cite", "frac", "hspace", "vspace",
                 "frontmatter", "mainmatter", "backmatter", "listoffigures", "listoftables",
                 "keyword", "tableofcontents", "clearpage", "newpage", "par", "zihao", "itshape", "vfill"):
            continue
        susp.setdefault(n, []).append(i + 1)
for n, v in sorted(susp.items(), key=lambda x: -len(x[1])):
    if len(v) >= 3:
        print("  骨架区可疑宏 \\%s ×%d 首现 L%d" % (n, len(v), v[0]))

for key in ("\\frontmatter", "\\mainmatter", "\\backmatter"):
    hits = [i + 1 for i, l in enumerate(lines) if l.strip() == key]
    print("%-14s %s" % (key, hits))

LV = re.compile(r"^\s*\\(section|subsection)\*?\{")
hdr = [(i, l.strip()) for i, l in enumerate(lines) if LV.match(l)]
empty = []
for k, (i, s) in enumerate(hdr):
    e = hdr[k + 1][0] if k + 1 < len(hdr) else len(lines)
    body = [x for x in lines[i + 1:e] if x.strip() and not x.strip().startswith("%") and not LV.match(x)]
    if not body:
        empty.append((i + 1, s))
print("全部 section/subsection %d 个；纯占位（无正文）%d 个" % (len(hdr), len(empty)))
for ln, s in empty[:12]:
    print("   L%-6d %s" % (ln, s[:60]))
