# -*- coding: utf-8 -*-
r"""r74z 修复：把误置于「LGBTQ+ 性健康 章 > 性传播感染风险」下的滴虫病内容块，
搬回第四篇「寄生虫性 STI」章内属于它的位置（该章末尾新增小节）。

同时输出被搬移块的原文到 _r74z_block.txt 存档。
"""
import io

PATH = "book.tex"
raw = io.open(PATH, encoding="utf-8", newline="").read()
assert "\r" not in raw, "book.tex 应为纯 LF"
lines = raw.split("\n")

# 1) 定位错位块：从 LGBTQ+ 章的 \subsection{性传播感染风险}(L18251) 之后的正文块
start_anchor = None
for i, l in enumerate(lines):
    if l.strip() == "\\subsection{性传播感染风险}" and i + 1 < len(lines) \
            and "滴虫感染与性传播感染风险的关联" in lines[i + 2]:
        start_anchor = i
        break
assert start_anchor is not None, "未找到错位槽位"
print("错位锚行（0-based）=", start_anchor, "->", lines[start_anchor])

# 块起点：跳过空行
b = start_anchor + 1
while b < len(lines) and not lines[b].strip():
    b += 1
# 块终点：下一个非空且以 \ 开头（骨架标题）的行之前
e = b
while e < len(lines):
    s = lines[e].strip()
    if s.startswith("\\subsection") or s.startswith("\\section") or s.startswith("\\chapter") or s.startswith("\\part"):
        break
    e += 1
# 回退尾部空行
while e > b and not lines[e - 1].strip():
    e -= 1
block = lines[b:e]
print("块范围 L%d ~ L%d（%d 行）" % (b + 1, e, len(block)))
print("首行:", block[0][:60])
print("末行:", block[-1][:60])
assert any("滴虫" in x for x in block), "块内容不含滴虫，定位可疑"
assert any("tcolorbox" in x for x in block), "块缺少 tcolorbox 收尾"

io.open("_r74z_block.txt", "w", encoding="utf-8", newline="").write("\n".join(block) + "\n")
print("已存档 -> _r74z_block.txt")

# 2) 删除该块（连同其后多余空行，保持原槽位干净）
new = lines[:b] + lines[e:]
# 去掉紧随的空行冗余：若 b-1 是 \subsection 行且 new[b-1] 处已有空行残留，规范化
changed = raw != "\n".join(new)
print("删除后行数:", len(lines), "->", len(new))
assert changed
io.open("_r74z_stage1.tex", "w", encoding="utf-8", newline="").write("\n".join(new))
print("阶段1 已写 -> _r74z_stage1.tex")
