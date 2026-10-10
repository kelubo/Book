# -*- coding: utf-8 -*-
"""r68a：探测 book.tex 当前骨架全貌（part / chapter / section），并定位旧区边界。"""
import io, os, re, time

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
P = os.path.join(BASE, "book.tex")

st = os.stat(P)
print("mtime", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime)), "size", st.st_size)
raw = io.open(P, "rb").read()
print("CRLF", raw.count(b"\r\n"), "裸LF", raw.count(b"\n") - raw.count(b"\r\n"))
lines = raw.decode("utf-8", errors="replace").replace("\r\n", "\n").split("\n")
N = len(lines)
print("总行数", N)

H = re.compile(r"^\s*\\(part|chapter|section|subsection)\*?\{")
LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3}


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

OLD = None
for ln, lv, t in T:
    if lv == "part" and t == "old":
        OLD = ln
        break
print("旧区 \\part{old} 行号:", OLD)

# 其它顶层标记
for key in ["\\frontmatter", "\\mainmatter", "\\backmatter", "\\appendix", "\\tableofcontents"]:
    print(key, [i + 1 for i, l in enumerate(lines) if l.strip() == key])

print()
print("=" * 78)
print("骨架区（\\part{old} 之前）完整结构")
print("=" * 78)

cur_part = cur_ch = None
pch = {}
nch = nsec = 0
for ln, lv, t in T:
    if OLD is not None and ln >= OLD:
        break
    if lv == "part":
        cur_part = t
        pch.setdefault(t, {"ch": [], "sec": 0, "line": ln})
        print()
        print("## 篇 L%-5d %s" % (ln, t))
    elif lv == "chapter":
        cur_ch = t
        nch += 1
        if cur_part:
            pch[cur_part]["ch"].append((ln, t))
        print("   L%-5d 章 %s" % (ln, t))
    elif lv == "section":
        nsec += 1
        if cur_part:
            pch[cur_part]["sec"] += 1
        print("        L%-5d 节 %s" % (ln, t))
    else:
        print("             L%-5d 小节 %s" % (ln, t))

print()
print("=" * 78)
print("统计")
print("=" * 78)
tc = ts = 0
for k, v in pch.items():
    print("  %-24s 章 %2d  节 %3d  (L%d)" % (k[:24], len(v["ch"]), v["sec"], v["line"]))
    tc += len(v["ch"])
    ts += v["sec"]
print("  合计：篇 %d / 章 %d / 节 %d" % (len(pch), tc, ts))

print()
print("旧区（L%d 起）part 列表：" % OLD)
for ln, lv, t in T:
    if OLD is not None and ln >= OLD and lv == "part":
        e = None
        cnt = 0
        for ln2, lv2, _ in T:
            if ln2 > ln and lv2 == "chapter":
                cnt += 1
        print("   L%-6d %s" % (ln, t))
