# -*- coding: utf-8 -*-
"""r57：修复 female.tex 中"全角句号吞字符"的存量缺陷（数字/量词被替换为「。」）
用法：python _r57_fix.py          # dry-run
      python _r57_fix.py apply    # 落盘
说明：逐条按行号 + 行内正则定位，断言每行匹配恰 1 次；回填值依据见报告。
"""
import io, os, re, shutil, sys

D = 'D:/Git/Book/整理中/1_原文校对/ad/'
SRC = D + 'female.tex'
BAK = D + '_backup_r57/female.tex'
OUT = D + '_r57_fix_out.txt'
APPLY = len(sys.argv) > 1 and sys.argv[1] == 'apply'

DASH = r'[-\u2010-\u2011\u2013-\u2015\u2212]'   # 各种连字符/减号
COLON = r'[:：]'

# (行号, 正则, 新串, 定值依据)
FIXES = [
    (9009, r'直径。\.6厘米', '直径0.6厘米',
     '女性尿道长3~5cm、直径约0.6cm（科普中国/人体解剖学名词）'),
    (9010, r'长。' + DASH + r'5厘米', '长3-5厘米',
     '同上：女性尿道长约3-5厘米'),
    (9089, r'持续时间超。天', '持续时间超过7天',
     '正常经期3-7天，超过7天为经期延长'),
    (9215, r'收缩频率。\.8。次', '收缩频率0.8秒/次',
     '高潮平台收缩间隔约0.8秒（Masters & Johnson 1966）'),
    (9219, r'，。' + DASH + r'3厘米', '，4-5厘米',
     '儿童期阴道只有4~5cm长，上皮薄无皱襞（北京协和医院科普，与本句逐字对应）'),
    (9220, r'长度增加。' + DASH + r'10厘米', '长度增加至7-10厘米',
     '青春期阴道发育至接近成人（7-10厘米）'),
    (11109, r'长。' + DASH + r'8厘米，宽。' + DASH + r'5厘米，厚。' + DASH + r'3厘米，重。0-70克',
     '长7-8厘米，宽4-5厘米，厚2-3厘米，重40-70克',
     '教科书成人子宫：7-8×4-5×2-3cm、重40-70g'),
    (11140, r'平均。8天，提前或延。天', '平均28天，提前或延7天',
     '月经周期21-35天，即提前或延后7天'),
    (11141, r'月经周期的。' + DASH + r'14天', '月经周期的第5-14天',
     '增殖期为月经周期第5-14天'),
    (11141, r'厚度。\.5毫米增加。' + DASH + r'5毫米', '厚度0.5毫米增加至3-5毫米',
     '增殖期子宫内膜由0.5mm增至3-5mm'),
    (11142, r'月经周期的。5-28天', '月经周期的第15-28天',
     '分泌期为月经周期第15-28天'),
    (11143, r'月经周期的。' + DASH + r'4天', '月经周期的第1-4天',
     '月经期为月经周期第1-4天'),
    (11148, r'长度增加。' + DASH + r'8厘米', '长度增加至7-8厘米',
     '青春期子宫发育至接近成人（长7-8厘米）'),
    (11148, r'比例变。' + COLON + r'1', '比例变为2:1',
     '本卷 book.tex L15890：青春期宫体与宫颈比例逐渐变为2:1'),
    (11150, r'重量可。100克', '重量可达1000克',
     '妊娠足月子宫重约1000克（未孕的20倍）'),
    (11150, r'子宫腔容积可。000毫升', '子宫腔容积可达5000毫升',
     '妊娠足月子宫腔容积约5000毫升（未孕的1000倍）'),
    (11151, r'产。周左右', '产后6周左右',
     '子宫复旧：book.tex L17005 作6-8周'),
    (11222, r'长。厘米，管腔最窄', '长1厘米，管腔最窄',
     'book.tex L16921：输卵管间质部长约1-2厘米'),
    (11223, r'长。' + DASH + r'3厘米', '长2-3厘米',
     'book.tex L16922：峡部长约2-3厘米'),
    (11292, r'约。厘米×3厘米×1厘米', '约4厘米×3厘米×1厘米',
     'book.tex L15043：卵巢大小约4×3×1厘米'),
    (11292, r'重。' + DASH + r'6克', '重5-6克',
     'book.tex L15043：卵巢重量约5-6克'),
    (11308, r'前。4天左右', '前14天左右',
     '排卵发生在下次月经来潮前14天左右'),
]

log = []


def fail(msg):
    log.append('【失败】' + msg)
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(log))
    sys.exit(1)


raw = io.open(SRC, encoding='utf-8', newline='').read()
lines = raw.splitlines(keepends=True)
log.append('读入 female.tex：行数 %d，字节 %d' % (len(lines), len(raw.encode('utf-8'))))
log.append('bare LF = %d' % sum(1 for ln in raw.split('\n')[:-1] if not ln.endswith('\r')))

new = list(lines)
touched = {}
for lineno, pat, rep, why in FIXES:
    i = lineno - 1
    if i < 0 or i >= len(new):
        fail('行号 %d 越界' % lineno)
    hits = re.findall(pat, new[i])
    if len(hits) != 1:
        fail('L%d 正则命中 %d 次（应为 1）：%s\n    实际行：%r' % (lineno, len(hits), pat, new[i][:120]))
    before = new[i]
    new[i] = re.sub(pat, rep, new[i], count=1)
    if new[i] == before:
        fail('L%d 替换无变化' % lineno)
    touched.setdefault(lineno, []).append((before.rstrip('\r\n'), new[i].rstrip('\r\n'), why))

log.append('替换条数 = %d，涉及行数 = %d' % (len(FIXES), len(touched)))
log.append('')
for lineno in sorted(touched):
    for before, after, why in touched[lineno]:
        log.append('L%d' % lineno)
        log.append('  旧：%s' % before)
        log.append('  新：%s' % after)
        log.append('  据：%s' % why)

# ---- 落盘前校验 ----
if len(new) != len(lines):
    fail('行数发生变化：%d -> %d' % (len(lines), len(new)))
changed = [k for k in range(len(lines)) if new[k] != lines[k]]
if sorted(k + 1 for k in changed) != sorted(touched.keys()):
    fail('改动行集合与预期不符：%s' % [k + 1 for k in changed])
res = ''.join(new)
for lineno in sorted(touched):
    if '。' in new[lineno - 1] and re.search(r'。' + DASH + r'?\d', new[lineno - 1]):
        fail('L%d 仍残留「。+数字」形态' % lineno)
if '**' in res:
    fail('结果含 markdown 加粗 **')
if res.count('\t') != raw.count('\t'):
    fail('制表符数量变化：%d -> %d' % (raw.count('\t'), res.count('\t')))
if sum(1 for ln in res.split('\n')[:-1] if not ln.endswith('\r')) != 0:
    fail('结果出现 bare LF')
log.append('')
log.append('校验通过：行数不变（%d）；改动行恰为预期 %d 行；无「。+数字」残留；无 bare LF' % (len(new), len(touched)))

if APPLY:
    if not os.path.exists(BAK):
        fail('备份不存在，拒绝落盘')
    io.open(SRC, 'w', encoding='utf-8', newline='').write(res)
    log.append('已落盘：%s' % SRC)
else:
    log.append('（dry-run，未写盘）')

io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(log))
print('\n'.join(log))
