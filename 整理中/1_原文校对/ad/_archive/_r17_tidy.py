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
fixes = {
 'book.tex': [
   ('还是制造了新问题？' + E + '\\end{tcolorbox}' + E + '\\section{数字时代的性教育}',
    '还是制造了新问题？' + E + '\\end{tcolorbox}' + E + E + '\\section{数字时代的性教育}'),
   (E + '\\end{tcolorbox}' + '\\section{住院、卧床与康复期间的性}',
    E + '\\end{tcolorbox}' + E + E + '\\section{住院、卧床与康复期间的性}'),
   (E + '\\end{tcolorbox}' + '\\section{临终关怀与性亲密}',
    E + '\\end{tcolorbox}' + E + E + '\\section{临终关怀与性亲密}'),
   ('（详见“求助与资源导航”章）。' + '\\item[安宁疗护（Hospice Care）]',
    '（详见“求助与资源导航”章）。' + E + E + '\\item[安宁疗护（Hospice Care）]'),
 ],
 'male.tex': [
   (E + '\\end{itemize}' + '\\section{男性性欲的波动与节律}',
    E + '\\end{itemize}' + E + E + '\\section{男性性欲的波动与节律}'),
 ],
}
for f, jobs in fixes.items():
    t = rd(f)
    for a, b in jobs:
        n = t.count(a)
        if n != 1:
            print('!! %s 锚点计数=%d: %r' % (f, n, a[:40])); continue
        t = t.replace(a, b)
        print('[fix] %s' % f)
    wr(f, t)
print('TIDY DONE')
