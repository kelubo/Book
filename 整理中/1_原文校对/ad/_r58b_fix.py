# -*- coding: utf-8 -*-
# r58b: 修补交叉引用段落的空行——A 段前补空行、B 段后去掉连续双空行
import io, sys, os
from collections import Counter

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, 'book.tex')
APPLY = 'apply' in sys.argv

A_SIG = '概率之差'
B_SIG = '本节转向时间层面'
MINTZ_SIG = '成为阴蒂'

raw = io.open(P, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in raw else '\n'
lines = raw.split(nl)
log = ['行数=%d' % len(lines)]

i_a = [i for i, ln in enumerate(lines) if A_SIG in ln]
i_b = [i for i, ln in enumerate(lines) if B_SIG in ln]
if len(i_a) != 1 or len(i_b) != 1 or i_a[0] >= i_b[0]:
    sys.exit('锚点异常: A=%r B=%r' % (i_a, i_b))
ia, ib = i_a[0], i_b[0]

# 断言 1：A 段前一行应为编者注（明茨）——即当前缺空行
if MINTZ_SIG not in lines[ia - 1]:
    sys.exit('A 段前一行不是明茨编者注: %s' % lines[ia - 1][:50])
# 断言 2：B 段后两行均为空行（连续双空行）
if lines[ib + 1].strip() or lines[ib + 2].strip():
    sys.exit('B 段后不是连续两个空行')

# A 前补空行；B 后保留第一个空行、丢弃第二个
new = lines[:ia] + ['', lines[ia]] + lines[ia + 1:ib + 1] + [lines[ib + 1]] + lines[ib + 3:]
log.append('新行数=%d（净 0：+1 空行 / -1 空行）' % len(new))
if len(new) != len(lines):
    sys.exit('行数应不变')

ca, cb = Counter(lines), Counter(new)
d = (cb - ca) + (ca - cb)
if d:
    sys.exit('多重集应完全不变，实际差异 %r' % list(d.items())[:4])
log.append('多重集守恒（纯重排）')

if APPLY:
    io.open(P, 'w', encoding='utf-8', newline='').write(nl.join(new))
    log.append('>>> 已写盘')
else:
    log.append('(dry-run)')

io.open(os.path.join(D, '_r58b_fix_out.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(log))
print('\n'.join(log))
