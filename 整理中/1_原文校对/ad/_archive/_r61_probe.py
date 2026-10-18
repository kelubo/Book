# -*- coding: utf-8 -*-
"""r61 探测：按层级（chapter/section/subsection/subsubsection）普查标题长度。
显示宽度：CJK/全角按 2 计，ASCII 按 1 计。
"""
import os, re, sys, unicodedata

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FILES = ["book.tex", "female.tex", "male.tex"]
LV = ["chapter", "section", "subsection", "subsubsection"]

HEAD_RE = re.compile(r"^\\(chapter|section|subsection|subsubsection)\*?\{")
# 标题内嵌套命令（\textbf{..} 等）先剥掉，便于计长
CMD_RE = re.compile(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?(\{[^{}]*\})?")
BRC_RE = re.compile(r"\{([^{}]*)\}")


def width(s):
    w = 0
    for ch in s:
        if unicodedata.east_asian_width(ch) in ("W", "F"):
            w += 2
        else:
            w += 1
    return w


def clean_title(raw):
    """去掉外层花括号，剥掉嵌套命令只留文字，返回 (标题全文, 纯文本)"""
    t = raw.strip()
    txt = t
    # 反复剥离命令
    for _ in range(6):
        new = CMD_RE.sub(lambda m: (m.group(2) or ""), txt)
        if new == txt:
            break
        txt = new
    txt = txt.replace("\\", "")
    return t, txt


def scan(path):
    with open(path, encoding="utf-8", newline="") as f:
        lines = f.read().replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out = []
    for i, ln in enumerate(lines, 1):
        if not HEAD_RE.match(ln):
            continue
        head = ln.strip()
        # 取第一个 {...} 内的标题（处理嵌套需配平）
        pos = head.index("{")
        depth = 0
        for j in range(pos, len(head)):
            if head[j] == "{":
                depth += 1
            elif head[j] == "}":
                depth -= 1
                if depth == 0:
                    raw = head[pos + 1:j]
                    break
        else:
            raw = head[pos + 1:]
        level = head[1:head.index("{")].rstrip("*")
        t, txt = clean_title(raw)
        out.append((i, level, raw, width(txt), txt))
    return out


def main():
    allrows = []
    for f in FILES:
        p = os.path.join(BASE, f)
        rows = scan(p)
        allrows.append((f, rows))
        print("=" * 70)
        print(f, "总标题数", len(rows))
        for lv in LV:
            sub = [r for r in rows if r[1] == lv]
            if not sub:
                print("  %-14s 0" % lv)
                continue
            ws = sorted(r[3] for r in sub)
            n = len(ws)
            def pct(q):
                return ws[min(n - 1, int(n * q))]
            print("  %-14s n=%-5d 中位=%-3d p90=%-3d p95=%-3d max=%d" % (
                lv, n, pct(0.5), pct(0.9), pct(0.95), ws[-1]))
    print("=" * 70)
    # 按层级 + 宽度倒序列出超阈值标题
    TH = {"chapter": 24, "section": 20, "subsection": 18, "subsubsection": 16}
    for f, rows in allrows:
        print("#### %s" % f)
        for lv in LV:
            cand = [r for r in rows if r[1] == lv and r[3] > TH[lv]]
            cand.sort(key=lambda x: -x[3])
            print("-- %s 超阈值(>%d)：%d 条" % (lv, TH[lv], len(cand)))
            for r in cand:
                print("   L%-6d w=%-3d %s" % (r[0], r[3], r[2]))


if __name__ == "__main__":
    main()
