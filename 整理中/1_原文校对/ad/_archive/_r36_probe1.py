# -*- coding: utf-8 -*-
import io, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
T = {}
for fn in ['book.tex', 'female.tex', 'male.tex']:
    T[fn] = io.open(BASE + '\\' + fn, encoding='utf-8', newline='').read()

G = {
 '避孕': ['避孕套', '安全套', '避孕药', '口服避孕药', '短效避孕', '长效避孕', '紧急避孕', '事后避孕',
          '宫内节育器', 'IUD', '节育环', '皮下埋植', '避孕针', '避孕贴', '阴道环', '杀精剂', '避孕海绵',
          '隔膜', '宫颈帽', '结扎', '输精管', '输卵管', '男性避孕', '避孕责任', '避孕失败', '避孕有效率',
          '完美使用', '典型使用', '珍珠指数', '安全期', '体外射精', '基础体温', '比林斯', '哺乳期闭经',
          '避孕方法选择', '避孕咨询', '月经杯', '避孕观念', '避孕副作用', '激素避孕'],
 '经期性爱': ['经期性爱', '经期性交', '月经期性交', '经期做爱', '月经期性行为', '经期同房', '经血',
              '经期卫生', '月经期', '痛经', '经前综合征', 'PMS', '经期怀孕', '经期高潮', '经期缓解',
              '经期禁忌', '子宫内膜异位', '经期欲望', '经期变化', '月经周期与性欲', '排卵期', '围绝经',
              '月经推迟', '经期不适'],
}

def wc(word, text):
    if re.match(r'^[A-Za-z][A-Za-z\- ]*$', word):
        return len(re.findall(re.escape(word), text, re.I))
    return text.count(word)

for name, words in G.items():
    print('===== %s =====' % name)
    for w in words:
        c = [wc(w, T[fn]) for fn in ['book.tex', 'female.tex', 'male.tex']]
        flag = ' <== 全零' if sum(c) == 0 else (' (薄)' if sum(c) <= 3 else '')
        print('%-18s book=%-5d female=%-5d male=%-5d%s' % (w, c[0], c[1], c[2], flag))
    print()

print('===== 含关键词的标题（三卷）=====')
pat = re.compile(r'\\(section|subsection|subsubsection)\{([^{}]*)\}')
kw = ['避孕', '安全套', '节育', '绝育', '结扎', '经期', '月经', '痛经', '经前', '排卵', '周期',
      '性欲与激素', '激素', '生育控制', '安全期']
for fn, t in T.items():
    for i, l in enumerate(t.split('\n'), 1):
        s = l.strip()
        m = pat.match(s)
        if m and any(k in m.group(2) for k in kw):
            print('%-11s L%-6d %s %s' % (fn, i, m.group(1), m.group(2)[:76]))
