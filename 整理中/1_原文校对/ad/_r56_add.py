# -*- coding: utf-8 -*-
"""r56：为《女性的性反应》高潮期补充两条科学修正
   ① 收缩次数与快感强度无可靠对应（分级缺数据支持）
   ② 收缩并非每次高潮都出现（常见但非必要条件）
用法：python _r56_add.py          # dry-run
      python _r56_add.py apply    # 落盘
"""
import io, os, shutil, sys

D = 'D:/Git/Book/整理中/1_原文校对/ad/'
SRC = D + 'book.tex'
BAK = D + '_backup_r56/book.tex'
OUT = D + '_r56_add_out.txt'
APPLY = len(sys.argv) > 1 and sys.argv[1] == 'apply'
EOL = '\r\n'
log = []


def fail(msg):
    log.append('【失败】' + msg)
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(log))
    sys.exit(1)


# ---------- 新增内容 ----------
SIG_ANCHOR = '有些女性会随着骨盆肌肉的收缩向上挺起臀部'
SIG_NEXT = '性高潮出现后，女性背部和足部的肌肉都会出现不自主痉挛'

P1 = ('收缩的次数与性高潮的强烈程度之间，其实并没有可靠的对应关系。'
      '用阴道内压力记录所做的生理研究，未能建立起收缩次数与主观快感强度之间的关联；'
      '玛斯特斯和约翰逊提出的上述分级，在后来的综述中也被注明缺乏数据支持。')

P2 = ('阴道与骨盆的节律性收缩也不是每次性高潮都会出现。'
      '有研究在持续时间较长的性高潮中记录到十几次、最多三十余次的不规则骨盆收缩，也有受试者完全没有收缩；'
      '在一项针对数百名女性的问卷调查中，约六成受访者自述在高潮时感受到收缩或搏动。'
      '可见收缩虽然常见，却并非性高潮的必要条件。')

NEW_TXT = [P1, P2]

# ---------- 读取 ----------
raw = io.open(SRC, encoding='utf-8', newline='').read()
lines = raw.splitlines(keepends=True)
log.append('读入 book.tex：行数 %d，字节 %d' % (len(lines), os.path.getsize(SRC)))
log.append('bare LF = %d' % sum(1 for ln in raw.split('\n')[:-1] if not ln.endswith('\r')))

# ---------- 前置校验 ----------
idx = [i for i, ln in enumerate(lines) if SIG_ANCHOR in ln]
if len(idx) != 1:
    fail('锚签名命中 %d 次（应为 1）' % len(idx))
i = idx[0]
log.append('锚点 L%d：%s' % (i + 1, lines[i].strip()[:50]))

if lines[i + 1].strip() != '':
    fail('锚段后一行不是空行：%r' % lines[i + 1][:40])
if not lines[i + 2].startswith(SIG_NEXT):
    fail('锚段后第二行不是预期段落：%r' % lines[i + 2][:40])
if not lines[i + 1].endswith(EOL):
    fail('锚段后空行行尾异常（期望 CRLF）')
log.append('落点：L%d 之前（锚段与下一段之间）' % (i + 3))

for txt in NEW_TXT:
    if '**' in txt:
        fail('新增内容含 markdown 加粗 **')
    if '%' in txt:
        fail('新增内容含裸 %')
    if '\n' in txt or '\r' in txt:
        fail('新增内容含内部换行')
    if txt.count('收缩') == 0:
        fail('新增内容主题异常')
    if raw.count(txt) != 0:
        fail('新增内容已存在于文件中：%s' % txt[:20])
log.append('新增 2 段：长度 %d / %d 字，无 markdown 加粗 / 无裸百分号 / 无换行 / 均不存在于原文' % (len(P1), len(P2)))

# ---------- 构造 ----------
block = [P1 + EOL, EOL, P2 + EOL, EOL]
new = lines[:i + 2] + block + lines[i + 2:]

# ---------- 落盘后校验 ----------
if len(new) != len(lines) + 4:
    fail('行数增量异常：预期 +4，实际 %+d' % (len(new) - len(lines)))
if new[:i + 2] != lines[:i + 2] or new[i + 2 + 4:] != lines[i + 2:]:
    fail('锚点前后内容被意外改动（差分不守恒）')
if new[i + 2] != P1 + EOL or new[i + 3] != EOL or new[i + 4] != P2 + EOL or new[i + 5] != EOL:
    fail('插入块内容/顺序不符')
joined = ''.join(new)
if joined.count(P1) != 1 or joined.count(P2) != 1:
    fail('新增段落在结果中出现次数不为 1')
if sum(1 for ln in joined.split('\n')[:-1] if not ln.endswith('\r')) != 0:
    fail('结果出现 bare LF')
log.append('结果行数 = %d（%+d）' % (len(new), len(new) - len(lines)))
log.append('差分守恒：锚点前后逐行完全一致，新增内容各出现 1 次')

# ---------- 落盘 ----------
if APPLY:
    if not os.path.exists(BAK):
        fail('备份不存在，拒绝落盘')
    io.open(SRC, 'w', encoding='utf-8', newline='').write(joined)
    log.append('已落盘：%s' % SRC)
else:
    log.append('（dry-run，未写盘）')

log.append('')
log.append('--- 插入后 L%d ~ L%d ---' % (i + 1, i + 8))
for k in range(i, min(i + 8, len(new))):
    log.append('  L%-5d %s' % (k + 1, new[k].rstrip('\r\n')[:80] or '（空行）'))

io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(log))
print('\n'.join(log))
