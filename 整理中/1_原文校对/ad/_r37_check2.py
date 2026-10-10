# -*- coding: utf-8 -*-
"""r37 复查：ection 任意位置匹配 + book 双反斜杠 suspect 明细"""
import io, os, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'

for name in ['book.tex', 'female.tex', 'male.tex']:
    txt = io.open(os.path.join(BASE, name), encoding='utf-8', newline='').read()
    lines = txt.split('\r\n')
    ect = [(i+1, l.strip()[:60]) for i, l in enumerate(lines) if '\\ection{' in l]
    print(name, '\\ection{ anywhere =', len(ect))
    for ln, s in ect:
        print('   L%d: %s' % (ln, s))

print()
bk = io.open(os.path.join(BASE, 'book.tex'), encoding='utf-8', newline='').read()
bl = bk.split('\r\n')
pat = re.compile(r'\\\\(?:textbf|textit|item|begin|end|noindent|section|subsection|subsubsection|par\b|title|emph|underline|chapter|tcolorbox)')
print('=== book double-backslash suspects ===')
for i, l in enumerate(bl):
    m = pat.search(l)
    if m:
        print('L%d: ...%s...' % (i+1, l[max(0, m.start()-40):m.start()+40]))

print()
print('=== book \\par literal count (口径: 字面 \\\\par 出现次数) ===')
print('bk contains \\\\par:', bk.count('\\\\par'))
