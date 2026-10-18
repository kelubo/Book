# -*- coding: utf-8 -*-
"""r78b: 移出后重复性检查 —— position.tex 的章/节名不应再出现在三卷正文标题里（除注释标记行）。"""
import re, os
DIR = os.path.dirname(os.path.abspath(__file__))

def norm(s):
    s = re.sub(r"\s+", "", s)
    s = s.replace('"', '"').replace('"', '"')
    s = re.sub(r"（[A-Za-z][^）]*）", "", s)   # 剥纯英文对照括号
    return s

def heads(fn, lv):
    raw = open(os.path.join(DIR, fn), encoding="utf-8").read()
    out = []
    for ln in raw.split("\n"):
        s = ln.rstrip("\r")
        m = re.match(r"^\\" + lv + r"\*?\{([^}]*)\}", s)
        if m:
            out.append((lv, m.group(1).strip()))
    return out

pos_ch = heads("position.tex", "chapter")
pos_se = heads("position.tex", "section")
print("position.tex: %d 章 / %d 节" % (len(pos_ch), len(pos_se)))

posset = {norm(t) for _, t in pos_ch[1:]}  # 去掉「前言」「参考文献」
posset |= {norm(t) for _, t in pos_se}

for fn in ["book.tex", "female.tex", "male.tex"]:
    raw = open(os.path.join(DIR, fn), encoding="utf-8").read()
    # 只取「非注释」的标题行
    hit = []
    for ln in raw.split("\n"):
        s = ln.rstrip("\r")
        if s.lstrip().startswith("%"):
            continue
        m = re.match(r"^\\(chapter|section)\*?\{([^}]*)\}", s)
        if m and norm(m.group(2).strip()) in posset:
            hit.append((m.group(1), m.group(2).strip()))
    print("=== %s 仍含 position.tex 同名标题: %d 处 ===" % (fn, len(hit)))
    for lv, t in hit:
        print("   [%s] %s" % (lv, t))
