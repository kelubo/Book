# -*- coding: utf-8 -*-
"""r80 移出标记对账：book/female 的每个移出声明，核对目标卷是否有对应内容"""
import io, re

AD = "D:/Git/Book/整理中/1_原文校对/ad/"

def read(fn):
    raw = io.open(AD + fn, encoding="utf-8", newline="").read()
    return [x.rstrip("\r") for x in raw.split("\n")]

book = read("0_book.tex")
male = read("1_male.tex")
fem = read("2_female.tex")
pos = read("3_position.tex")

def norm(s):
    return re.sub(r"\s+", "", s)

def has_content(lines, title, min_body=1):
    """标题在目标卷出现且其后有正文（排除纯骨架注释/空壳）"""
    t = norm(title)
    found = []
    for i, x in enumerate(lines):
        if re.match(r"^\\(chapter|section|subsection)\*?\{", x) and t in norm(x):
            # 向后看 30 行内是否有正文
            body = 0
            for y in lines[i + 1:i + 40]:
                s = y.strip()
                if not s or s.startswith("%"):
                    continue
                if re.match(r"^\\(part|chapter|section|subsection)\*?\{", s):
                    break
                body += 1
            found.append((i + 1, body))
    return found

# 收集 book 的移出标记
markers = []
for i, x in enumerate(book):
    s = x.strip()
    m = re.search(r"[⇒→]\s*\[?已移出\]?\s*(.*?)(?:（r\d+）)?$", s)
    if m and (s.startswith("%") or "⇒" in s):
        markers.append((i + 1, s))

print("book 移出标记共 %d 条" % len(markers))
miss = 0
for ln, s in markers:
    # 提取目标：→ volume.tex《章》 或 volume.tex（...）
    m = re.search(r"(0_book|1_male|2_female|3_position|male|female|position)\.tex[《（]([^》）》]+)", s)
    if not m:
        print("  L%d [无目标卷] %s" % (ln, s[:90]))
        continue
    vol, title = m.group(1), m.group(2)
    tgt = {"male": male, "1_male": male, "female": fem, "2_female": fem,
           "position": pos, "3_position": pos}[vol]
    hits = has_content(tgt, title)
    ok = any(b > 0 for _, b in hits)
    if not ok:
        miss += 1
        print("  L%d [目标无正文!] %s" % (ln, s[:100]))
print("目标无正文的标记: %d 条" % miss)
