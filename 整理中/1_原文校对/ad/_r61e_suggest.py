# -*- coding: utf-8 -*-
"""r61e 生成机械化建议新名，供人工审阅。
规则：
  A 冒号式	  -> 取冒号前；若冒号前过短(<8 显示宽)则标记 NEED
  B 中文括号  -> 剥离含汉字的括号（保留纯英文括号）
  C 其余长定语 -> 标记 NEED（人工压缩）
"""
import os, re
import importlib.util

spec = importlib.util.spec_from_file_location(
    "p", r"D:\Git\Book\整理中\1_原文校对\ad\_r61b_probe.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FILES = ["book.tex", "female.tex", "male.tex"]
LV = ["chapter", "section", "subsection", "subsubsection"]
# 含汉字的括号
CJK_PAREN = re.compile(r"[（(]([^（）()]*[\u4e00-\u9fff][^（）()]*)[）)]")


def suggest(txt):
    t = txt
    kinds = []
    if "：" in t:
        kinds.append("冒号")
    if CJK_PAREN.search(t):
        kinds.append("中括号")
    note = ""
    # 冒号式：取前半
    if "：" in t:
        head = t.split("：")[0]
        head_clean = CJK_PAREN.sub("", head).strip()
        if m.width(head_clean) >= 8:
            cand = head_clean
            if CJK_PAREN.search(t) and not CJK_PAREN.search(cand):
                note = "另含可剥括号"
            return cand, "A-取冒号前", note
        else:
            note = "冒号前过短"
    # 剥中文括号
    body = CJK_PAREN.sub("", t)
    body = re.sub(r"[ \t]+", " ", body).strip()
    if body != t and body:
        return body, "B-剥括号", note
    return "", "C-NEED", note


for f in FILES:
    rows = m.scan(os.path.join(BASE, f))
    cand = [r for r in rows if r["bw"] >= 30]
    cand.sort(key=lambda x: (LV.index(x["lv"]), -x["bw"]))
    print("=" * 78)
    print(f, len(cand))
    for r in cand:
        s, how, note = suggest(r["txt"])
        nw = m.width(s) if s else -1
        print("%-6s L%-6d %-3d -> %-3d [%s] %s%s" % (
            r["lv"][:6], r["ln"], r["bw"], nw, how, note,
            "\n        OLD: " + r["raw"] + "\n        NEW: " + (s or "(待定)")))
