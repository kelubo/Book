# -*- coding: utf-8 -*-
import io, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
T = {}
for fn in ['book.tex', 'female.tex', 'male.tex']:
    T[fn] = io.open(BASE + '\\' + fn, encoding='utf-8', newline='').read()

def show(word, fns=['book.tex'], limit=14, w=100):
    print('----- %s -----' % word)
    n = 0
    for fn in fns:
        for i, l in enumerate(T[fn].split('\n'), 1):
            s = l.strip()
            if s.startswith('%'):
                continue
            if word.lower() in s.lower():
                print('%-10s L%-6d %s' % (fn, i, s[:w]))
                n += 1
                if n >= limit:
                    return
    if n == 0:
        print('(无)')

# 1. 婚外性行为节的内容厚度与周边结构
print('===== 1. 婚外/开放式关系 区域结构 L39260-L39340 =====')
pat = re.compile(r'\\(section|subsection|subsubsection)\{([^{}]*)\}')
for i in range(39260, 39341):
    s = T['book.tex'].split('\n')[i - 1].strip()
    m = pat.match(s)
    if m:
        print('L%-6d %s %s' % (i, m.group(1), m.group(2)[:76]))
print('--- 婚外节正文抽样 ---')
for i in range(39278, 39300):
    s = T['book.tex'].split('\n')[i - 1].strip()
    if s:
        print('L%d | %s' % (i, s[:110]))

print()
print('===== 2. 束縛安全区域 L17140-L17480 标题结构 =====')
for i in range(17140, 17481):
    s = T['book.tex'].split('\n')[i - 1].strip()
    m = pat.match(s)
    if m:
        print('L%-6d %s %s' % (i, m.group(1), m.group(2)[:76]))

print()
print('===== 3. 关键词上下文 =====')
for w in ['绳痕', '尺神经', '桡神经', '神经损伤', '解绳', '坠床', '悬吊']:
    show(w, ['book.tex'], 6)
for w in ['润滑剂兼容', '硅胶润滑', '油性润滑', '共用']:
    show(w, ['book.tex'], 6)
for w in ['灌肠', '浅清洁', '深灌']:
    show(w, ['book.tex'], 8)
