# -*- coding: utf-8 -*-
import io, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
T = {}
for fn in ['book.tex', 'female.tex', 'male.tex']:
    T[fn] = io.open(BASE + '\\' + fn, encoding='utf-8', newline='').read()

def show(word, fns, limit=8, w=104):
    print('----- %s -----' % word)
    n = 0
    for fn in fns:
        for i, l in enumerate(T[fn].split('\n'), 1):
            s = l.strip()
            if s.startswith('%'):
                continue
            if word in s:
                print('%-10s L%-6d %s' % (fn, i, s[:w]))
                n += 1
                if n >= limit:
                    return
    if n == 0:
        print('(无)')

print('===== male 婚外语境 =====')
for w in ['外遇', '偷情', '婚外性']:
    show(w, ['male.tex'], 6)
print()
print('===== book 情趣内衣/丝袜 内容（L11400-11500 抽样）=====')
for i in range(11416, 11490):
    s = T['book.tex'].split('\n')[i - 1].strip()
    if s:
        print('L%d | %s' % (i, s[:112]))
print()
print('===== book 玩具材质/清洁节 L34780-L34820, L35010-L35045 抽样 =====')
for rng in [(34780, 34800), (35010, 35045)]:
    for i in range(rng[0], rng[1]):
        s = T['book.tex'].split('\n')[i - 1].strip()
        if s:
            print('L%d | %s' % (i, s[:112]))
    print('   ---')
print()
print('===== 关键词：背叛创伤/信任/无性婚姻/情感出轨 =====')
for w in ['背叛创伤', '信任危机', '无性婚姻', '情感出轨', '线上', '网恋', '虚拟出轨']:
    show(w, ['book.tex', 'male.tex', 'female.tex'], 5)
