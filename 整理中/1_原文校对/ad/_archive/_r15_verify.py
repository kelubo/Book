# -*- coding: utf-8 -*-
"""第十五轮插入后静态自检"""
import os, re
from collections import Counter

BASE = r"D:/Git/Book/整理中/1_原文校对/ad"
FILES = ["book.tex", "female.tex", "male.tex"]

NEW = {
    "book.tex": [
        r"\section{性交后反应：头痛、悲伤与不适的识别与处置}",
        r"\section{青少年性健康咨询常见疑问}",
        r"\subsection{性交后悲伤（Post-Coital Dysphoria, PCD）}",
        r"\subsection{尿路不适",  # 占位, 可能不存在
    ],
    "female.tex": [
        r"\subsection{阴毛修剪、脱毛与私处外观护理（安全与误区）}",
        r"\subsection{性交疼痛恐惧（Coitophobia）与初夜焦虑}",
    ],
    "male.tex": [
        r"\section{男性盆底肌训练（凯格尔运动·男性版）}",
        r"\subsection{性高潮后疾病综合征（POIS）与射精后头痛}",
    ],
}

for f in FILES:
    with open(os.path.join(BASE, f), encoding="utf-8", newline="") as fp:
        t = fp.read()
    lines = t.count("\n") + (0 if t.endswith("\n") else 1)
    # 朴素括号计数
    ob, cb = t.count("{"), t.count("}")
    # 转义括号修正
    esc_ob = len(re.findall(r"\\\{", t))
    esc_cb = len(re.findall(r"\\\}", t))
    ob_eff, cb_eff = ob - esc_ob, cb - esc_cb
    # 环境配对
    begins = Counter(re.findall(r"\\begin\{([^}]+)\}", t))
    ends = Counter(re.findall(r"\\end\{([^}]+)\}", t))
    env_bad = [(k, begins[k], ends.get(k, 0)) for k in set(list(begins)+list(ends)) if begins[k] != ends.get(k, 0)]
    print(f"--- {f} ---")
    print(f"  行数: {lines}")
    print(f"  原始 {{ }}: {ob} / {cb}  delta={ob-cb}")
    print(f"  转义后 {{ }}: {ob_eff} / {cb_eff}  delta={ob_eff-cb_eff}")
    if env_bad:
        print(f"  环境不平衡: {env_bad}")
    else:
        print(f"  环境全部配对 (共 {len(begins)} 类)")
    for nk in NEW.get(f, []):
        c = t.count(nk)
        if c:
            print(f"  新节存在 x{c}: {nk}")
