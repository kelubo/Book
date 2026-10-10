# -*- coding: utf-8 -*-
# r58: 高潮差距 / 性反应是同步的吗？ 两节互加交叉引用
import io, sys, os
from collections import Counter

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, 'book.tex')
APPLY = 'apply' in sys.argv

A_LINE = '高潮差距讨论的是“能否达到高潮”的概率之差；而即便双方都达到了高潮，节奏上也未必合拍——这就引出了下一节的话题：性反应的同步。'
B_LINE = '上一节处理的是概率层面的差距——“能不能达到高潮”；本节转向时间层面——两性的反应节奏能否合拍。'

raw = io.open(P, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in raw else '\n'
lines = raw.split(nl)
log = []
log.append('行数=%d  nl=%s' % (len(lines), repr(nl)))

# 锚点：两个 section 标题行
i_a = [i for i, ln in enumerate(lines) if ln.strip() == r'\section{性反应是同步的吗？}']
if len(i_a) != 1:
    sys.exit('同步节标题命中 %d 次' % len(i_a))
i_sec = i_a[0]
log.append('同步节标题在 L%d' % (i_sec + 1))

# 结构断言：标题前一行、后一行均为空行
if lines[i_sec - 1].strip() or lines[i_sec + 1].strip():
    sys.exit('标题前后行不是空行')

# 前一段应是编者注（明茨）
if '成为阴蒂' not in lines[i_sec - 2]:
    sys.exit('标题前第二行不是明茨编者注，实际: %s' % lines[i_sec - 2][:60])

# B: 标题之后插入引言段（标题、空行、新段、空行）
# A: 标题之前（即原空行位置之前）插入过渡段（新段、空行）→ 新段位于编者注段与标题之间
new = lines[:i_sec - 1]          # ...编者注段（不含其后空行）
new += [A_LINE, '']              # A 段 + 空行
new += [lines[i_sec], '']        # 标题 + 空行
new += [B_LINE, '']              # B 段 + 空行
new += lines[i_sec + 1:]         # 原正文

log.append('新行数=%d（增量 %d）' % (len(new), len(new) - len(lines)))
if len(new) - len(lines) != 4:
    sys.exit('增量异常：预期 +4')

# 守恒：删除 2 空行的位置重排，其余行必须一致
old_wo = lines[:i_sec - 1] + [lines[i_sec]] + lines[i_sec + 1:]
new_wo = new[:i_sec - 1] + new[i_sec + 1:i_sec + 4] + new[i_sec + 5:]
ca, cb = Counter(lines), Counter(new)
d = (cb - ca) + (ca - cb)
expect = Counter({A_LINE: 1, B_LINE: 1, '': 2})
if d - expect:
    sys.exit('差异异常: %r' % list((d - expect).items())[:4])
log.append('多重集守恒：新增恰为 A/B 两段 + 2 空行')

# 新段质量
for x in (A_LINE, B_LINE):
    if '**' in x or '%' in x or '\n' in x:
        sys.exit('新段含 ** / 裸 %% / 换行')
    if x in raw:
        sys.exit('新段已存在于原文')
log.append('新段无 ** / 无裸 %% / 原文不存在，长度 %d / %d 字' % (len(A_LINE), len(B_LINE)))

if APPLY:
    io.open(P, 'w', encoding='utf-8', newline='').write(nl.join(new))
    log.append('>>> 已写盘')
else:
    log.append('(dry-run，未写盘；加 apply 参数落盘)')

out = os.path.join(D, '_r58_xref_out.txt')
io.open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(log))
print('\n'.join(log))
