# r53：《阶段性的性反应》删除 r50/r51 新增的过渡语 + 四段总览，只留一句纲领
# 用法：python _r53_trim.py [apply]   默认 dry-run
import io, os, sys, shutil, collections

D = 'D:/Git/Book/整理中/1_原文校对/ad/'
F = D + 'book.tex'
BK = D + '_backup_r53/'
OUT = D + '_r53_trim_out.txt'

NEW = '四个阶段在两性之间是同构的，差别只在于以哪套器官为中心；各期在两性身上的具体变化，分别在本章后两节中展开。'

SIG_LEAD = '四个阶段的生理机制在两性之间是同构的'
SIG = [
    '兴奋期是性反应周期的第一个阶段',
    '平台期是兴奋与高潮之间的高原段',
    '高潮期是整个周期中持续时间最短',
    '消退期是身体回到性唤起前状态',
]
DEP = dict(zip(SIG, ['兴奋期', '平台期', '高潮期', '消退期']))

APPLY = len(sys.argv) > 1 and sys.argv[1] == 'apply'
log = []

txt = io.open(F, encoding='utf-8', newline='').read()
lines = txt.splitlines(keepends=True)
log.append('原行数 = %d' % len(lines))

# ---------- 1. 签名唯一性 ----------
for s in [SIG_LEAD] + SIG:
    c = txt.count(s)
    if c != 1:
        sys.exit('签名命中 %d 次（应为 1）：%s' % (c, s))
log.append('5 条签名命中数均为 1')

# ---------- 2. 定位块首 ----------
i = next(k for k, ln in enumerate(lines) if ln.startswith(SIG_LEAD))
if not (lines[i - 1].strip() == '' and lines[i - 2].startswith('\\end{figure}')):
    sys.exit('块首前置结构异常：%r / %r' % (lines[i - 2][:30], lines[i - 1][:30]))
log.append('块首 = L%d（前置为 \\end{figure} + 空行）' % (i + 1))

# ---------- 3. 定位块尾 ----------
j = next(k for k, ln in enumerate(lines) if ln.startswith(SIG[-1]))
if not (lines[j + 1].strip() == '' and lines[j + 2].startswith('\\subsection{女性的性反应}')):
    sys.exit('块尾后置结构异常：%r / %r' % (lines[j + 1][:30], lines[j + 2][:30]))
log.append('块尾 = L%d（后置为 空行 + \\subsection{女性的性反应}）' % (j + 1))

# ---------- 4. 块内必须恰为「过渡语 + 四段」9 行 ----------
block = lines[i:j + 1]
if len(block) != 9:
    sys.exit('块长度 %d 行，应为 9 行' % len(block))
for slot, (line, sig) in enumerate(zip([block[0], block[2], block[4], block[6], block[8]], [SIG_LEAD] + SIG)):
    if not line.startswith(sig):
        sys.exit('块内第 %d 个非空行前缀不符：%r' % (slot + 1, line[:30]))
for k in (1, 3, 5, 7):
    if block[k].strip() != '':
        sys.exit('块内 L%d 不是空行' % (i + k + 1))
log.append('块内结构校验通过：过渡语 + 兴奋/平台/高潮/消退 四段，间隔空行')
log.append('将删除的块（L%d–L%d）：' % (i + 1, j + 1))
for k, ln in enumerate(block):
    log.append('   - L%-5d %s' % (i + k + 1, (ln.rstrip('\r\n')[:56] or '<空行>')))

# ---------- 5. 构造新内容 ----------
eol = '\r\n' if lines[i - 1].endswith('\r\n') else '\n'
new = lines[:i] + [NEW + eol] + lines[j + 1:]

# ---------- 6. 守恒校验：差异必须恰为「删 9 行、增 1 行」 ----------
c_old, c_new = collections.Counter(lines), collections.Counter(new)
only_new = c_new - c_old
only_old = c_old - c_new
if only_new != collections.Counter([NEW + eol]):
    sys.exit('新增行异常：%r' % list(only_new))
if only_old != collections.Counter(block):
    sys.exit('删除行与预期块不符：%r' % list(only_old)[:3])
if len(new) != len(lines) - 8:
    sys.exit('行数变化异常：%d → %d（应为 -8）' % (len(lines), len(new)))
log.append('守恒校验通过：仅删块内 9 行、仅增纲领 1 行，行数 %d → %d' % (len(lines), len(new)))

# ---------- 7. 残留检查 ----------
body = ''.join(new)
for s in SIG + [SIG_LEAD]:
    if s in body:
        sys.exit('删除后仍残留：%s' % s)
log.append('残留检查通过：五处旧文本已全部不存在')
if '**' in NEW or '%' in NEW:
    sys.exit('纲领句含 ** 或裸 %')
log.append('纲领句无 ** / 无裸 %')

# ---------- 8. 落盘 ----------
if APPLY:
    if not os.path.isdir(BK):
        os.makedirs(BK)
    if not os.path.exists(BK + 'book.tex'):
        shutil.copy2(F, BK + 'book.tex')
        log.append('备份 -> _backup_r53/book.tex')
    with io.open(BK + 'book_r53_pre.tex', 'w', encoding='utf-8', newline='') as fh:
        fh.write(txt)
    log.append('备份 -> _backup_r53/book_r53_pre.tex')
    with io.open(F, 'w', encoding='utf-8', newline='') as fh:
        fh.write(''.join(new))
    log.append('已写盘：%s' % F)
else:
    log.append('【dry-run】未写盘')

log.append('')
log.append('--- 改后该区域预览 ---')
for k, ln in enumerate(new[i - 6:i + 6]):
    log.append('   L%-5d %s' % (i - 5 + k, ln.rstrip('\r\n')[:60]))

with io.open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('\n'.join(log))
print('OK  APPLY=%s' % APPLY)
