# -*- coding: utf-8 -*-
"""r63 探针：book.tex 目录骨架（part/chapter/section 数量与行数）"""
import io, re, os, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
HEAD = re.compile(r"^\\(part|chapter|section)\*?\{")


def scan(path):
    lines = io.open(path, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
    out = []
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith("%"):
            continue
        m = HEAD.match(s)
        if m:
            lv = m.group(1)
            t = s[s.index("{") + 1:]
            t = t[:t.rindex("}")] if "}" in t else t
            out.append((i + 1, lv, t))
    return lines, out


def main():
    for tag, fn in (("当前 book.tex", "book.tex"), ("r62 备份", r"_backup_r62\book.tex")):
        path = os.path.join(BASE, fn)
        if not os.path.exists(path):
            print("缺:", path); continue
        lines, ents = scan(path)
        c = collections.Counter(lv for _, lv, _ in ents)
        print("==== %s：%d 行  part=%d chapter=%d section=%d" % (
            tag, len(lines), c["part"], c["chapter"], c["section"]))

    lines, ents = scan(os.path.join(BASE, "book.tex"))
    print("\n==== 当前骨架（part/chapter 层级，缩进表示归属）====")
    cur_part = ""
    cur_ch = -1
    part_start = 0
    for idx, (ln, lv, t) in enumerate(ents):
        if lv == "part":
            if cur_part:
                print("        └ 共 %d 行" % (ln - part_start))
            cur_part = t
            part_start = ln
            print("L%-6d [PART] %s" % (ln, t))
            cur_ch = -1
        elif lv == "chapter":
            if cur_ch > 0:
                print("        └ 共 %d 行" % (ln - cur_ch))
            cur_ch = ln
            print("  L%-6d ch  %s" % (ln, t))
        elif lv == "section":
            if cur_ch < 0:
                print("      !! 裸节（无章）L%d %s" % (ln, t))
    if cur_ch > 0:
        print("        └ 共 %d 行" % (len(lines) - cur_ch))


if __name__ == "__main__":
    main()
