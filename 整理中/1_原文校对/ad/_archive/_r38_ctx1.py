# -*- coding: utf-8 -*-
"""r38 探测二：重点方向上下文核查"""
import io, os, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
FILES = ['book.tex', 'female.tex', 'male.tex']
texts = {}
for fn in FILES:
    lines = io.open(os.path.join(BASE, fn), encoding='utf-8', newline='').read().split('\r\n')
    texts[fn] = [(i+1, l) for i, l in enumerate(lines) if not l.strip().startswith('%')]

def show(fn, word, limit=8, width=85):
    print('--- %s 「%s」 ---' % (fn, word))
    for n, l in texts[fn]:
        if word in l:
            print('  L%d: %s' % (n, l.strip()[:width]))

# 1. 残障：book 是否有专章/专节
print('===== 1. 残障与性的既有结构 =====')
for fn in FILES:
    for n, l in texts[fn]:
        st = l.strip()
        m = re.match(r'\\(chapter|section|subsection)\{([^{}]*)\}', st)
        if m and any(w in st for w in ['残障', '残疾', '障碍', '轮椅', '脊髓']):
            print('  %s L%d %s %s' % (fn, n, m.group(1), m.group(2)[:50]))

# 2. 数字亲密/隐私：book 私密照片/偷拍/泄露/亲密影像的所在
print()
print('===== 2. 私密照片/偷拍/亲密影像 位置 =====')
for w in ['私密照片', '偷拍', '亲密影像', '隐私照']:
    show('book.tex', w, width=70)

# 3. 育儿 27 处的形态
print()
print('===== 3. 育儿 内容形态（book 前 10 条）=====')
cnt = 0
for n, l in texts['book.tex']:
    if '育儿' in l and cnt < 10:
        print('  L%d: %s' % (n, l.strip()[:70]))
        cnt += 1

# 4. 性头痛 4 处
print()
print('===== 4. 性头痛 =====')
for fn in FILES:
    show(fn, '性头痛', width=70)

# 5. 脊髓损伤所在章节结构
print()
print('===== 5. 脊髓损伤 位置 =====')
for fn in FILES:
    show(fn, '脊髓损伤', limit=6, width=70)

# 6. 无性婚姻/激情消退/七年之痒 专节？
print()
print('===== 6. 无性婚姻等标题命中 =====')
for fn in FILES:
    for n, l in texts[fn]:
        st = l.strip()
        m = re.match(r'\\(chapter|section|subsection|subsubsection)\{([^{}]*)\}', st)
        if m and any(w in st for w in ['无性', '激情', '倦怠', '痒', '欲望', '性脚本', '冷却']):
            print('  %s L%d %s %s' % (fn, n, m.group(1), m.group(2)[:50]))
