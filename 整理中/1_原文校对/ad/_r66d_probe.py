# -*- coding: utf-8 -*-
"""r66d：核实 0 来源章的可得性 + 修正锚解析（多候选时列出全部）。"""
import io, re, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
raw = io.open(BASE + r"\book.tex", encoding="utf-8", newline="").read().replace("\r\n", "\n")
lines = raw.split("\n")
N = len(lines)
H = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection)\*?\{")


def get_title(s):
    rest = s[s.index("{"):]
    d = 0
    for j, ch in enumerate(rest):
        if ch == "{":
            d += 1
        elif ch == "}":
            d -= 1
            if d == 0:
                return rest[1:j]
    return rest[1:]


titles = []
for i, l in enumerate(lines):
    s = l.strip()
    if s.startswith("%"):
        continue
    m = H.match(s)
    if m:
        titles.append((i + 1, m.group(1), get_title(s)))

OLD = next(i + 1 for i, l in enumerate(lines) if l.strip() == "\\part{old}")

print("1) 「性别社会学 / 女权主义」相关词的全文命中（含旧区，排除骨架 L<%d）" % OLD)
for kw in ["社会学", "女权", "平权", "性别平等", "刻板印象", "性别角色", "性别社会化",
           "家务分工", "职场性别", "交叉性", "社会性别", "男性运动", "父权"]:
    hit = [(ln, lv, t) for ln, lv, t in titles if kw in t and ln >= OLD]
    print("   「%-8s」旧区 %d 条" % (kw, len(hit)))
    for ln, lv, t in hit[:5]:
        print("        L%-6d %-10s %s" % (ln, lv, t[:50]))

print()
print("2) 「依恋 / 爱情 / 择偶」相关词在旧区的命中")
for kw in ["依恋", "爱情", "择偶", "吸引", "亲密关系", "关系维护"]:
    hit = [(ln, lv, t) for ln, lv, t in titles if kw in t and ln >= OLD]
    print("   「%-8s」旧区 %d 条" % (kw, len(hit)))
    for ln, lv, t in hit[:8]:
        print("        L%-6d %-10s %s" % (ln, lv, t[:50]))

print()
print("3) 「结语」章 / 「走向更平等」在全文的命中")
for kw in ["走向更平等", "结语"]:
    hit = [(ln, lv, t) for ln, lv, t in titles if kw in t]
    print("   「%s」全文 %d 条" % (kw, len(hit)))
    for ln, lv, t in hit[:10]:
        print("        L%-6d %-10s %s %s" % (ln, lv, t[:44], "【骨架前】" if ln < OLD else ""))

print()
print("4) 「性取向与性别认同」章（骨架 L331）的目的地候选")
for ln, lv, t in titles:
    if ln >= OLD and ("性取向" in t or "性别认同" in t) and lv in ("chapter", "section"):
        print("   L%-6d %-9s %s" % (ln, lv, t[:56]))
