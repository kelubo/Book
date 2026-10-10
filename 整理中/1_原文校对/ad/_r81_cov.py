# -*- coding: utf-8 -*-
"""r81: 建立四卷知识点覆盖图 —— book 旧区 vs 四卷新目录（标题级）"""
import io, re, sys, collections

BASE = "D:/Git/Book/整理中/1_原文校对/ad/"
FILES = ["0_book.tex", "1_male.tex", "2_female.tex", "3_position.tex"]

HEAD_RE = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{([^}]*)\}")


def load(fn):
    return [x.rstrip("\r") for x in io.open(BASE + fn, encoding="utf-8").read().split("\n")]


def norm(t):
    """标题归一化：剥英文对照括号、去空白、统一引号"""
    t = t.strip()
    t = re.sub(r"（[A-Za-z0-9 ,\.\-/'&+]+）\s*$", "", t)   # 结尾纯英文对照
    t = re.sub(r"\([A-Za-z0-9 ,\.\-/'&+]+\)\s*$", "", t)
    t = t.replace("\u201c", '"').replace("\u201d", '"')
    t = re.sub(r"\s+", "", t)
    return t


def collect(lines, lo, hi):
    """返回 [(idx, level, title, normtitle)]"""
    out = []
    for i in range(lo, min(hi, len(lines))):
        x = lines[i]
        if x.lstrip().startswith("%"):
            continue
        m = HEAD_RE.match(x)
        if m:
            out.append((i, m.group(1), m.group(2).strip(), norm(m.group(2))))
    return out


def zone_boundaries(fn, lines):
    """返回各卷分区 (名称, lo, hi)"""
    z = []
    if fn == "0_book.tex":
        O = next(i for i, x in enumerate(lines) if re.match(r"^\\part\{old\}", x))
        # 骨架区：mainmatter 之后到 part{old}
        mm = next(i for i, x in enumerate(lines) if re.match(r"^\\mainmatter", x))
        z.append(("book骨架", mm, O))
        z.append(("book旧区", O, len(lines)))
    elif fn == "1_male.tex":
        dc = [i for i, x in enumerate(lines) if x.startswith("\\documentclass")]
        dc = dc[-1]
        O = next(i for i, x in enumerate(lines) if re.match(r"^\\part\*\{原始内容\}", x))
        z.append(("male停用框架", 150, dc))
        z.append(("male骨架+正文", dc, O))
        z.append(("male老区", O, len(lines)))
    elif fn == "2_female.tex":
        dc = [i for i, x in enumerate(lines) if x.startswith("\\documentclass")]
        dc = dc[-1]
        z.append(("female停用框架", 250, dc))
        z.append(("female编译区", dc, len(lines)))
    elif fn == "3_position.tex":
        z.append(("position全部", 0, len(lines)))
    return z


def main():
    allz = {}
    for fn in FILES:
        lines = load(fn)
        for nm, lo, hi in zone_boundaries(fn, lines):
            allz[nm] = (fn, collect(lines, lo, hi), hi - lo)

    # 全四卷"新目录"标题集合（去掉 book 旧区 / male 老区 / 停用框架）
    NEW = {}
    for nm, (fn, hs, n) in allz.items():
        if nm in ("book旧区", "male老区", "male停用框架", "female停用框架"):
            continue
        for idx, lv, t, nt in hs:
            NEW.setdefault(nt, []).append((nm, lv, t))

    print("=" * 70)
    print("各分区规模")
    for nm, (fn, hs, n) in sorted(allz.items(), key=lambda k: -k[1][2]):
        c = collections.Counter(lv for _, lv, _, _ in hs)
        print("  %-16s %-14s %6d 行  ch=%-3d sec=%-4d sub=%-4d" % (
            nm, fn, n, c.get("chapter", 0), c.get("section", 0), c.get("subsection", 0)))

    print("=" * 70)
    print("book 旧区 section 级标题覆盖情况")
    fn, hs, n = allz["book旧区"]
    secs = [h for h in hs if h[1] == "section"]
    miss, hit = [], []
    seen = set()
    for idx, lv, t, nt in secs:
        if nt in seen:
            continue
        seen.add(nt)
        if nt in NEW:
            hit.append((idx, t, NEW[nt][0]))
        else:
            miss.append((idx, t))
    print("  旧区 section 唯一 %d 个：已覆盖 %d，未覆盖 %d" % (len(seen), len(hit), len(miss)))
    print("-" * 70)
    print("  【未覆盖 section 清单】")
    for idx, t in miss:
        print("   L%-6d %s" % (idx + 1, t))

    # 二级标题未覆盖
    print("=" * 70)
    subs = [h for h in hs if h[1] in ("subsection", "subsubsection")]
    seen2 = set()
    miss2 = []
    for idx, lv, t, nt in subs:
        if nt in seen2:
            continue
        seen2.add(nt)
        if nt not in NEW:
            miss2.append((idx, lv, t))
    print("  旧区 sub 级唯一 %d 个：未覆盖 %d" % (len(seen2), len(miss2)))
    for idx, lv, t in miss2[:200]:
        print("   L%-6d %-13s %s" % (idx + 1, lv, t))


main()
