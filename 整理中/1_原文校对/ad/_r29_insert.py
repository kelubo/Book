# -*- coding: utf-8 -*-
"""第二十九轮插入：3 处（均 book；blk1/blk2 before 型，blk3 组合锚 before 型，CRLF，幂等）"""
import io

CR = '\r\n'

JOBS = [
    ('book.tex',
     r'\subsection{性侵犯与性暴力的法律应对}',
     '_r29_blk1.tex', 'before', r'\subsection{婚姻内的同意：结婚证不是'),
    ('book.tex',
     r'\subsection{性沟通的高级技巧与练习}',
     '_r29_blk2.tex', 'before', r'\subsection{空巢期的性与亲密'),
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

# ---- blk3：组合锚（注意事项尾行 + 空行 + \section{紧急避孕}） ----
fname = 'book.tex'
combo = ('3. **心理准备**：做好心理准备，接受永久性避孕的事实。' + CR + CR
         + r'\section{紧急避孕}')
blk = '_r29_blk3.tex'
ikey = r'\subsubsection{绝育后悔'

text = io.open(fname, encoding='utf-8', newline='').read()
core = io.open(blk, encoding='utf-8', newline='').read()
core = core.replace('\r\n', '\n').replace('\n', CR).rstrip(CR)

if ikey in text:
    print('SKIP (idempotent):', ikey)
else:
    if text.count(combo) != 1:
        raise SystemExit('COMBO ANCHOR FAIL (%d)' % text.count(combo))
    new = text.replace(combo, '3. **心理准备**：做好心理准备，接受永久性避孕的事实。' + CR + CR
                       + core + CR + CR + r'\section{紧急避孕}', 1)
    io.open(fname, 'w', encoding='utf-8', newline='').write(new)
    print('OK:', fname, '<-', blk, '( combo-before 尾行+section )')

print('done')
