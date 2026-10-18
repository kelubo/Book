"""r64b：校验骨架注释里的行号引用在当前文件中是否仍指向正确内容。

背景：骨架（L138-752）的 `% 移入：L1587"性科学的沧桑"整章` 这类注释，行号是
生成骨架时记录的。用户 2026-09-20 重写过 book.tex，需确认这些行号是否失效。
"""
import io, re, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
P = os.path.join(BASE, "book.tex")

src = io.open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n")
lines = src.split("\n")
print("总行数", len(lines))

# 骨架范围：L152 起到 \backmatter 前
start, end = 151, 744
skel = lines[start:end]

# 匹配注释里的引用：L数字 后面可跟 "标题" 或 直接标题
REF = re.compile(r"L(\d+)\s*(?:\u201c([^\u201d]+)\u201d|\"([^\"]+)\")?")

refs = []
for i, l in enumerate(skel):
    s = l.strip()
    if not s.startswith("%"):
        continue
    if "移入" not in s and "去重" not in s and "重复" not in s:
        continue
    for m in REF.finditer(s):
        num = int(m.group(1))
        title = m.group(2) or m.group(3)
        refs.append((i + start + 1, num, title))

print("骨架注释中的行号引用条数：", len(refs))

ok = bad = notitle = beyond = 0
badlist = []
for cmtline, num, title in refs:
    if num > len(lines):
        beyond += 1
        badlist.append((cmtline, num, title, "<超出文件末尾>"))
        continue
    if not title:
        notitle += 1
        continue
    # 提取标题主名（去掉括号内容、去空格）
    key = re.sub(r"[\s（(].*$", "", title).strip()
    key = key[:8]
    target = lines[num - 1]
    # 在目标行及其 ±2 行内找标题
    window = "\n".join(lines[max(0, num - 3):num + 2])
    if key and key in window:
        ok += 1
    else:
        bad += 1
        badlist.append((cmtline, num, title, target.strip()[:70]))

print("  命中 %d / 越界 %d / 无法比对(无标题) %d" % (ok, beyond, notitle))
print("  **失配 %d 条**" % bad)
print()
print("=" * 90)
print("失配明细（骨架注释行 -> 引用行号 -> 该行当前实际内容）")
print("=" * 90)
for cl, num, title, actual in badlist[:60]:
    print("骨架L%-4d 引L%-6d 期望「%s」" % (cl, num, title))
    print("             实际 %s" % actual)
if len(badlist) > 60:
    print("... 其余 %d 条省略" % (len(badlist) - 60))

# 反向：当前旧区里各章的标题与行号，供重新建立映射用
print()
print("=" * 90)
print("当前旧区（L744 起）的 chapter/section 骨架（前 120 条）")
print("=" * 90)
H = re.compile(r"^\s*\\(part|chapter|section)\*?\{")
n = 0
for i in range(743, len(lines)):
    s = lines[i].strip()
    if H.match(s):
        n += 1
        if n <= 120:
            print("L%-7d %s" % (i + 1, s[:80]))
print("旧区 part/chapter/section 总数：", n)
