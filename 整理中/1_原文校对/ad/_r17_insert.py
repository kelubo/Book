# -*- coding: utf-8 -*-
import io, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
def rd(p):
    with io.open(os.path.join(BASE, p), 'r', encoding='utf-8', newline='') as f:
        return f.read()
def wr(p, s):
    with io.open(os.path.join(BASE, p), 'w', encoding='utf-8', newline='') as f:
        f.write(s)

def block(name):
    s = rd(name)
    return s.replace('\r\n', '\n').replace('\n', '\r\n')  # 统一为 CRLF

def do_replace(text, anchor, blk, where='after'):
    a = anchor.replace('\r\n', '\n')
    cands = [a.replace('\n', '\r\n'), a]
    for c in cands:
        n = text.count(c)
        if n == 1:
            if where == 'after':
                return text.replace(c, c + blk), 1
            else:
                return text.replace(c, blk + c), 1
        elif n > 1:
            raise SystemExit('!! 锚点不唯一 n=%d: %r' % (n, anchor[:40]))
    raise SystemExit('!! 未找到锚点: %r' % anchor[:40])

# ── book.tex ──
TASKS = {
 'book.tex': [
    # (锚点, 块文件, 位置, 幂等键)
    ('\\section{数字时代的性教育}',
     '_r17_blk1.tex', 'before', '\\subsection{性健康 App 与可穿戴设备'),
    ('若长期出现性欲明显低下、勃起困难或情绪问题，请及时就医——这与职业无关，只与健康有关。\r\n\\end{tcolorbox}',
     '_r17_blk2.tex', 'after', '\\section{住院、卧床与康复期间的性}'),
    ('把"什么时候可以"问清楚，比含含糊糊地冒险要稳妥得多。\r\n\\end{tcolorbox}',
     '_r17_blk3.tex', 'after', '\\section{临终关怀与性亲密}'),
    ('\\item[年度性健康自查] 将 STI 筛查、疫苗状态核对、生殖器自检与避孕方式复核纳入年度计划的自我管理做法，按人群与风险等级差异化安排（详见“求助与资源导航”章）。',
     '_r17_blk5.tex', 'after', '\\item[安宁疗护（Hospice Care）]'),
 ],
 'male.tex': [
    ('\t\\item \\textbf{治疗建议}：综合评估很重要，可能包括医学检查、心理治疗、关系咨询，必要时可考虑激素治疗（需严格评估）\r\n\\end{itemize}',
     '_r17_blk4.tex', 'after', '\\section{男性性欲的波动与节律}'),
 ],
}

for fname, jobs in TASKS.items():
    text = rd(fname)
    for anchor, blkf, where, key in jobs:
        if key in text:
            print('[skip] %s 已含 %s' % (fname, key[:30]))
            continue
        blk = block(blkf)
        text, _ = do_replace(text, anchor, blk, where)
        print('[ok]   %s ← %s (%s)' % (fname, blkf, where))
    wr(fname, text)
    print('== %s 已写回 ==' % fname)
print('DONE')
