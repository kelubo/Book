# -*- coding: utf-8 -*-
"""r71c：dump 停用新框架的 篇/章/节 结构 + 编译区完整 outline。只读。"""
import re

TITLE = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection)\*?\s*\{")


def tname(ln):
    m = TITLE.match(ln)
    if not m:
        return None, None
    cmd = m.group(1)
    s = ln[m.end():]
    depth, buf, i = 1, [], 0
    while i < len(s) and depth:
        c = s[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                break
        buf.append(c)
        i += 1
    return cmd, "".join(buf).strip()


for fn, doc_ln in (("female.tex", 6417), ("male.tex", 5745)):
    lines = open(fn, encoding="utf-8").read().split("\n")
    print("=" * 72)
    print(fn, "—— 停用新框架结构（篇/章/节）")
    for i in range(doc_ln - 1):
        cmd, name = tname(lines[i])
        if cmd in ("part", "chapter", "section"):
            print("  L%-6d %-8s %s" % (i + 1, cmd, name))
    print()
    print(fn, "—— 编译区 outline（章/节/小节）")
    for i in range(doc_ln - 1, len(lines)):
        cmd, name = tname(lines[i])
        if cmd in ("chapter", "section", "subsection"):
            print("  L%-6d %-10s %s" % (i + 1, cmd, name))
    print()
