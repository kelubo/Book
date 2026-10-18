# -*- coding: utf-8 -*-
"""r37 插入点上下文抽查 + 笔误基线对比"""
import io, os
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'

bk = io.open(os.path.join(BASE, 'book.tex'), encoding='utf-8', newline='').read()
bl = bk.split('\r\n')
ma = io.open(os.path.join(BASE, 'male.tex'), encoding='utf-8', newline='').read()
ml = ma.split('\r\n')

print('=== book: 新《男性的性反应》上下文（定位）===')
for i, ln in enumerate(bl):
    if ln.strip() == '\\subsection{男性的性反应}':
        st = max(0, i-2)
        print('... (L%d 起) ...' % (i+1))
        for j in range(st, min(i+5, len(bl))):
            print(j+1, bl[j][:80])
        break

print()
print('=== book: 消退期 subsubsection 之后应衔接高潮差距 section ===')
for i, ln in enumerate(bl):
    if ln.strip() == '\\section{高潮差距（Orgasm Gap）——性别愉悦不平等现象}':
        for j in range(max(0, i-8), i+2):
            print(j+1, bl[j][:80])
        break

print()
print('=== male: 消退期上下文（高潮期 -> 消退期 -> 传统中医）===')
for i, ln in enumerate(ml):
    if ln.strip() == '\\subsection{消退期}':
        for j in range(max(0, i-6), min(i+8, len(ml))):
            print(j+1, ml[j][:80])
        break

print()
print('=== 笔误扫描（ect 基线 4 处 / 双反斜杠）===')
import re
for name, txt, lines in [('book', bk, bl), ('female', None, None), ('male', ma, ml)]:
    if txt is None:
        txt = io.open(os.path.join(BASE, name + '.tex'), encoding='utf-8', newline='').read()
        lines = txt.split('\r\n')
    ect = [(i+1, l.strip()[:50]) for i, l in enumerate(lines) if re.match(r'\\ection\{', l)]
    dbl = sum(1 for l in lines if re.search(r'\\\\(?:textbf|textit|item|begin|end|noindent|section|subsection|subsubsection|par\b|title|emph|underline|chapter|tcolorbox)', l))
    print(name, 'ection{ lines =', len(ect), ect, ' double-backslash-suspect =', dbl)

print()
print('=== 新块内英文残留检查（应只有数字/无意外英文）===')
for blk in ['_r37_blk_book.tex', '_r37_blk_male.tex']:
    t = io.open(os.path.join(BASE, blk), encoding='utf-8', newline='').read()
    en = re.findall(r'[A-Za-z]{3,}', t)
    print(blk, 'english tokens =', sorted(set(en)))
