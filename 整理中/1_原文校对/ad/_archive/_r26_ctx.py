# -*- coding: utf-8 -*-
"""r26 上下文核实：打印命中行及其行号，判断是否有专节/整合内容"""
import io, re

BASE = r'D:/Git/Book/整理中/1_原文校对/ad/'

CHECKS = {
    'book.tex': [
        '失独', '器官移植', '心脏康复',
        '促排', '取卵', '胚胎移植', '囊胚',
        '透析', '肾衰', '尿毒', '免疫抑制',
        '痴呆', '阿尔茨海默',
    ],
    'female.tex': ['促排', '取卵', '胚胎移植'],
    'male.tex': ['免疫抑制', '透析'],
}

MAX_SHOW = 40
for f, terms in CHECKS.items():
    print('=' * 72)
    print('FILE:', f)
    lines = io.open(BASE + f, encoding='utf-8').read().split('\n')
    for term in terms:
        hits = [(i + 1, ln) for i, ln in enumerate(lines) if term in ln]
        print('-' * 60)
        print('[%s] %d hits' % (term, len(hits)))
        for i, ln in hits[:MAX_SHOW]:
            s = ln.strip()
            if len(s) > 110:
                s = s[:107] + '...'
            print('  L%-6d %s' % (i, s))
        if len(hits) > MAX_SHOW:
            print('  ...(%d more)' % (len(hits) - MAX_SHOW))
