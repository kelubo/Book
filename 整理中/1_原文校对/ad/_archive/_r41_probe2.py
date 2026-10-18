# -*- coding: utf-8 -*-
"""r41 补充探测：数字时代章实际标题、损伤/急救相关节、尾部附录区结构"""
import io, re, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FN = "book.tex"
p = os.path.join(BASE, FN)
with io.open(p, "r", encoding="utf-8", newline="") as f:
    raw = f.read()
lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")

KW = ["数字", "网络", "在线", "远程", "虚拟", " App", "app", "应用",
      "损伤", "急救", "急诊", "意外", "事故", "安全"]
sec_re = re.compile(r"^\\(chapter|section|subsection|subsubsection)\{")

print("== A. 含关键词的章节行（行首真实结构行） ==")
for i, ln in enumerate(lines, 1):
    s = ln.strip()
    m = sec_re.match(s)
    if not m:
        continue
    title = s.split("{", 1)[1].rsplit("}", 1)[0] if "}" in s else s
    for kw in KW:
        if kw in s:
            print(f"L{i} [{m.group(1)}] {s}")
            break

print()
print("== B. 尾部附录区结构（L53750 之后所有 chapter/section 行） ==")
for i, ln in enumerate(lines, 1):
    if i < 53750:
        continue
    s = ln.strip()
    m = sec_re.match(s)
    if m:
        print(f"L{i} [{m.group(1)}] {s[:70]}")

print()
print("== C. 术语表区内容密度抽查（L53803-53946 非空行数与样例） ==")
seg = lines[53802:53946]
ne = [x for x in seg if x.strip()]
print(f"非空行数: {len(ne)} / {len(seg)}")
for x in ne[:12]:
    print("  |", x.strip()[:80])

print()
print("== D. 就医导航区内容密度抽查（L54356-54494） ==")
seg2 = lines[54355:54494]
ne2 = [x for x in seg2 if x.strip()]
print(f"非空行数: {len(ne2)} / {len(seg2)}")
for x in ne2[:14]:
    print("  |", x.strip()[:80])

print()
print("== E. 索引区内容密度抽查（L53947-54235） ==")
seg3 = lines[53946:54235]
ne3 = [x for x in seg3 if x.strip()]
print(f"非空行数: {len(ne3)} / {len(seg3)}")
for x in ne3[:10]:
    print("  |", x.strip()[:80])
