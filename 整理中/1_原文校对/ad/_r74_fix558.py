# -*- coding: utf-8 -*-
p = 'book.tex'
raw = open(p, 'r', encoding='utf-8', newline='').read()
assert '\r\n' not in raw, 'CRLF detected'
lines = raw.split('\n')
i = 557
assert 'colbacktitle' in lines[i], lines[i]
lines[i] = lines[i].replace('colbacktitle={},', '')
out = '\n'.join(lines)
assert out.count('colbacktitle') == 0
open(p, 'w', encoding='utf-8', newline='').write(out)
print('OK 修复 L558:', lines[i])
print('行数', len(lines))
