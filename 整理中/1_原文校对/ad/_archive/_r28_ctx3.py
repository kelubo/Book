# -*- coding: utf-8 -*-
"""r28 落位核查：阴吹上下文 + female 子宫/性交痛结构"""
import io, re

BASE = r'D:/Git/Book/整理中/1_原文校对/ad/'
raws = {f: io.open(BASE + f, encoding='utf-8').read() for f in ['book.tex', 'female.tex']}

# 1) book 阴吹所在节
lines = raws['book.tex'].split('\n')
print('=== book L29185-29225（阴吹上下文） ===')
for i in range(29184, 29225):
    print('L%-6d %s' % (i + 1, lines[i].rstrip()[:120]))

# 2) female 子宫/性交痛/阴道 相关标题
print()
print('=== female 标题（子宫/性交痛/阴道/尴尬/排气） ===')
lines = raws['female.tex'].split('\n')
for i, ln in enumerate(lines):
    s = ln.strip()
    if re.match(r'\\(chapter|section|subsection|subsubsection|paragraph)\{', s) and re.search(
            r'子宫|性交痛|阴道|尴尬|排气|盆底|深部', s):
        print('L%-6d %s' % (i + 1, s[:110]))
