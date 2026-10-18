# -*- coding: utf-8 -*-
import io, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
T = {}
for fn in ['book.tex', 'female.tex', 'male.tex']:
    T[fn] = io.open(BASE + '\\' + fn, encoding='utf-8', newline='').read()
pat = re.compile(r'\\(section|subsection|subsubsection)\{([^{}]*)\}')

print('===== 1. female L580-L680 结构（经期相关）=====')
for i in range(580, 681):
    s = T['female.tex'].split('\n')[i - 1].strip()
    m = pat.match(s)
    if m:
        print('L%-6d %s %s' % (i, m.group(1), m.group(2)[:72]))

print()
print('===== 2. female L624-L640《经期性行为》正文全览 =====')
for i in range(624, 641):
    s = T['female.tex'].split('\n')[i - 1]
    if s.strip():
        print('L%d | %s' % (i, s.strip()[:118]))

print()
print('===== 3. book L939-L1000 结构 + 经期节正文 =====')
for i in range(939, 1001):
    s = T['book.tex'].split('\n')[i - 1]
    st = s.strip()
    m = pat.match(st)
    if m:
        print('L%-6d %s %s' % (i, m.group(1), m.group(2)[:70]))
print('--- L959 起的正文 ---')
for i in range(959, 1000):
    s = T['book.tex'].split('\n')[i - 1].strip()
    if s:
        print('L%d | %s' % (i, s[:118]))

print()
print('===== 4. female L615-L624 经期注意事项 =====')
for i in range(615, 624):
    s = T['female.tex'].split('\n')[i - 1].strip()
    if s:
        print('L%d | %s' % (i, s[:118]))
