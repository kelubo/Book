# -*- coding: utf-8 -*-
"""r66c：定点核实。
1) \begin{figure}/\begin{table} 数量（判断 \listoffigures/\listoftables 是否为空列表）
2) \tableofcontents / \frontmatter / \mainmatter / \backmatter / \appendix 位置
3) 0 锚章（性别社会学 / 女权主义 / 依恋 / 结语 / 性取向与性别认同 / 两性关系的未来）
   在旧区是否存在同名或近名来源
4) STI 各章在旧区的真实块行数
"""
import io, re, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
raw = io.open(BASE + r"\book.tex", encoding="utf-8", newline="").read().replace("\r\n", "\n")
lines = raw.split("\n")
N = len(lines)
H = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection)\*?\{")


def get_title(s):
    rest = s[s.index("{"):]
    d = 0
    for j, ch in enumerate(rest):
        if ch == "{":
            d += 1
        elif ch == "}":
            d -= 1
            if d == 0:
                return rest[1:j]
    return rest[1:]


print("1) 浮动体数量")
for env in ("figure", "table", "longtable", "tabular"):
    for mode in ("begin", "end"):
        pass
    print("   \\begin{%s} = %d" % (env, raw.count("\\begin{%s}" % env)))
print("   \\includegraphics = %d" % raw.count("\\includegraphics"))

print()
print("2) matter / toc 位置")
for key in ("\\tableofcontents", "\\listoffigures", "\\listoftables",
            "\\frontmatter", "\\mainmatter", "\\backmatter", "\\appendix"):
    hits = [i + 1 for i, l in enumerate(lines) if l.strip() == key]
    print("   %-20s %s" % (key, hits))

OLD = next(i + 1 for i, l in enumerate(lines) if l.strip() == "\\part{old}")
print()
print("3) 0 锚章在旧区的近名来源（旧区起点 L%d）" % OLD)
PROBE = ["性别社会学", "女权主义", "性别平等", "依恋", "爱情", "择偶", "结语", "未来",
         "性取向", "性别认同", "人际关系", "亲密"]
titles = []
for i in range(OLD - 1, N):
    s = lines[i].strip()
    if s.startswith("%"):
        continue
    m = H.match(s)
    if m:
        titles.append((i + 1, m.group(1), get_title(s)))
for kw in PROBE:
    hit = [(ln, lv, t) for ln, lv, t in titles if kw in t]
    print("   「%s」 旧区命中 %d 条" % (kw, len(hit)))
    for ln, lv, t in hit[:6]:
        print("        L%-6d %-10s %s" % (ln, lv, t[:52]))

print()
print("4) 旧区 STI 相关章的真实块行数")
LEVEL = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}
blocks = {}
for k, (ln, lv, t) in enumerate(titles):
    lvl = LEVEL[lv]
    end = N + 1
    for ln2, lv2, t2 in titles[k + 1:]:
        if LEVEL[lv2] <= lvl:
            end = ln2
            break
    body = sum(1 for x in lines[ln:end - 1] if x.strip() and not x.strip().startswith("%"))
    blocks[ln] = (lv, t, end, body)
for ln, lv, t in titles:
    if re.search(r"梅毒|淋病|衣原体|软下疳|滴虫|阴虱|疱疹|尖锐湿疣|艾滋病|肝炎|猴痘|COVID",
                 t) and lv in ("chapter", "section"):
        print("   L%-6d %-9s %-40s %5d 行" % (ln, lv, t[:40], blocks[ln][3]))
