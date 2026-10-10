# -*- coding: utf-8 -*-
"""r28 三轮核查：阴吹/子宫后位/chemsex/贫血/约会软件/正念"""
import io, re

BASE = r'D:/Git/Book/整理中/1_原文校对/ad/'
raws = {f: io.open(BASE + f, encoding='utf-8').read() for f in ['book.tex', 'female.tex', 'male.tex']}

# 阴吹 / 子宫后位 / 约会软件 / chemsex / GHB 命中行
for f, t in raws.items():
    lines = t.split('\n')
    for kw in ['阴吹', '子宫后位', '约会软件', 'chemsex', 'GHB', '正念', '缺铁']:
        hits = [(i + 1, ln.strip()) for i, ln in enumerate(lines) if kw in ln]
        if hits:
            print('--- %s [%s] %d' % (f, kw, len(hits)))
            for i, s in hits[:12]:
                print('  L%-6d %s' % (i, s[:115]))
print()

# male 娱乐性药物节全文
lines = raws['male.tex'].split('\n')
print('=== male L3739-3775 娱乐性药物节 ===')
for i in range(3738, 3776):
    print('L%-6d %s' % (i + 1, lines[i].rstrip()[:125]))

# female 贫血命中行
print()
print('=== female [贫血] 30 hits ===')
lines = raws['female.tex'].split('\n')
for i, ln in enumerate(lines):
    if '贫血' in ln:
        print('  L%-6d %s' % (i + 1, ln.strip()[:110]))
