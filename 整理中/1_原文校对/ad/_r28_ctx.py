# -*- coding: utf-8 -*-
"""r28 上下文核实：候选域命中分布与既有标题"""
import io, re

BASE = r'D:/Git/Book/整理中/1_原文校对/ad/'
files = {f: io.open(BASE + f, encoding='utf-8').read() for f in ['book.tex', 'female.tex', 'male.tex']}

# 1) 相关既有标题
print('=== 既有标题（虚拟/网络/影像/隐私/机器人/AI/乳房/高潮/射精痛） ===')
for f, t in files.items():
    for i, ln in enumerate(t.split('\n')):
        s = ln.strip()
        if re.match(r'\\(chapter|section|subsection|subsubsection|paragraph)\{', s) and re.search(
                r'虚拟|网络|影像|隐私|偷拍|机器人|人工智能|乳房|高潮|射精|身体意象|媒体|社交|科技', s):
            print('%-11s L%-6d %s' % (f, i + 1, s[:100]))

# 2) 关键词命中行
print()
for f, t in files.items():
    lines = t.split('\n')
    for kw in ['虚拟性', '私密影像', '复仇式', 'revenge', '性爱机器人', 'AI伴侣', '人工智能',
               '潮吹', '乳房切除', '乳房重建', '射精疼痛', '痛性射精', '乳胶过敏', '杀猪盘', '裸聊']:
        hits = [(i + 1, ln.strip()) for i, ln in enumerate(lines) if kw in ln]
        if hits:
            print('--- %s [%s] %d hits' % (f, kw, len(hits)))
            for i, s in hits[:8]:
                print('  L%-6d %s' % (i, s[:110]))
