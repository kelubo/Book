# -*- coding: utf-8 -*-
"""第二十一轮：插入 5 处内容块（CRLF 文件，幂等，唯一性校验）"""
import io, os, sys

CR = '\r\n'

TASKS = [
    # (file, mode, anchor, blockfile, idempotency_key)
    ('book.tex',  'replace', '\t\\item [预留更多内容]', '_r21_blk1.tex', '抽送的速度、角度与深度都由女方掌握'),
    ('book.tex',  'after',
     '   - \\textbf{卫生顾虑}：保持双脚清洁，使用防护措施（如袜子或脚套）',
     '_r21_blk2.tex', '\\subsubsection{素股与股交}'),
    ('book.tex',  'before', '\\subsection{口交技巧}', '_r21_blk3.tex', '\\subsection{情欲按摩与感官按摩}'),
    ('male.tex',  'before', '\\subsection{药物治疗（达泊西汀 / SSRI外用）}',
     '_r21_blk4.tex', '\\subsubsection{射精控制训练与龟头脱敏（自我管理实操）}'),
    ('female.tex', 'before', '\\subsection{HSDD 与氟班色林（Addyi）}',
     '_r21_blk5.tex', '\\subsection{拒绝的艺术：如何温柔而坚定地说"不"}'),
]

def rd(f):
    return io.open(f, encoding='utf-8', newline='').read()

def wr(f, s):
    with io.open(f, 'w', encoding='utf-8', newline='') as fp:
        fp.write(s)

# 1) 唯一性校验
ok = True
for f, mode, a, bf, key in TASKS:
    s = rd(f)
    c = s.count(a)
    print('锚点 %s  cnt=%d  mode=%s  %s' % (f, c, mode, a[:40]))
    if c != 1:
        ok = False
if not ok:
    print('!! 锚点不唯一，中止'); sys.exit(1)

# 2) 幂等检查
for f, mode, a, bf, key in TASKS:
    s = rd(f)
    if key in s:
        print('跳过（已存在）: %s <- %s' % (key[:30], bf))

# 3) 按文件聚合后原子提交
files = {}
for f, mode, a, bf, key in TASKS:
    files.setdefault(f, []).append((mode, a, bf, key))

for f, jobs in files.items():
    s = rd(f)
    changed = False
    for mode, a, bf, key in jobs:
        if key in s:
            continue
        blk = rd(bf).replace('\r\n', '\n').rstrip('\n').replace('\n', CR)
        if mode == 'replace':
            s = s.replace(a, blk, 1)
        elif mode == 'after':
            s = s.replace(a, a + CR + CR + blk, 1)
        elif mode == 'before':
            s = s.replace(a, blk + CR + CR + a, 1)
        changed = True
        print('已插入: %s  %s' % (f, key[:40]))
    if changed:
        wr(f, s)
        print('已保存: %s' % f)

print('完成。')
