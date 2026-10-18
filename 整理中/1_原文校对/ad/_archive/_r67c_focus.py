# -*- coding: utf-8 -*-
"""r67：按指定标题，输出旧区对应块的 section 级结构（含行数）。
用于给骨架巨章/第六篇各章补二级结构，标题全部取自旧区实际，不凭空造。
"""
import io, os, re, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
lines = io.open(os.path.join(BASE, "book.tex"), encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
N = len(lines)
H = re.compile(r"^[ \t]*\\(part|chapter|section|subsection|subsubsection)\*?\{")
LVN = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}


def gt(s):
    r = s[s.index("{"):]
    d = 0
    for j, c in enumerate(r):
        if c == "{":
            d += 1
        elif c == "}":
            d -= 1
            if d == 0:
                return r[1:j]
    return r[1:]


T = []
for i, l in enumerate(lines):
    s = l.strip()
    if not s or s.startswith("%"):
        continue
    m = H.match(s)
    if m:
        T.append((i + 1, m.group(1), gt(s)))

OLD = next(ln for ln, lv, t in T if lv == "part" and t == "old")
ENDMAP = {}
for k, (ln, lv, t) in enumerate(T):
    lvl = LVN[lv]
    e = N + 1
    for ln2, lv2, _ in T[k + 1:]:
        if LVN[lv2] <= lvl:
            e = ln2
            break
    ENDMAP[ln] = e


def nb(ln, e):
    return sum(1 for x in lines[ln:e - 1] if x.strip() and not x.strip().startswith("%"))


def n2(t):
    return re.sub(r"[\s\u3000]", "", re.sub(r"[（(][^（）()]*[）)]", "", t))


idx = collections.defaultdict(list)
for ln, lv, t in T:
    if ln >= OLD:
        idx[n2(t)].append((ln, lv, t))

QUERIES = [
    "前戏与爱抚", "前戏技巧", "性生活的前奏曲",
    "定期检查指南", "年度性健康自查清单", "生殖健康检查",
    "性爱中的尴尬与意外", "性行为中的意外损伤与家庭急救",
    "性交时长、频率与“正常”的标准", "性爱前后的清洁与准备", "性健康的其他重要方面",
    "男性生殖系统", "女性生殖系统", "生殖器官的额外知识",
    "性健康核心要素与整体福祉", "性欲与性渴望",
    "性功能障碍", "性功能障碍（续）", "性心理障碍与治疗", "性欲与性功能",
    "性与药物", "性与饮酒", "电子烟与性功能", "物质使用障碍与性功能", "药物与性功能速查",
    "男性常见性健康问题", "女性常见性健康问题",
    "慢性疾病与性健康", "盆底健康与性功能", "性与生活方式", "性与年龄",
    "传统中医与性健康", "中医与性健康", "外生殖器手术与美学决策", "私处整容",
    "性技巧与性辅助", "性爱体验的升华", "口交的艺术与亲密意义", "无插入性交",
    "自慰", "新婚首夜",
]

out = []
for q in QUERIES:
    c = idx.get(n2(q), [])
    out.append("\n### %s   -> %s" % (q, " ; ".join("L%d %s %d行" % (l, v, nb(l, ENDMAP[l])) for l, v, _ in c) or "未命中"))
    for ln, lv, t in c[:2]:
        e = ENDMAP[ln]
        if lv in ("chapter", "section"):
            for ln2, lv2, t2 in T:
                if ln < ln2 < e and lv2 == "section":
                    out.append("      S  %-46s L%-6d %d行" % (t2[:46], ln2, nb(ln2, ENDMAP[ln2])))

io.open(os.path.join(BASE, "_r67c_focus.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
print("written", len(out))
