# -*- coding: utf-8 -*-
import io, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
T = {}
for fn in ['book.tex', 'female.tex', 'male.tex']:
    T[fn] = io.open(BASE + '\\' + fn, encoding='utf-8', newline='').read()

def show(word, fns, limit=8, w=118):
    print('----- %s -----' % word)
    n = 0
    for fn in fns:
        for i, l in enumerate(T[fn].split('\n'), 1):
            s = l.strip()
            if s.startswith('%'):
                continue
            if word in s:
                print('%-10s L%-6d %s' % (fn, i, s[:w]))
                n += 1
                if n >= limit:
                    return
    if n == 0:
        print('(无)')

show('漏服', ['book.tex'], 6)
show('忘记服', ['book.tex'], 4)
show('滑脱', ['book.tex'], 8)
show('抗癫痫', ['book.tex'], 6)
show('利福平', ['book.tex'], 5)
show('经血逆流', ['female.tex'], 5)
show('逆流', ['female.tex'], 5)
show('生育力恢复', ['book.tex', 'female.tex', 'male.tex'], 6)
show('停药后', ['book.tex', 'female.tex'], 6)
print()
print('===== book 紧急避孕节结构 L41683-L41760 =====')
pat = re.compile(r'\\(section|subsection|subsubsection)\{([^{}]*)\}')
for i in range(41683, 41761):
    s = T['book.tex'].split('\n')[i - 1].strip()
    m = pat.match(s)
    if m:
        print('L%-6d %s %s' % (i, m.group(1), m.group(2)[:72]))
print()
print('===== book L41747-L41760 紧急避孕注意事项正文 =====')
for i in range(41747, 41760):
    s = T['book.tex'].split('\n')[i - 1].strip()
    if s:
        print('L%d | %s' % (i, s[:118]))
