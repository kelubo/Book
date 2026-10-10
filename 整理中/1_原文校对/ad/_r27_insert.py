# -*- coding: utf-8 -*-
"""第二十七轮插入：2 处（book 2，均为 before 型，CRLF，幂等）"""
import io

CR = '\r\n'

JOBS = [
    ('book.tex',
     r'\section{优生优育与性健康的关系}',
     '_r27_blk1.tex', 'before', r'\subsection{辅助生殖期间的性生活：常见疑问速答}'),
    ('book.tex',
     r'\section{微塑料与生殖健康（Microplastics \& Reproductive Health）}',
     '_r27_blk2.tex', 'before', r'\subsection{高原、海拔与性健康}'),
]

for fname, anchor, blk, mode, ikey in JOBS:
    text = io.open(fname, encoding='utf-8', newline='').read()
    core = io.open(blk, encoding='utf-8', newline='').read()
    core = core.replace('\r\n', '\n').replace('\n', CR).rstrip(CR)

    if ikey in text:
        print('SKIP (idempotent):', fname, ikey)
        continue

    if text.count(anchor) != 1:
        raise SystemExit('ANCHOR FAIL (%d): %s | %s' % (text.count(anchor), fname, anchor))

    if mode == 'before':
        new = text.replace(anchor, core + CR + CR + anchor, 1)
    else:
        new = text.replace(anchor, anchor + CR + CR + core + CR, 1)

    io.open(fname, 'w', encoding='utf-8', newline='').write(new)
    print('OK:', fname, '<-', blk, '(', mode, anchor[:40], ')')

print('done')
