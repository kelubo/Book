# -*- coding: utf-8 -*-
"""r37：book 增《男性的性反应》(before 高潮差距) + male 增《消退期》(before 传统中医)"""
import io, os, shutil

BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
CR = '\r\n'
BAK = os.path.join(BASE, '_backup_r37')
os.makedirs(BAK, exist_ok=True)

JOBS = {
    'book.tex': [
        ('_r37_blk_book.tex',
         '\\section{高潮差距（Orgasm Gap）——性别愉悦不平等现象}',
         '\\subsection{男性的性反应}'),
    ],
    'male.tex': [
        ('_r37_blk_male.tex',
         '\\section{传统中医与男性性健康}',
         '\\subsection{消退期}'),
    ],
}

def load(blk):
    t = io.open(os.path.join(BASE, blk), encoding='utf-8', newline='').read()
    return t.replace('\r\n', '\n').replace('\n', CR).rstrip(CR)

for fn, jobs in JOBS.items():
    p = os.path.join(BASE, fn)
    shutil.copy2(p, os.path.join(BAK, fn))
    text = io.open(p, encoding='utf-8', newline='').read()
    for blk, anchor, ikey in jobs:
        if ikey in text:
            print(fn, blk, 'SKIP (idempotent)')
            continue
        n = text.count(anchor)
        if n != 1:
            raise SystemExit('ANCHOR FAIL %s %s count=%d' % (fn, anchor, n))
        core = load(blk)
        text = text.replace(anchor, core + CR + CR + anchor, 1)
        print(fn, blk, 'inserted before', anchor[:40], '... new size =', len(text))
    io.open(p, 'w', encoding='utf-8', newline='').write(text)

print('--- post-insert counts ---')
bk = io.open(os.path.join(BASE, 'book.tex'), encoding='utf-8', newline='').read()
ma = io.open(os.path.join(BASE, 'male.tex'), encoding='utf-8', newline='').read()
print('book  \\\\subsection{男性的性反应} =', bk.count('\\subsection{男性的性反应}'))
print('book  \\\\subsubsection{兴奋期} =', bk.count('\\subsubsection{兴奋期}'))
print('male  \\\\subsection{消退期} =', ma.count('\\subsection{消退期}'))
print('book lines =', len(bk.split(CR)), ' male lines =', len(ma.split(CR)))
