# -*- coding: utf-8 -*-
import io, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
B = io.open(BASE + r'\book.tex', encoding='utf-8', newline='').read().split('\r\n')
M = io.open(BASE + r'\male.tex', encoding='utf-8', newline='').read().split('\r\n')

print('===== book L426-L506《女性的性反应》正文格式（前 40 行非空）=====')
n = 0
for i in range(426, 507):
    s = B[i - 1].strip()
    if s:
        print('L%d | %s' % (i, s[:116]))
        n += 1
        if n >= 40:
            break

print()
print('===== male L7299-L7318《男性的性反应》现有正文 =====')
for i in range(7299, 7319):
    s = M[i - 1].strip()
    if s:
        print('L%d | %s' % (i, s[:116]))

print()
print('===== 锚点唯一性 =====')
for a in [r'\section{高潮差距（Orgasm Gap）——性别愉悦不平等现象}', r'\subsection{传统中医与男性性健康}']:
    print('book=%d male=%d | %s' % (B.count(a), M.count(a), a))

print()
print('===== "不应期"词面分布 =====')
for fn, T in [('book', B), ('male', M), ('female', io.open(BASE + r'\female.tex', encoding='utf-8', newline='').read().split('\r\n'))]:
    hits = [i for i, l in enumerate(T, 1) if '不应期' in l and not l.strip().startswith('%')]
    print('%s: %d 处 -> %s' % (fn, len(hits), hits[:12]))
