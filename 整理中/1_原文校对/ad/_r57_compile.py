# -*- coding: utf-8 -*-
"""r57：编译指定卷验证（默认 female）——用法：python _r57_compile.py [卷名] [遍数]"""
import io, os, re, subprocess, glob, sys

D = 'D:/Git/Book/整理中/1_原文校对/ad/'
vol = sys.argv[1] if len(sys.argv) > 1 else 'female'
runs = int(sys.argv[2]) if len(sys.argv) > 2 else 2
OUT = D + '_r57_compile_out.txt'
out = []

cands = []
for pat in (r'C:/Program Files/MiKTeX/miktex/bin/x64/xelatex.exe',
            r'C:/Users/Administrator/AppData/Local/Programs/MiKTeX/miktex/bin/x64/xelatex.exe',
            r'C:/Program Files (x86)/MiKTeX/miktex/bin/xelatex.exe',
            r'C:/texlive/*/bin/windows/xelatex.exe'):
    cands += glob.glob(pat)
if not cands:
    out.append('未找到 xelatex')
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
    sys.exit(1)
XE = cands[0]
out.append('使用: %s' % XE)
os.chdir(D)

for k in range(runs):
    p = subprocess.run([XE, '-interaction=nonstopmode', '-enable-installer', vol + '.tex'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    out.append('--- 第 %d 遍 returncode = %s ---' % (k + 1, p.returncode))

log = io.open(D + vol + '.log', encoding='utf-8', errors='replace').read()
lines = log.splitlines()
errs = [ln for ln in lines if ln.startswith('!')]
out.append('=== 以 ! 开头的错误行 %d 条 ===' % len(errs))
for ln in errs[:30]:
    out.append('  ' + ln)
m = re.findall(r'Output written on .*?\((\d+) pages', log)
out.append('页数 = %s' % m)
out.append('Undefined control sequence = %d' % len([x for x in lines if 'Undefined control sequence' in x]))
out.append('Missing/Illegal unit = %d' % len([x for x in lines if 'Missing' in x or 'Illegal unit' in x]))
out.append('Rerun 提示 = %d' % log.count('Rerun'))

io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
print('\n'.join(out))
