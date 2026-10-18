# -*- coding: utf-8 -*-
"""第三十轮插入：1 处（book，before 型，CRLF，幂等）"""
import io

CR = '\r\n'

fname = 'book.tex'
anchor = r'\subsubsection{新兴数字性文化术语的社会影响}'
blk = '_r30_blk1.tex'
ikey = r'\subsubsection{偶遇性行为（一夜情 / 419）'

text = io.open(fname, encoding='utf-8', newline='').read()
core = io.open(blk, encoding='utf-8', newline='').read()
core = core.replace('\r\n', '\n').replace('\n', CR).rstrip(CR)

if ikey in text:
    print('SKIP (idempotent):', ikey)
else:
    if text.count(anchor) != 1:
        raise SystemExit('ANCHOR FAIL (%d): %s' % (text.count(anchor), anchor))
    new = text.replace(anchor, core + CR + CR + anchor, 1)
    io.open(fname, 'w', encoding='utf-8', newline='').write(new)
    print('OK:', fname, '<-', blk, '( before', anchor[:40], ')')

print('done')
