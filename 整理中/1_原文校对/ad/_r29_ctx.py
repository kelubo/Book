# -*- coding: utf-8 -*-
"""r29 核查：空巢/婚内强奸/费洛蒙/复通/割礼/丁克 上下文与既有节"""
import io, re

BASE = r'D:/Git/Book/整理中/1_原文校对/ad/'
raws = {f: io.open(BASE + f, encoding='utf-8').read() for f in ['book.tex', 'female.tex', 'male.tex']}

for f, t in raws.items():
    lines = t.split('\n')
    for kw in ['空巢', '婚内强奸', '费洛蒙', '复通', '割礼', '丁克', '二度蜜月', '蜜月']:
        hits = [(i + 1, ln.strip()) for i, ln in enumerate(lines) if kw in ln]
        if hits:
            print('--- %s [%s] %d' % (f, kw, len(hits)))
            for i, s in hits[:10]:
                print('  L%-6d %s' % (i, s[:115]))
print()

# 退休 16 处分布（是否覆盖空巢话题）
print('=== book [退休] 16 hits ===')
lines = raws['book.tex'].split('\n')
for i, ln in enumerate(lines):
    if '退休' in ln:
        print('  L%-6d %s' % (i + 1, ln.strip()[:110]))
print()
# 标题：婚姻/家庭/生命周期/绝育/结扎
print('=== book 标题（婚姻/家庭/生命周期/绝育/结扎/气味/信息素） ===')
for i, ln in enumerate(lines):
    s = ln.strip()
    if re.match(r'\\(chapter|section|subsection|subsubsection)\{', s) and re.search(
            r'婚姻|家庭|生命周期|绝育|结扎|气味|信息素|退休|老年|长期|长期关系|激情', s):
        print('L%-6d %s' % (i + 1, s[:100]))
