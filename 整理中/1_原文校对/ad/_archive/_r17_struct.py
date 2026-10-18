# -*- coding: utf-8 -*-
import re, sys
f = sys.argv[1] if len(sys.argv) > 1 else 'book.tex'
lines = open(f, encoding='utf-8').read().split('\n')
for i, ln in enumerate(lines, 1):
    s = ln.strip()
    if s.startswith('%'):
        continue
    m = re.match(r'\\(part|chapter|section)\{(.+?)\}', s)
    if m:
        lvl = {'part': '', 'chapter': '  ', 'section': '    '}[m.group(1)]
        print('%6d %s%s' % (i, lvl, m.group(2)))
