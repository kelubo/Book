# -*- coding: utf-8 -*-
"""第十五轮扩展：7 个新节的锚点插入（CRLF 安全，含唯一性与幂等校验，按文件独立提交）"""
import os
from collections import OrderedDict

BASE = r"D:/Git/Book/整理中/1_原文校对/ad"

def load(name):
    with open(os.path.join(BASE, name), "r", encoding="utf-8", newline="") as f:
        t = f.read()
    return t.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\r\n")

def save(name, text):
    with open(os.path.join(BASE, name), "w", encoding="utf-8", newline="") as f:
        f.write(text)

# (目标文件, 锚文本, 插入内容文件, 方向, 幂等判据(内容中的独特片段))
TASKS = [
    ("book.tex",
     "- \\textbf{寻求专业帮助}：如果性厌倦的问题严重影响了夫妻关系和性生活的质量，可以寻求性治疗师或心理咨询师的帮助。",
     "_r15_blk1.tex", "after",
     "性活动结束之后，身体并不总是立刻回到平静"),

    ("book.tex",
     "- 性健康维护：建立健康的性行为习惯，定期进行性健康检查",
     "_r15_blk2.tex", "after",
     "青春期是性发育与性意识觉醒的时期"),

    ("female.tex",
     "\\item \\textbf{如出现瘙痒、异味、异常分泌物}：\\textbf{不要自行使用洗液或药物}，应及时就诊明确病因后规范治疗。\r\n\\end{itemize}",
     "_r15_blk3.tex", "after",
     "阴毛的生理功能"),

    ("female.tex",
     "\\item \\textbf{综合治疗}：通常结合心理治疗、盆底物理治疗等\r\n\\end{itemize}",
     "_r15_blk4.tex", "after",
     "性交疼痛恐惧（coitophobia，又称 genophobia"),

    ("female.tex",
     "\\subsection{女性高潮类型（阴蒂 / 阴道 / G点 / 混合）}",
     "_r15_blk5.tex", "after",
     "阴蒂高潮}：由阴蒂及其周围组织受刺激引发"),

    ("male.tex",
     "\\section{环境内分泌干扰物与男性生殖健康}",
     "_r15_blk6.tex", "before",
     "盆底肌（pelvic floor muscles）是封闭骨盆下口"),

    ("male.tex",
     "如果您发现家人服用多巴胺激动剂后出现异常强烈的性欲、赌博、购物等行为，应及时告知医生，这可能是药物引起的冲动控制障碍，需要调整治疗方案。\r\n\\end{tcolorbox}",
     "_r15_blk7.tex", "after",
     "性高潮后疾病综合征（Post-Orgasmic Illness Syndrome, POIS）"),
]

by_file = OrderedDict()
for t in TASKS:
    by_file.setdefault(t[0], []).append(t)

all_ok = True
for fname, tasks in by_file.items():
    text = load(fname)
    file_ok = True
    for (_, anchor, blk, direction, idem) in tasks:
        if idem in text:
            print(f"[SKIP ] {fname}: 已存在 -> {idem[:30]}")
            continue
        n = text.count(anchor)
        if n != 1:
            print(f"[FAIL ] {fname}: 锚点命中 {n} 次(期望1) -> {anchor[:45]}")
            file_ok = False
            all_ok = False
            continue
        content = load(blk)
        new = (anchor + "\r\n\r\n" + content) if direction == "after" else (content + "\r\n\r\n" + anchor)
        text = text.replace(anchor, new, 1)
        print(f"[ OK  ] {fname}: {blk} 已插入")
    if file_ok:
        save(fname, text)
        print(f"[SAVE ] {fname}")
    else:
        print(f"[HOLD ] {fname}: 有失败项，未写入")

print("=== 完成 ===" if all_ok else "=== 存在失败项 ===")
