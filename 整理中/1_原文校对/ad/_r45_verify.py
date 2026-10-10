# -*- coding: utf-8 -*-
"""r45 校验：36 条增写独特定位串 + bare LF + markdown 残留"""
import io, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
texts = {}
for fn in ("book.tex", "female.tex", "male.tex"):
    with io.open(os.path.join(BASE, fn), "r", encoding="utf-8", newline="") as f:
        texts[fn] = f.read()

MARK = [
    ("b539", "发表于《性行为档案》"), ("b616", "抗副中肾管激素"),
    ("b628", "同源器官——两者都由胚胎期的生殖结节"), ("b652", "产房超声曾记录到胎儿"),
    ("b1134", "一滴精十滴血"), ("b1549", "穿衣认知"),
    ("b2997", "肺孢子菌肺炎"), ("b3021", "NAMES Project"),
    ("b3057", "规范接受抗逆转录病毒治疗（ART）者"), ("b3349", "悄然上行感染"),
    ("b3517", "专门寄生于阴毛区域"), ("b7639", "最好的选择永远是不开始"),
    ("b8231", "择偶偏好"), ("b8280", "延长小鼠卵巢寿命"),
    ("b21028", "用顺从换取关系"), ("b21052", "把注意力从表现监控"),
    ("b21308", "眼动脱敏再加工"), ("b24692", "勉强点头不算同意"),
    ("b25416", "复合性行为"), ("b25653", "口水题"),
    ("b26055", "沿用数十年的"), ("b30181", "前列腺癌风险相关联"),
    ("b46508", "贩卖焦虑的私立营销"), ("b53968", "哺乳闭经避孕法"),
    ("f3207", "高欲望窗口"), ("f3404", "边躲边笑的"),
    ("f3436", "蓝色小药丸"), ("f4865", "冲刷尿道口细菌"),
    ("f11725", "走到哪一步为止"), ("f12341", "以 6 周复查为起点"),
    ("m561", "菌血症"), ("m1078", "带上秒表做爱"),
    ("m1108", "三管齐下者"), ("m2702", "显微取精"),
    ("m5338", "借工作或酒精逃避"), ("m7816", "最伤宗筋"),
]
ok = 0
for key, mark in MARK:
    n = sum(t.count(mark) for t in texts.values())
    s = "OK" if n == 1 else "x%d <<检查>>" % n if n > 1 else "MISSING!"
    if n == 1:
        ok += 1
    print("%-8s %-9s %s" % (key, s, mark))
print("定位 %d/%d" % (ok, len(MARK)))
for fn, raw in texts.items():
    bare = raw.replace("\r\n", "").count("\n")
    md = sum(1 for ln in raw.split("\r\n") if re.match(r"^\s*(#{1,4}\s|\*\*|\|.*\|)", ln))
    print("%-12s bareLF=%d md残留=%d" % (fn, bare, md))
