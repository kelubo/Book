# -*- coding: utf-8 -*-
"""r50：book.tex《男性的性反应》节内两段通用总览上移归位（方案 A）
   - 只搬位置，正文一字不改；用内容签名定位，绝不手打正文
   - L527（兴奋期子节内）L536（平台期子节内） -> \subsection 概述区（L519 之后）
"""
import io, os, shutil, sys

D = 'D:/Git/Book/整理中/1_原文校对/ad/'
SRC = D + 'book.tex'
BK = D + '_backup_r50/'
LOG = []

SIG_P1 = '兴奋期是性反应周期的第一个阶段'   # 原 L527
SIG_P2 = '平台期是兴奋与高潮之间的高原段'   # 原 L536
SIG_ANCHOR = '值得强调的是交感神经的角色'    # 原 L519

def fail(msg):
    io.open(D + '_r50_move_out.txt', 'w', encoding='utf-8', newline='\n').write(
        '\n'.join(LOG + ['!! ABORT: ' + msg]))
    sys.exit(1)

content = io.open(SRC, encoding='utf-8', newline='').read()
eol = '\r\n' if '\r\n' in content else '\n'
lines = content.splitlines(keepends=True)
LOG.append('原文件行数 = %d ; EOL = %s' % (len(lines), repr(eol)))

def find(sig):
    hits = [i for i, ln in enumerate(lines) if ln.startswith(sig)]
    if len(hits) != 1:
        fail('签名 %s 命中 %d 次（须唯一）' % (sig, len(hits)))
    return hits[0]

i1 = find(SIG_P1)
i2 = find(SIG_P2)
ia = find(SIG_ANCHOR)
LOG.append('定位：P1(兴奋期通用段)=L%d  P2(平台期通用段)=L%d  ANCHOR(交感神经段)=L%d'
           % (i1 + 1, i2 + 1, ia + 1))

def blank(i):
    return 0 <= i < len(lines) and lines[i].strip() == ''

def heading(i):
    return 0 <= i < len(lines) and lines[i].lstrip().startswith('\\sub')

if not (i1 > ia and i2 > ia):
    fail('段落不在锚点之后，行号顺序异常（i1=%d i2=%d ia=%d）' % (i1, i2, ia))
if not (blank(i1 + 1) and heading(i1 + 2)):
    fail('P1 不是所在子节的最后一段（后接 %r）' % lines[i1 + 2][:40])
if not (blank(i1 - 1)):
    fail('P1 之前不是空行')
if not (blank(i2 + 1) and heading(i2 + 2)):
    fail('P2 不是所在子节的最后一段（后接 %r）' % lines[i2 + 2][:40])
LOG.append('结构前置校验通过：')
LOG.append('  P1 后接 -> %s' % lines[i1 + 2].strip())
LOG.append('  P2 后接 -> %s' % lines[i2 + 2].strip())
LOG.append('  P2 之前连续空行 = %d' % sum(1 for j in range(i2 - 1, i2 - 6, -1) if blank(j)))

payload1 = lines[i1]
payload2 = lines[i2]

# 删除集合：段落行 + 其后空行；并清理段落上方多余空行（保留一个）
skip = set()
for k in (i1, i2):
    skip.add(k)
    if blank(k + 1):
        skip.add(k + 1)
    j = k - 1
    while blank(j) and blank(j - 1):
        skip.add(j)
        j -= 1
LOG.append('删除行数 = %d（%s）' % (len(skip), sorted(x + 1 for x in skip)))

COMMENT = ('% —— r50 迁移：以下两段原位于《兴奋期》《平台期》子节内部，实为四期通用规律（男女并列），'
           '上移至此，与《女性的性反应》的概览段结构对齐 ——' + eol)

new = []
for i, ln in enumerate(lines):
    if i in skip:
        continue
    new.append(ln)
    if i == ia:
        new.append(eol)
        new.append(COMMENT)
        new.append(payload1)
        new.append(eol)
        new.append(payload2)

out = ''.join(new)
LOG.append('新文件行数 = %d ; 增量 = %+d' % (len(new), len(new) - len(lines)))

# 内容守恒：正文字符应完全一致（仅位置变化 + 1 行注释）
def body(s):
    return [x for x in s.splitlines() if x.strip() and not x.lstrip().startswith('%')]
b_old, b_new = sorted(body(content)), sorted(body(out))
LOG.append('正文行多重集一致 = %s（old %d / new %d）' % (b_old == b_new, len(b_old), len(b_new)))
if b_old != b_new:
    fail('正文行集合发生变化，疑似误删/误改')

if not os.path.isdir(BK):
    os.makedirs(BK)
shutil.copy2(SRC, BK + 'book.tex')
LOG.append('备份 -> %sbook.tex' % BK)

io.open(SRC, 'w', encoding='utf-8', newline='').write(out)
LOG.append('已写入 %s' % SRC)

# 新位置复核
nl = out.splitlines()
for tag, sig in (('P1', SIG_P1), ('P2', SIG_P2)):
    for i, ln in enumerate(nl):
        if ln.startswith(sig):
            LOG.append('新位置 %s -> L%d（上一行 %r / 下一行 %r）'
                       % (tag, i + 1, nl[i - 1][:30], nl[i + 2][:30]))
            break
for i, ln in enumerate(nl):
    if ln.lstrip().startswith('\\subsubsection{兴奋期}'):
        LOG.append('上下文 L%d-L%d:' % (i - 6, i + 1))
        for j in range(max(0, i - 6), i + 1):
            LOG.append('  L%-5d %s' % (j + 1, nl[j][:90]))
        break

io.open(D + '_r50_move_out.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(LOG))
