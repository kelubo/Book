# -*- coding: utf-8 -*-
"""r74a: 扫描 book.tex 骨架区，找出「无正文」的章 / 节 / 小节。
判定：某标题之后、下一个同级或更高级标题之前，除注释行与空行外，没有实质内容行。
只读。
"""
import io, re, sys
sys.stdout.reconfigure(encoding="utf-8")

F = "book.tex"
raw = io.open(F, encoding="utf-8", newline="").read()
lines = raw.replace("\r\n", "\n").split("\n")

H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{(.*)\}\s*(%.*)?$")
LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}

# 收集所有标题
heads = []
for i, l in enumerate(lines):
    m = H.match(l)
    if m:
        heads.append((i, m.group(1), m.group(2)))
        # 记录首个标题行
OLD = None
for i, lv, t in heads:
    if lv == "part" and t == "old":
        OLD = i
        break
print("\\part{old} 在第", OLD + 1, "行")

# \iffalse ... \fi 区间（不编译，统计时排除）
off = set()
d = 0
st = None
for i, l in enumerate(lines):
    s = l.strip()
    if re.match(r"^\\iffalse\b", s):
        if d == 0:
            st = i
        d += 1
    elif s == "\\fi" and d > 0:
        d -= 1
        if d == 0:
            for k in range(st, i + 1):
                off.add(k)

sk = [(i, lv, t) for i, lv, t in heads if i < OLD and i not in off]
print("骨架区标题数:", len(sk))

def body_lines(idx):
    """返回 (起始行, 结束行) 之间的实质内容行数（去注释、去空行）"""
    ln, lv, t = sk[idx]
    end = len(lines)
    for j in range(idx + 1, len(sk)):
        if LV[sk[j][1]] <= LV[lv]:
            end = sk[j][0]
            break
    n = 0
    for k in range(ln + 1, end):
        s = lines[k].strip()
        if not s or s.startswith("%"):
            continue
        n += 1
    return n, ln + 1, end

zero = {"chapter": [], "section": [], "subsection": [], "subsubsection": [], "part": []}
for idx in range(len(sk)):
    n, s_ln, e_ln = body_lines(idx)
    if n == 0:
        zero[sk[idx][1]].append((sk[idx][0] + 1, sk[idx][2], s_ln, e_ln))

for lv in ("part", "chapter", "section", "subsection", "subsubsection"):
    print("\n=== 无正文的 %s：%d 个 ===" % (lv, len(zero[lv])))
    for ln, t, s_ln, e_ln in zero[lv]:
        print("  L%-6d %s" % (ln, t[:70]))

# 汇总：无正文的 chapter
print("\n=== 汇总 ===")
for lv in zero:
    print("  %s: %d" % (lv, len(zero[lv])))
