# -*- coding: utf-8 -*-
"""第二十八轮插入：2 处（均 female；blk1 before 型，blk2 行级插入，CRLF，幂等）"""
import io

CR = '\r\n'

# ---- blk1：子宫后位，before 型 ----
fname = 'female.tex'
anchor = r'\subsection{不孕症的诊断}'
blk = '_r28_blk1.tex'
ikey = r'\subsection{子宫后位：正常变异，不是病}'

text = io.open(fname, encoding='utf-8', newline='').read()
core = io.open(blk, encoding='utf-8', newline='').read()
core = core.replace('\r\n', '\n').replace('\n', CR).rstrip(CR)

if ikey in text:
    print('SKIP (idempotent):', ikey)
else:
    if text.count(anchor) != 1:
        raise SystemExit('ANCHOR FAIL (%d): %s' % (text.count(anchor), anchor))
    text = text.replace(anchor, core + CR + CR + anchor, 1)
    io.open(fname, 'w', encoding='utf-8', newline='').write(text)
    print('OK: blk1 子宫后位 before', anchor)

# ---- blk2：阴吹，行级插入（绕开全角引号锚匹配）----
text = io.open(fname, encoding='utf-8', newline='').read()
core = io.open('_r28_blk2.tex', encoding='utf-8', newline='').read()
core = core.replace('\r\n', '\n').replace('\n', CR).rstrip(CR)
ikey2 = r'\subsection{阴吹（阴道排气）'
if ikey2 in text:
    print('SKIP (idempotent):', ikey2)
else:
    lines = text.split(CR)
    # 定位：L3384 编者按行（1-based）之后、\section{阴道干涩与萎缩} 正文区之前
    # 校验目标行内容（前缀匹配，避开引号形态）
    idx_edit = None
    idx_sec = None
    for i, ln in enumerate(lines):
        if ln.startswith(r'\noindent\textit{【编者按】}若恐惧已严重影响性生活'):
            idx_edit = i
        if ln == r'\section{阴道干涩与萎缩}':
            idx_sec = i
    if idx_edit is None or idx_sec is None:
        raise SystemExit('LINE LOCATE FAIL: edit=%s sec=%s' % (idx_edit, idx_sec))
    if not (0 < idx_sec - idx_edit <= 6):
        raise SystemExit('LOCATE RANGE FAIL: edit=%d sec=%d' % (idx_edit, idx_sec))
    new_lines = lines[:idx_edit + 1] + ['', '', core] + lines[idx_edit + 1:]
    io.open(fname, 'w', encoding='utf-8', newline='').write(CR.join(new_lines))
    print('OK: blk2 阴吹 after L%d (sec L%d)' % (idx_edit + 1, idx_sec + 1))

print('done')
