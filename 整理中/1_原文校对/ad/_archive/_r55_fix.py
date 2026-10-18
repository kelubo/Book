# r55：修正 L486 收缩次数——把无据的"5--15 次"换成玛斯特斯和约翰逊的强度分级表述
#   依据：Meston, Levin, Sipski, Hull & Heiman, Women's Orgasm,
#         Annual Review of Sex Research 2004 转述 M&J(1966) 原始分级：
#         轻微 3-5 次 / 一般 5-8 次 / 强烈 8-12 次；间隔 0.8 秒。
#   用户选定方案 B（强度分级表述）。
# 用法：python _r55_fix.py [apply]   默认 dry-run
import io, os, sys, shutil, collections

D = 'D:/Git/Book/整理中/1_原文校对/ad/'
F = D + 'book.tex'
BK = D + '_backup_r55/'
OUT = D + '_r55_fix_out.txt'

OLD_CLAUSE = '女性一般会体验到5--15次收缩；具体次数主要取决于性高潮的强度。'
NEW_CLAUSE = '阴道外 1/3 的节律性收缩次数随性高潮的强度而异：轻微的高潮约 3--5 次，一般的高潮约 5--8 次，强烈的高潮可达 8--12 次，这一分级出自玛斯特斯和约翰逊的观察。'
SIG = '有些女性会随着骨盆肌肉的收缩向上挺起臀部'

APPLY = len(sys.argv) > 1 and sys.argv[1] == 'apply'
log = []
txt = io.open(F, encoding='utf-8', newline='').read()
lines = txt.splitlines(keepends=True)
log.append('原行数 = %d' % len(lines))

# 1. 定位与唯一性
if txt.count(SIG) != 1:
    sys.exit('签名命中 %d 次（应为 1）' % txt.count(SIG))
if txt.count(OLD_CLAUSE) != 1:
    sys.exit('旧子句命中 %d 次（应为 1）' % txt.count(OLD_CLAUSE))
i = next(k for k, ln in enumerate(lines) if SIG in ln)
if OLD_CLAUSE not in lines[i]:
    sys.exit('旧子句不在签名所在行')
log.append('定位 = L%d（签名与旧子句均唯一）' % (i + 1))
log.append('旧：%s' % lines[i].rstrip('\r\n'))

# 2. 该行其余部分必须原样保留
head, tail = lines[i].split(OLD_CLAUSE)
if not head.startswith(SIG):
    sys.exit('前段异常：%r' % head[:40])
if '阴蒂会缩回到包皮里' not in tail:
    sys.exit('后段异常：%r' % tail[:40])
log.append('前段（挺起臀部句）与后段（阴蒂缩回句）原样保留')

# 3. 新行自检
new_line = head + NEW_CLAUSE + tail
for must in ['3--5 次', '5--8 次', '8--12 次', '玛斯特斯和约翰逊']:
    if must not in new_line:
        sys.exit('新行缺少：%s' % must)
for bad in ['5--15', '5～15', '**']:
    if bad in new_line:
        sys.exit('新行仍含：%s' % bad)
if '%' in new_line:
    sys.exit('新行含裸百分号')
log.append('新行自检通过：含三级数值与出处，无 5--15 / 无 ** / 无裸百分号')
log.append('新：%s' % new_line.rstrip('\r\n'))

# 4. 构造 + 守恒
eol = '\r\n' if lines[i].endswith('\r\n') else '\n'
new = lines[:i] + [new_line] + lines[i + 1:]
c_old, c_new = collections.Counter(lines), collections.Counter(new)
if (c_new - c_old) != collections.Counter([new_line]):
    sys.exit('新增行异常')
if (c_old - c_new) != collections.Counter([lines[i]]):
    sys.exit('删除行异常')
if len(new) != len(lines):
    sys.exit('行数应不变，实际 %d -> %d' % (len(lines), len(new)))
log.append('守恒校验通过：仅替换 L%d 一行，行数 %d 不变' % (i + 1, len(new)))

# 5. 全卷残留检查（只针对"收缩次数"语境，避免误命中 85--150 大卡 这类无关连字符）
body = ''.join(new)
for pat in ['5--15次', '5～15次', '体验到5']:
    if pat in body:
        sys.exit('全卷仍残留：%s' % pat)
if OLD_CLAUSE in body:
    sys.exit('旧子句仍残留')
log.append('全卷残留检查通过：5--15次 / 5～15次 / 旧子句 均 0 次')

# 6. 落盘
if APPLY:
    if not os.path.isdir(BK):
        os.makedirs(BK)
    if not os.path.exists(BK + 'book.tex'):
        shutil.copy2(F, BK + 'book.tex')
        log.append('备份 -> _backup_r55/book.tex')
    with io.open(BK + 'book_r55_pre.tex', 'w', encoding='utf-8', newline='') as fh:
        fh.write(txt)
    log.append('备份 -> _backup_r55/book_r55_pre.tex')
    with io.open(F, 'w', encoding='utf-8', newline='') as fh:
        fh.write(''.join(new))
    log.append('已写盘')
else:
    log.append('【dry-run】未写盘')

log.append('')
log.append('--- 改后上下文 ---')
for k, ln in enumerate(new[i - 2:i + 3]):
    log.append('   L%-5d %s' % (i - 1 + k, ln.rstrip('\r\n')[:110] or '<空行>'))

with io.open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('\n'.join(log))
print('OK APPLY=%s' % APPLY)
