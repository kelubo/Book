# -*- coding: utf-8 -*-
"""r66f：用更严格的解析重算每章来源预算。

规则：
 - 锚匹配：n2(标题) 相等（剥括号、去空白）
 - 候选优先级：section > subsection > subsubsection > chapter；
   同级取行号最小者；命中多条时记录候选数
 - 预算 = 各锚命中的"块正文行数"之和
"""
import io, re, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
lines = io.open(BASE + r"\book.tex", encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
N = len(lines)
H = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection)\*?\{")


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
LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}
blk = {}
for k, (ln, lv, t) in enumerate(T):
    lvl = LV[lv]
    end = N + 1
    for ln2, lv2, _ in T[k + 1:]:
        if LV[lv2] <= lvl:
            end = ln2
            break
    blk[ln] = (lv, t, end, sum(1 for x in lines[ln:end - 1] if x.strip() and not x.strip().startswith("%")))


def n2(t):
    return re.sub(r"[\s\u3000]", "", re.sub(r"[（(][^（）()]*[）)]", "", t))


idx = collections.defaultdict(list)
for ln, lv, t in T:
    if ln >= OLD:
        idx[n2(t)].append((ln, lv, t))

PREF = {"section": 0, "subsection": 1, "chapter": 2, "subsubsection": 3, "part": 9}


def resolve(a):
    c = idx.get(n2(a), [])
    if not c:
        return None, 0
    c = sorted(c, key=lambda x: (PREF[x[1]], x[0]))
    return c[0], len(c)


# ---- 解析骨架 ----
SK_START = next(i + 1 for i, l in enumerate(lines) if l.strip() == "\\part{基础与生理}")
Q = re.compile(r"[“\"]([^”\"]+)[”\"]")
chapters = []
cur_part = None
i = SK_START - 1
while i < OLD - 1:
    s = lines[i].strip()
    if not s:
        i += 1; continue
    if s.startswith("%"):
        if chapters:
            kind = None
            for k in ("移入", "去重", "合并", "可选", "回收", "拆分"):
                if k in s:
                    kind = k; break
            if kind:
                qs = Q.findall(s)
                if not qs:
                    tail = s.split("：", 1)[1] if "：" in s else ""
                    tail = re.sub(r"[（(][^）)]*[）)]", "", tail)
                    qs = [x.strip() for x in re.split(r"[/、+]", tail) if x.strip()]
                for t in qs:
                    chapters[-1][3].append((kind, t))
        i += 1; continue
    m = H.match(s)
    if not m:
        i += 1; continue
    lv, t = m.group(1), gt(s)
    if lv == "part":
        cur_part = t
    elif lv == "chapter":
        chapters.append([cur_part, t, i + 1, []])
    i += 1

print("%-14s %-38s %8s %8s %s" % ("篇", "章", "预算", "锚数", "锚明细"))
tot_by_part = collections.OrderedDict()
for part, ch, cl, items in chapters:
    if ch in ("术语表", "参考文献", "索引", "权威资源与数据来源", "常用问卷与量表",
              "性别认同（原列第一篇第 5 章，建议撤并）",
              "伴侣共同性问题（原列第六篇，已撤并）",
              "两性关系的未来（原列第九篇，建议撤并）"):
        continue
    b = 0; det = []
    for kind, t in items:
        if kind not in ("移入", "去重", "合并", "回收"):
            continue
        node, nc = resolve(t)
        if node:
            ln, lv, tt = node
            b += blk[ln][3]
            det.append("%s/%s=%d%s" % (t[:8], lv[:4], blk[ln][3], "*%d" % nc if nc > 1 else ""))
        else:
            det.append("%s=X" % t[:8])
    tot_by_part.setdefault(part, []).append((ch, b))
    print("%-14s %-38s %8d %8d %s" % (part[:13], ch[:36], b, len(items), " ".join(det)[:70]))

print()
print("== 各篇合计 ==")
for p, rs in tot_by_part.items():
    print("   %-22s 章%2d  预算 %6d" % (p[:22], len(rs), sum(x[1] for x in rs)))
