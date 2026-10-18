# -*- coding: utf-8 -*-
"""r51 执行器：把高潮期、消退期两段通用总览插到《男性的性反应》总览区末尾
   用法：python _r51_insert.py        -> dry-run 校验
         python _r51_insert.py apply  -> 写盘
"""
import io, os, shutil, sys

D = 'D:/Git/Book/整理中/1_原文校对/ad/'
SRC = D + 'book.tex'
BK = D + '_backup_r51/'
APPLY = len(sys.argv) > 1 and sys.argv[1] == 'apply'

sys.path.insert(0, D)
from _r51_new import NEW

ANCHOR = '平台期是兴奋与高潮之间的高原段'   # r50 上移的第二段（总览区最后一段）
ORDER = ['gaochao', 'xiaotui']

content = io.open(SRC, encoding='utf-8', newline='').read()
eol = '\r\n' if '\r\n' in content else '\n'
lines = content.splitlines(keepends=True)
log = ['模式 = %s ; 原行数 = %d ; EOL = %r' % ('APPLY' if APPLY else 'DRY-RUN', len(lines), eol)]

hits = [i for i, ln in enumerate(lines) if ln.startswith(ANCHOR)]
if len(hits) != 1:
    sys.exit('锚命中数 = %d（须为 1）' % len(hits))
pos = hits[0]
log.append('锚 L%d: %s' % (pos + 1, lines[pos].strip()[:40]))

# 结构校验：锚段是总览区最后一段（下一非空行应为 \subsubsection{兴奋期}）
nxt = pos + 1
while nxt < len(lines) and not lines[nxt].strip():
    nxt += 1
if not lines[nxt].lstrip().startswith('\\subsubsection{兴奋期}'):
    sys.exit('锚段之后不是 \\subsubsection{兴奋期}，实际: %r' % lines[nxt][:50])
log.append('锚后非空行 L%d = %s' % (nxt + 1, lines[nxt].strip()))
if not lines[pos + 1].strip() == '':
    sys.exit('锚段之后不是空行')

# 前置校验：锚段之前应已存在 r50 迁移的兴奋期通用段
if not any(lines[j].startswith('兴奋期是性反应周期的第一个阶段') for j in range(max(0, pos - 6), pos)):
    sys.exit('未找到兴奋期通用段，总览区结构异常')

# 内容校验：无裸 %、无 markdown 加粗、无 ** 
for k in ORDER:
    t = NEW[k]
    if '**' in t:
        sys.exit('%s 含 markdown 加粗' % k)
    if '%' in t:
        sys.exit('%s 含未转义 %%' % k)
    if '\n' in t.strip():
        sys.exit('%s 含内部换行' % k)
log.append('内容校验通过：%s' % ORDER)

# 位置去重：若已插入过则中止
for k in ORDER:
    if any(NEW[k][:20] in ln for ln in lines):
        sys.exit('%s 已存在于文件中' % k)

ins = ['', NEW['gaochao'], '', NEW['xiaotui']]
newlines = lines[:pos + 1] + [x + eol for x in ins] + lines[pos + 1:]
log.append('增量 = %+d 行（预期 +4）' % (len(newlines) - len(lines)))
log.append('预期新行数 = %d' % len(newlines))
if len(newlines) - len(lines) != 4:
    sys.exit('增量异常')

for j in range(pos - 1, pos + 7):
    src = lines[j].rstrip('\r\n') if j < len(lines) else ''
    log.append('  old L%-5d %s' % (j + 1, src[:70]))
for j in range(pos - 1, pos + 11):
    src = newlines[j].rstrip('\r\n') if j < len(newlines) else ''
    log.append('  new L%-5d %s' % (j + 1, src[:70]))

if APPLY:
    if not os.path.isdir(BK):
        os.makedirs(BK)
    shutil.copy2(SRC, BK + 'book.tex')
    log.append('备份 -> %sbook.tex' % BK)
    io.open(SRC, 'w', encoding='utf-8', newline='').write(''.join(newlines))
    chk = io.open(SRC, encoding='utf-8', newline='').read()
    bare = sum(1 for ln in chk.split('\n')[:-1] if not ln.endswith('\r'))
    log.append('已写盘 ; 新行数 = %d ; bare LF = %d' % (len(chk.splitlines()), bare))

io.open(D + '_r51_insert_out.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(log))
