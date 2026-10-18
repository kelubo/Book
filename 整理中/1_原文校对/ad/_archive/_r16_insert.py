# -*- coding: utf-8 -*-
"""第十六轮扩展：8 处新增/补全（CRLF 安全，唯一性 + 幂等校验，按文件独立提交）"""
import os
from collections import OrderedDict

BASE = r"D:/Git/Book/整理中/1_原文校对/ad"
CR = "\r\n"

def load(name):
    with open(os.path.join(BASE, name), encoding="utf-8", newline="") as f:
        t = f.read()
    return t.replace("\r\n", "\n").replace("\r", "\n").replace("\n", CR)

def save(name, text):
    with open(os.path.join(BASE, name), "w", encoding="utf-8", newline="") as f:
        f.write(text)

NEXT_GUT = "\\section{肠道菌群-脑-性轴（Gut-Brain-Sex Axis）}"
DISABLED = "\\section{残疾人的性需求与解决方案}"

# TASKS: (file, anchor, blk, mode, idem)
#   mode: after / before / fill(以 anchor 首行标题为界，正文插在标题后)
TASKS = [
    # 1) book 性欲节律 / 戒色
    ("book.tex",
     "- 参加性健康相关的课程或工作坊，学习性健康知识和技巧。",
     "_r16_blk1.tex", "after", "性欲不是一台恒速运转的发动机"),

    # 2) book 养老机构与长期照护
    ("book.tex",
     CR + DISABLED + CR,
     "_r16_blk2.tex", "special2", "当老年人进入养老院、护理院或需要家人长期照护时"),

    # 3) book 特殊职业人群
    ("book.tex",
     "尊重差异、明确同意、按需调整，与任何关系并无不同。" + CR + "\\end{tcolorbox}",
     "_r16_blk3.tex", "after", "长期异地、作息颠倒、封闭环境与高强度压力"),

    # 4) book 癫痫与性功能
    ("book.tex",
     NEXT_GUT,
     "_r16_blk4.tex", "before", "癫痫是常见的慢性神经系统疾病"),

    # 5) female 补全《性欲低下的原因与应对》
    ("female.tex",
     "\\subsection{性欲低下的原因与应对}" + CR + "\\subsection{性唤起障碍}",
     "_r16_blk5.tex", "fill5", "性欲低下是女性最常见的性困扰之一"),

    # 6) female 补全《性厌恶》
    ("female.tex",
     "\\subsection{性厌恶}" + CR + CR + "\\subsection{HSDD 与氟班色林（Addyi）}",
     "_r16_blk6.tex", "fill6", "性厌恶（sexual aversion）指对性接触产生强烈的厌恶"),

    # 7) female 性交后的身体护理与清洁
    ("female.tex",
     "\\item \\textbf{异常信号}：外阴持续性瘙痒、疼痛、溃疡、增厚变白、疣状赘生物、反复毛囊炎或出血，应及时就诊，不要自行涂抹激素或抗生素药膏。" + CR + "\\end{itemize}",
     "_r16_blk7.tex", "after", "性活动结束后的一小段自我照护"),

    # 8) male 男性不育的心理压力与伴侣支持
    ("male.tex",
     "HIV 感染不等于生育禁令。整个过程的关键词是：\\textbf{先治疗、后备孕、全程管理}——把病毒长期压到检测不到，再在专科医生指导下选择自然受孕或洗精路径，绝大多数感染者家庭都能迎来健康的孩子。" + CR + "\\end{tcolorbox}",
     "_r16_blk8.tex", "after", "生育困难带来的心理冲击，社会往往只看见女性"),
]

def build(anchor, content, mode):
    if mode == "after":
        return anchor + CR + CR + content
    if mode == "before":
        return content + CR + CR + anchor
    if mode == "special2":
        # anchor = CR + \section{...} + CR ；在其前插入
        head = CR
        tail = DISABLED + CR
        return head + content + CR + CR + tail
    if mode == "fill5":
        h = "\\subsection{性欲低下的原因与应对}"
        nxt = "\\subsection{性唤起障碍}"
        return h + CR + CR + content + CR + CR + nxt
    if mode == "fill6":
        h = "\\subsection{性厌恶}"
        nxt = "\\subsection{HSDD 与氟班色林（Addyi）}"
        return h + CR + CR + content + CR + CR + nxt
    raise ValueError(mode)

by_file = OrderedDict()
for t in TASKS:
    by_file.setdefault(t[0], []).append(t)

all_ok = True
for fname, tasks in by_file.items():
    text = load(fname)
    file_ok = True
    for (_, anchor, blk, mode, idem) in tasks:
        if idem in text:
            print(f"[SKIP ] {fname}: 已存在 -> {idem[:26]}")
            continue
        n = text.count(anchor)
        if n != 1:
            print(f"[FAIL ] {fname}: 锚点命中 {n} 次(期望1) -> {anchor[:50]!r}")
            file_ok = False; all_ok = False
            continue
        content = load(blk)
        text = text.replace(anchor, build(anchor, content, mode), 1)
        print(f"[ OK  ] {fname}: {blk} ({mode})")
    if file_ok:
        save(fname, text)
        print(f"[SAVE ] {fname}")
    else:
        print(f"[HOLD ] {fname}: 有失败项，未写入")

print("=== 完成 ===" if all_ok else "=== 存在失败项 ===")
