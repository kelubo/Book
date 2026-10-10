# -*- coding: utf-8 -*-
"""r38：book 三节插入（A 新手父母 / B 腰痛姿势 / C 倒班加班），均 before 型"""
import io, os, shutil

BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
CR = '\r\n'
BAK = os.path.join(BASE, '_backup_r38')
os.makedirs(BAK, exist_ok=True)

JOBS = [
    # (blk, anchor, ikey)
    ('_r38_blk_a.tex', '\\section{性描写与助兴用具}', '\\subsection{新手父母的性生活：睡眠、分工与碎片时间}'),
    ('_r38_blk_b.tex', '\\subsection{残疾伴侣辅助姿势}', '\\subsection{慢性腰痛与腰椎问题者的性姿势}'),
    ('_r38_blk_c.tex', '\\subsection{出差、旅行与酒店：路上的性健康}', '\\subsection{倒班与加班：作息错位下的性生活}'),
]

P = os.path.join(BASE, 'book.tex')
shutil.copy2(P, os.path.join(BAK, 'book.tex'))
text = io.open(P, encoding='utf-8', newline='').read()

def load(blk):
    t = io.open(os.path.join(BASE, blk), encoding='utf-8', newline='').read()
    return t.replace('\r\n', '\n').replace('\n', CR).rstrip(CR)

for blk, anchor, ikey in JOBS:
    if ikey in text:
        print(blk, 'SKIP (idempotent)')
        continue
    n = text.count(anchor)
    if n != 1:
        raise SystemExit('ANCHOR FAIL %s count=%d' % (anchor, n))
    core = load(blk)
    text = text.replace(anchor, core + CR + CR + anchor, 1)
    print(blk, 'inserted before', anchor[:40], ' new size =', len(text))

io.open(P, 'w', encoding='utf-8', newline='').write(text)

print('--- post-insert counts ---')
print('subsection 新手父母  =', text.count('\\subsection{新手父母的性生活：睡眠、分工与碎片时间}'))
print('subsection 慢性腰痛  =', text.count('\\subsection{慢性腰痛与腰椎问题者的性姿势}'))
print('subsection 倒班与加班 =', text.count('\\subsection{倒班与加班：作息错位下的性生活}'))
print('book lines =', len(text.split(CR)))
