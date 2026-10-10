# -*- coding: utf-8 -*-
import io, os
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
CR = '\r\n'
fname = os.path.join(BASE, 'book.tex')
text = io.open(fname, encoding='utf-8', newline='').read()
print('start lines:', len(text.split(CR)))

def load(blk):
    t = io.open(os.path.join(BASE, blk), encoding='utf-8', newline='').read()
    return t.replace('\r\n', '\n').replace('\n', CR).rstrip(CR)

# ---------- 1. 锚点型插入（B1、C1） ----------
jobs = [
    ('_r35_blk_b1.tex', r'\subsubsection{电击类玩具（e-stim）的安全使用}', '绳缚的神经与循环安全'),
    ('_r35_blk_c1.tex', r'\section{性交姿势}', '灌肠的安全边界'),
]
for blk, anchor, ikey in jobs:
    if ikey in text:
        print('SKIP (idempotent):', blk)
        continue
    if text.count(anchor) != 1:
        raise SystemExit('ANCHOR FAIL %s -> count=%d' % (anchor, text.count(anchor)))
    core = load(blk)
    text = text.replace(anchor, core + CR + CR + anchor, 1)
    print('OK:', blk, '<- before', anchor)

# ---------- 2. 热敷纠正 ----------
old_line = '     - 对于绳索痕迹，使用热敷和按摩促进血液循环'
new_line = ('     - 对于绳索痕迹：急性期（24 至 48 小时内）先冷敷，以减轻出血与肿胀，'
            '此时不要热敷、也不要用力揉搓；48 小时之后可转为温和的温热敷与轻柔按摩，促进吸收'
            '（详见本章绑缚安全相关小节）')
if old_line not in text:
    if '急性期（24 至 48 小时内）先冷敷' in text:
        print('SKIP (idempotent): 热敷纠正')
    else:
        raise SystemExit('FIX FAIL: old line not found')
else:
    if text.count(old_line) != 1:
        raise SystemExit('FIX FAIL: count=%d' % text.count(old_line))
    text = text.replace(old_line, new_line, 1)
    print('OK: 热敷纠正已替换')

# ---------- 3. 行级插入 A1 + A2（婚外节尾，动态校验） ----------
a1key = '背叛创伤：出轨被发现后'
a2key = '修复或不修复：可以从哪些证据'
if a1key in text and a2key in text:
    print('SKIP (idempotent): A1/A2')
else:
    lines = text.split(CR)
    sec_i = None
    tgt_i = None
    nxt_i = None
    for i, l in enumerate(lines):
        s = l.strip()
        if s == r'\subsection{婚外性行为的影响与婚姻修复}':
            sec_i = i
        elif sec_i is not None and tgt_i is None and '自我成长' in s and '自我反思' in s:
            tgt_i = i
        elif sec_i is not None and tgt_i is not None and nxt_i is None and s.startswith(r'\subsection{'):
            nxt_i = i
    print('sec_i=%s tgt_i=%s nxt_i=%s' % (sec_i, tgt_i, nxt_i))
    if sec_i is None or tgt_i is None or nxt_i is None:
        raise SystemExit('A1/A2 FAIL: 结构定位失败')
    if not (sec_i < tgt_i < nxt_i and tgt_i - sec_i < 40 and nxt_i - tgt_i < 10):
        raise SystemExit('A1/A2 FAIL: 位置校验不通过')
    print('anchor L%d | %s' % (tgt_i + 1, lines[tgt_i].strip()[:70]))
    print('next  L%d | %s' % (nxt_i + 1, lines[nxt_i].strip()[:70]))
    a1l = load('_r35_blk_a1.tex').split(CR)
    a2l = load('_r35_blk_a2.tex').split(CR)
    ins = ['', ''] + a1l + ['', ''] + a2l
    lines = lines[:tgt_i + 1] + ins + lines[tgt_i + 1:]
    text = CR.join(lines)
    print('OK: A1 + A2 inserted after L%d (+%d lines)' % (tgt_i + 1, len(ins)))

io.open(fname, 'w', encoding='utf-8', newline='').write(text)
print()
print('book.tex lines now:', len(text.split(CR)))
