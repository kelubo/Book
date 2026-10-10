# -*- coding: utf-8 -*-
"""r74c: 按篇统计无正文小节数，规划分批顺序。只读。
"""
import io, re, sys
sys.stdout.reconfigure(encoding="utf-8")

F = "book.tex"
raw = io.open(F, encoding="utf-8", newline="").read()
lines = raw.replace("\r\n", "\n").split("\n")

H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{(.*)\}\s*(%.*)?$")
LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}

heads = []
for i, l in enumerate(lines):
    m = H.match(l)
    if m:
        heads.append((i, m.group(1), m.group(2)))
OLD = next(i for i, lv, t in heads if lv == "part" and t == "old")

off = set()
d = 0
st = None
for i, l in enumerate(lines):
    s = l.strip()
    if re.match(r"^\\iffalse\b", s):
        if d == 0:
            st = i
        d += 1
    elif s == "\\fi" and d > 0:
        d -= 1
        if d == 0:
            for k in range(st, i + 1):
                off.add(k)

sk = [(i, lv, t) for i, lv, t in heads if i < OLD and i not in off]

def has_body(idx):
    ln, lv, t = sk[idx]
    end = len(lines)
    for j in range(idx + 1, len(sk)):
        if LV[sk[j][1]] <= LV[lv]:
            end = sk[j][0]
            break
    for k in range(ln + 1, end):
        s = lines[k].strip()
        if s and not s.startswith("%"):
            return True
    return False

# 按篇/章归集（stat 那段已废弃，直接走下面精确统计）
out = []

print("%-22s %-38s %5s %5s %6s" % ("篇", "章", "节", "小节", "空小节"))
print("-" * 82)
# 重新精确统计空小节
cur_part = "（前置）"
cur_chap = None
empty = {}
order = []
for idx, (ln, lv, t) in enumerate(sk):
    if lv == "part":
        cur_part = t
    elif lv == "chapter":
        cur_chap = (ln + 1, t)
        order.append((cur_part, cur_chap, 0, 0, 0))
    elif lv == "subsection":
        if order:
            p, c, s, u, e = order[-1]
            e2 = e + (0 if has_body(idx) else 1)
            order[-1] = (p, c, s, u + 1, e2)

cur = None
tot_e = 0
for p, (cln, ct), s, u, e in order:
    tot_e += e
    if p != cur:
        print("\n【%s】" % p)
        cur = p
    flag = "  <<< 全空" if u and e == u else ("  <空%d>" % e if e else "")
    print("  L%-5d %-34s 小节%3d 空%3d%s" % (cln, ct[:34], u, e, flag))

print()
print("=== 空小节合计: %d ===" % tot_e)
print("=== 章数: %d ===" % len(order))
# 完全无正文的章
empty_ch = [(cln, ct, u) for p, (cln, ct), s, u, e in order if u and e == u]
print("=== 全章小节皆空: %d 章 ===" % len(empty_ch))
for cln, ct, u in empty_ch:
    print("   L%-5d %-34s (%d 小节)" % (cln, ct[:34], u))
