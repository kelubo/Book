# -*- coding: utf-8 -*-
"""r26 终核：辅助生殖章节内是否已有同房指引；哀伤章与肾衰节结构定位"""
import io, re

BASE = r'D:/Git/Book/整理中/1_原文校对/ad/'

def show(f, lo, hi, kws):
    lines = io.open(BASE + f, encoding='utf-8').read().split('\n')
    print('=== %s  L%d-%d ===' % (f, lo, hi))
    for i in range(lo - 1, min(hi, len(lines))):
        ln = lines[i]
        s = ln.strip()
        mark = '>>' if any(k in ln for k in kws) else '  '
        if mark == '>>' or re.match(r'\\(chapter|section|subsection|subsubsection|paragraph)\{', s):
            if len(s) > 100:
                s = s[:97] + '...'
            print('%s L%-6d %s' % (mark, i + 1, s))

# 1) female IVF/辅助生殖大区(L9900-10160)内"同房/性生活/性生"是否出现
lines = io.open(BASE + 'female.tex', encoding='utf-8').read().split('\n')
kw = ['同房', '性生活', '性生', '性爱']
n = 0
print('=== female.tex L9900-10160 内 性生活相关 ===')
for i in range(9899, 10160):
    if any(k in lines[i] for k in kw):
        print('  L%-6d %s' % (i + 1, lines[i].strip()[:100]))
        n += 1
print('  hits:', n)

# 2) book 哀伤/丧偶章结构：找哀伤相关标题行
print()
lines = io.open(BASE + 'book.tex', encoding='utf-8').read().split('\n')
print('=== book.tex 哀伤/丧偶/丧失 标题 ===')
for i, ln in enumerate(lines):
    if re.match(r'\\(chapter|section|subsection|subsubsection)\{', ln) and re.search(r'哀伤|丧偶|丧失|丧亲|离世|死亡|悲伤', ln):
        print('  L%-6d %s' % (i + 1, ln.strip()[:100]))

# 3) book 慢性肾衰节前后的标题层级（定位器官移植节锚点）
show('book.tex', 7240, 7360, ['肾移植', '移植'])

# 4) 全书标题含"移植"的
print()
print('=== book.tex 标题含 移植/透析/肾 ===')
for i, ln in enumerate(lines):
    if re.match(r'\\(chapter|section|subsection|subsubsection)\{', ln) and re.search(r'移植|透析|肾', ln):
        print('  L%-6d %s' % (i + 1, ln.strip()[:100]))

# 5) female 卷标题含 辅助生殖/试管/IVF 的
lines = io.open(BASE + 'female.tex', encoding='utf-8').read().split('\n')
print()
print('=== female.tex 标题含 辅助生殖/试管/IVF/生育 ===')
for i, ln in enumerate(lines):
    if re.match(r'\\(chapter|section|subsection|subsubsection|paragraph)\{', ln) and re.search(r'辅助生殖|试管|IVF|冻卵|人工授精', ln):
        print('  L%-6d %s' % (i + 1, ln.strip()[:100]))
