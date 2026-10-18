# -*- coding: utf-8 -*-
import io, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
B = io.open(BASE + r'\book.tex', encoding='utf-8', newline='').read().split('\r\n')
F = io.open(BASE + r'\female.tex', encoding='utf-8', newline='').read().split('\r\n')
pat = re.compile(r'\\(section|subsection|subsubsection)\{([^{}]*)\}')

print('===== book L41755-L41840 避孕方法选择指南区结构 =====')
for i in range(41755, 41841):
    s = B[i - 1].strip()
    m = pat.match(s)
    if m:
        print('L%-6d %s %s' % (i, m.group(1), m.group(2)[:72]))

print()
print('===== book L36360-L36430 各种避孕方法的详细比较区 =====')
for i in range(36360, 36431):
    s = B[i - 1].strip()
    m = pat.match(s)
    if m:
        print('L%-6d %s %s' % (i, m.group(1), m.group(2)[:72]))

print()
print('===== book L35929-L36000 激素避孕法区（D1 落位）=====')
for i in range(35929, 36001):
    s = B[i - 1].strip()
    m = pat.match(s)
    if m:
        print('L%-6d %s %s' % (i, m.group(1), m.group(2)[:72]))

print()
print('===== female L624-L648 经期性行为区（E 落位）=====')
for i in range(624, 649):
    s = F[i - 1].strip()
    m = pat.match(s)
    if m:
        print('L%-6d %s %s' % (i, m.group(1), m.group(2)[:72]))

print()
print('===== 锚点计数 =====')
def c(lines, a):
    return lines.count(a)
for a in [r'\subsection{避孕贴片}', r'\section{梦交（Nocturnal Sexual Dreams）——正常还是异常？}',
          r'\section{月经贫困与经期平等}', r'\section{避孕方法选择指南}',
          r'\section{各种避孕方法的详细比较}', r'\subsection{特殊情况下的避孕选择}']:
    print('book=%d female=%d | %s' % (c(B, a), c(F, a), a))
