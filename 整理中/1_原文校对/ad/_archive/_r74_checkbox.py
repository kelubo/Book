# -*- coding: utf-8 -*-
"""r74 独立校验器：扫描已写入骨架区的 tcolorbox 起始行，确认参数合法。
用途：在继续批量写盘的过程中，随时防止 colbacktitle 类污染再次混入。
"""
import re

p = 'book.tex'
raw = open(p, 'r', encoding='utf-8', newline='').read()
lines = raw.split('\n')

# 骨架区 = 到 \part{old} 为止
old = next(i for i, l in enumerate(lines) if l.startswith('\\part{old}'))
skel = lines[:old]

bad = []
for i, l in enumerate(skel):
    if '\\begin{tcolorbox}' in l:
        # 允许的参数键
        args = l[l.find('[') + 1:l.rfind(']')] if '[' in l else ''
        for key in re.findall(r'([a-zA-Z]+)=', args):
            if key not in ('colback', 'colframe', 'colbacktitle', 'coltitle', 'title', 'fonttitle'):
                bad.append((i + 1, key, l.strip()[:100]))

print('骨架区 tcolorbox 总数 =', sum(1 for l in skel if '\\begin{tcolorbox}' in l))
print('参数键异常 =', len(bad))
for b in bad:
    print(' ', b)
