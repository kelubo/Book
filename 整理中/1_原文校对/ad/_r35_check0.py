# -*- coding: utf-8 -*-
import io, os, re, shutil
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
book = io.open(BASE + r'\book.tex', encoding='utf-8', newline='').read()

# 1. 新标题唯一性
titles = [
    r'\subsection{背叛创伤：出轨被发现后，被背叛者会经历什么}',
    r'\subsection{修复或不修复：可以从哪些证据判断可行性}',
    r'\subsubsection{绳缚的神经与循环安全：麻木、绳痕与自救}',
    r'\subsubsection{灌肠的安全边界：作为准备与作为玩法}',
]
print('== 新标题唯一性 ==')
for t in titles:
    print(book.count(t), '|', t)

# 2. 引号码位对照：既有 r34 块的引号 vs 本轮新块
print()
print('== 引号码位对照 ==')
for f in ['_r34_blk3.tex', '_r35_blk_a1.tex', '_r35_blk_a2.tex', '_r35_blk_b1.tex', '_r35_blk_c1.tex']:
    p = os.path.join(BASE, f)
    if not os.path.isfile(p):
        print(f, 'MISSING'); continue
    t = io.open(p, encoding='utf-8', newline='').read()
    dq = t.count('"')
    ld = t.count(u'\u201c'); rd = t.count(u'\u201d')
    print('%-20s ASCII\"=%d  U+201C=%d  U+201D=%d' % (f, dq, ld, rd))

# 3. 备份
dst = os.path.join(BASE, '_backup_r35')
os.makedirs(dst, exist_ok=True)
for fn in ['book.tex', 'female.tex', 'male.tex']:
    shutil.copy2(os.path.join(BASE, fn), os.path.join(dst, fn))
print()
print('backup ok:', sorted(os.listdir(dst)))

# 4. 待纠正行的精确文本
lines = book.split('\r\n')
target = None
for i, l in enumerate(lines, 1):
    if '绳索痕迹' in l and '热敷' in l:
        target = (i, l)
print()
print('纠正目标行:', repr(target))
