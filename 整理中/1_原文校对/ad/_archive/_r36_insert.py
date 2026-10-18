# -*- coding: utf-8 -*-
import io, os
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
CR = '\r\n'

def load(blk):
    t = io.open(os.path.join(BASE, blk), encoding='utf-8', newline='').read()
    return t.replace('\r\n', '\n').replace('\n', CR).rstrip(CR)

JOBS = {
    'book.tex': [
        ('_r36_blk_d1.tex', r'\subsection{避孕贴片}', '漏服之后怎么办'),
        ('_r36_blk_d2.tex', r'\subsection{特殊情况的避孕选择}', '停用之后还能怀上吗'),
        ('_r36_blk_d3.tex', r'\subsection{特殊情况的避孕选择}', '避孕责任：谁承担'),
        ('_r36_blk_e1.tex', r'\section{梦交（Nocturnal Sexual Dreams）——正常还是异常？}', '经期性行为的常见疑问速答'),
    ],
    'female.tex': [
        ('_r36_blk_e2.tex', r'\section{月经贫困与经期平等}', '经期性行为的实操与舒适度'),
        ('_r36_blk_e3.tex', r'\section{月经贫困与经期平等}', '经期还能做什么'),
        ('_r36_blk_e4.tex', r'\section{月经贫困与经期平等}', '经血逆流与子宫内膜异位症：经期性交会加重吗'),
    ],
}

for fn, jobs in JOBS.items():
    fname = os.path.join(BASE, fn)
    text = io.open(fname, encoding='utf-8', newline='').read()
    print('=== %s (start %d lines) ===' % (fn, len(text.split(CR))))
    for blk, anchor, ikey in jobs:
        if ikey in text:
            print('  SKIP (idempotent):', blk)
            continue
        if text.count(anchor) != 1:
            raise SystemExit('ANCHOR FAIL %s in %s -> count=%d' % (anchor, fn, text.count(anchor)))
        core = load(blk)
        text = text.replace(anchor, core + CR + CR + anchor, 1)
        print('  OK: %s <- before %s' % (blk, anchor[:46]))
    io.open(fname, 'w', encoding='utf-8', newline='').write(text)
    print('  -> now %d lines' % len(text.split(CR)))
print('done')
