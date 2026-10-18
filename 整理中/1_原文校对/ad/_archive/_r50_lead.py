# -*- coding: utf-8 -*-
"""r50b：在迁移注释后补一句过渡语，使上移的两段读作"总述"（纯插入，保留 CRLF）"""
import io, os, shutil, sys

D = 'D:/Git/Book/整理中/1_原文校对/ad/'
SRC = D + 'book.tex'
BK = D + '_backup_r50/'

LEAD = ('四个阶段在两性之间是同构的，差别只在于以哪套器官为中心：'
        '下面两段先说四期共有的规律，随后再分述男性在各期中的具体变化。')

content = io.open(SRC, encoding='utf-8', newline='').read()
eol = '\r\n' if '\r\n' in content else '\n'
lines = content.splitlines(keepends=True)

hit = [i for i, ln in enumerate(lines) if ln.startswith('% —— r50 迁移')]
if len(hit) != 1:
    sys.exit('注释行未唯一命中: %d' % len(hit))
i = hit[0]
if not lines[i + 1].startswith('兴奋期是性反应周期的第一个阶段'):
    sys.exit('注释后一行不是 P1，实际: %r' % lines[i + 1][:50])

if not os.path.exists(BK + 'book_r50b_pre.tex'):
    shutil.copy2(SRC, BK + 'book_r50b_pre.tex')

lines[i + 1:i + 1] = [LEAD + eol, eol]
out = ''.join(lines)
io.open(SRC, 'w', encoding='utf-8', newline='').write(out)

chk = io.open(SRC, encoding='utf-8', newline='').read()
bare = sum(1 for ln in chk.split('\n')[:-1] if not ln.endswith('\r')) if eol == '\r\n' else 0
rec = ['插入位置: L%d 之后' % (i + 1), 'LEAD = ' + LEAD,
       '新行数 = %d（+2）' % len(lines), 'bare LF = %d' % bare]
for j in range(i - 1, i + 6):
    rec.append('  L%-5d %s' % (j + 1, lines[j].rstrip('\r\n')[:80]))
io.open(D + '_r50_lead_out.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(rec))
