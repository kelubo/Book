# -*- coding: utf-8 -*-
"""r38 导览★审计：找出所有★行，甄别同名误标"""
import io, re
P = r'D:\Git\Book\整理中\1_原文校对\ad\_全书导览_三卷目录总览_2026-09-10.md'
cur = None
rows = []
for line in io.open(P, encoding='utf-8'):
    line = line.rstrip('\n')
    if line.startswith('## '):
        cur = line.split()[1]
    if '★' in line and not line.startswith('#') and not line.startswith('>'):
        m = re.search(r'(\d+)｜(.+?)★', line)
        if m:
            rows.append((cur, int(m.group(1)), m.group(2)))
print('total star rows =', len(rows))
# 与历轮基线对比：r37 结束时应为 133 行（r36 的 131 + book男性的性反应 + male消退期）
# r38 新增 3 个 → 应 136。打印全部，重点看非 PREFIXES 短标题
SHORT = {'消退期', '兴奋期', '平台期', '高潮期', '男性的性反应', '女性的性反应'}
for fn, ln, t in rows:
    mark = ' <== SHORT' if t in SHORT else ''
    print('%-9s L%-6d %s%s' % (fn, ln, t[:60], mark))
