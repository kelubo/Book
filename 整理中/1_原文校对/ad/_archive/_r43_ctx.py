# -*- coding: utf-8 -*-
"""r43 抽查：判断候选方向是真空白还是已有覆盖"""
import io, os
BASE = os.path.dirname(os.path.abspath(__file__))

def load(fn):
    with io.open(os.path.join(BASE, fn), "r", encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n").replace("\r", "\n").split("\n")

BOOK = load("book.tex")

SEGS = [
    ("A 性交后反应节", 43840, 43920),
    ("B AI性伴侣与性机器人伦理", 26157, 26250),
    ("C 性与分手、离婚", 25218, 25260),
    ("D 强奸罪/性骚扰罪", 27168, 27232),
    ("E 养老机构与长期照护", 27615, 27650),
    ("F 长新冠后遗症", 3837, 3862),
    ("G 器官移植受者", 7875, 7920),
    ("H 甲状腺功能异常与性欲", 8098, 8140),
    ("I 肥胖症与性功能", 7825, 7875),
    ("J 睡眠与性健康", 29249, 29280),
    ("K 性爱体验的升华", 824, 880),
    ("L 老年期性健康特点", 52858, 52900),
]

for name, a, b in SEGS:
    print("\n" + "=" * 78)
    print("### %s  (L%d-%d)" % (name, a, b))
    print("=" * 78)
    for i in range(a, b + 1):
        if i - 1 < len(BOOK):
            print("%6d | %s" % (i, BOOK[i - 1][:96]))
