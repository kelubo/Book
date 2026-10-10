# -*- coding: utf-8 -*-
"""r42 薄点抽查：确认结构缺口区的真实内容"""
import io, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"

def show(fn, a, b, label):
    raw = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read()
    lines = raw.replace("\r\n", "\n").split("\n")
    print("=" * 70)
    print("[%s] %s L%d-%d" % (fn, label, a, b))
    ne = 0
    for i in range(a, min(b, len(lines)) + 1):
        s = lines[i - 1].strip()
        if s:
            ne += 1
            print("  L%-6d %s" % (i, s[:100]))
    print("  非空行: %d" % ne)

show("book.tex", 54692, 54697, "参考文献章")
show("book.tex", 54406, 54432, "辟谣误区章")
show("book.tex", 50074, 50097, "SM初学者指导章")
show("book.tex", 53951, 53993, "性健康与整体健康章")
show("book.tex", 54346, 54405, "药物与性功能速查章")
show("male.tex", 7715, 7730, "male 参考资料")
show("female.tex", 4640, 4700, "female 更年期章尾部")

print()
print("== 浅小节按卷/章分组统计 ==")
marks_all = {}
for fn in ["book.tex", "female.tex", "male.tex"]:
    raw = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read()
    lines = raw.replace("\r\n", "\n").split("\n")
    marks = []
    curch = "(卷首)"
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if s.startswith("%"):
            continue
        if s.startswith("\\chapter{"):
            curch = s.split("{", 1)[1].rsplit("}", 1)[0]
        m = None
        for lv in ("section", "subsection"):
            if s.startswith("\\" + lv + "{"):
                m = lv
                break
        if m:
            marks.append((i, m, s.split("{", 1)[1].rsplit("}", 1)[0], curch))
    from collections import Counter
    cnt = Counter()
    tot = 0
    for idx, (ln_no, lv, t, ch) in enumerate(marks):
        end = None
        for j in range(idx + 1, len(marks)):
            if marks[j][1] == "section":
                end = marks[j][0]
                break
        if end is None:
            end = len(lines)
        body_n = sum(1 for x in lines[ln_no:end - 1] if x.strip() and not x.strip().startswith("%"))
        if body_n < 5:
            cnt[ch] += 1
            tot += 1
    print("--- %s: 浅小节 %d 处，按章分布 ---" % (fn, tot))
    for ch, c in cnt.most_common(20):
        print("   %-40s %d" % (ch[:38], c))
