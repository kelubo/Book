# -*- coding: utf-8 -*-
"""r51b：修正 r50 过渡语的"下面两段"（现已是四段），保留 CRLF"""
import io, os, shutil

D = 'D:/Git/Book/整理中/1_原文校对/ad/'
SRC = D + 'book.tex'
BK = D + '_backup_r51/'

OLD = '下面两段先说四期共有的规律，随后再分述男性在各期中的具体变化。'
NEW = '下面四段先逐期说明四期共有的规律，随后再分述男性在各期中的具体变化。'

content = io.open(SRC, encoding='utf-8', newline='').read()
n = content.count(OLD)
if n != 1:
    raise SystemExit('旧串命中 %d 次（须为 1）' % n)
if not os.path.exists(BK + 'book_r51b_pre.tex'):
    shutil.copy2(SRC, BK + 'book_r51b_pre.tex')

content = content.replace(OLD, NEW)
io.open(SRC, 'w', encoding='utf-8', newline='').write(content)

chk = io.open(SRC, encoding='utf-8', newline='').read()
bare = sum(1 for ln in chk.split('\n')[:-1] if not ln.endswith('\r'))
lines = chk.splitlines()
rec = ['替换 %d 处' % n, '新行数 = %d' % len(lines), 'bare LF = %d' % bare]
for i, ln in enumerate(lines):
    if ln.startswith('四个阶段在两性之间是同构的'):
        rec.append('  L%-5d %s' % (i + 1, ln))
        break
io.open(D + '_r51_fix_out.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(rec))
