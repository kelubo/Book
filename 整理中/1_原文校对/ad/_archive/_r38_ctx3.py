# -*- coding: utf-8 -*-
"""r38 探测四：最后一轮甄别（L1387 全文 / 腰痛 / 约会安全结构 / 佩罗尼等）"""
import io, os, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
FILES = ['book.tex', 'female.tex', 'male.tex']
texts = {}
for fn in FILES:
    lines = io.open(os.path.join(BASE, fn), encoding='utf-8', newline='').read().split('\r\n')
    texts[fn] = [(i+1, l) for i, l in enumerate(lines) if not l.strip().startswith('%')]
raw_lines = {}
for fn in FILES:
    raw_lines[fn] = io.open(os.path.join(BASE, fn), encoding='utf-8', newline='').read().split('\r\n')

# 1. book L1387《育儿与夫妻关系》全文（L1387-L1394）
print('===== 1. book 育儿与夫妻关系 全文 =====')
ls = raw_lines['book.tex']
for j in range(1386, 1395):
    print('  %d %s' % (j+1, ls[j][:90]))

# 2. 腰痛/腰酸词面
print()
print('===== 2. 腰痛/腰酸 =====')
for w in ['腰痛', '腰酸', '腰疼']:
    for fn in FILES:
        for n, l in texts[fn]:
            if w in l:
                print('  [%s] %s L%d: %s' % (w, fn[:3], n, l.strip()[:70]))

# 3. 约会/初次见面安全既有结构（强暴/约会强奸相关节标题已做过 r32——确认"约会"）
print()
print('===== 3. 约会 词面 =====')
for fn in FILES:
    for n, l in texts[fn]:
        if '约会' in l:
            print('  %s L%d: %s' % (fn[:3], n, l.strip()[:70]))

# 4. 佩罗尼 / 阴茎弯曲
print()
print('===== 4. 佩罗尼/阴茎弯曲 =====')
for w in ['佩罗尼', '阴茎弯曲', 'Peyronie', '硬结']:
    for fn in FILES:
        for n, l in texts[fn]:
            if w in l:
                print('  [%s] %s L%d: %s' % (w, fn[:3], n, l.strip()[:70]))

# 5. 痔疮 / 便秘
print()
print('===== 5. 痔疮/便秘 =====')
for w in ['痔疮', '便秘']:
    row = []
    for fn in FILES:
        hits = [n for n, l in texts[fn] if w in l]
        row.append('%s:%d' % (fn[:3], len(hits)))
    print('  %-6s %s' % (w, '  '.join(row)))

# 6. 性爱时长/多久
print()
print('===== 6. 时长预期 =====')
for w in ['多久', '持续时间', '时间太短']:
    row = []
    for fn in FILES:
        hits = [n for n, l in texts[fn] if w in l]
        row.append('%s:%d' % (fn[:3], len(hits)))
    print('  %-8s %s' % (w, '  '.join(row)))

# 7. 双职工/加班/通勤 与性
print()
print('===== 7. 工作节奏词面 =====')
for w in ['加班', '通勤', '倒班', '出差', '工作压力']:
    row = []
    for fn in FILES:
        hits = [n for n, l in texts[fn] if w in l]
        row.append('%s:%d' % (fn[:3], len(hits)))
    print('  %-8s %s' % (w, '  '.join(row)))
