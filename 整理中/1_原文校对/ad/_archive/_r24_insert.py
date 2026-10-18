# -*- coding: utf-8 -*-
"""第二十四轮插入：5 处（book 4 + female 1，CRLF 处理，唯一性校验，幂等判重）"""
import io

CR = '\r\n'

JOBS = [
    # (file, anchor, block, mode, idempotent-key)
    ('book.tex',
     '\\begin{tcolorbox}[colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]' + CR + '对长期焦虑、表现压力大',
     '_r24_blk1.tex', 'before', r'\subsubsection{进阶：睾丸、会阴的抚触与按摩}'),
    ('book.tex',
     '\\begin{tcolorbox}[colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]' + CR + '床上语言的首要功能不是',
     '_r24_blk2.tex', 'before', r'\subsubsection{三个场景演练'),
    ('book.tex',
     '\\begin{tcolorbox}[colback=blue!5!white,colframe=blue!70!black,title=给家长与教育者]',
     '_r24_blk3.tex', 'before', r'\subsection{给家长：分龄谈性与就医陪伴的要点}'),
    ('book.tex',
     '把这些反应当作"需要了解的身体信息"，而不是"羞于启齿的秘密"。' + CR + '\\end{tcolorbox}',
     '_r24_blk4.tex', 'after', r'\section{精液过敏：一个常被误诊的"怪病"}'),
    ('female.tex',
     '\\subsection{性唤起障碍}',
     '_r24_blk5.tex', 'before', r'\subsection{围绝经期性欲：变化规律与主动应对}'),
]

for fname, anchor, blk, mode, ikey in JOBS:
    text = io.open(fname, encoding='utf-8', newline='').read()
    core = io.open(blk, encoding='utf-8', newline='').read()
    core = core.replace('\r\n', '\n').replace('\n', CR).rstrip(CR)

    if ikey in text:
        print('SKIP (idempotent):', fname, ikey)
        continue

    if text.count(anchor) != 1:
        raise SystemExit('ANCHOR FAIL (%d hits): %s | %s' % (text.count(anchor), fname, anchor[:40]))

    if mode == 'before':
        new = text.replace(anchor, core + CR + CR + anchor, 1)
    else:
        new = text.replace(anchor, anchor + CR + CR + core, 1)

    io.open(fname, 'w', encoding='utf-8', newline='').write(new)
    print('OK:', fname, '<-', blk, '(', mode, anchor[:30].replace(CR, '|'), ')')

print('done')
