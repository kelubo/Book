# -*- coding: utf-8 -*-
import re
T = {k: open(f, encoding='utf-8').read() for k, f in
     {'book': 'book.tex', 'female': 'female.tex', 'male': 'male.tex'}.items()}

topics = [
    '造口', '肠造口', '尿路造口', '瘫痪与性', '截瘫', '脊髓损伤',
    '临终', '濒死', '生命最后', '末期患者', '癌症晚期与性', '癌痛',
    '疼痛与性', '安宁', '舒缓医疗', 'hospice', 'palliative',
    '性欲亢进（男性）', '性欲亢进与躁狂', '双相与性欲', '躁狂性欲',
    '男性性欲下降', '性欲减退（男性）', '心理性勃起障碍', '焦虑性ED',
    '性幻想', '晨勃监测', '邮票试验', 'RigiScan', '睡眠相关勃起',
    '生物反馈', '性治疗', '性感集中训练', '感官聚焦',
    '性健康自测', '性功能自评', '健康日记',
]
print('%-22s %8s %8s %8s' % ('主题', 'book', 'female', 'male'))
for c in topics:
    print('%-22s %8d %8d %8d' % (c, len(re.findall(c, T['book'])),
                                 len(re.findall(c, T['female'])), len(re.findall(c, T['male']))))

print('\n===== male 性欲亢进 上下文 =====')
for m in re.finditer('性欲亢进', T['male']):
    s = max(0, m.start()-40); e = min(len(T['male']), m.end()+40)
    print('...' + T['male'][s:e].replace('\n', '⏎') + '...')

print('\n===== book 丧偶 上下文（前5处）=====')
for i, m in enumerate(re.finditer('丧偶', T['book'])):
    if i >= 5: break
    s = max(0, m.start()-50); e = min(len(T['book']), m.end()+50)
    print('...' + T['book'][s:e].replace('\n', '⏎') + '...')
