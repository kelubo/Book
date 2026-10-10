# -*- coding: utf-8 -*-
"""r38 插入点上下文抽查 + 笔误基线对比 + 新块英文残留"""
import io, os, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
bk = io.open(os.path.join(BASE, 'book.tex'), encoding='utf-8', newline='').read()
bl = bk.split('\r\n')

def ctx(anchor, before=4, after=3):
    for i, l in enumerate(bl):
        if l.strip() == anchor:
            print('[ctx @ L%d] %s' % (i+1, anchor[:50]))
            for j in range(max(0, i-before), min(i+after, len(bl))):
                print('   %d %s' % (j+1, bl[j].strip()[:70]))
            print()
            return

ctx('\\subsection{新手父母的性生活：睡眠、分工与碎片时间}')
ctx('\\section{性描写与助兴用具}')
ctx('\\subsection{慢性腰痛与腰椎问题者的性姿势}', before=6, after=3)
ctx('\\subsection{倒班与加班：作息错位下的性生活}', before=6, after=3)

print('=== 笔误基线（裸 ection 4 处 / 双反斜杠 suspect 2 处）===')
hits = [(i+1, l.strip()[:50]) for i, l in enumerate(bl) if re.match(r'^\s*ection\{', l)]
print('bare ection{ =', len(hits), hits)
pat = re.compile(r'\\\\(?:textbf|textit|item|begin|end|noindent|section|subsection|subsubsection|par\b|title|emph|underline|chapter|tcolorbox)')
sus = [(i+1) for i, l in enumerate(bl) if pat.search(l)]
print('double-backslash-suspect =', len(sus), sus)

print()
print('=== 新块英文残留（应仅 LaTeX 命令 + 少量术语）===')
for blk in ['_r38_blk_a.tex', '_r38_blk_b.tex', '_r38_blk_c.tex']:
    t = io.open(os.path.join(BASE, blk), encoding='utf-8', newline='').read()
    en = re.findall(r'[A-Za-z]{3,}', t)
    print(blk, sorted(set(en)))
