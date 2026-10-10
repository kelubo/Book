# -*- coding: utf-8 -*-
import io, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
T = {}
for fn in ['book.tex', 'female.tex', 'male.tex']:
    T[fn] = io.open(BASE + '\\' + fn, encoding='utf-8', newline='').read()

def cnt(w):
    c = [T[fn].count(w) for fn in ['book.tex', 'female.tex', 'male.tex']]
    return c

print('===== 避孕细项词面 =====')
words = ['漏服', '忘记服', '忘记吃', '错过服药', '服药依从', '呕吐', '腹泻', '抗生素', '药物相互作用',
         '圣约翰草', '抗癫痫', '利福平', '体重', 'BMI', '超重', '停用', '停药', '恢复生育力', '生育力恢复',
         '避孕协商', '共同决策', '避孕责任', '责任分担', '男性参与', '避孕套使用意愿', '拒用',
         '避孕方法转换', '更换避孕', '长期使用', '连续服用', '安慰剂', '服药时间', '定时服药',
         '避孕套过敏', '乳胶过敏', '避孕套失败', '滑脱', '破裂', '双重保护', '双保险']
for w in words:
    c = cnt(w)
    flag = ' <== 全零' if sum(c) == 0 else (' (薄)' if sum(c) <= 3 else '')
    print('%-16s book=%-5d female=%-5d male=%-5d%s' % (w, c[0], c[1], c[2], flag))

print()
print('===== 经期细项词面 =====')
words2 = ['经期性欲', '经期盆腔', '盆腔充血', '月经杯性交', '软杯', '逆流', '经血逆流', '经期疼痛',
          '经期运动', '经期游泳', '经期沟通', '经期观念', '文化禁忌', '月经禁忌', '经期口交',
          '经期肛交', '经期自慰', '经期高潮缓解', '内啡肽', '催产素', '经期激素', '月经周期激素',
          '卵泡期性欲', '黄体期性欲', '排卵期性欲', '性欲高峰']
for w in words2:
    c = cnt(w)
    flag = ' <== 全零' if sum(c) == 0 else (' (薄)' if sum(c) <= 3 else '')
    print('%-16s book=%-5d female=%-5d male=%-5d%s' % (w, c[0], c[1], c[2], flag))

print()
print('===== female L2763《女性性欲的激素周期性波动》=====')
for i in range(2763, 2810):
    s = T['female.tex'].split('\n')[i - 1].strip()
    if s:
        print('L%d | %s' % (i, s[:118]))
