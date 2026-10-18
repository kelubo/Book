# -*- coding: utf-8 -*-
"""由 _r65_toc.py 派生 _r69_toc.py（更新轮次说明），然后运行。"""
import io, subprocess, sys

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
src = io.open(BASE + r"\_r65_toc.py", encoding="utf-8").read()

pairs = [
    ('"""第六十五轮：重生成三卷目录总览（book 前置目录骨架重构为九篇 53 章后同步）"""',
     '"""第六十九轮：重生成三卷目录总览（book 前置骨架补齐第三层：八篇 58 章 288 节 1027 小节）"""'),
    ('out.append("> 生成日期：2026-09-20（第六十五轮目录骨架重构后重新生成） ｜ 路径：整理中/1_原文校对/ad/ ｜ 用途：审校/合并/阅读导航底图")',
     'out.append("> 生成日期：2026-09-21（第六十九轮骨架补第三层后重新生成） ｜ 路径：整理中/1_原文校对/ad/ ｜ 用途：审校/合并/阅读导航底图")'),
    ('out.append("> 第六十五轮（2026-09-20）：综合卷前置目录骨架重构',
     'out.append("> 第六十九轮（2026-09-21）：综合卷前置骨架补第三层——为 213 个零小节节补 784 条学习要点（section 74 -> 288、subsection 96 -> 1027），'
     '新增 7 章补知识框架缺口（性发育与青春期 / 家庭形态的多样性 / 精神健康与性 / 性治疗与性康复 / 性健康前沿研究 / 暴力、安全与保护 / 性与公共卫生），'
     '「结语」独立成篇，消 4 处重名节，删除重复说明块；正文与旧区未动。")\n'
     'out.append("> 第六十五轮（2026-09-20）：综合卷前置目录骨架重构'),
]
for a, b in pairs:
    n = src.count(a)
    assert n == 1, (a[:50], n)
    src = src.replace(a, b)

io.open(BASE + r"\_r69_toc.py", "w", encoding="utf-8", newline="\n").write(src)
print("written _r69_toc.py", len(src))

r = subprocess.run([sys.executable, os.path.join(BASE, "_r69_toc.py")],
                   capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=BASE)
print(r.stdout[-1500:])
print("ERR:", r.stderr[-600:])
