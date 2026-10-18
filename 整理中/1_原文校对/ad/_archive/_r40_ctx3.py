# -*- coding: utf-8 -*-
"""r40 探测第 5 轮：最后的甄别——专节归属检查"""
import re, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FILES = ["book.tex", "female.tex", "male.tex"]

texts = {}
for fn in FILES:
    raw = open(os.path.join(BASE, fn), "rb").read()
    crlf = "\r\n" if b"\r\n" in raw else "\n"
    texts[fn] = raw.decode("utf-8").split(crlf)

HDR = re.compile(r"\\(chapter|section|subsection|subsubsection|subparagraph)\{([^{}]*)\}")

def near_title(fn, lineno):
    """向上找最近的标题行"""
    for i in range(lineno, 0, -1):
        st = texts[fn][i - 1].strip()
        m = HDR.match(st)
        if m:
            return "L%d %s[%s]" % (i, m.group(1), m.group(2)[:40])
    return "?"

KWS = ["白癜风", "强迫性性行为", "单身", "进食障碍", "丧偶", "骚扰", "独身"]
print("==== 专节归属检查 ====")
for kw in KWS:
    print("--- 「%s」 ---" % kw)
    shown = 0
    for fn in FILES:
        for i, ln in enumerate(texts[fn], 1):
            st = ln.strip()
            if st.startswith("%"):
                continue
            # 只看标题行含关键词的（=有专节）或正文命中但打印所属标题
            if kw in st:
                if HDR.match(st) and kw in st:
                    print("  [专节] %s L%d: %s" % (fn, i, st[:80]))
                    shown += 1
                elif shown < 6:
                    print("  %s L%d (%s): %s" % (fn, i, near_title(fn, i), st[:60]))
                    shown += 1
    if shown == 0:
        print("  (无)")

# L20018 性伤害分级的所属节
print("\n--- book L20018 所属节 ---")
print(" ", near_title("book.tex", 20018))
for i in range(19990, 20025):
    print("  %5d| %s" % (i, texts["book.tex"][i - 1].strip()[:95]))
