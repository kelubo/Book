# -*- coding: utf-8 -*-
"""r57 扫描：全角句号吞字符（数字/量词被替换为「。」）——放宽版
   候选判定：句号左侧 ≤6 字内出现"取值类"词（长/重/约/平均/可达/延/产/变/为/第/比例/容积…），
             且句号右侧 ≤2 字内是数字、冒号+数字、或度量量词。
"""
import io, re

D = 'D:/Git/Book/整理中/1_原文校对/ad/'
OUT = D + '_r57_scan_out.txt'

LEFT = re.compile(r'(长|重|约|平均|可达|可|延|产|变|为|至|到|宽|厚|高|直径|容积|长度|重量|'
                  r'增加|缩短|延长|持续|间隔|比例|第|占|达|在|每|超过|不足|约)\s*。\s*$')
LEFT_NEAR = re.compile(r'(长|重|约|平均|可达|可|延|产|变|为|至|到|宽|厚|高|直径|容积|长度|重量|'
                       r'增加|缩短|延长|持续|间隔|比例|第|占|达|在|每|超过|不足)\s*。')
RIGHT = re.compile(r'^\s*([-–~]?\d|[:：]\d|厘米|毫米|克|天|次|周|月|岁|毫升|小时|分钟|倍|％|%)')
RIGHT_UNIT = re.compile(r'^\s*[-–~]?\d+\s*(厘米|毫米|克|天|次|周|月|岁|毫升|小时|分钟|倍|％|%)')
# 明显正常的句末：后面是完整新句（年份/常见句首）
OK_HEAD = re.compile(r'^\s*(\d{4}\s*年|这|其|在|但|而|因此|所以|女性|男性|子宫|阴道|卵巢|月经|正常|'
                     r'如果|若|第一|此外|另外|同时|其中|可见|例如|目前|由|从|注意|值得|一般|通常|'
                     r'多数|有|无|不|研究|据|根据|以上|下面|上|下|她|他|她们|他们|由于|虽然|尽管|'
                     r'当|随着|为了|许多|部分|大多|有些|很多|极少|可能|约|近|自|至|从|到了|直到)')

lines_out = []
tot = 0
for f in ['book.tex', 'female.tex', 'male.tex']:
    t = io.open(D + f, encoding='utf-8', newline='').read()
    L = t.splitlines()
    rows = []
    for i, ln in enumerate(L, 1):
        code = ln.split('%')[0]
        for m in re.finditer('。', code):
            s = m.start()
            left = code[max(0, s - 6):s]
            right = code[s + 1:s + 12]
            if not LEFT_NEAR.search(left + '。'):
                continue
            if OK_HEAD.match(right):
                continue
            if RIGHT.match(right):
                rows.append((i, s, code[max(0, s - 22):s + 22]))
                break
    lines_out.append('===== %s：%d 行' % (f, len(rows)))
    for i, s, ctx in rows:
        lines_out.append('  L%-6d %s' % (i, ctx))
    lines_out.append('')
    tot += len(rows)
lines_out.append('三卷候选合计 %d 行' % tot)

io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines_out))
print('\n'.join(lines_out))
