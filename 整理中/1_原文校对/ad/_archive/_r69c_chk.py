# -*- coding: utf-8 -*-
"""r69c：预览版骨架统计（供人工检查）"""
import io, re

s = io.open(r"D:\Git\Book\整理中\1_原文校对\ad\_r69_preview.txt", encoding="utf-8").read().split("\n")
H = re.compile(r"^\\(part|chapter|section|subsection)\*?\{")
LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3}


def gt(x):
    r = x[x.index("{"):]
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
for i, l in enumerate(s):
    t = l.strip()
    if not t or t.startswith("%"):
        continue
    m = H.match(t)
    if m:
        T.append((i + 1, m.group(1), gt(t)))
OLD = next(i for i, lv, t in T if lv == "part" and t == "old")
print("旧区起点 L%d（原 L1349）" % OLD)
cur = "（前置）"
st = {"（前置）": {"line": 0, "ch": 0, "sec": 0, "sub": 0}}
order = ["（前置）"]
for i, lv, t in T:
    if i >= OLD:
        break
    if lv == "part":
        cur = t
        st[cur] = {"line": i, "ch": 0, "sec": 0, "sub": 0}
        order.append(cur)
    elif lv == "chapter":
        st[cur]["ch"] += 1
    elif lv == "section":
        st[cur]["sec"] += 1
    elif lv == "subsection":
        st[cur]["sub"] += 1
print("%-24s %4s %4s %5s" % ("篇", "章", "节", "小节"))
tc = ts = tu = 0
for k in order:
    v = st[k]
    print("%-24s %4d %4d %5d   (L%d)" % (k[:24], v["ch"], v["sec"], v["sub"], v["line"]))
    tc += v["ch"]
    ts += v["sec"]
    tu += v["sub"]
print("%-24s %4d %4d %5d" % ("合计", tc, ts, tu))

print()
print("零节章：")
cur = None
last = None
for i, lv, t in T:
    if i >= OLD:
        break
    if lv == "part":
        cur = t
    if lv == "chapter":
        last = (i, t)
    if lv == "section" and last:
        last = None
if last:
    print("   ", last)

print()
print("=== 新增章定位 ===")
for i, lv, t in T:
    if lv == "chapter" and t in ("性发育与青春期", "家庭形态的多样性", "精神健康与性",
                                 "性治疗与性康复", "性健康前沿研究", "暴力、安全与保护", "性与公共卫生"):
        print("   L%-5d %s" % (i, t))
print()
print("=== 重名节检查 ===")
import collections
nm = collections.defaultdict(list)
cur = None
for i, lv, t in T:
    if i >= OLD:
        break
    if lv == "chapter":
        cur = t
    if lv in ("section", "subsection"):
        nm[t].append((cur, i, lv))
dup = {k: v for k, v in nm.items() if len(v) > 1}
print("重名节/小节：", len(dup))
for k, v in sorted(dup.items(), key=lambda x: -len(x[1]))[:20]:
    print("   %-34s x%d  %s" % (k[:34], len(v), [(a, b) for a, b, c in v]))
