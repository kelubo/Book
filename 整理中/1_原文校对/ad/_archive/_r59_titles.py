# -*- coding: utf-8 -*-
# r59: 疑问句标题全部改为陈述式（book 17 处 + female 1 处）
import io, sys, os
from collections import Counter

D = os.path.dirname(os.path.abspath(__file__))
APPLY = 'apply' in sys.argv

# (文件, 旧标题行全文, 新标题行全文)
EDITS = [
    ('book.tex', r'\section{性反应是同步的吗？}', r'\section{性反应的同步性}'),
    ('book.tex', r'\subsection{睾丸还是卵巢？}', r'\subsection{性腺的分化：睾丸或卵巢}'),
    ('book.tex', r'\subsection{阴茎还是阴蒂？}', r'\subsection{外生殖器的分化}'),
    ('book.tex', r'\subsection{经期可以性交吗？}', r'\subsection{经期性交的可行性与注意}'),
    ('book.tex', r'\section{梦交（Nocturnal Sexual Dreams）——正常还是异常？}', r'\section{梦交（Nocturnal Sexual Dreams）的正常与异常}'),
    ('book.tex', r'\subsection{怎样做流产？}', r'\subsection{流产的方法}'),
    ('book.tex', r'\subsubsection{夫妻分床睡：疏远亲密还是拯救睡眠？}', r'\subsubsection{夫妻分床睡：亲密与睡眠的权衡}'),
    ('book.tex', r'\subsubsection{性爱等于性交吗？}', r'\subsubsection{性爱与性交的区别}'),
    ('book.tex', r'\subsubsection{性感的女人性欲也强吗？}', r'\subsubsection{性感与性欲的区别}'),
    ('book.tex', r'\subsubsection{性的误区：完美的性生活可以计划吗？}', r'\subsubsection{性的误区：完美性生活是计划的产物}'),
    ('book.tex', r'\subsubsection{什么是SM？打破刻板印象}', r'\subsubsection{SM的概念与刻板印象}'),
    ('book.tex', r'\subsubsection{SM正常吗？}', r'\subsubsection{SM的争议与定位}'),
    ('book.tex', r'\subsubsection{为什么要SM？—— 动机与心理机制}', r'\subsubsection{SM的动机与心理机制}'),
    ('book.tex', r'\subsection{男人的性渴望强于女人吗？}', r'\subsection{男女的性渴望差异}'),
    ('book.tex', r'\subsection{男性也有更年期吗？（Male Menopause / Andropause / LOH）}', r'\subsection{男性更年期（Male Menopause / Andropause / LOH）}'),
    ('book.tex', r'\subsection{男人的性欲和女人的性欲一样吗？}', r'\subsection{男女的性欲差异}'),
    ('book.tex', r'\subsection{性爱时机与作息型：清晨还是夜晚？}', r'\subsection{性爱时机与作息型}'),
    ('female.tex', r'\subsection{经血逆流与子宫内膜异位症：经期性交会加重吗？}', r'\subsection{经血逆流与子宫内膜异位症：经期性交的影响}'),
]

texts = {}
for f in ('book.tex', 'female.tex'):
    raw = io.open(os.path.join(D, f), encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in raw else '\n'
    texts[f] = [raw, nl, raw.split(nl)]

log = []
# 预检：旧标题唯一存在；新标题不存在；新标题之间无重名
seen_new = {}
for f, old, new in EDITS:
    _, nl, lines = texts[f]
    c = lines.count(old)
    if c != 1:
        sys.exit('%s 中 %r 命中 %d 次' % (f, old[:40], c))
    if lines.count(new):
        sys.exit('新标题已存在于 %s：%r' % (f, new))
    key = (f, new)
    if key in seen_new:
        sys.exit('新标题重名：%r 与 %r' % (seen_new[key], new))
    seen_new[key] = old

# 逐条替换
for f, old, new in EDITS:
    lines = texts[f][2]
    lines[lines.index(old)] = new

for f in ('book.tex', 'female.tex'):
    raw, nl, lines = texts[f]
    newraw = nl.join(lines)
    if len(lines) != raw.count('\n') + (0 if raw.endswith(nl) else 1) - 0:
        pass  # 行数校验放下面统一做
    # 多重集差异应恰为 18 处旧→新
    ca, cb = Counter(io.open(os.path.join(D, f), encoding='utf-8', newline='').read().split(nl)), Counter(lines)
    d = (cb - ca) + (ca - cb)
    exp = Counter()
    for ff, old, new in EDITS:
        if ff == f:
            exp[old] += 1
            exp[new] += 1
    if d != exp:
        sys.exit('%s 差异异常: %r' % (f, list((d - exp).items())[:3]))
    log.append('%s：替换 %d 处，行数 %d → %d，多重集差异恰为预期' % (f, sum(1 for e in EDITS if e[0] == f), len(ca), len(lines)))
    # 新标题质量
    for ff, old, new in EDITS:
        if ff == f:
            if '**' in new or '%' in new:
                sys.exit('新标题含 ** / %%：%r' % new)
    texts[f][0] = newraw

if APPLY:
    for f in ('book.tex', 'female.tex'):
        raw, nl, lines = texts[f]
        io.open(os.path.join(D, f), 'w', encoding='utf-8', newline='').write(nl.join(lines))
    log.append('>>> 已写盘 book.tex / female.tex')
else:
    log.append('(dry-run；加 apply 落盘)')

io.open(os.path.join(D, '_r59_titles_out.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(log))
print('\n'.join(log))
