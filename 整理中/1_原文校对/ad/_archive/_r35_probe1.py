# -*- coding: utf-8 -*-
import io, re
BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
T = {}
for fn in ['book.tex', 'female.tex', 'male.tex']:
    T[fn] = io.open(BASE + '\\' + fn, encoding='utf-8', newline='').read()

G = {
 '婚外': ['婚外情', '婚外性', '婚外恋', '出轨', '外遇', '不忠', '背叛', '偷情', '小三', '情人', 'affair',
          'infidelity', 'cheating', '开放式关系', '开放关系', '多边恋', 'polyamory', '多元关系', '非单偶',
          '婚内单身', '无性婚姻', '原谅', '修复信任'],
 '捆绑': ['捆绑', '绳缚', '绳艺', '紧缚', '束缚', '绳痕', '神经压迫', '悬吊', '安全剪', '自救', '尺神经',
          '桡神经', '黄麻', '棉绳', '绳索', '解绳', '拘束', '手铐', '绑缚'],
 '情趣用品': ['情趣用品', '性玩具', '振动棒', '跳蛋', '按摩棒', '飞机杯', '自慰器', '成人用品', '玩具清洁',
              '消毒', '材质', '硅胶', 'TPE', '邻苯二甲', '多孔', '润滑剂兼容', '共用玩具', '蛋蛋', '炮机'],
 '情趣内衣': ['情趣内衣', '内衣', '蕾丝', '丝袜', '制服', '恋物', 'fetish', '角色扮演', 'cosplay', '睡衣',
              '高跟鞋', '皮革', 'latex', '乳胶'],
 '灌肠': ['灌肠', '灌肠器', '肠道准备', '深灌', '浅清洁', '肛门清洁', '生理盐水', '肠道菌群', '开塞露',
          '灌洗', 'enema', '肛交准备', '肛交疼痛'],
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
        print('%-16s book=%-5d female=%-5d male=%-5d%s' % (w, c[0], c[1], c[2], flag))
    print()

print('===== 含关键词的标题（三卷）=====')
pat = re.compile(r'\\(section|subsection|subsubsection)\{([^{}]*)\}')
kw = ['婚外', '出轨', '不忠', '外遇', '开放', '多边', 'polyam', '捆', '绳', '缚', '束缚', '拘束', '玩具',
      '情趣', '振动', '自慰器', '内衣', '丝袜', '制服', '恋物', 'fetish', '角色', '灌肠', '清洁', '消毒']
for fn, t in T.items():
    for i, l in enumerate(t.split('\n'), 1):
        s = l.strip()
        m = pat.match(s)
        if m and any(k.lower() in m.group(2).lower() for k in kw):
            print('%-11s L%-6d %s %s' % (fn, i, m.group(1), m.group(2)[:78]))
