# -*- coding: utf-8 -*-
"""r33 探测：女性性健康服务获取障碍 / 社群支持资源清单"""
import io, os, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
T = {}
for fn in ["book.tex", "female.tex", "male.tex"]:
    T[fn] = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read()

G = {
    "服务获取障碍": ["就医障碍", "服务获取", "就医歧视", "医疗歧视", "恐同", "恐跨", "就医体验", "敏感度", "友善医疗",
                "性别肯定医疗", "问诊", "就医延迟", "害怕就医", "医保", "未出柜", "自我披露", "隐私保护",
                "女同性恋者的性健康需求", "医疗服务可及性", "健康服务不足", "可及性"],
    "社群资源": ["支持团体", "社群", "热线", "援助热线", "NGO", "公益组织", "互助", "社群组织", "同伴支持",
              "资源清单", "求助渠道", "心理咨询资源", "危机干预", "社区中心", "健康中心", "疾控", "CDC",
              "免费检测", "匿名检测", "自检试剂", "PrEP", "PrEP 获取"],
}

for name, words in G.items():
    print("===== %s =====" % name)
    for w in words:
        c = [T[fn].count(w) for fn in ["book.tex", "female.tex", "male.tex"]]
        flag = " <== 全零" if sum(c) == 0 else (" (薄)" if sum(c) <= 3 else "")
        print("%-22s book=%-4d female=%-4d male=%-4d%s" % (w, c[0], c[1], c[2], flag))
    print()

print("===== 相关标题 =====")
pat = re.compile(r"\\(section|subsection|subsubsection)\{([^{}]*)\}")
kw = ["服务", "获取", "资源", "支持", "障碍", "就医", "医疗", "社群", "热线", "帮助", "权利", "权益"]
for fn, t in T.items():
    for i, l in enumerate(t.split("\n"), 1):
        m = pat.match(l.strip())
        if m and any(k in m.group(2) for k in kw):
            print("%-11s L%-6d %s %s" % (fn, i, m.group(1), m.group(2)))
