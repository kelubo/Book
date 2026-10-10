# -*- coding: utf-8 -*-
"""第二十二轮：把 9 个内容块插入三卷（行尾 CRLF；锚点唯一性校验 + 幂等跳过）"""
import io, sys

CR = "\r\n"

def load_block(name):
    s = io.open(name, encoding="utf-8").read()
    s = s.replace("\r\n", "\n").replace("\r", "\n").strip("\n")
    return s.replace("\n", CR)

# (文件, 锚文本, 块文件, 位置, 幂等键)
JOBS = [
    ('book.tex', r'\subsubsection{女用避孕套}', '_r22_blk1.tex', 'before',
     r'\subsubsection{避孕套的正确使用、尺寸选择与储存}'),
    ('book.tex', '- 避免过度运动，以免导致疲劳和损伤。', '_r22_blk2.tex', 'after',
     r'\subsection{健身、骑行与性功能：运动的"双刃剑"}'),
    ('book.tex',
     r'5. \textbf{关注非性亲密}：加强非性的亲密行为，如拥抱、亲吻、按摩等，增强情感连接，减少性差异带来的影响。',
     '_r22_blk3.tex', 'after', r'\section{依恋类型与性'),
    ('book.tex',
     r'- \textbf{接受变化}：接受长期关系中性的变化，将这些变化视为关系发展的自然过程，而不是问题或失败。',
     '_r22_blk4.tex', 'after', r'\subsection{"七年之痒"与长期关系的激情维护}'),
    ('book.tex',
     r'- \textbf{重新连接}：通过非性的亲密行为和性活动，重新建立伴侣之间的情感连接和亲密感。',
     '_r22_blk5.tex', 'after', r'\section{性爱意愿不一致与"无性婚姻"'),
    ('book.tex',
     '在尝试任何饮食干预前，建议咨询医生或注册营养师，尤其是备孕、孕期或有内分泌疾病的人群。' + CR + r'\end{tcolorbox}',
     '_r22_blk6.tex', 'after', r'\subsection{"壮阳"补充剂与性健康产品：循证评价}'),
    ('female.tex', r'\subsection{性唤起障碍}', '_r22_blk7.tex', 'before',
     r'\subsection{不同避孕方式对女性性欲与性体验的影响}'),
    ('female.tex', r'\subsection{深层性交痛（子宫内膜异位 / PID / 卵巢病变）}', '_r22_blk8.tex', 'after',
     '与插入时或阴道口的'),
    ('male.tex', r'\subsection{年龄轨迹与"波动"和"异常"的界线}', '_r22_blk9.tex', 'before',
     r'\subsection{二次性爱与不应期的管理}'),
]

def main():
    files = {}
    for f, *_ in JOBS:
        if f not in files:
            files[f] = io.open(f, encoding='utf-8', newline='').read()

    ok = True
    for f, anchor, blkfile, pos, key in JOBS:
        text = files[f]
        if key in text:
            print('[跳过·已存在] %-10s %s' % (f, key[:38]))
            continue
        n = text.count(anchor)
        if n != 1:
            print('[失败·锚点=%d] %-10s %s' % (n, f, anchor[:50]))
            ok = False
            continue
        block = load_block(blkfile)
        repl = (anchor + CR + CR + block) if pos == 'after' else (block + CR + CR + anchor)
        files[f] = text.replace(anchor, repl, 1)
        print('[写入] %-10s %s  (%s)' % (f, blkfile, pos))

    if not ok:
        print('\n有锚点未命中，未写盘。')
        sys.exit(1)

    for f, data in files.items():
        io.open(f, 'w', encoding='utf-8', newline='').write(data)
        print('[保存] %s' % f)

main()
