# -*- coding: utf-8 -*-
"""r81: 旧区章 -> 骨架章 映射提案"""
import io, re, collections

BASE = "D:/Git/Book/整理中/1_原文校对/ad/"
lines = [x.rstrip("\r") for x in io.open(BASE + "0_book.tex", encoding="utf-8").read().split("\n")]
O = next(i for i, x in enumerate(lines) if re.match(r"^\\part\{old\}", x))
mm = next(i for i, x in enumerate(lines) if re.match(r"^\\mainmatter", x))

HEAD = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{([^}]*)\}")


def norm(t):
    t = t.strip()
    t = re.sub(r"^(第[一二三四五六七八九十]+篇)[：:、]?", "", t)
    t = re.sub(r"（[A-Za-z0-9 ,\.\-/'&+]*）\s*$", "", t)
    t = re.sub(r"\([A-Za-z0-9 ,\.\-/'&+]*\)\s*$", "", t)
    t = t.replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", "", t)


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

sk_parts = [(i, t) for i, lv, t in SK if lv == "part"]
sk_chaps = [(i, t) for i, lv, t in SK if lv == "chapter"]
old_parts = [(i, t) for i, lv, t in OLD if lv == "part"]
old_chaps = [(i, t) for i, lv, t in OLD if lv == "chapter"]

print("骨架：%d 篇 %d 章；旧区：%d 篇 %d 章" % (len(sk_parts), len(sk_chaps), len(old_parts), len(old_chaps)))
print("=" * 78)
print("【骨架章】")
for k, (i, t) in enumerate(sk_chaps):
    e = sk_chaps[k + 1][0] if k + 1 < len(sk_chaps) else O
    secs = [x for x in SK if x[0] > i and x[0] < e and x[1] == "section"]
    print("  #%-3d L%-6d %-30s %4d行 sec=%-3d" % (k + 1, i + 1, t[:30], e - i, len(secs)))

print("=" * 78)
print("【旧区章 / 篇内节群】")
cur_part = None
for k, (i, t) in enumerate(old_chaps):
    e = old_chaps[k + 1][0] if k + 1 < len(old_chaps) else len(lines)
    # 找所属 part
    p = None
    for pi, pt in old_parts:
        if pi < i:
            p = pt
    secs = [x for x in OLD if x[0] > i and x[0] < e and x[1] == "section"]
    print("  L%-6d %-30s [篇:%s] %4d行 sec=%-3d %s" % (
        i + 1, t[:30], (p or "")[:14], e - i, len(secs),
        ";".join(s[2][:12] for s in secs[:3])))

# 篇级：旧区里那些「篇」下面直接挂 section 的
print("=" * 78)
print("【旧区篇下直属 section（无章）】")
for k, (i, t) in enumerate(old_parts):
    e = old_parts[k + 1][0] if k + 1 < len(old_parts) else len(lines)
    has_chap = any(i < ci < e for ci, _ in old_chaps)
    secs = [x for x in OLD if x[0] > i and x[0] < e and x[1] == "section"]
    print("  L%-6d %-34s %4d行 有章=%s 直属sec=%d" % (i + 1, t[:34], e - i, has_chap, len(secs) if not has_chap else 0))
