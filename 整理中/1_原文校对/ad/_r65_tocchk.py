# -*- coding: utf-8 -*-
"""r65：检查编译生成的 book.toc，确认新目录结构显示正确。"""
import io, re

t = io.open(r"D:\Git\Book\整理中\1_原文校对\ad\book.toc", encoding="utf-8", errors="replace").read()
lines = t.split("\n")


def strip(s):
    s = re.sub(r"\\[a-zA-Z]+ *", "", s)
    s = re.sub(r"[{}]", "", s)
    s = s.replace("\\", "")
    return re.sub(r"\s+", " ", s).strip()


print("=== 1. 目录里的 part 行 ===")
for l in lines:
    if "contentsline {part}" in l:
        print("   " + strip(l)[:80])

print("\n=== 2. 骨架区 chapter 条目（前 32 条）===")
n = 0
for l in lines:
    if "contentsline {chapter}" in l:
        n += 1
        if n <= 32:
            print("   %2d  %s" % (n, strip(l)[:70]))
print("   ... 全书共 %d 个 chapter 条目（含旧区与附录）" % n)

print("\n=== 3. 各篇 section 分布（骨架 9 篇）===")
cur = None
cnt = {}
for l in lines:
    m = re.search(r"contentsline \{part\}\{\\numberline \{([^}]*)\}(.*?)\}", l)
    if m:
        cur = strip(m.group(2))
        cnt.setdefault(cur, 0)
        continue
    if cur and "contentsline {section}" in l:
        cnt[cur] += 1
for k, v in list(cnt.items())[:14]:
    print("   %-30s section %d" % (k[:30], v))

print("\n=== 4. 抽查：第四篇 细菌性 STI 的二级结构 ===")
hit = False
for l in lines:
    if "细菌性" in l:
        hit = True
    if hit:
        print("   " + strip(l)[:70])
        if "病毒性" in l:
            break
