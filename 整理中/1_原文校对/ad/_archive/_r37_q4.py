# -*- coding: utf-8 -*-
import io, os
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'

ma = io.open(os.path.join(BASE, 'male.tex'), encoding='utf-8', newline='').read()
ml = ma.split('\r\n')
bk = io.open(os.path.join(BASE, 'book.tex'), encoding='utf-8', newline='').read()
bl = bk.split('\r\n')

print('=== male L7295-7325 repr ===')
for i in range(7294, 7325):
    print(i+1, repr(ml[i]))

print()
print('=== male all lines containing 传统中医 ===')
for i, ln in enumerate(ml):
    if '传统中医' in ln:
        print(i+1, repr(ln))

print()
print('=== male section structure L7299-7420 ===')
for i in range(7298, min(7420, len(ml))):
    s = ml[i].lstrip()
    if s.startswith('\\sub'):
        print(i+1, s[:60])

print()
print('=== male L1315-1360 (不应期 existing content) ===')
for i in range(1314, 1360):
    print(i+1, ml[i][:90])

print()
print('=== book 不应期 locations (18 expected) ===')
for i, ln in enumerate(bl):
    if '不应期' in ln:
        print(i+1, ln.strip()[:80])

print()
print('=== book L426-470 女性的性反应 format sample ===')
for i in range(425, 470):
    print(i+1, bl[i][:100])

print()
print('=== anchors ===')
a1 = '\\section{高潮差距（Orgasm Gap）——性别愉悦不平等现象}'
print('book a1 count =', bk.count(a1))
