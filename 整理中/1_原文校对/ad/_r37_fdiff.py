# -*- coding: utf-8 -*-
import io, os, difflib
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
old = io.open(os.path.join(BASE, '_backup_r36', 'female.tex'), encoding='utf-8', newline='').read().split('\r\n')
cur = io.open(os.path.join(BASE, 'female.tex'), encoding='utf-8', newline='').read().split('\r\n')
print('r35后(backup_r36) =', len(old), ' 当前 =', len(cur))
d = list(difflib.unified_diff(old, cur, lineterm='', n=1))
print('diff 条目 =', len(d))
n = 0
for line in d:
    if line.startswith(('+', '-')) and not line.startswith(('+++', '---')):
        n += 1
        print(repr(line[:100]))
        if n > 80:
            print('...(截断)')
            break
