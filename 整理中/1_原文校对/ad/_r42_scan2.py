# -*- coding: utf-8 -*-
"""r42 补充扫描2：注释素材区 / 引用体系 / 索引标记 / 视觉元素 / 巨节结构"""
import io, os, re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FILES = ["book.tex", "female.tex", "male.tex"]

print("== 1. 参考文献基础设施 ==")
for f in os.listdir(BASE):
    if f.endswith(".bib") or "reference" in f.lower():
        print("  存在:", f, os.path.getsize(os.path.join(BASE, f)), "bytes")

for fn in FILES:
    raw = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read()
    print("  %s: \\cite=%d, \\nocite=%d, \\bibliography=%d, 显式书目 item=%d" % (
        fn, raw.count("\\cite{") + raw.count("\\cite["), raw.count("\\nocite"),
        raw.count("\\bibliography"), len(re.findall(r"\\item\s*\*\*.*？.*出版|ISBN", raw))))

print()
print("== 2. 索引标记 ==")
for fn in FILES:
    raw = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read()
    print("  %s: \\index{=%d, \\printindex=%d" % (fn, raw.count("\\index{"), raw.count("\\printindex")))

print()
print("== 3. 注释掉的正文素材（行首 % 后跟 LaTeX 结构或长中文段落） ==")
for fn in FILES:
    lines = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
    hits = []
    for i, ln in enumerate(lines, 1):
        s = ln.lstrip()
        if not s.startswith("%"):
            continue
        body = s.lstrip("%").strip()
        if len(body) > 40 and re.search(r"[\u4e00-\u9fff]", body):
            hits.append((i, body[:70]))
    print("  --- %s: %d 处被注释的长文本 ---" % (fn, len(hits)))
    for i, t in hits[:15]:
        print("     L%-6d %s" % (i, t))

print()
print("== 4. 视觉与增强元素 ==")
for fn in FILES:
    raw = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read()
    print("  %s: tcolorbox=%d, tabular=%d, includegraphics=%d, figure=%d, itemize=%d, enumerate=%d, 表格环境(longtable)=%d" % (
        fn, raw.count("\\begin{tcolorbox}"), raw.count("\\begin{tabular}"),
        raw.count("\\includegraphics"), raw.count("\\begin{figure}"),
        raw.count("\\begin{itemize}"), raw.count("\\begin{enumerate}"),
        raw.count("\\begin{longtable}")))

print()
print("== 5. 巨节（section 行数 > 1500 的） ==")
for fn in FILES:
    lines = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
    secs = []
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if s.startswith("%"):
            continue
        if s.startswith("\\section{") or s.startswith("\\chapter{"):
            secs.append((i, "ch" if s.startswith("\\chapter") else "sec", s.split("{", 1)[1].rsplit("}", 1)[0]))
    for idx, (i, lv, t) in enumerate(secs):
        # 下一个 section 或 chapter
        end = len(lines)
        for j in range(idx + 1, len(secs)):
            if secs[j][1] == "sec" or (lv == "ch" and secs[j][1] == "ch"):
                end = secs[j][0]
                break
        span = end - i
        if span > 1500:
            print("  %s L%-6d [%s] %-44s 跨度=%d 行" % (fn, i, lv, t[:42], span))

print()
print("== 6. 三卷章名对称性（book 有而 female/male 无） ==")


def chaps(fn):
    lines = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
    out = []
    for ln in lines:
        s = ln.strip()
        if s.startswith("%"):
            continue
        if s.startswith("\\chapter{"):
            out.append(s.split("{", 1)[1].rsplit("}", 1)[0])
    return out


bc, fc, mc = chaps("book.tex"), chaps("female.tex"), chaps("male.tex")
print("  book 章数", len(bc), "| female", len(fc), "| male", len(mc))
print("  female 独有章:", [c for c in fc if c not in bc])
print("  male 独有章:", [c for c in mc if c not in bc])
