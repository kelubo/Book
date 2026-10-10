# -*- coding: utf-8 -*-
"""r77: 分析 book.tex 旧区巨块（part{性爱与亲密关系}）的节/小节结构、体量与重复度。

输出：_r77_bigblock.txt
"""
import io, re, hashlib, collections

H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{(.*)\}\s*$")
LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}

A, B = 53683, 67498  # chapter{性爱技巧与沟通} 起 ~ part{避孕与性健康} 前
lines = [x.rstrip("\r") for x in io.open("book.tex", encoding="utf-8", newline="").read().split("\n")]

toks = []
for i in range(A - 1, min(B, len(lines))):
    m = H.match(lines[i])
    if m:
        toks.append((i, m.group(1), m.group(2).strip()))
toks.append((B, None, None))

def body(i, lvl, nxt):
    """去掉空行、注释、纯结构行后的正文行数与签名。"""
    out = []
    depth = 0
    for j in range(i + 1, nxt):
        s = lines[j].strip()
        if not s or s.startswith("%"):
            continue
        if re.match(r"^\\(begin|end)\{", s):
            continue
        out.append(s)
    return out

print("=== 巨块层级构成 ===")
c = collections.Counter(t[1] for t in toks[:-1])
print(dict(c))

# 只取 section / subsection
rows = []
for k in range(len(toks) - 1):
    i, lvl, t = toks[k]
    nxt = toks[k + 1][0]
    if lvl not in ("section", "subsection"):
        continue
    b = body(i, lvl, nxt)
    sig = hashlib.md5(("\n".join(b[:6])).encode("utf-8")).hexdigest()[:8]
    rows.append((i + 1, lvl, t, nxt - i, len(b), sig))

print("\n=== 全部 section ===")
for ln, lvl, t, n, nb, sig in rows:
    if lvl == "section":
        print("  L%-6d %-46s 跨度 %6d 行，正文 %5d 行" % (ln, t[:46], n, nb))

print("\n=== subsection 按体量排序（前 40） ===")
for ln, lvl, t, n, nb, sig in sorted([r for r in rows if r[1] == "subsection"], key=lambda x: -x[4])[:40]:
    print("  L%-6d %-40s 跨度 %5d  正文 %4d  %s" % (ln, t[:40], n, nb, sig))

print("\n=== subsection 按体量排序（最短 60） ===")
for ln, lvl, t, n, nb, sig in sorted([r for r in rows if r[1] == "subsection"], key=lambda x: x[4])[:60]:
    print("  L%-6d %-40s 跨度 %5d  正文 %4d  %s" % (ln, t[:40], n, nb, sig))

print("\n=== 正文签名重复组（疑似凑数/复制） ===")
g = collections.defaultdict(list)
for ln, lvl, t, n, nb, sig in rows:
    if lvl == "subsection":
        g[sig].append((ln, t, nb))
for sig, items in g.items():
    if len(items) > 1:
        print("  [%s] ×%d" % (sig, len(items)))
        for ln, t, nb in items:
            print("       L%-6d %-40s 正文 %d 行" % (ln, t[:40], nb))
