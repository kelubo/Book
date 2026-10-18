# -*- coding: utf-8 -*-
"""r46 校验：36 条增写独特定位串 + bare LF + markdown 残留"""
import io, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
texts = {}
for fn in ("book.tex", "female.tex", "male.tex"):
    with io.open(os.path.join(BASE, fn), "r", encoding="utf-8", newline="") as f:
        texts[fn] = f.read()

MARK = [
    ("b428", "性刺激开始后约 10--30 秒"), ("b509", "尿道球腺分泌少量清亮液体"),
    ("b869", "起源于印度、包含仪轨与身心整合的宗教传统"), ("b1019", "不要向阴道或直肠内灌洗"),
    ("b1432", "意定监护"), ("b1604", "带底座或拉环的款式"),
    ("b3011", "第四代试剂可同时检测抗原与抗体"), ("b3483", "主要是 6 型与 11 型"),
    ("b3832", "斑疹—丘疹—水疱—脓疱—结痂"), ("b21234", "自我客体化"),
    ("b21280", "自发型（无缘由地想到性）与反应型"), ("b21392", "免费站点普遍存在未经同意上传"),
    ("b22612", "良性前列腺增生（BPH"), ("b22771", "白色稠厚豆渣样分泌物"),
    ("b23032", "sexual aversion"), ("b23390", "球海绵体肌与耻骨尾骨肌"),
    ("b24700", "愿望清单，各自写下想尝试"), ("b24913", "全国妇联维权热线 12338"),
    ("b24983", "把性以外的亲密纳入"), ("b26272", "看源头（专业学会、公立医院、疾控中心"),
    ("b26319", "公开场所、告知朋友行程"), ("b26373", "拍之前、存之时、泄之后"),
    ("b27517", "负有监护、收养、看护、教育、医疗等特殊职责者"), ("b27690", "生命伦理四原则"),
    ("f587", "采用神经保留技术的重建与部分缩乳手术"), ("f3255", "re-enactment"),
    ("f3497", "8--12 周评估变化"), ("f6594", "子宫位置（前倾/后倾）在正常范围内变异很大"),
    ("f8719", "provoked vestibulodynia"), ("f19764", "infibulation"),
    ("m622", "研究者误以为来自前列腺"), ("m2166", "折叠术、斑块切开加补片"),
    ("m2223", "一个生精周期约 74 天"), ("m4107", "双酚 A（BPA"),
    ("m5259", "bigorexia"), ("m6644", "男性性感带地图"),
]
ok = 0
warns = []
for key, mark in MARK:
    n = sum(t.count(mark) for t in texts.values())
    if n == 1:
        ok += 1
        s = "OK"
    elif n > 1:
        s = "x%d <<检查>>" % n
        warns.append(key)
    else:
        s = "MISSING!"
        warns.append(key)
    print("%-8s %-12s %s" % (key, s, mark))
print("定位 %d/%d  需复核: %s" % (ok, len(MARK), warns or "无"))
for fn, raw in texts.items():
    bare = raw.replace("\r\n", "").count("\n")
    md = sum(1 for ln in raw.split("\r\n") if re.match(r"^\s*(#{1,4}\s|\*\*|\|.*\|)", ln))
    print("%-12s bareLF=%d md残留=%d" % (fn, bare, md))
