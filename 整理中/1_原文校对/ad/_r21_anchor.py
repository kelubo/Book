# -*- coding: utf-8 -*-
"""第二十一轮：锚点唯一性校验"""
import io

def rd(f):
    return io.open(f, encoding='utf-8', newline='').read()

anchors = [
    ('book.tex', '\t\\item [预留更多内容]'),
    ('book.tex', '   - \\textbf{卫生顾虑}：保持双脚清洁，使用防护措施（如袜子或脚套）'),
    ('book.tex', '\\subsection{口交技巧}'),
    ('book.tex', '手部爱抚是性爱中不可或缺的重要环节，通过不同的技巧和方式，可以激发对方的性欲望和性兴奋，提高性满意度和性快感。掌握良好的手部爱抚技巧，有助于建立更加健康、和谐的性关系。'),
    ('male.tex', '\\subsection{药物治疗（达泊西汀 / SSRI外用）}'),
    ('male.tex', '\\subsubsection{阴道静止法}'),
    ('female.tex', '\\section{性高潮障碍}'),
    ('female.tex', '\\subsection{高潮困难的解决途径}'),
    ('female.tex', '\\section{性交疼痛}'),
]

for f, a in anchors:
    s = rd(f)
    print('%s  cnt=%d  %s' % (f, s.count(a), a[:50]))
