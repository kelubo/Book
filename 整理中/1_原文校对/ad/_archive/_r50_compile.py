# -*- coding: utf-8 -*-
"""r50：编译 book.tex 验证（定位 xelatex → chdir → 编译 → 扫描 .log 错误）"""
import io, os, re, subprocess, glob, sys

D = 'D:/Git/Book/整理中/1_原文校对/ad/'
out = []

cands = []
for pat in (r'C:/Users/Administrator/AppData/Local/Programs/MiKTeX/miktex/bin/x64/xelatex.exe',
            r'C:/Program Files/MiKTeX/miktex/bin/x64/xelatex.exe',
            r'C:/Program Files (x86)/MiKTeX/miktex/bin/xelatex.exe',
            r'C:/texlive/*/bin/windows/xelatex.exe',
            r'C:/Program Files/MiKTeX*/miktex/bin*/xelatex.exe'):
    cands += glob.glob(pat)
out.append('xelatex 候选: %s' % cands)
if not cands:
    io.open(D + '_r50_compile_out.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
    sys.exit(1)
XE = cands[0]
out.append('使用: %s' % XE)

os.chdir(D)
p = subprocess.run([XE, '-interaction=nonstopmode', '-enable-installer', 'book.tex'],
                   capture_output=True, text=True, encoding='utf-8', errors='replace')
out.append('returncode = %s' % p.returncode)

log = io.open(D + 'book.log', encoding='utf-8', errors='replace').read()
errs = [ln for ln in log.splitlines() if ln.startswith('!')]
out.append('=== .log 以 ! 开头的错误行 %d 条 ===' % len(errs))
for ln in errs[:40]:
    out.append('  ' + ln)
out.append('=== 前 20 条 "! " 上下文 ===')
lines = log.splitlines()
for i, ln in enumerate(lines):
    if ln.startswith('!'):
        out.append('  ... %s | %s' % (ln[:120], lines[i + 1][:120] if i + 1 < len(lines) else ''))
    if len([x for x in lines[:i] if x.startswith('!')]) >= 20:
        break
m = re.findall(r'Output written on .*?\((\d+) pages', log)
out.append('页数 = %s' % m)
und = [ln for ln in lines if 'Undefined control sequence' in ln]
out.append('Undefined control sequence = %d' % len(und))
miss = [ln for ln in lines if 'Missing' in ln or 'Illegal unit' in ln]
out.append('Missing/Illegal unit = %d' % len(miss))
torun = log.count('Rerun')
out.append('Rerun 提示 = %d' % torun)
io.open(D + '_r50_compile_out.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
