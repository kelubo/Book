# -*- coding: utf-8 -*-
"""检查 _r67_preview.txt 的骨架：各篇章数/节数。"""
import io, re

s = io.open(r"D:\Git\Book\整理中\1_原文校对\ad\_r67_preview.txt", encoding="utf-8").read().split("\n")
cur = None
cnt = {}
order = []
for l in s:
    t = l.strip()
    if not t or t.startswith("%"):
        continue
    if t.startswith("\\part"):
        cur = t[6:-1] if t.endswith("}") else t
        if cur not in cnt:
            cnt[cur] = {"ch": 0, "sec": 0}
            order.append(cur)
        continue
    m = re.match(r"^\\chapter\{(.*)\}$", t)
    if m and cur:
        cnt[cur]["ch"] += 1
        continue
    m = re.match(r"^\\section\{(.*)\}$", t)
    if m and cur:
        cnt[cur]["sec"] += 1

tc = ts = 0
for k in order:
    v = cnt[k]
    print("  %-24s 章 %2d   节 %3d" % (k[:24], v["ch"], v["sec"]))
    tc += v["ch"]
    ts += v["sec"]
print("  合计：章 %d / 节 %d" % (tc, ts))
print()
print("=== 前 60 行（说明注释 + 前言区）===")
for i in range(104, 150):
    print("L%4d| %s" % (i + 1, s[i][:96]))
