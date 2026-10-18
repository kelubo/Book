# -*- coding: utf-8 -*-
"""r74 槽位状态体检：对重名小节，逐处报告"是否已有正文"，用于确定该补哪一处。"""

import re

P = "book.tex"
raw = open(P, "r", encoding="utf-8", newline="").read()
lines = raw.split("\n")
old = next(i for i, l in enumerate(lines) if l.startswith("\\part{old}"))

H = re.compile(r"^\\(part|chapter|section|subsection)\*?\{(.*)\}\s*(%.*)?$")

# 收集章节上下文
ctx = []           # (kind, title)
info = []          # (kind, title, lineno) 按出现顺序
for i in range(old):
    m = H.match(lines[i])
    if m:
        info.append((m.group(1), m.group(2).strip(), i + 1))

# 每个 subsection 的行号 -> 所属章
def owner(ln):
    ch = sec = ""
    for kind, t, l2 in info:
        if l2 > ln:
            break
        if kind == "chapter":
            ch = t
        elif kind == "section":
            sec = t
    return ch, sec


def has_body(ln):
    """锚行之后跳过空行/注释，遇非空非注释行 => 已有正文。"""
    j = ln
    while j < old and (not lines[j].strip() or lines[j].strip().startswith("%")):
        j += 1
    return j < old and not lines[j].startswith("\\")


TARGETS = ["病原体与传播途径", "并发症", "诊断与治疗", "传播途径",
           "病原体与传播", "常见误区辨析", "精液过敏",
           "对男性勃起的影响", "对女性性功能的影响",
           "常见问题", "促进策略", "性别认同的发展", "性传播感染风险"]

for t in TARGETS:
    print("### %s" % t)
    for kind, t2, ln in info:
        if kind == "subsection" and t2 == t:
            ch, sec = owner(ln)
            print("    L%-6d %s / %s   %s" % (ln, ch, sec, "已有正文" if has_body(ln) else "空"))
    print()
