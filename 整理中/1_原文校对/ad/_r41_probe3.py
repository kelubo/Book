# -*- coding: utf-8 -*-
"""r41 探测3：急救节锚细查 + 术语表现有词条清单 + 各插入锚上下文"""
import io, re, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
with io.open(os.path.join(BASE, "book.tex"), "r", encoding="utf-8", newline="") as f:
    raw = f.read()
lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
N = len(lines)
print(f"book.tex 总行数: {N}")

sec_re = re.compile(r"^\\(chapter|section|subsection|subsubsection)\{")

print("\n== A. L932 尴尬与意外节内部结构（至下一个 section/chapter） ==")
end = None
for i in range(933, N):
    s = lines[i-1].strip()
    m = sec_re.match(s)
    if m and m.group(1) in ("section", "chapter"):
        end = i
        break
print(f"下一 section/chapter 在 L{end}")
for i in range(925, min(end or 1100, 1120)):
    s = lines[i-1].strip()
    m = sec_re.match(s)
    if m:
        print(f"  L{i} [{m.group(1)}] {s[:64]}")

print("\n== B. 术语表现有 \\item 词条标题（L53803-53947） ==")
items = []
for i in range(53803, 53948):
    s = lines[i-1].strip()
    if s.startswith("\\item["):
        t = s[6:].split("]", 1)[0]
        items.append((i, t))
print(f"共 {len(items)} 条:")
print("，".join(t for _, t in items))

print("\n== C. 五个插入锚上下文（锚行前1行~后2行） ==")
for label, anchor_ln in [("丁克->新婚首夜前", 3864), ("急救(见A结果后定)", 932),
                          ("烧伤截肢->残疾人前", 27529), ("异地恋->多元关系前", 25211),
                          ("数字遗产->数字性教育前", 26319)]:
    print(f"--- {label} (L{anchor_ln}) ---")
    for i in range(anchor_ln-1, anchor_ln+2):
        print(f"  L{i}: {lines[i-1].strip()[:70]}")

print("\n== D. L932 前一个 section 是什么（确认急救节位置语境） ==")
prev = None
for i in range(931, 0, -1):
    s = lines[i-1].strip()
    m = sec_re.match(s)
    if m and m.group(1) in ("section", "chapter"):
        prev = (i, s[:64])
        break
print("L932 之前最近的 section/chapter:", prev)
