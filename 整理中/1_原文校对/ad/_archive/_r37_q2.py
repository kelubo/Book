# -*- coding: utf-8 -*-
import io, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
B = io.open(BASE + r'\book.tex', encoding='utf-8', newline='').read().split('\r\n')
F = io.open(BASE + r'\female.tex', encoding='utf-8', newline='').read().split('\r\n')
M = io.open(BASE + r'\male.tex', encoding='utf-8', newline='').read().split('\r\n')
pat = re.compile(r'\\(chapter|section|subsection|subsubsection|subparagraph)\{([^{}]*)\}')

print('===== book L411-L545 完整标题结构（性反应周期 section 全貌）=====')
for i in range(411, 546):
    s = B[i - 1].strip()
    m = pat.match(s)
    if m:
        print('L%-6d %s %s' % (i, m.group(1), m.group(2)[:76]))

print()
print('===== book L411-L425《阶段性的性反应》正文抽样 =====')
for i in range(411, 426):
    s = B[i - 1].strip()
    if s:
        print('L%d | %s' % (i, s[:110]))

print()
print('===== female L12040-L12200 结构（L12113 性反应周期所在章）=====')
for i in range(12040, 12201):
    s = F[i - 1].strip()
    m = pat.match(s)
    if m:
        print('L%-6d %s %s' % (i, m.group(1), m.group(2)[:76]))

print()
print('===== female L12113-L12172《性反应周期》正文抽样 =====')
for i in range(12113, 12173):
    s = F[i - 1].strip()
    if s:
        print('L%d | %s' % (i, s[:110]))

print()
print('===== male L7299-L7360《男性的性反应》结构（对称参照）=====')
for i in range(7299, 7361):
    s = M[i - 1].strip()
    m = pat.match(s)
    if m:
        print('L%-6d %s %s' % (i, m.group(1), m.group(2)[:76]))
