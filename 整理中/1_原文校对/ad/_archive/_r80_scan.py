# -*- coding: utf-8 -*-
"""r80 分区扫描：各卷各区的篇章体量与迁移进度"""
import io, re

AD = "D:/Git/Book/整理中/1_原文校对/ad/"

def read(fn):
    raw = io.open(AD + fn, encoding="utf-8", newline="").read()
    return [x.rstrip("\r") for x in raw.split("\n")]

def body_n(lines, a, b):
    n = 0
    for x in lines[a:b]:
        s = x.strip()
        if not s or s.startswith("%"):
            continue
        if re.match(r"^\\(part|chapter|section|subsection|subsubsection|item)\b", s):
            continue
        if s in (r"\begin{itemize}", r"\end{itemize}", r"\begin{enumerate}", r"\end{enumerate}"):
            continue
        n += 1
    return n

def scan(lines, a, b, label, skip_iffalse=True):
    """扫描 [a,b) 区间的 part/chapter 结构"""
    # 处理 \iffalse...\fi 区间
    zones = []
    if skip_iffalse:
        depth = 0
        start = a
        for i in range(a, b):
            if re.match(r"^\\iffalse\b", lines[i]):
                if depth == 0:
                    zones.append((start, i))
                depth += 1
            elif re.match(r"^\\fi\b", lines[i]):
                depth -= 1
                if depth == 0:
                    start = i + 1
        zones.append((start, b))
    else:
        zones = [(a, b)]

    parts, chaps = [], []
    for za, zb in zones:
        for i in range(za, zb):
            if lines[i].lstrip().startswith("%"):
                continue
            m = re.match(r"^\\part\*?\{([^}]*)\}", lines[i])
            if m:
                parts.append((i, m.group(1)))
            m = re.match(r"^\\chapter\*?\{([^}]*)\}", lines[i])
            if m:
                chaps.append((i, m.group(1)))

    print("  [%s] part=%d chapter=%d" % (label, len(parts), len(chaps)))
    for i, t in parts:
        print("    L%-6d PART %s" % (i + 1, t))
    # 章体量
    for k, (i, t) in enumerate(chaps):
        nb = chaps[k + 1][0] if k + 1 < len(chaps) else b
        n = body_n(lines, i + 1, min(nb, b))
        flag = "空" if n < 3 else ""
        print("    L%-6d CHAP %-30s 正文%s行 %s" % (i + 1, t, n, flag))
    return parts, chaps

# ===== 0_book =====
print("### 0_book.tex")
lines = read("0_book.tex")
old_i = next(i for i, x in enumerate(lines) if re.match(r"^\\part\{old\}", x))
print("  \\part{old} @ L%d" % (old_i + 1))
scan(lines, 0, old_i, "骨架区")
scan(lines, old_i, len(lines), "旧区")

# ===== 1_male =====
print("### 1_male.tex")
lines = read("1_male.tex")
dc = next(i for i, x in enumerate(lines) if x.startswith("\\documentclass"))
pi = next(i for i, x in enumerate(lines) if re.match(r"^\\part\*?\{原始内容\}", x))
print("  \\documentclass @ L%d, \\part*{原始内容} @ L%d" % (dc + 1, pi + 1))
scan(lines, 0, dc, "停用框架区")
scan(lines, dc, pi, "编译区骨架")
scan(lines, pi, len(lines), "原始内容区")

# ===== 2_female =====
print("### 2_female.tex")
lines = read("2_female.tex")
dc = next(i for i, x in enumerate(lines) if x.startswith("\\documentclass"))
pi = next(i for i, x in enumerate(lines) if re.match(r"^\\part\*?\{原始内容\}", x))
print("  \\documentclass @ L%d, \\part*{原始内容} @ L%d" % (dc + 1, pi + 1))
scan(lines, 0, dc, "停用框架区")
scan(lines, dc, pi, "编译区骨架")
scan(lines, pi, len(lines), "原始内容区")

# ===== 3_position =====
print("### 3_position.tex")
lines = read("3_position.tex")
scan(lines, 0, len(lines), "全文")
