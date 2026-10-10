# -*- coding: utf-8 -*-
r"""r74 两卷体检：定位 female.tex / male.tex 的新目录骨架区，统计其中「仍无正文」的小节。

骨架区判定：从文件头到 `\part*{原始内容}` 之间的部分即新骨架（含篇/章/节/小节标题），
其后的 `\part*{原始内容}` 起为原始内容（逐字未动）。
"""
import io, re, sys

sys.stdout.reconfigure(encoding="utf-8")
H = re.compile(r"^\\(part|chapter|section|subsection)\*?\{(.*?)\}")

for f in ("female.tex", "male.tex"):
    raw = io.open(f, encoding="utf-8", newline="").read()
    lines = raw.split("\n")
    # 骨架区 = 到 \part*{原始内容} 为止
    anchor = None
    for i, l in enumerate(lines):
        s = l.rstrip("\r").strip()
        if s.startswith("\\part*{原始内容}"):
            anchor = i
            break
    if anchor is None:
        print("%s: 未找到 \\part*{原始内容}" % f)
        continue
    skel = lines[:anchor]
    print("=" * 70)
    print("%s：骨架区 L1 ~ L%d（共 %d 行），原始内容自 L%d 起" % (f, anchor, anchor, anchor + 1))

    # 列出骨架区标题 + 空小节
    cur = []
    empt = []
    marks = 0
    for i, l in enumerate(skel):
        m = H.match(l.rstrip("\r"))
        if not m:
            continue
        marks += 1
        k, t = m.group(1), m.group(2).strip()
        if k == "part":
            cur = [t]
        elif k == "chapter":
            cur = cur[:1] + [t]
        elif k == "section":
            cur = cur[:2] + [t]
        else:
            j = i + 1
            while j < anchor and (not skel[j].strip() or skel[j].strip().startswith("%")):
                j += 1
            empty = True
            if j < anchor:
                s2 = skel[j].rstrip("\r").strip()
                if not re.match(r"^\\(part|chapter|section|subsection)\*?\{", s2):
                    empty = False
            if empty:
                empt.append(" > ".join(cur + [t]))
    print("  骨架区标题行 %d 个；空小节 %d 个" % (marks, len(empt)))
    for x in empt:
        print("    -", x)
