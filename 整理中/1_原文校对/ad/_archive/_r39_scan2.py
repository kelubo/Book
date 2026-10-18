# -*- coding: utf-8 -*-
"""r39 补充探测：表格样例 / 最大嵌套深度 / female * 行甄别 / 行内单星"""
import io, os, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
FILES = ['book.tex', 'female.tex', 'male.tex']
raws = {fn: io.open(os.path.join(BASE, fn), encoding='utf-8', newline='').read().split('\r\n') for fn in FILES}

# 1. book 表格 | 行样例（找连续段）
print('=== 1. book | 表格行 ===')
bl = raws['book.tex']
trows = [(i+1, l) for i, l in enumerate(bl) if l.strip().startswith('|')]
print('total =', len(trows))
# 找第一个连续段
seg_start = 0
for k in range(len(trows)-1):
    if trows[k+1][0] - trows[k][0] <= 2 and trows[k+1][0] - trows[k][0] >= 1:
        seg_start = k
        break
a = trows[seg_start][0]
for j in range(max(0, a-3), min(a+14, len(bl))):
    print('%5d %s' % (j+1, bl[j][:80]))
print('...')
print('其他 | 行行号:', [n for n, _ in trows][:40])

# 2. 最大 bullet 嵌套深度 + bullet 缩进分布
print()
print('=== 2. bullet 缩进分布与最大深度 ===')
for fn in FILES:
    ls = raws[fn]
    depths = {}
    maxd = 0
    for l in ls:
        st = l.strip()
        m = re.match(r'^(\s*)[-*]\s+\S', l)
        if m:
            ind = len(m.group(1))
            d = 1 if ind <= 0 else (2 if ind <= 3 else 3)
            if ind >= 8: d = 4
            depths[d] = depths.get(d, 0) + 1
            maxd = max(maxd, d)
    print(fn, 'depth dist =', depths, 'max =', maxd)

# 3. female 行首 * 行全部列出（甄别真 bullet vs 漏%注释树）
print()
print('=== 3. female 行首 * 行（去注释后）===')
fe = raws['female.tex']
for i, l in enumerate(fe):
    st = l.strip()
    if re.match(r'^\*\s+\S', st) and not st.startswith('%'):
        kind = 'TREE(漏%)' if ('├' in st or '└' in st or '│' in st) else 'BULLET'
        print('L%-6d %-10s %s' % (i+1, kind, st[:60]))

# 4. 行内单星对（非行首、非 **）：粗查
print()
print('=== 4. 行内单星斜体嫌疑 ===')
for fn in FILES:
    cnt = 0
    for i, l in enumerate(raws[fn]):
        st = l.strip()
        if st.startswith('%'): continue
        body = re.sub(r'\*\*[^*]*\*\*', '', l)  # 去 bold
        body = re.sub(r'^\s*[-*]\s+', '', body)  # 去 bullet 标记
        if '*' in body:
            cnt += 1
            if cnt <= 8:
                print('%s L%d: %s' % (fn[:3], i+1, body.strip()[:70]))
    print(fn, 'single-star suspect lines =', cnt)
    print()
