# -*- coding: utf-8 -*-
import io, os

BASE = os.path.dirname(os.path.abspath(__file__))
def rd(p):
    with io.open(os.path.join(BASE, p), 'r', encoding='utf-8', newline='') as f:
        return f.read()
def wr(p, s):
    with io.open(os.path.join(BASE, p), 'w', encoding='utf-8', newline='') as f:
        f.write(s)

E = '\r\n'
def core(name):
    s = rd(name)
    s = s.replace('\r\n', '\n').replace('\n', E)   # -> CRLF
    return s.strip(E)                               # 去掉首尾换行

def do_replace(text, anchor, blk_core, where):
    a = anchor.replace('\r\n', '\n')
    for c in (a.replace('\n', E), a):
        n = text.count(c)
        if n == 1:
            if where == 'after':
                return text.replace(c, c + E + E + blk_core + E)
            else:
                return text.replace(c, blk_core + E + E + c)
        elif n > 1:
            raise SystemExit('!! 锚点不唯一 n=%d: %r' % (n, anchor[:50]))
    raise SystemExit('!! 未找到锚点: %r' % anchor[:50])

TASKS = {
 'female.tex': [
    ('\\subsection{性欲低下的原因与应对}',
     '_r18_blk1.tex', 'before', '\\subsection{女性性欲的激素周期性波动}'),
 ],
 'book.tex': [
    ('既不回避，也不越界，而是把老年人当作有权表达情感与欲望的成年人。\r\n\\end{tcolorbox}',
     '_r18_blk2.tex', 'after', '\\subsection{与护理人员、家属的沟通与照护边界}'),
    ('\\section{HIV 与其他性传播疾病的检测与阻断}',
     '_r18_blk3.tex', 'before', '\\section{哀伤、丧亲与心理支持资源}'),
 ],
}

for fname, jobs in TASKS.items():
    text = rd(fname)
    for anchor, blkf, where, key in jobs:
        if key in text:
            print('[skip] %s 已含 %s' % (fname, key[:34])); continue
        blk_core = core(blkf)
        text = do_replace(text, anchor, blk_core, where)
        print('[ok]   %s ← %s (%s)' % (fname, blkf, where))
    wr(fname, text)
    print('== %s 已写回 ==' % fname)
print('DONE')
