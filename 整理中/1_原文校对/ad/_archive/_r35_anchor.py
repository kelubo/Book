# -*- coding: utf-8 -*-
import io
p = r'D:\Git\Book\整理中\1_原文校对\ad\book.tex'
lines = io.open(p, encoding='utf-8', newline='').read().split('\r\n')
print('book.tex lines:', len(lines))
print()
print('== 锚点计数 ==')
anchors = [
    r'\subsection{不同文化对性的传统观念与现代演变}',
    r'\subsubsection{电击类玩具（e-stim）的安全使用}',
    r'\section{性交姿势}',
    r'\subsection{婚外性行为的影响与婚姻修复}',
]
for a in anchors:
    print(lines.count(a), '|', a)
print()
print('== L17530-17545 恢复护理段原文 ==')
for i in range(17530, 17546):
    print('L%d | %s' % (i, lines[i - 1]))
print()
print('== L39276-39310 婚外节尾部 ==')
for i in range(39276, 39310):
    print('L%d | %s' % (i, lines[i - 1]))
