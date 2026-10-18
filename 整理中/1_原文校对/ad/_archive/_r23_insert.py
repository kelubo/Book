# -*- coding: utf-8 -*-
"""第二十三轮插入：4 处（均 before 型，CRLF 处理，幂等判重）"""
import io

CR = '\r\n'

JOBS = [
    # (file, anchor, block, mode, idempotent-key)
    ('book.tex',
     r'\section{肠道菌群-脑-性轴（Gut-Brain-Sex Axis）}',
     '_r23_blk1.tex', 'before', r'\subsection{甲状腺功能异常与性欲'),
    ('book.tex',
     r'\subsubsection{口交的沟通与边界}',
     '_r23_blk2.tex', 'before', r'\subsubsection{口交中的射精、吞咽与精液安全}'),
    ('book.tex',
     r'\section{性、爱与承诺}',
     '_r23_blk3.tex', 'before', r'\section{周末夫妻与两地分居'),
    ('book.tex',
     r'\subsection{长期关系中的性}',
     '_r23_blk4.tex', 'before', r'\subsection{新婚之夜与初夜'),
]

for fname, anchor, blk, mode, ikey in JOBS:
    path = fname
    text = io.open(path, encoding='utf-8', newline='').read()
    core = io.open(blk, encoding='utf-8', newline='').read()
    core = core.replace('\r\n', '\n').replace('\n', CR)
    core = core.rstrip(CR)  # 去尾部空行，统一由下面拼装

    if ikey in text:
        print('SKIP (idempotent):', fname, ikey)
        continue

    if text.count(anchor) != 1:
        raise SystemExit('ANCHOR FAIL (%d hits): %s | %s' % (text.count(anchor), fname, anchor))

    if mode == 'before':
        new = text.replace(anchor, core + CR + CR + anchor, 1)
    else:  # after
        new = text.replace(anchor, anchor + CR + CR + core + CR, 1)

    io.open(path, 'w', encoding='utf-8', newline='').write(new)
    print('OK:', fname, '<-', blk, '(', mode, anchor[:30], ')')

print('done')
