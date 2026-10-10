# -*- coding: utf-8 -*-
"""r43 锚点探测：候选插入位置 + 精确标题 count"""
import io, os, re
BASE = os.path.dirname(os.path.abspath(__file__))

def load(fn):
    with io.open(os.path.join(BASE, fn), "r", encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n").replace("\r", "\n").split("\n")

P = {fn: load(fn) for fn in ("book.tex", "female.tex", "male.tex")}

# ---- (1) 关键词搜索：找候选锚 ----
KEYS = [
    "造口", "结直肠", "肠道", "直肠",
    "癫痫", "惊厥",
    "继亲", "继子女", "再婚", "复婚",
    "军人", "警察", "消防", "特殊职业", "高强度职业", "夜班",
    "留学", "移民", "跨文化", "跨国",
    "依恋", "拒绝",
    "密宗", "坦陀罗", "慢爱", "冥想",
    "间性", "双性人", "DSD",
    "独居", "空巢",
    "呼吸暂停", "打鼾", "睡眠呼吸",
    "监狱", "服刑", "军旅",
]

for fn in ("book.tex", "female.tex", "male.tex"):
    print("\n" + "#" * 70)
    print("### 关键词搜索 %s" % fn)
    print("#" * 70)
    for i, ln in enumerate(P[fn], 1):
        s = ln.strip()
        if s.startswith("\\chapter{") or s.startswith("\\section{") or s.startswith("\\subsection{"):
            for k in KEYS:
                if k in s:
                    print("%6d %s" % (i, s[:100]))
                    break

# ---- (2) 精确锚标题 count（用于校验锚唯一性）----
ANCHORS = {
    "book.tex": [
        r"\section{年龄差伴侣：忘年恋的亲密与挑战}",
        r"\section{性反应的个体差异与常见问题}",
        r"\subsection{睡眠建议}",
        r"\subsection{老年期性传播感染的预防}",
        r"\subsection{不同类型残疾人群的性健康特点}",
        r"\subsection{联合国 CRPD 公约与残疾人性权利}",
        r"\section{性与多元关系}",
        r"\section{周末夫妻与两地分居：维系性亲密的策略}",
        r"\section{性焦虑与性恐惧}",
        r"\subsection{性心理障碍与治疗}",
        r"\section{残疾人的性需求与解决方案}",
        r"\section{性与分手、离婚}",
        r"\section{性与特殊人群}",
    ],
}
for fn, arr in ANCHORS.items():
    print("\n" + "=" * 70)
    print("### 精确锚 count %s" % fn)
    print("=" * 70)
    for a in arr:
        hits = [i for i, ln in enumerate(P[fn], 1) if ln.strip() == a]
        print("count=%d  %s  @%s" % (len(hits), a, hits))
