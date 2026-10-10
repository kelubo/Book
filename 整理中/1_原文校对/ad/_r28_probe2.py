# -*- coding: utf-8 -*-
"""r28 二轮探测：药物副作用/chemsex/性工作者/民间困惑/冷话题"""
import io, re

BASE = r'D:/Git/Book/整理中/1_原文校对/ad/'
FILES = ['book.tex', 'female.tex', 'male.tex']

def strip_comments(s):
    return '\n'.join(re.sub(r'(?<!\\)%.*', '', ln) for ln in s.split('\n'))

texts = {f: strip_comments(io.open(BASE + f, encoding='utf-8').read()) for f in FILES}
raws = {f: io.open(BASE + f, encoding='utf-8').read() for f in FILES}

TERMS = {
    '药物与性': ['非那雄胺', '米诺地尔', 'SSRI', '抗抑郁药', '舍曲林', '帕罗西汀', '氟西汀',
             '降压药', 'β受体阻滞', '地平', '他汀', '抗精神病', '锂', '安眠药', '苯二氮'],
    'chemsex/助性物质': ['chemsex', '化学性爱', 'GHB', '摇头丸', '氯胺酮', 'K粉', 'rush', 'Rush',
                  '亚硝酸', 'Poppers', 'poppers', '助性', '催情'],
    '性交易': ['性工作者', '嫖娼', '卖淫', '援交', '嫖客', '商业性'],
    '生活方式/民间': ['裸睡', '晨勃', '性幻想', '情趣内衣', '指交', '乳交', '股交', '车震',
               '事后', '洗浴', '洗澡', '吹风', '空调', '冷水'],
    '女性困惑': ['阴吹', '子宫后位', '宫颈高潮', 'A点', 'U点', '漏尿', '性交漏尿',
             '阴道排气', '放屁'],
    '约会/正念/贫血': ['约会软件', '正念', '冥想', '贫血', '缺铁'],
}

hdr = '%-12s' % 'TERM' + ''.join('%9s' % f[:7] for f in FILES)
print(hdr)
for g, terms in TERMS.items():
    print('==== %s ====' % g)
    for term in terms:
        row = '%-12s' % term
        for f in FILES:
            row += '%9d' % texts[f].count(term)
        print(row)

# 标题级核查
print()
print('=== 标题含（避孕药/抑郁/药物/贫血/正念/冥想/晨勃/性幻想/嫖/工作者/漏尿/后位） ===')
for f, t in raws.items():
    for i, ln in enumerate(t.split('\n')):
        s = ln.strip()
        if re.match(r'\\(chapter|section|subsection|subsubsection)\{', s) and re.search(
                r'避孕药|抑郁|药物|贫血|正念|冥想|晨勃|性幻想|嫖|工作者|漏尿|后位|裸睡|酒精|吸烟|吸烟|烟', s):
            print('%-11s L%-6d %s' % (f, i + 1, s[:100]))
