# -*- coding: utf-8 -*-
"""r43 步骤1：备份三卷 + 探测本轮候选锚点（关键词扫描 section/subsection 行）"""
import io, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
BK = os.path.join(BASE, "_backup_r43")

# ---- 1. 备份 ----
if not os.path.isdir(BK):
    os.makedirs(BK)
for fn in ("book.tex", "female.tex", "male.tex"):
    src = os.path.join(BASE, fn)
    dst = os.path.join(BK, fn)
    shutil.copy2(src, dst)
    print("[backup]", fn, os.path.getsize(dst), "bytes")

# ---- 2. 读三卷 ----
def load(fn):
    with io.open(os.path.join(BASE, fn), "r", encoding="utf-8", newline="") as f:
        raw = f.read()
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    return raw.split("\n")

PAGES = {fn: load(fn) for fn in ("book.tex", "female.tex", "male.tex")}
for fn, L in PAGES.items():
    print("[load]", fn, len(L), "lines")

# ---- 3. 关键词探测 ----
KEYS = [
    "离婚", "分居", "复婚", "再婚",
    "数字时代", "虚拟", "人工智能", "机器人", "远程", "VR", "算法", "深伪", "深度伪造",
    "升华", "高级技巧", "性爱体验", "密宗", "坦陀罗", "慢爱", "冥想",
    "养老", "老年", "照护", "机构", "空巢", "独居",
    "移植", "器官", "透析", "肾病", "造口", "结直肠",
    "暴力", "强奸", "胁迫", "骚扰", "安全计划",
    "性反应", "性心理", "性欲", "性焦虑", "性厌恶", "忧郁", "头痛",
    "绝经", "更年期", "泌尿生殖", "GSM", "萎缩", "干燥",
    "勃起功能", "ED", "勃起", "早泄",
    "睡眠", "呼吸", "打鼾", "缺氧",
    "肥胖", "代谢", "减重", "体重", "糖尿病", "甲状腺", "内分泌",
    "新冠", "后遗症", "长新冠",
    "HIV", "艾滋病", "艾滋病病毒", "梅毒", "HPV",
    "特殊人群", "残障", "残疾", "无障碍",
    "药物治疗", "药物影响", "药物速查", "术语表", "辟谣", "索引", "参考文献",
]

for fn in ("book.tex", "female.tex", "male.tex"):
    print("\n========== %s ==========" % fn)
    L = PAGES[fn]
    for i, ln in enumerate(L, 1):
        s = ln.strip()
        if s.startswith("\\chapter{") or s.startswith("\\section{") or s.startswith("\\subsection{"):
            for k in KEYS:
                if k in s:
                    print("%6d %s" % (i, s[:110]))
                    break
