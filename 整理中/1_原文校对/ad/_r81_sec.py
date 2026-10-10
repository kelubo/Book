# -*- coding: utf-8 -*-
"""r81: 旧区 section 与骨架 section 的同名匹配统计"""
import io, re, collections

BASE = "D:/Git/Book/整理中/1_原文校对/ad/"
HEAD = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{([^}]*)\}")
lines = [x.rstrip("\r") for x in io.open(BASE + "0_book.tex", encoding="utf-8").read().split("\n")]
O = next(i for i, x in enumerate(lines) if re.match(r"^\\part\{old\}", x))
mm = next(i for i, x in enumerate(lines) if re.match(r"^\\mainmatter", x))


def norm(t):
    t = t.strip()
    t = re.sub(r"^(第[一二三四五六七八九十]+篇)[：:、]?", "", t)
    t = re.sub(r"[（(][A-Za-z0-9 ,\.\-/'&+\\]*[）)]\s*$", "", t)
    t = t.replace("\u201c", '"').replace("\u201d", '"')
    t = re.sub(r"[\s\u3000]+", "", t)
    return t


def heads(lo, hi):
    out = []
    for i in range(lo, min(hi, len(lines))):
        x = lines[i]
        if x.lstrip().startswith("%"):
            continue
        m = HEAD.match(x)
        if m:
            out.append((i, m.group(1), m.group(2).strip()))
    return out


SK = heads(mm, O)
OLD = heads(O, len(lines))
sk_chap = [(i, t) for i, lv, t in SK if lv == "chapter"]
sk_sec = [(i, t) for i, lv, t in SK if lv == "section"]
sk_all = {norm(t): (i, lv, t) for i, lv, t in SK if lv in ("section", "subsection")}

# 旧区 section（含 part 下直属）
old_sec = [(i, t) for i, lv, t in OLD if lv == "section"]
print("旧区 section 总数 %d（含重复）" % len(old_sec))

# 当前所属章/篇
def owner(i):
    cur = None
    for j, lv, t in OLD:
        if j <= i and lv in ("part", "chapter"):
            cur = t
    return cur

hit, miss = [], []
seen = set()
for i, t in old_sec:
    n = norm(t)
    if (i, n) in seen:
        continue
    if n in sk_all:
        hit.append((i, t, sk_all[n]))
    else:
        miss.append((i, t, owner(i)))
print("唯一 section %d：命中骨架同名 %d，未命中 %d" % (len(seen) if False else len(set(norm(t) for _, t in old_sec)), len(hit), len(miss)))

print("=" * 92)
print("【未命中：需要人工路由】")
grp = collections.defaultdict(list)
for i, t, o in miss:
    grp[o].append((i, t))
for o, lst in grp.items():
    print("---- 旧区归属：%s ----" % o)
    for i, t in lst:
        print("   L%-6d %s" % (i + 1, t[:70]))
