# -*- coding: utf-8 -*-
"""第二十六轮插入：3 处（book 2 + female 1，before 型，CRLF，幂等）"""
import io

CR = '\r\n'

JOBS = [
    ('female.tex',
     r'\subsection{辅助生殖技术的风险与并发症}',
     '_r26_blk1.tex', 'before', r'\subsection{辅助生殖各阶段的性生活指引'),
    ('book.tex',
     r'\subsection{可用的支持资源}',
     '_r26_blk2.tex', 'before', r'\subsection{失独家庭：当亲密被巨大的丧失冻结'),
    ('book.tex',
     r'\subsection{肝病（Hepatic Disease）与性生活}',
     '_r26_blk3.tex', 'before', r'\subsection{器官移植受者的性生活'),
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
