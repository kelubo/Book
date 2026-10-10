# -*- coding: utf-8 -*-
"""r71b：分区统计 —— 每卷分「头部注释/新框架(停用)」与「原始内容(编译区)」两段统计标题。只读。"""
import re

TITLE = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection|paragraph|subparagraph)\*?\s*\{")

for fn, doc_ln in (("female.tex", 6417), ("male.tex", 5745)):
    lines = open(fn, encoding="utf-8").read().split("\n")
    print("=" * 72)
    print(fn)
    for name, seg in (("头部+新框架(停用区)", lines[: doc_ln - 1]),
                      ("原始内容(编译区)", lines[doc_ln - 1:])):
        cnt = {}
        firsts = {}
        for i, l in enumerate(seg, 1):
            m = TITLE.match(l)
            if m:
                k = m.group(1)
                cnt[k] = cnt.get(k, 0) + 1
                firsts.setdefault(k, []).append(i + doc_ln - 1 if seg is lines[doc_ln - 1:] else i)
        print("  [%s] 行数 %d" % (name, len(seg)))
        print("    ", {k: cnt.get(k, 0) for k in
                       ("part", "chapter", "section", "subsection", "subsubsection", "paragraph", "subparagraph")})
        # 编译区内的 section 清单
        if "编译区" in name:
            print("    -- 编译区 section --")
            for i, l in enumerate(seg, 1):
                if re.match(r"^\s*\\section\*?\s*\{", l):
                    print("      L%-6d %s" % (i + doc_ln - 1, l.strip()[:76]))
    print()
