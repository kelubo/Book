# -*- coding: utf-8 -*-
"""r67：解析 book.toc，核对目录显示效果。"""
import io, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
t = io.open(BASE + r"\book.toc", encoding="utf-8", errors="replace").read()
lines = t.split("\n")


def strip(s):
    s = re.sub(r"\\[a-zA-Z]+ *", "", s)
    s = re.sub(r"[{}]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


parts, chs = [], []
for l in lines:
    if "contentsline {part}" in l:
        parts.append(strip(l))
    elif "contentsline {chapter}" in l:
        chs.append(strip(l))

print("=== 目录中的 part 条目（%d 个）===" % len(parts))
for p in parts:
    print("   ", p[:70])

print("\n=== 目录中的 chapter 条目：共 %d 个 ===" % len(chs))
print("  前 8 个：")
for c in chs[:8]:
    print("     ", c[:60])
print("  末 8 个：")
for c in chs[-8:]:
    print("     ", c[:60])

print("\n=== 关键检查 ===")
full = t
for kw in ["性别认同（原列第一篇", "伴侣共同性问题（原列第六篇", "两性关系的未来（原列第九篇"]:
    print("  %-30s 是否出现在目录：%s" % (kw[:28], "是 ⚠" if kw in full else "否 ✓"))
print("  出现 '附录' part 条目：%s" % ("是 ✓" if any("附录" == p.replace(" ", "") for p in parts) else "否 ⚠"))

# 第一篇的层级展开
print("\n=== 目录中第一篇的前 26 条（part + chapter + section 混排）===")
n = 0
started = False
for l in lines:
    if "contentsline {part}" in l and "基础与生理" in l:
        started = True
    if not started:
        continue
    if "contentsline {part}" in l and "性心理与情感" in l:
        break
    if any(k in l for k in ["contentsline {part}", "contentsline {chapter}", "contentsline {section}"]):
        n += 1
        if n <= 26:
            ind = "  " if "chapter" in l else ("    " if "section" in l else "")
            print("%s%s" % (ind, strip(l)[:64]))
print("  第一篇条目合计：%d" % n)
