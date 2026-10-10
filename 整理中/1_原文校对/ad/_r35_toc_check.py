# -*- coding: utf-8 -*-
import io, re, os
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
p = os.path.join(BASE, '_全书导览_三卷目录总览_2026-09-10.md')
lines = io.open(p, encoding='utf-8').read().split('\n')
star_lines = [l for l in lines if '★' in l]
print('含★行合计:', len(star_lines))
print('  其中头部说明行:', len([l for l in star_lines if l.startswith('>') or l.startswith('#')]))
ent = [l for l in star_lines if not l.startswith('>') and not l.startswith('#')]
print('  实体★行:', len(ent))
print('  实体★行中章级(**) :', len([l for l in ent if l.startswith('**')]))
print()
print('== 本轮 4 节标星核验 ==')
for k in ['背叛创伤', '修复或不修复', '绳缚的神经与循环安全', '灌肠的安全边界']:
    hit = [l for l in lines if k in l]
    for h in hit:
        print(repr(h[:98]))
print()
print('== 实体★行中的子节/小节级清单（最近 20 条，用于查异常）==')
for l in ent[-20:]:
    print('   ', l[:96])
print()
# 重名双行检查（同一标题出现两行且都带★）
titles = {}
for l in ent:
    m = re.match(r'^[　\*\s]*\d+｜(.+?)★\s*$', l)
    if m:
        titles.setdefault(m.group(1).strip(), 0)
        titles[m.group(1).strip()] += 1
dup = {t: c for t, c in titles.items() if c > 1}
print('带★的重名标题:', dup)
print('去重标题数:', len(titles))
