# -*- coding: utf-8 -*-
"""第二十五轮插入：3 处（book 2 + female 1，before 型，CRLF，幂等）"""
import io

CR = '\r\n'

JOBS = [
    ('book.tex',
     r'\section{避孕方法总览}',
     '_r25_blk1.tex', 'before', r'\section{备孕期间的性生活'),
    ('book.tex',
     r'\subsection{实现性健康的行动框架}',
     '_r25_blk2.tex', 'before', r'\subsection{规律性生活的健康获益'),
    ('female.tex',
     r'\subsection{宫颈锥切术（LEEP / 冷刀）}',
     '_r25_blk3.tex', 'before', r'\subsection{流产后的心理调适'),
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
    print('OK:', fname, '<-', blk, '(', mode, anchor[:34], ')')

print('done')
