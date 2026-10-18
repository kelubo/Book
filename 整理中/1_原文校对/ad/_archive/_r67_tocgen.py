# -*- coding: utf-8 -*-
"""由 _r65_toc.py 派生 _r67_toc.py（更新轮次说明），然后运行。"""
import io

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
src = io.open(BASE + r"\_r65_toc.py", encoding="utf-8").read()

pairs = [
    ('"""第六十五轮：重生成三卷目录总览（book 前置目录骨架重构为九篇 53 章后同步）"""',
     '"""第六十七轮：重生成三卷目录总览（book 前置骨架补二级结构、附录独立、待处理章移出后同步）"""'),
    ('out.append("> 生成日期：2026-09-20（第六十五轮目录骨架重构后重新生成） ｜ 路径：整理中/1_原文校对/ad/ ｜ 用途：审校/合并/阅读导航底图")',
     'out.append("> 生成日期：2026-09-21（第六十七轮骨架补二级结构后重新生成） ｜ 路径：整理中/1_原文校对/ad/ ｜ 用途：审校/合并/阅读导航底图")'),
    ('out.append("> 第六十五轮（2026-09-20）：综合卷前置目录骨架重构',
     'out.append("> 第六十七轮（2026-09-21）：综合卷前置骨架——九篇 51 章，为 35 章补二级结构（section 65 -> 249），附录独立成篇（\\\\part*{附录}），3 章迁移过渡记录移出目录（\\\\iffalse 保留源码），\\\\tableofcontents 移入 \\\\frontmatter，正文与旧区未动。")\n'
     'out.append("> 第六十五轮（2026-09-20）：综合卷前置目录骨架重构'),
]
for a, b in pairs:
    n = src.count(a)
    assert n == 1, (a[:50], n)
    src = src.replace(a, b)

io.open(BASE + r"\_r67_toc.py", "w", encoding="utf-8", newline="\n").write(src)
print("written _r67_toc.py", len(src))
