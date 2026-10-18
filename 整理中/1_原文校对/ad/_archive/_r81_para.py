# -*- coding: utf-8 -*-
"""r81: 段落级知识点覆盖 —— book 旧区每一段是否已在四卷新目录中出现"""
import io, re, collections

BASE = "D:/Git/Book/整理中/1_原文校对/ad/"
HEAD_RE = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{")
ENV_RE = re.compile(r"^\\(begin|end)\{")


def load(fn):
    return [x.rstrip("\r") for x in io.open(BASE + fn, encoding="utf-8").read().split("\n")]


def pnorm(s):
    s = s.strip()
    s = re.sub(r"\s+", "", s)
    return s


def paras(lines, lo, hi, minlen=12):
    """收集段落级内容行：非标题、非注释、非纯环境行、长度>=minlen"""
    out = []
    for i in range(lo, min(hi, len(lines))):
        x = lines[i]
        s = x.strip()
        if not s or s.startswith("%"):
            continue
        if HEAD_RE.match(s) or ENV_RE.match(s):
            continue
        if s in ("\\par", "\\\\", "\\noindent", "\\bigskip", "\\medskip", "\\smallskip"):
            continue
        p = pnorm(s)
        if len(p) < minlen:
            continue
        out.append((i, p))
    return out


book = load("0_book.tex")
male = load("1_male.tex")
fem = load("2_female.tex")
pos = load("3_position.tex")

O = next(i for i, x in enumerate(book) if re.match(r"^\\part\{old\}", x))
mm = next(i for i, x in enumerate(book) if re.match(r"^\\mainmatter", x))
mdc = [i for i, x in enumerate(male) if x.startswith("\\documentclass")][-1]
mO = next(i for i, x in enumerate(male) if re.match(r"^\\part\*\{原始内容\}", x))
fdc = [i for i, x in enumerate(fem) if x.startswith("\\documentclass")][-1]

# 新目录区（不含旧区/停用框架）
NEW = []
NEW += paras(book, mm, O)          # book 骨架区
NEW += paras(male, mdc, mO)        # male 编译区
NEW += paras(fem, fdc, len(fem))   # female 编译区
NEW += paras(pos, 0, len(pos))     # position 全部
NEWSET = collections.Counter(p for _, p in NEW)
print("新目录区段落（含重复）: %d 条，唯一 %d 条" % (len(NEW), len(NEWSET)))

# book 旧区
OLD = paras(book, O, len(book))
print("book 旧区段落: %d 条" % len(OLD))

miss = [(i, p) for i, p in OLD if p not in NEWSET]
print("  未在新目录出现: %d 条 (%.1f%%)" % (len(miss), 100.0 * len(miss) / max(1, len(OLD))))

# 按章节归组失配段落
heads = [(i, m.group(1), m.group(2).strip()) for i, x in enumerate(book)
         if i >= O and not x.lstrip().startswith("%")
         for m in [re.match(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{([^}]*)\}", x)] if m]
def owner(i):
    cur = ("?", "?")
    for hi, lv, t in heads:
        if hi <= i:
            if lv in ("chapter", "part"):
                cur = (lv, t)
        else:
            break
    return cur

grp = collections.defaultdict(list)
for i, p in miss:
    grp[owner(i)].append((i, p))

print("=" * 70)
print("未覆盖段落按旧区章归组（只显示 >=5 条的章）")
for (lv, t), lst in sorted(grp.items(), key=lambda k: -len(k[1])):
    if len(lst) < 5:
        continue
    print("  %-32s %5d 条  (首 L%d)" % (t[:32], len(lst), lst[0][0] + 1))

print("=" * 70)
print("未覆盖段落样例（前 40 条）")
for i, p in miss[:40]:
    print("  L%-6d %s" % (i + 1, p[:88]))

with io.open(BASE + "_r81_miss.txt", "w", encoding="utf-8") as f:
    for i, p in miss:
        lv, t = owner(i)
        f.write("L%d\t%s\t%s\n" % (i + 1, t, p))
print("\n明细已写 _r81_miss.txt")
