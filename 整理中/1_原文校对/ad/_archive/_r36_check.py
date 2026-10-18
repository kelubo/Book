# -*- coding: utf-8 -*-
import io, os, re, collections
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
CR = '\r\n'

for fn in ['book.tex', 'female.tex']:
    new = io.open(os.path.join(BASE, fn), encoding='utf-8', newline='').read()
    old = io.open(os.path.join(BASE, '_backup_r36', fn), encoding='utf-8', newline='').read()
    pat = re.compile(r'\\\\\\\\(?:textbf|textit|item|begin|end|noindent|section|subsection|subsubsection|par|title|emph|underline|chapter|tcolorbox)')
    print('%-11s 双反斜杠笔误: 前=%d 后=%d 增量=%d | 行数 %d -> %d' % (
        fn, len(pat.findall(old)), len(pat.findall(new)), len(pat.findall(new)) - len(pat.findall(old)),
        len(old.split(CR)), len(new.split(CR))))

print()
w = collections.Counter()
blks = ['_r36_blk_d1.tex', '_r36_blk_d2.tex', '_r36_blk_d3.tex', '_r36_blk_e1.tex',
        '_r36_blk_e2.tex', '_r36_blk_e3.tex', '_r36_blk_e4.tex']
for blk in blks:
    t = io.open(os.path.join(BASE, blk), encoding='utf-8', newline='').read()
    body = re.sub(r'\\[A-Za-z]+', ' ', t)
    for x in re.findall(r'[A-Za-z][A-Za-z/-]{2,}', body):
        w[x] += 1
print('英文词:', dict(sorted(w.items())))
print()
print('== 新节行号 ==')
B = io.open(os.path.join(BASE, 'book.tex'), encoding='utf-8', newline='').read().split(CR)
F = io.open(os.path.join(BASE, 'female.tex'), encoding='utf-8', newline='').read().split(CR)
for lines, keys in [(B, ['漏服之后怎么办', '停用之后还能怀上吗', '避孕责任：谁承担', '经期性行为的常见疑问速答']),
                    (F, ['经期性行为的实操与舒适度', '经期还能做什么', '经血逆流与子宫内膜异位症：经期性交'])]:
    for k in keys:
        hit = [i for i, l in enumerate(lines, 1) if k in l and l.strip().startswith('\\')]
        print(hit[0] if hit else 'MISS', '|', k)
print()
print('== tcolorbox 配平 ==')
for tag, lines in [('book', B), ('female', F)]:
    b = sum(1 for l in lines if l.strip().startswith(r'\begin{tcolorbox}'))
    e = sum(1 for l in lines if l.strip().startswith(r'\end{tcolorbox}'))
    print('%s: begin=%d end=%d' % (tag, b, e))
