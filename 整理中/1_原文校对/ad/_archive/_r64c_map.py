"""r64c：建立「骨架引用标题 <-> 旧区实际标题」的匹配，产出迁移映射表。

骨架注释格式示例：
  % 移入：L1587"性科学的沧桑"整章
  % 去重：L17843"性生理反应"（旧内容，与"性反应周期"重复，择优并入）
行号已全部失效，本脚本只用「标题」做锚。
"""
import io, re, os, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
P = os.path.join(BASE, "book.tex")
src = io.open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n")
lines = src.split("\n")
N = len(lines)

# ---------- 1. 收集全文件所有标题（含行号、层级） ----------
H = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection)\*?\{")
titles = []          # (line, level, title)
for i, l in enumerate(lines):
    s = l.strip()
    if s.startswith("%"):
        continue
    m = H.match(s)
    if not m:
        continue
    rest = s[s.index("{"):]
    d = 0
    for j, ch in enumerate(rest):
        if ch == "{":
            d += 1
        elif ch == "}":
            d -= 1
            if d == 0:
                t = rest[1:j]
                break
    else:
        t = rest[1:]
    titles.append((i + 1, m.group(1), t))

print("全文件标题总数：", len(titles))
bylv = collections.Counter(t[1] for t in titles)
print("  按层级：", dict(bylv))

# ---------- 2. 骨架区引用的标题 ----------
SK_START, SK_END = 151, 744
REF = re.compile(r"L(\d+)\s*(?:\u201c([^\u201d]+)\u201d|\"([^\"]+)\")?")
refs = []      # (骨架注释行, 行号, 标题, 类型)
for i in range(SK_START, SK_END):
    s = lines[i].strip()
    if not s.startswith("%"):
        continue
    kind = "移入" if "移入" in s else ("去重" if "去重" in s else None)
    if not kind:
        continue
    for m in REF.finditer(s):
        t = m.group(2) or m.group(3)
        if t:
            refs.append((i + 1, int(m.group(1)), t.strip(), kind))
print("骨架注释中带标题的引用：", len(refs))

# ---------- 3. 匹配 ----------
title_index = collections.defaultdict(list)   # 归一化标题 -> [(行,层级)]
def norm(t):
    return re.sub(r"[\s\u3000]", "", t)

for ln, lv, t in titles:
    title_index[norm(t)].append((ln, lv))

hit, miss = [], []
for cmt, num, t, kind in refs:
    key = norm(t)
    if key in title_index:
        hit.append((cmt, num, t, kind, title_index[key]))
    else:
        # 尝试子串模糊：引用标题是实际标题的前缀或包含关系
        cand = [(ln, lv, at) for ln, lv, at in titles
                if key and (key in norm(at) or norm(at) in key) and len(key) >= 4]
        if len(cand) == 1:
            hit.append((cmt, num, t, kind, [(cand[0][0], cand[0][1])], "模糊"))
        else:
            miss.append((cmt, num, t, kind, cand[:4]))

print("  精确/唯一模糊命中 %d 条" % len(hit))
print("  **未命中 %d 条**" % len(miss))
print()

print("=" * 88)
print("未命中清单（骨架注释行 / 旧行号 / 期望标题 / 候选）")
print("=" * 88)
for cmt, num, t, kind, cand in miss:
    print("骨架L%-4d [%s] L%-6d 「%s」" % (cmt, kind, num, t))
    for c in cand:
        print("        候选?: L%-6d %s  %s" % (c[0], c[1], c[2][:56]))

# ---------- 4. 旧区（L744 起）标题清单 + 内容行数 ----------
print()
print("=" * 88)
print("旧区（L744 起）全部 chapter 及内容行数")
print("=" * 88)
idx = [i for i, (ln, lv, t) in enumerate(titles) if ln > 743 and lv in ("part", "chapter")]
for k, i in enumerate(idx):
    ln, lv, t = titles[i]
    nxt = titles[idx[k + 1]][0] if k + 1 < len(idx) else N
    body = sum(1 for x in lines[ln:nxt - 1] if x.strip() and not x.strip().startswith("%"))
    print("L%-7d %-8s %-44s 正文行 %d" % (ln, lv, t[:44], body))
