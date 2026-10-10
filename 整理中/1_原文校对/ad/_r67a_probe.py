# -*- coding: utf-8 -*-
"""r67 前置探测：book.tex 当前状态、骨架边界、篇/章/节骨架。"""
import io, os, re, time

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
P = os.path.join(BASE, "book.tex")

st = os.stat(P)
print("mtime", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime)), "size", st.st_size)
b = io.open(P, "rb").read()
print("CRLF", b.count(b"\r\n"), "裸LF", b.count(b"\n") - b.count(b"\r\n"))
lines = b.decode("utf-8", errors="replace").replace("\r\n", "\n").split("\n")
N = len(lines)
print("总行数", N)
print()

H = re.compile(r"^[ \t]*\\(part|chapter|section|subsection|subsubsection)\*?\{")
LVN = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}


def gt(s):
    r = s[s.index("{"):]
    d = 0
    for j, c in enumerate(r):
        if c == "{":
            d += 1
        elif c == "}":
            d -= 1
            if d == 0:
                return r[1:j]
    return r[1:]


T = []
for i, l in enumerate(lines):
    s = l.strip()
    if not s or s.startswith("%"):
        continue
    m = H.match(s)
    if m:
        T.append((i + 1, m.group(1), gt(s)))

print("=== part 列表（按层级=part 的一级标题，含前后各 1 行上下文）===")
for i, l in enumerate(lines):
    s = l.strip()
    if s.startswith("\\part"):
        print("L%6d| %s" % (i + 1, s[:80]))
print()

print("=== matter / toc / appendix ===")
for key in ("\\frontmatter", "\\mainmatter", "\\backmatter", "\\tableofcontents", "\\appendix"):
    hits = [i + 1 for i, l in enumerate(lines) if l.strip() == key]
    print("%-18s %s" % (key, hits))
print()

OLD = None
for ln, lv, t in T:
    if lv == "part" and t in ("old", "旧内容"):
        OLD = ln
        break
print("旧区起点 L%d；骨架区 = L1..L%d" % (OLD, OLD - 1))
print()

ENDMAP = {}
for k, (ln, lv, t) in enumerate(T):
    lvl = LVN[lv]
    e = N + 1
    for ln2, lv2, _ in T[k + 1:]:
        if LVN[lv2] <= lvl:
            e = ln2
            break
    ENDMAP[ln] = e


def count_body(ln, e):
    return sum(1 for x in lines[ln:e - 1] if x.strip() and not x.strip().startswith("%"))


print("=== 骨架区逐章骨架 ===")
for ln, lv, t in T:
    if ln >= OLD:
        break
    if lv == "part":
        e = ENDMAP[ln]
        nch = sum(1 for l2, v2, _ in T if l2 >= ln and l2 < e and v2 == "chapter")
        print("\n【L%d %s】章数=%d 区块=%d行" % (ln, t, nch, e - ln))
    elif lv in ("chapter", "section"):
        e = ENDMAP[ln]
        ind = "  " if lv == "chapter" else "      "
        print("%sL%5d %-9s %-44s body=%d" % (ind, ln, lv, t[:44], count_body(ln, e)))
