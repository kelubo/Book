# -*- coding: utf-8 -*-
"""r52：把《男性的性反应》里的"男女并列四期通用总览"（当前 L521-L530）
   整体移入《阶段性的性反应》末尾（图之后）。不新增注释行（用户已删除 r50 注释）。
   用法：python _r52_move.py [apply]
"""
import io, os, shutil, sys

D = 'D:/Git/Book/整理中/1_原文校对/ad/'
SRC = D + 'book.tex'
BK = D + '_backup_r52/'
APPLY = len(sys.argv) > 1 and sys.argv[1] == 'apply'
log = []

SIG_LEAD = '四个阶段在两性之间是同构的'
SIG_HEAD = '\\subsubsection{兴奋期}'
SIG_DEST = '\\subsection{女性的性反应}'
SIG_FIGEND = '\\end{figure}'
PREFIX = ['兴奋期是性反应周期的第一个阶段',
          '平台期是兴奋与高潮之间的高原段',
          '高潮期是整个周期中持续时间最短',
          '消退期是身体回到性唤起前状态的收尾阶段']
NEW_LEAD = ('四个阶段的生理机制在两性之间是同构的，差别只在于以哪套器官为中心：'
            '下面逐期说明四期共有的规律，而各性别在每一期中的具体变化，'
            '分别在《女性的性反应》与《男性的性反应》两节中展开。')

content = io.open(SRC, encoding='utf-8', newline='').read()
eol = '\r\n' if '\r\n' in content else '\n'
lines = content.splitlines(keepends=True)
log.append('模式 = %s ; 原行数 = %d ; EOL = %r' % ('APPLY' if APPLY else 'DRY-RUN', len(lines), eol))

def uniq(sig, arr=None):
    arr = lines if arr is None else arr
    h = [i for i, ln in enumerate(arr) if ln.startswith(sig)]
    if len(h) != 1:
        sys.exit('签名 %r 命中 %d 次' % (sig, len(h)))
    return h[0]

i_l = uniq(SIG_LEAD)
# 男性节内的 \subsubsection{兴奋期}：取 i_l 之后第一个
heads = [i for i, ln in enumerate(lines) if ln.lstrip().startswith(SIG_HEAD) and i > i_l]
if len(heads) != 1:
    sys.exit('i_l 之后的 \\subsubsection{兴奋期} 命中 %d 次' % len(heads))
i_h = heads[0]
log.append('过渡语 L%d ；其后目标标题 L%d %s' % (i_l + 1, i_h + 1, lines[i_h].strip()))

# 待搬块 = i_l .. i_h-1，其中非空行必须恰为"过渡语 + 四段"
block = lines[i_l:i_h]
nonblank = [x for x in block if x.strip()]
if len(nonblank) != 5:
    sys.exit('待搬块非空行数 = %d（预期 5：过渡语 + 四段）' % len(nonblank))
if not nonblank[0].startswith(SIG_LEAD):
    sys.exit('块首不是过渡语')
paras = nonblank[1:]
for sig, ln in zip(PREFIX, paras):
    if not ln.startswith(sig):
        sys.exit('段落顺序异常，期望 %r，实际 %r' % (sig, ln[:20]))
if block[-1].strip():
    sys.exit('块尾不是空行（实际 %r）' % block[-1][:40])
if lines[i_l - 1].strip() != '':
    sys.exit('块首之前不是空行')
log.append('待搬块 L%d-L%d（%d 行，含 4 个空行分隔）' % (i_l + 1, i_h, len(block)))
log.append('段落：' + ' / '.join(p[:8] for p in paras))

# 落点：\subsection{女性的性反应} 之前最近的 \end{figure}
i_d = uniq(SIG_DEST)
back = i_d - 1
while back > 0 and not lines[back].strip():
    back -= 1
if not lines[back].startswith(SIG_FIGEND):
    sys.exit('落点前不是 \\end{figure}，实际 %r' % lines[back][:40])
if not lines[i_d - 1].strip() == '':
    sys.exit('目标标题之前应有空行')
log.append('落点：L%d 之后（%s，位于阶段性的性反应末尾）' % (back + 1, lines[back].strip()))

payload = [eol, NEW_LEAD + eol] + [x for p in paras for x in (eol, p)]
rm = set(range(i_l, i_h))
log.append('删除 %d 行 ; 插入 %d 行 ; 净增 %+d' % (len(rm), len(payload), len(payload) - len(rm)))

new = []
for i, ln in enumerate(lines):
    if i in rm:
        continue
    new.append(ln)
    if i == back:
        new.extend(payload)

exp = len(lines) - len(rm) + len(payload)
if len(new) != exp:
    sys.exit('行数异常：预期 %d，实际 %d' % (exp, len(new)))

txt = ''.join(new)
if txt.count(NEW_LEAD) != 1:
    sys.exit('新过渡语出现 %d 次' % txt.count(NEW_LEAD))
if SIG_LEAD in txt:
    sys.exit('旧过渡语残留')
for s in PREFIX:
    if txt.count(s) != 1:
        sys.exit('段落 %r 出现 %d 次' % (s[:10], txt.count(s)))
if 'r52 归位' in txt:
    sys.exit('不应写入注释')

# 正文守恒：剔除空行后按多重集比对（含新增过渡语，故需允许 +1）
def body(s):
    return sorted(x for x in s.splitlines() if x.strip())
bo, bn = body(content), body(txt)
diff_rm = [x for x in bo if x not in bn]
log.append('正文多重集：old %d / new %d ; 消失 %d 行' % (len(bo), len(bn), len(diff_rm)))
for x in diff_rm[:5]:
    log.append('  消失: %s' % x[:70])
extra = [x for x in bn if x not in bo]
log.append('新增 %d 行' % len(extra))
for x in extra[:5]:
    log.append('  新增: %s' % x[:70])

nl = txt.splitlines()
for i, ln in enumerate(nl):
    if ln.startswith(NEW_LEAD):
        log.append('新落点上下文：')
        for j in range(max(0, i - 5), min(len(nl), i + 11)):
            log.append('  L%-5d %s' % (j + 1, nl[j][:64]))
        break
for i, ln in enumerate(nl):
    if ln.lstrip().startswith(SIG_HEAD):
        log.append('首个 \\subsubsection{兴奋期}（女性节）L%d' % (i + 1))
        break
for i, ln in enumerate(nl):
    if ln.startswith('\\subsection{男性的性反应}'):
        log.append('男性节现状：')
        for j in range(i, min(len(nl), i + 8)):
            log.append('  L%-5d %s' % (j + 1, nl[j][:64]))
        break

if APPLY:
    if not os.path.isdir(BK):
        os.makedirs(BK)
    shutil.copy2(SRC, BK + 'book.tex')
    log.append('备份 -> %sbook.tex' % BK)
    io.open(SRC, 'w', encoding='utf-8', newline='').write(txt)
    chk = io.open(SRC, encoding='utf-8', newline='').read()
    log.append('已写盘 ; 行数 = %d ; bare LF = %d'
               % (len(chk.splitlines()), sum(1 for x in chk.split('\n')[:-1] if not x.endswith('\r'))))

io.open(D + '_r52_move_out.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(log))
