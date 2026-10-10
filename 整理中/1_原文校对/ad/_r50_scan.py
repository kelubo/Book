# -*- coding: utf-8 -*-
"""r50：扫描 book.tex《男性的性反应》(L513-551) 中夹杂的女性表述"""
import io, re

D = 'D:/Git/Book/整理中/1_原文校对/ad/'
lines = io.open(D + 'book.tex', encoding='utf-8', newline='').read().split('\n')
out = []

FEM = ['女性', '阴道', '阴蒂', '阴唇', '子宫', '乳房', '乳头', '乳晕', 'G点']
MALE = ['阴茎', '睾丸', '阴囊', '精液', '射精', '勃起', '前列腺', '尿道球腺', '精子']

start, end = 512, 552
out.append('=== 《男性的性反应》节内逐行性别词扫描（L513-L552）===')
for i in range(start, end):
    t = lines[i]
    if not t.strip():
        out.append('L%-5d (空行)' % (i + 1))
        continue
    f = sorted({w for w in FEM if w in t})
    m = sorted({w for w in MALE if w in t})
    if f and not m:
        tag = 'FEM-ONLY'
    elif f and m:
        tag = 'MIXED'
    elif m:
        tag = 'male'
    else:
        tag = 'other'
    out.append('L%-5d [%-9s] F=%s | M=%s' % (i + 1, tag, '/'.join(f) or '-', '/'.join(m) or '-'))
    if tag in ('FEM-ONLY', 'MIXED'):
        out.append('        > ' + t[:220])

out.append('')
out.append('=== L509-560 节内标题 ===')
for i in range(508, 560):
    s = lines[i].strip()
    if re.match(r'\\(sub)*section\{', s):
        out.append('L%d  %s' % (i + 1, s))

out.append('')
out.append('总行数 = %d' % len(lines))
io.open(D + '_r50_scan_out.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
