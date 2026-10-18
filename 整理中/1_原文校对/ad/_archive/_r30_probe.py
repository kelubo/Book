# -*- coding: utf-8 -*-
"""r30 探测：俚语行为域（69/一夜情/约炮/多人等）"""
import io, re

BASE = r'D:/Git/Book/整理中/1_原文校对/ad/'
FILES = ['book.tex', 'female.tex', 'male.tex']

def strip_comments(s):
    return '\n'.join(re.sub(r'(?<!\\)%.*', '', ln) for ln in s.split('\n'))

texts = {f: strip_comments(io.open(BASE + f, encoding='utf-8').read()) for f in FILES}

TERMS = {
    '体位/数字俚语': ['69式', '69 式', '六九', '69体位', '69体', '姿势69', '419', '一夜情',
               '一夜性', '偶遇性', '约炮', '炮友', '开房', '野战', '车震', '快餐性'],
    '多人/交换': ['3P', '三人行', '群交', '换妻', '换偶', '交换伴侣', '双飞', '多人性行为',
             '多伴侣', '群p', '群P', '轮X'],
    '俚语/口语': ['啪啪', '打飞机', '口活', '自嗨', '要爱爱', '做爱', '性交'],
}

hdr = '%-12s' % 'TERM' + ''.join('%9s' % f[:7] for f in FILES)
print(hdr)
for g, terms in TERMS.items():
    print('==== %s ====' % g)
    for term in terms:
        row = '%-12s' % term
        for f in FILES:
            row += '%9d' % texts[f].count(term)
        print(row)

# 69 边界匹配（避免匹配 0.69/169 等）
print()
print('=== \\b69\\b 按行 ===')
for f, t in texts.items():
    lines = t.split('\n')
    hits = [(i + 1, ln.strip()) for i, ln in enumerate(lines) if re.search(r'(?<![\d.])69(?![\d.])', ln)]
    print('--- %s: %d' % (f, len(hits)))
    for i, s in hits[:12]:
        print('  L%-6d %s' % (i, s[:110]))
