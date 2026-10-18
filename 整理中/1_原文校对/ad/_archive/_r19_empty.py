# -*- coding: utf-8 -*-
"""扫描指定文件区间内的空标题（标题后紧跟另一个标题或 \end{）"""
import re, sys

fname = sys.argv[1]
a = int(sys.argv[2]); b = int(sys.argv[3])
s = open(fname, encoding='utf-8').read()
lines = s.split('\n')
hdr = re.compile(r'^\\(sub)*section\*?\{|^\\(sub)*paragraph\{')

for i in range(a-1, min(b, len(lines))):
    t = lines[i].strip()
    if hdr.match(t):
        j = i + 1
        while j < len(lines) and (lines[j].strip() == '' or lines[j].strip().startswith('%')):
            j += 1
        nxt = lines[j].strip() if j < len(lines) else ''
        empty = (nxt == '') or bool(hdr.match(nxt)) or nxt.startswith('\\end{')
        print(('EMPTY ' if empty else '      ') + str(i+1) + ': ' + t[:70])
