# r54：《女性的性反应》开头概览瘦身
#   原 L435 = 四期条列的"概览段"，其中 4 项细节与后面四个 \subsubsection 全面重复
#             （阴道润滑/阴蒂回缩·高潮平台/节律性收缩/消退期缓慢）；
#             仅"润滑 10--30 秒"与"情绪与安全感影响更大"为后文所无。
#   处理：L435 换成一句只保留独有信息；L436（情境依赖，唯一无重复）原样保留。
# 用法：python _r54_trim.py [apply]   默认 dry-run
import io, os, sys, shutil, collections

D = 'D:/Git/Book/整理中/1_原文校对/ad/'
F = D + 'book.tex'
BK = D + '_backup_r54/'
OUT = D + '_r54_trim_out.txt'

SIG_OLD = '女性的性反应有几个值得记住的生理特征'
SIG_KEEP = '与男性相比，女性的反应对情境的依赖更明显'
SIG_LEAD = '在玛斯特斯和约翰逊提出的四阶段框架下'

NEW = '其中最先出现、也最容易观察到的变化是阴道润滑：性刺激开始后约 10--30 秒即会出现，其速度受情绪与安全感影响远大于受物理刺激影响。'

# 被删细节 → 后文落点（仅用于日志留痕）
DUP = [
    ('信号是阴道润滑', '女性节·兴奋期'),
    ('阴蒂回缩到包皮下', '女性节·平台期'),
    ('节律性收缩为特征（一般 3--15 次）', '女性节·高潮期'),
    ('消退期通常比男性缓慢', '女性节·消退期'),
]

APPLY = len(sys.argv) > 1 and sys.argv[1] == 'apply'
log = []
txt = io.open(F, encoding='utf-8', newline='').read()
lines = txt.splitlines(keepends=True)
log.append('原行数 = %d' % len(lines))

# 1. 签名唯一性
for s in (SIG_OLD, SIG_KEEP, SIG_LEAD):
    c = txt.count(s)
    if c != 1:
        sys.exit('签名命中 %d 次（应为 1）：%s' % (c, s))
log.append('三条签名命中数均为 1')

# 2. 定位
i = next(k for k, ln in enumerate(lines) if ln.startswith(SIG_OLD))
if not lines[i + 1].startswith(SIG_KEEP):
    sys.exit('L%d 之后不是 L436，实际 %r' % (i + 1, lines[i + 1][:40]))
if not (lines[i - 1].strip() == '' and lines[i - 2].startswith(SIG_LEAD)):
    sys.exit('L%d 之前结构异常：%r / %r' % (i + 1, lines[i - 2][:40], lines[i - 1][:40]))
log.append('待替换 = L%d（前为节导语+空行，后为 L436 原样保留）' % (i + 1))
for d, w in DUP:
    if d not in lines[i]:
        sys.exit('待删段落中未找到该重复项：%s' % d)
log.append('重复项确认（替换后由后文承担）：')
for d, w in DUP:
    log.append('   - %-46s -> %s' % (d, w))
for u in ['10--30 秒', '情绪与安全感']:
    if u not in lines[i]:
        sys.exit('待保留的独有信息缺失：%s' % u)
log.append('独有信息确认（保留）：阴道润滑 10--30 秒、情绪与安全感的影响权重')

# 3. 新句自检
if '**' in NEW or '%' in NEW or '\n' in NEW:
    sys.exit('新句含 ** / 裸 % / 换行')
log.append('新句无 ** 加粗 / 无裸百分号 / 无换行，长度 %d 字' % len(NEW))

# 4. 构造 + 守恒
eol = '\r\n' if lines[i].endswith('\r\n') else '\n'
new = lines[:i] + [NEW + eol] + lines[i + 1:]
old_line = lines[i]
c_old, c_new = collections.Counter(lines), collections.Counter(new)
if (c_new - c_old) != collections.Counter([NEW + eol]):
    sys.exit('新增行异常')
if (c_old - c_new) != collections.Counter([old_line]):
    sys.exit('删除行异常')
if len(new) != len(lines):
    sys.exit('行数应不变，实际 %d -> %d' % (len(lines), len(new)))
log.append('守恒校验通过：仅替换 L%d 一行，行数 %d 不变' % (i + 1, len(new)))

# 5. 落盘
if APPLY:
    if not os.path.isdir(BK):
        os.makedirs(BK)
    if not os.path.exists(BK + 'book.tex'):
        shutil.copy2(F, BK + 'book.tex')
        log.append('备份 -> _backup_r54/book.tex')
    with io.open(BK + 'book_r54_pre.tex', 'w', encoding='utf-8', newline='') as fh:
        fh.write(txt)
    log.append('备份 -> _backup_r54/book_r54_pre.tex')
    with io.open(F, 'w', encoding='utf-8', newline='') as fh:
        fh.write(''.join(new))
    log.append('已写盘')
else:
    log.append('【dry-run】未写盘')

log.append('')
log.append('--- 改后该区域 ---')
for k, ln in enumerate(new[i - 4:i + 6]):
    log.append('   L%-5d %s' % (i - 3 + k, ln.rstrip('\r\n')[:74] or '<空行>'))

with io.open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('\n'.join(log))
print('OK APPLY=%s' % APPLY)
