# -*- coding: utf-8 -*-
import io, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
T = {}
for fn in ['book.tex', 'female.tex', 'male.tex']:
    T[fn] = io.open(BASE + '\\' + fn, encoding='utf-8', newline='').read()
pat = re.compile(r'\\(chapter|section|subsection|subsubsection|subparagraph)\{([^{}]*)\}')

print('===== book.tex L380-L470 结构 =====')
for i in range(380, 471):
    s = T['book.tex'].split('\n')[i - 1].strip()
    m = pat.match(s)
    if m:
        print('L%-6d %s %s' % (i, m.group(1), m.group(2)[:76]))

print()
print('===== "性反应"相关标题（三卷）=====')
for fn, t in T.items():
    for i, l in enumerate(t.split('\n'), 1):
        s = l.strip()
        m = pat.match(s)
        if m and '性反应' in m.group(2):
            print('%-11s L%-6d %s %s' % (fn, i, m.group(1), m.group(2)[:76]))

print()
print('===== book.tex 各 chapter 起始行（看 426 所在章）=====')
for i, l in enumerate(T['book.tex'].split('\n'), 1):
    s = l.strip()
    m = pat.match(s)
    if m and m.group(1) == 'chapter' and i < 600:
        print('L%-6d chapter %s' % (i, m.group(2)[:70]))

print()
print('===== book.tex 中 "女性的" / "男性的" 开头标题分布 =====')
for fn, t in T.items():
    hits = []
    for i, l in enumerate(t.split('\n'), 1):
        s = l.strip()
        m = pat.match(s)
        if m and (m.group(2).startswith('女性的') or m.group(2).startswith('男性的')):
            hits.append((i, m.group(1), m.group(2)[:60]))
    print('%s: %d 处' % (fn, len(hits)))
    for h in hits[:14]:
        print('   L%-6d %s %s' % h)
