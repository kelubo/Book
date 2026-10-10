# -*- coding: utf-8 -*-
"""第十九轮插入：早泄治疗优化（male.tex 3 处 + book.tex 2 处）"""
import io, sys

DIR = 'D:/Git/Book/整理中/1_原文校对/ad/'
CR = '\r\n'

def read(p):
    with io.open(DIR + p, encoding='utf-8', newline='') as f:
        return f.read()

def write(p, s):
    with io.open(DIR + p, 'w', encoding='utf-8', newline='') as f:
        f.write(s)

def load_block(n):
    with io.open(DIR + '_r19_blk%d.tex' % n, encoding='utf-8', newline='') as f:
        s = f.read()
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    return s.strip('\n').replace('\n', CR)

def after_anchor(text, anchor, block):
    c = text.count(anchor)
    assert c == 1, 'anchor count=%d for %r' % (c, anchor[:50])
    return text.replace(anchor, anchor + CR + CR + block, 1)

def before_anchor(text, anchor, block):
    c = text.count(anchor)
    assert c == 1, 'anchor count=%d for %r' % (c, anchor[:50])
    return text.replace(anchor, block + CR + CR + anchor, 1)

def after_line(text, sub, block):
    hits = [ln for ln in text.split(CR) if sub in ln]
    assert len(hits) == 1, 'line hits=%d for %r' % (len(hits), sub)
    return text.replace(hits[0], hits[0] + CR + CR + block, 1)

# ---------------- 任务定义 ----------------
JOBS = [
    # (文件, 模式, 锚/子串, 块号, 幂等键)
    ('male.tex', 'after_line', 'PE治疗应遵循', 3, '治疗的循证阶梯与常见误区'),
    ('male.tex', 'after', '\\subsection{评估工具（PEDT / IPELT）}', 2, '早泄诊断工具（PEDT）'),
    ('male.tex', 'after', '\\subsection{分类（原发性 / 继发性 / 自然变异性）}', 1, 'Waldinger'),
    ('book.tex', 'before', '\\subsection{性欲低下（性欲减退）}', 4, '循证阶梯与常见误区'),
    ('book.tex', 'after_line', '\\item[逆行射精]', 5, 'PEDT（早泄诊断工具）'),
]

files = {}
for f, mode, anchor, blk, key in JOBS:
    if f not in files:
        files[f] = read(f)
    text = files[f]
    if key in text:
        print('[SKIP] %s  已含 %r' % (f, key))
        continue
    block = load_block(blk)
    if mode == 'after':
        files[f] = after_anchor(text, anchor, block)
    elif mode == 'before':
        files[f] = before_anchor(text, anchor, block)
    elif mode == 'after_line':
        files[f] = after_line(text, anchor, block)
    print('[OK]   %s  <- blk%d  (%s)' % (f, blk, anchor[:40]))

for f, text in files.items():
    write(f, text)
    print('WRITE %s  lines=%d' % (f, text.count(CR) + 1))
