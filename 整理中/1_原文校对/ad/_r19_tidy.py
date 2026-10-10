# -*- coding: utf-8 -*-
import io
p = 'D:/Git/Book/整理中/1_原文校对/ad/male.tex'
CR = '\r\n'
s = io.open(p, encoding='utf-8', newline='').read()

pairs = [
    ('才是诊断的核心。' + CR + '\\subsection{评估工具（PEDT / IPELT）}',
     '才是诊断的核心。' + CR + CR + '\\subsection{评估工具（PEDT / IPELT）}'),
    ('\\end{tcolorbox}' + CR + '\\subsection{治疗方法}',
     '\\end{tcolorbox}' + CR + CR + '\\subsection{治疗方法}'),
]
for a, b in pairs:
    c = s.count(a)
    print('count=%d  %s' % (c, a[:34].replace(CR, '\\n')))
    if c == 1:
        s = s.replace(a, b, 1)

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('done')
