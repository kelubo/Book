# -*- coding: utf-8 -*-
import io
p = 'D:/Git/Book/整理中/1_原文校对/ad/book.tex'
s = io.open(p, encoding='utf-8', newline='').read()

titles = [
    '\\section{性爱前后的清洁、准备与经期性交}',
    '\\section{性交时长、频率与',
    '\\section{性爱中的尴尬与意外',
    '\\section{性爱过程的节奏：当一方想快',
    '\\section{梦交（Nocturnal Sexual Dreams）',
]
pos = [s.index(t) for t in titles]
segs = [s[pos[i]:pos[i + 1]] for i in range(4)]
# 目标顺序：节奏(3) -> 尴尬(2) -> 时长(1) -> 清洁(0)
new = s[:pos[0]] + segs[3] + segs[2] + segs[1] + segs[0] + s[pos[4]:]
io.open(p, 'w', encoding='utf-8', newline='').write(new)
print('reordered ok; new lines =', new.count('\r\n') + 1)
