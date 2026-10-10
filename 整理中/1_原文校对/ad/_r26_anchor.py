# -*- coding: utf-8 -*-
"""r26 锚点确认：count 校验 + 哀伤节尾部结构"""
import io, re

BASE = r'D:/Git/Book/整理中/1_原文校对/ad/'

b = io.open(BASE + 'book.tex', encoding='utf-8').read()
f = io.open(BASE + 'female.tex', encoding='utf-8').read()

ANCHORS = [
    ('book', r'\subsection{肝病（Hepatic Disease）与性生活}'),
    ('female', r'\subsection{辅助生殖技术的风险与并发症}'),
]
for name, a in ANCHORS:
    t = b if name == 'book' else f
    print('%-7s count=%d  %s' % (name, t.count(a), a))

# 哀伤节尾部：L43492 到文件尾的标题结构
lines = b.split('\n')
print()
print('=== book L43480-43693 标题与非空行示意 ===')
for i in range(43479, min(43693, len(lines))):
    s = lines[i].strip()
    if re.match(r'\\(chapter|section|subsection|subsubsection|paragraph|item)\b', s):
        print('L%-6d %s' % (i + 1, s[:100]))

# 查书内是否已有失独/器官移植 专节标题
print()
for kw in ['失独', '器官移植', '性生活指引', '移植受者']:
    hits = [(i + 1, ln.strip()) for i, ln in enumerate(lines)
            if re.match(r'\\(chapter|section|subsection|subsubsection)\{', ln) and kw in ln]
    print('book 标题含[%s]: %s' % (kw, hits))
flines = f.split('\n')
for kw in ['性生活指引', '各阶段']:
    hits = [(i + 1, ln.strip()) for i, ln in enumerate(flines)
            if re.match(r'\\(chapter|section|subsection|subsubsection)\{', ln) and kw in ln]
    print('female 标题含[%s]: %s' % (kw, hits))
