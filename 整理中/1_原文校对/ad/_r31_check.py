# -*- coding: utf-8 -*-
"""第三十一轮：双反斜杠笔误精确扫描 + 新增标题定位"""
import io, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
book = io.open(BASE + r"\book.tex", encoding="utf-8", newline="").read()
lines = book.split("\r\n")

# 真笔误：源码中出现 \\textbf 这类双反斜杠+命令名
bad = re.findall(r"\\\\(?:textbf|textit|item|begin|end|noindent|section|subsection|subsubsection|par|title)\b", book)
print("double-backslash typos:", len(bad), bad[:5])

print()
print("== 本轮 10 个新标题的当前行号 ==")
titles = [
    "多人性行为（3P / 群交 / 换偶）的安全与协商",
    "色情与勃起功能障碍：\"色情诱导 ED\"之争与使用自查",
    "同志桑拿与性场所：文化、安全与法律",
    "中医方剂补遗：五子衍宗丸、左归丸与蛇床子",
    "壮阳中药与西药的相互作用：同服之前必读",
    "传统功法的安全审视：铁裆功、气功导引与提肛",
    "\"以形补形\"与壮阳食疗：传统说法的现代审视",
    "电击类玩具（e-stim）的安全使用",
    "乳头夹与夹具：佩戴安全细节",
    "BDSM 后的情绪跌落（Sub Drop / Top Drop）：机制、识别与照护",
]
for t in titles:
    hit = [i for i, l in enumerate(lines, 1) if t in l]
    print(hit[0] if hit else "MISS", "|", t)
