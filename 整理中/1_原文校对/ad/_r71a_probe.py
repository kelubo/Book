# -*- coding: utf-8 -*-
"""r71a：探测 female.tex / male.tex 的结构与编译基线。只读。"""
import re, sys

FILES = ["female.tex", "male.tex"]
TITLE = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection|paragraph|subparagraph)\*?\s*\{")

for fn in FILES:
    s = open(fn, encoding="utf-8").read()
    lines = s.split("\n")
    print("=" * 70)
    print(fn, " 总行数", len(lines), " CRLF", s.count("\r\n"))
    # 关键命令行号
    keys = [r"\documentclass", r"\begin{document}", r"\frontmatter", r"\mainmatter",
            r"\tableofcontents", r"\backmatter", r"\appendix", r"\end{document}"]
    for k in keys:
        hits = [i + 1 for i, l in enumerate(lines) if k in l and not l.strip().startswith("%")]
        print("  %-18s %s" % (k, hits[:6]))
    cnt = {}
    for l in lines:
        m = TITLE.match(l)
        if m:
            cnt[m.group(1)] = cnt.get(m.group(1), 0) + 1
    print("  标题统计:", cnt)
    # part / chapter 清单（非注释行）
    print("  -- part --")
    for i, l in enumerate(lines, 1):
        if re.match(r"^\s*\\part\*?\s*\{", l):
            print("    L%-6d %s" % (i, l.strip()[:80]))
    print("  -- chapter（前 60） --")
    n = 0
    for i, l in enumerate(lines, 1):
        if re.match(r"^\s*\\chapter\*?\s*\{", l):
            n += 1
            if n <= 60:
                print("    L%-6d %s" % (i, l.strip()[:80]))
    print("    合计 %d 章" % n)
