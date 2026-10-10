# -*- coding: utf-8 -*-
import io, os, re, collections
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
CR = '\r\n'
new = io.open(os.path.join(BASE, 'book.tex'), encoding='utf-8', newline='').read()
old = io.open(os.path.join(BASE, '_backup_r35', 'book.tex'), encoding='utf-8', newline='').read()

# 1. 双反斜杠笔误（精确：连续两个反斜杠后跟命令名）
pat = re.compile(r'\\\\\\\\(?:textbf|textit|item|begin|end|noindent|section|subsection|subsubsection|par|title|emph|underline|chapter)')
print('双反斜杠笔误: 前=%d 后=%d 增量=%d' % (len(pat.findall(old)), len(pat.findall(new)), len(pat.findall(new)) - len(pat.findall(old))))

# 2. 新块英文词
w = collections.Counter()
blks = ['_r35_blk_a1.tex', '_r35_blk_a2.tex', '_r35_blk_b1.tex', '_r35_blk_c1.tex']
for blk in blks:
    t = io.open(os.path.join(BASE, blk), encoding='utf-8', newline='').read()
    body = re.sub(r'\\[A-Za-z]+', ' ', t)
    for x in re.findall(r'[A-Za-z][A-Za-z/-]{2,}', body):
        w[x] += 1
print('英文词:', dict(sorted(w.items())))

# 3. 新节行号与热敷纠正
lines = new.split(CR)
print('book.tex lines:', len(lines))
for t in ['背叛创伤：出轨被发现后', '修复或不修复：可以从哪些证据',
          '绳缚的神经与循环安全', '灌肠的安全边界：作为准备']:
    hit = [i for i, l in enumerate(lines, 1) if t in l and l.strip().startswith('\\')]
    print(hit[0] if hit else 'MISS', '|', t)
hit = [i for i, l in enumerate(lines, 1) if '对于绳索痕迹' in l]
print('热敷纠正行:', [(i, lines[i - 1].strip()[:60]) for i in hit])

# 4. 既有损坏行确认（ection{）
for tag, txt, fn in [('backup', old, '_backup_r35/book.tex'), ('current', new, 'book.tex')]:
    ln = txt.split(CR)
    bad = [(i, l.strip()) for i, l in enumerate(ln, 1) if re.match(r'^ection\{', l.strip())]
    print('%s 中 ection{ 损坏行: %s' % (tag, bad))
