# -*- coding: utf-8 -*-
"""r44 校验：36 条增写内容各出现一次 + bare LF + markdown 残留"""
import io, os, re, importlib.util

BASE = os.path.dirname(os.path.abspath(__file__))

def load_mod(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(BASE, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.C

C = {}
for mod in ("_r44_c1", "_r44_c2", "_r44_c3"):
    C.update(load_mod(mod))

texts = {}
for fn in ("book.tex", "female.tex", "male.tex"):
    with io.open(os.path.join(BASE, fn), "r", encoding="utf-8", newline="") as f:
        texts[fn] = f.read()

MARK = {
    "b577": "把前戏当作", "b1188": "科学人道主义委员会", "b1192": "张竞生",
    "b1301": "时间差补齐器", "b3087": "胎传梅毒", "b3363": "杜克雷嗜血杆菌",
    "b3392": "只治女方", "b3516": "长期抑制疗法", "b3554": "被动免疫",
    "b5013": "掌控权在女方", "b5221": "仰卧位低血压", "b5226": "借力支撑",
    "b5231": "降低体能消耗与心肺负担", "b21682": "四根支柱", "b21703": "禁欲 2--7 天",
    "b23548": "典型使用失败率", "b27361": "性同意年龄", "b28877": "配偶团聚",
    "b28941": "一种性取向", "b29616": "RED-S", "b29690": "连续一周每晚只睡 5 小时",
    "b30158": "全面性教育", "b30416": "复述对方的重点",
    "f1057": "两小时浸透一片", "f11351": "0.4--0.8 毫克叶酸", "f13930": "分层应对",
    "f14438": "阴道有自净能力", "f15586": "更换体位或请女性医护协助", "f20662": "产后多虚多瘀",
    "m1325": "晨勃", "m1526": "第 6 版参考值", "m1744": "RISUG",
    "m3796": "戒烟数月后", "m5057": "低创伤性骨折", "m7656": "不应期", "m7684": "肾主生殖",
}
ok = 0
for key, mark in MARK.items():
    n = sum(texts[fn].count(mark) for fn in texts)
    status = "OK " if n == 1 else ("WARN x%d" % n if n > 1 else "MISSING!")
    if n == 1:
        ok += 1
    print("%-8s %s  [%s]" % (key, status, mark))
print("定位 %d/%d" % (ok, len(MARK)))

# bare LF 与 markdown 残留
for fn, raw in texts.items():
    bare = raw.replace("\r\n", "").count("\n")
    md = sum(1 for ln in raw.split("\r\n") if re.match(r"^\s*(#{1,4}\s|\*\*|\|.*\|)", ln))
    print("%-12s bareLF=%d md残留=%d" % (fn, bare, md))
