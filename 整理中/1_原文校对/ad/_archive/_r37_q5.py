# -*- coding: utf-8 -*-
import io, os
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'

ma = io.open(os.path.join(BASE, 'male.tex'), encoding='utf-8', newline='').read()
bk = io.open(os.path.join(BASE, 'book.tex'), encoding='utf-8', newline='').read()
bl = bk.split('\r\n')

print('=== book L470-515 (女性的性反应: 消退期 + 节尾 + 高潮差距开头) ===')
for i in range(469, 515):
    print(i+1, bl[i][:110])

print()
print('=== book L428 引导段全文 ===')
print(bl[427])

print()
print('=== 重名风险 count 校验 ===')
checks = [
    (bk, 'book  \\subsection{男性的性反应}', '\\subsection{男性的性反应}'),
    (bk, 'book  \\subsubsection{消退期}', '\\subsubsection{消退期}'),
    (bk, 'book  \\subsubsection{兴奋期}', '\\subsubsection{兴奋期}'),
    (ma, 'male  \\subsection{消退期}', '\\subsection{消退期}'),
    (ma, 'male  \\section{传统中医与男性性健康}', '\\section{传统中医与男性性健康}'),
    (ma, 'male  \\subsection{高潮期}', '\\subsection{高潮期}'),
]
for t, label, a in checks:
    print(label, 'count =', t.count(a))
