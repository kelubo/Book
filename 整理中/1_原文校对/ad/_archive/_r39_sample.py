# -*- coding: utf-8 -*-
"""r39 结构样例：看真实文本形态再定算法"""
import io, os
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
bk = io.open(os.path.join(BASE, 'book.tex'), encoding='utf-8', newline='').read().split('\r\n')
fe = io.open(os.path.join(BASE, 'female.tex'), encoding='utf-8', newline='').read().split('\r\n')
ma = io.open(os.path.join(BASE, 'male.tex'), encoding='utf-8', newline='').read().split('\r\n')

def dump(tag, ls, a, b, width=78):
    print('--- %s (L%d-%d) ---' % (tag, a, b))
    for j in range(a-1, min(b, len(ls))):
        print('%5d %s' % (j+1, ls[j][:width]))
    print()

dump('book 纯 bullet 群', bk, 5085, 5095)
dump('book 混合 N.+bullet 群', bk, 8616, 8640)
dump('book bullet 内 bold', bk, 35640, 35660)
dump('book 表格 | 行样例', bk, 16170, 16190)
dump('book * bullet 群', bk, 9025, 9035)
dump('book 数字列表群', bk, 9485, 9505)
dump('female * bullet + bold', fe, 244, 258)
dump('female - 群', fe, 3496, 3512)
dump('male - 群', ma, 1120, 1140)
