# -*- coding: utf-8 -*-
"""第二十轮插入：性爱过程内容（book.tex：补全 7 处预留位 + 新增 4 节）"""
import io

DIR = 'D:/Git/Book/整理中/1_原文校对/ad/'
CR = '\r\n'

def read(p):
    with io.open(DIR + p, encoding='utf-8', newline='') as f:
        return f.read()

def write(p, s):
    with io.open(DIR + p, 'w', encoding='utf-8', newline='') as f:
        f.write(s)

def block(n):
    with io.open(DIR + '_r20_blk%d.tex' % n, encoding='utf-8', newline='') as f:
        s = f.read()
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    return s.strip('\n').replace('\n', CR)

text = read('book.tex')
log = []

# ---------- A. 补全 7 处 [预留内容] ----------
RESERVE = [
    ('\\section{侧卧位 vs 坐位 vs 站位}', 1, '最省力，腰背负担小'),
    ('\\section{女上位的变体}', 2, '最便于女方掌控节奏的体位'),
    ('\\section{后入式的变体}', 3, '插入角度特殊'),
    ('\\section{组合式体位}', 4, '串联并切换多种体位'),
    ('\\section{增加受孕机会的体位}', 5, '科学证据并不充分'),
    ('\\section{体位与情感连接}', 6, '不只关乎生理刺激'),
    ('\\section{探索与尝试的建议}', 7, '性爱容易陷入'),
]

for title, n, key in RESERVE:
    if key in text:
        log.append('[SKIP] 预留位 blk%d 已填' % n); continue
    anchor = title + CR + CR + '[预留内容]'
    c = text.count(anchor)
    if c != 1:
        log.append('[FAIL] 预留位 blk%d 锚命中=%d' % (n, c)); continue
    text = text.replace(anchor, title + CR + CR + block(n), 1)
    log.append('[OK]   预留位 blk%d  <- %s' % (n, title))

# ---------- B. 新增 4 节，插在《梦交》节之前（逆序保证顺序） ----------
ANCHOR2 = '\\section{梦交（Nocturnal Sexual Dreams）——正常还是异常？}'
NEW = [(11, '性爱前后的清洁、准备与经期性交'),
       (10, '性交时长、频率与'),
       (9, '性爱中的尴尬与意外'),
       (8, '性爱过程的节奏：当一方想快')]

for n, key in NEW:
    if key in text:
        log.append('[SKIP] 新节 blk%d 已存在' % n); continue
    if text.count(ANCHOR2) != 1:
        log.append('[FAIL] 新节 blk%d：梦交锚命中=%d' % (n, text.count(ANCHOR2))); break
    text = text.replace(ANCHOR2, block(n) + CR + CR + ANCHOR2, 1)
    log.append('[OK]   新节   blk%d  插于《梦交》前' % n)

write('book.tex', text)
for l in log:
    print(l)
print('WRITE book.tex  lines=%d' % (text.count(CR) + 1))
