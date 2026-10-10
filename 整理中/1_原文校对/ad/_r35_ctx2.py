# -*- coding: utf-8 -*-
import io, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
T = {}
for fn in ['book.tex', 'female.tex', 'male.tex']:
    T[fn] = io.open(BASE + '\\' + fn, encoding='utf-8', newline='').read()
pat = re.compile(r'\\(section|subsection|subsubsection)\{([^{}]*)\}')

print('===== 1. book L17100-17160（束縛区域入口）=====')
for i in range(17100, 17161):
    s = T['book.tex'].split('\n')[i - 1].strip()
    m = pat.match(s)
    if m:
        print('L%-6d %s %s' % (i, m.group(1), m.group(2)[:76]))
print('--- L17130-17160 正文 ---')
for i in range(17130, 17161):
    s = T['book.tex'].split('\n')[i - 1].strip()
    if s:
        print('L%d | %s' % (i, s[:112]))

print()
print('===== 2. L17460 SM的健康与安全 内容全览 =====')
for i in range(17460, 17580):
    s = T['book.tex'].split('\n')[i - 1].strip()
    if s:
        print('L%d | %s' % (i, s[:112]))

print()
print('===== 3. r34 三方式补遗节 行数范围 L29510-L29570 =====')
for i in range(29510, 29571):
    s = T['book.tex'].split('\n')[i - 1].strip()
    if s:
        print('L%d | %s' % (i, s[:112]))
