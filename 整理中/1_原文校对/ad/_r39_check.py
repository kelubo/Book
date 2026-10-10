# -*- coding: utf-8 -*-
"""r39 转换质量抽样（按锚文本定位）"""
import io, os
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
bk = io.open(os.path.join(BASE, 'book.tex'), encoding='utf-8', newline='').read().split('\r\n')
fe = io.open(os.path.join(BASE, 'female.tex'), encoding='utf-8', newline='').read().split('\r\n')
ma = io.open(os.path.join(BASE, 'male.tex'), encoding='utf-8', newline='').read().split('\r\n')

def find(ls, anchor, from_=0):
    for i in range(from_, len(ls)):
        if anchor in ls[i]:
            return i
    return -1

def dump(tag, ls, anchor, pre=3, post=14):
    i = find(ls, anchor)
    print('--- %s (锚 L%d) ---' % (tag, i+1))
    for j in range(max(0, i-pre), min(i+post, len(ls))):
        print('%6d %s' % (j+1, ls[j][:76]))
    print()

# 1. 编者注 bullet 群
dump('book 编者注 bullet 群', bk, '捏阴茎法类似于性治疗中的')
# 2. 混合 N. + 子 bullet
dump('book 海绵体混合结构', bk, '阴茎由三个平行的海绵体组成')
# 3. 三级嵌套
dump('book 三级嵌套(社交媒体)', bk, '数字时代的性健康')
# 4. 表格
dump('book 表格1', bk, '| 特点 | 传统性教育 |')
# 5. female 漏% 已补
dump('female 漏%补丁', fe, '产后抑郁识别与求助', pre=2, post=3)
# 6. female bullet 群
dump('female 处女膜 bullet', fe, '筛状处女膜', pre=4, post=8)
# 7. male 混合
dump('male 停动法混合', ma, '射精阈值感知训练', pre=2, post=10)
