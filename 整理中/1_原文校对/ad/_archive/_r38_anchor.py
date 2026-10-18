# -*- coding: utf-8 -*-
"""r38 执行前锚点探测：A 育儿 / B 腰痛姿势 / C 工作节奏"""
import io, os, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
bk = io.open(os.path.join(BASE, 'book.tex'), encoding='utf-8', newline='').read()
bl = bk.split('\r\n')

def count(s):
    return bk.count(s)

print('=== A 锚：\\section{性描写与助兴用具} count =', count('\\section{性描写与助兴用具}'))

print()
print('=== B：姿势章结构（\\section{性交姿势} 之后 120 行内的标题）===')
pos = None
for i, l in enumerate(bl):
    if l.strip() == '\\section{性交姿势}':
        pos = i
        break
print('section 性交姿势 @ L%d, count(section 标题串) = %d' % (pos+1 if pos else -1, count('\\section{性交姿势}')))
for j in range(pos, pos+260):
    st = bl[j].strip()
    m = re.match(r'\\(section|subsection|subsubsection)\{([^{}]*)\}', st)
    if m:
        print('  L%d %s %s' % (j+1, m.group(1), m.group(2)[:55]))

print()
print('=== C：L24399 上下文（预约性爱所在结构）===')
for j in range(24370, 24470):
    st = bl[j].strip()
    m = re.match(r'\\(section|subsection|subsubsection)\{([^{}]*)\}', st)
    if m:
        print('  L%d %s %s' % (j+1, m.group(1), m.group(2)[:55]))
print('  L24417 行: ', bl[24416].strip()[:70])

print()
print('=== 候选锚 count 校验 ===')
for a in ['\\subsection{残疾伴侣辅助姿势}',
          '\\subsection{轮椅使用者辅助姿势}',
          '\\subsection{视力障碍者友好姿势：触觉之爱}',
          '\\subsection{安全与舒适的基本原则}',
          '\\section{性交姿势的注意事项}']:
    print('  %-45s count = %d' % (a, count(a)))
