# -*- coding: utf-8 -*-
"""r38 探测三：剩余候选的最后一轮甄别"""
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

def near(fn, ln, span=6, width=80):
    print('    [context %s L%d]' % (fn, ln))
    ls = raw_lines[fn]
    for j in range(max(0, ln-1-span), min(ln+span, len(ls))):
        print('      %d %s' % (j+1, ls[j].strip()[:width]))

# 1. 育儿与夫妻关系 section 的结构（到下一个 section）
print('===== 1. book L1387 育儿与夫妻关系 结构 =====')
ls = raw_lines['book.tex']
for j in range(1386, 1480):
    st = ls[j].strip()
    m = re.match(r'\\(section|subsection|subsubsection)\{', st)
    if m:
        print('  L%d %s' % (j+1, st[:60]))

# 2. 异地恋 4 处形态
print()
print('===== 2. 异地恋 =====')
for n, l in texts['book.tex']:
    if '异地恋' in l:
        print('  L%d: %s' % (n, l.strip()[:75]))

# 3. 养老院 / 临终关怀 / 护理机构
print()
print('===== 3. 养老院/临终关怀/长期照护 =====')
for w in ['养老院', '临终关怀', '养老机构', '护理院', '养老', '照护机构']:
    for fn in FILES:
        for n, l in texts[fn]:
            if w in l:
                print('  [%s] %s L%d: %s' % (w, fn[:3], n, l.strip()[:70]))

# 4. 骨折形态（抽 4 条）
print()
print('===== 4. 骨折 抽样 =====')
cnt = 0
for fn in FILES:
    for n, l in texts[fn]:
        if '骨折' in l and cnt < 6:
            print('  %s L%d: %s' % (fn[:3], n, l.strip()[:70]))
            cnt += 1

# 5. 新词面：造口 / 乳房切除 / 前列腺癌 / 围手术期 / 住院
print()
print('===== 5. 医疗场景词面 =====')
for w in ['造口', '乳房切除', '前列腺癌', '手术', '住院', '化疗']:
    row = []
    for fn in FILES:
        hits = [n for n, l in texts[fn] if w in l]
        row.append('%s:%d' % (fn[:3], len(hits)))
    print('  %-8s %s' % (w, '  '.join(row)))

# 6. 润滑剂/安全套材质
print()
print('===== 6. 润滑剂/安全套材质 =====')
for w in ['润滑剂', '聚氨酯', '硅性', '水性润滑', '油性润滑']:
    row = []
    for fn in FILES:
        hits = [n for n, l in texts[fn] if w in l]
        row.append('%s:%d' % (fn[:3], len(hits)))
    print('  %-8s %s' % (w, '  '.join(row)))

# 7. 数字亲密新词面确认（远程/视频/线上）
print()
print('===== 7. 远程/线上亲密 =====')
for w in ['远程', '线上', '视频', '网恋', '屏幕']:
    row = []
    for fn in FILES:
        hits = [n for n, l in texts[fn] if w in l]
        row.append('%s:%d' % (fn[:3], len(hits)))
    print('  %-8s %s' % (w, '  '.join(row)))
