# -*- coding: utf-8 -*-
"""r57b：补修 female.tex L11317（妊娠黄体「妊。个月」→「妊娠3个月」）"""
import io, os, re, shutil, sys

D = 'D:/Git/Book/整理中/1_原文校对/ad/'
SRC = D + 'female.tex'
BAK = D + '_backup_r57/female_pre2.tex'
OUT = D + '_r57b_fix_out.txt'
APPLY = len(sys.argv) > 1 and sys.argv[1] == 'apply'
log = []


def fail(msg):
    log.append('【失败】' + msg)
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(log))
    sys.exit(1)


raw = io.open(SRC, encoding='utf-8', newline='').read()
lines = raw.splitlines(keepends=True)
log.append('读入 female.tex：行数 %d' % len(lines))

i = 11316
if '妊娠黄体' not in lines[i]:
    fail('L11317 不是妊娠黄体句：%r' % lines[i][:120])
pat = r'可维持到妊。个月左右'
if len(re.findall(pat, lines[i])) != 1:
    fail('L11317 目标片段匹配 %d 次' % len(re.findall(pat, lines[i])))

new = list(lines)
before = new[i]
new[i] = re.sub(pat, '可维持到妊娠3个月左右', new[i], count=1)
log.append('L11317')
log.append('  旧：%s' % before.rstrip('\r\n'))
log.append('  新：%s' % new[i].rstrip('\r\n'))
log.append('  据：妊娠黄体分泌孕激素维持早期妊娠至约10周（3个月），此后由胎盘接替')

if len(new) != len(lines):
    fail('行数变化')
changed = [k + 1 for k in range(len(lines)) if new[k] != lines[k]]
if changed != [11317]:
    fail('改动行不符：%s' % changed)
res = ''.join(new)
if '妊。个月' in res:
    fail('目标片段仍残留')
log.append('目标片段残留检查通过')
if sum(1 for ln in res.split('\n')[:-1] if not ln.endswith('\r')) != 0:
    fail('bare LF')
if res.count('\t') != raw.count('\t'):
    fail('制表符数量变化')
log.append('校验通过：行数不变（%d）；改动行恰为 L11317；目标片段无残留' % len(new))

if APPLY:
    if not os.path.exists(BAK):
        shutil.copy2(SRC, BAK)
    io.open(SRC, 'w', encoding='utf-8', newline='').write(res)
    log.append('已落盘：%s' % SRC)
else:
    log.append('（dry-run，未写盘）')

io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(log))
print('\n'.join(log))
