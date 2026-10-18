# -*- coding: utf-8 -*-
"""修正 r67 报告/导览脚本/记忆中"section 65"的不准确口径 -> 74。"""
import io, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FIX = [
    (os.path.join(BASE, "_r67_目录重构报告_2026-09-21.md"), [
        ("`\\section` 从 65 个增至 248 个", "`\\section` 从 74 个增至 248 个（+174）"),
        ("**八篇 51 章 248 节**", "**八篇 51 章 248 节**"),
        ("section 65 -> 249", "section 74 -> 248"),
    ]),
    (os.path.join(BASE, "_r67_toc.py"), [
        ("（section 65 -> 249）", "（section 74 -> 248）"),
    ]),
    (os.path.join(BASE, "_r67_list.py"), []),
]
for p, pairs in FIX:
    if not os.path.exists(p):
        continue
    s = io.open(p, encoding="utf-8").read()
    for a, b in pairs:
        n = s.count(a)
        if n:
            s = s.replace(a, b)
        print("%-42s %-34s -> %d 处" % (os.path.basename(p), a[:32], n))
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# 记忆与技能
MEM = [
    (r"D:\Git\Book\.workbuddy\memory\2026-09-21.md", [
        ("**为 35 章补二级结构**：`\\section` 65 → 248", "**为 35 章补二级结构**：`\\section` 74 → 248（+174）"),
    ]),
    (r"D:\Git\Book\.workbuddy\memory\MEMORY.md", [
        ("**248 个 `\\section`**（r66 时 196）", "**248 个 `\\section`**（r66 时 74）"),
    ]),
    (r"C:\Users\Administrator\.workbuddy\skills\ad-book-expansion\SKILL.md", [
        ("`\\section` 65 → 248", "`\\section` 74 → 248（+174）"),
    ]),
]
for p, pairs in MEM:
    s = io.open(p, encoding="utf-8").read()
    for a, b in pairs:
        n = s.count(a)
        print("%-42s %-34s -> %d 处" % (os.path.basename(p), a[:32], n))
        s = s.replace(a, b)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("done")
