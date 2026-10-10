"""r64e：骨架目录合理性审查。

1) 修正解析：第三篇 14 章用 `% 移入：L3438 同名节（升为章）` 写法（无引号标题），
   锚就是章标题自身 —— 去旧区找同名 section/chapter。
2) 统计每篇的章数 / 来源预算 / 细化程度。
3) 章粒度排序、命名问题检测、骨架内重叠检测。
"""
import io, re, os, collections, unicodedata

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
SRC = os.path.join(BASE, "book.tex")
raw = io.open(SRC, encoding="utf-8", newline="").read().replace("\r\n", "\n")
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


titles = []
for i, l in enumerate(lines):
    s = l.strip()
    if s.startswith("%"):
        continue
    m = H.match(s)
    if m:
        titles.append((i + 1, m.group(1), get_title(s)))

# 骨架区终点：\part{old} 所在行
OLD_PART = next(ln for ln, lv, t in titles if lv == "part" and t.strip() == "old")
SK_START = next(ln for ln, lv, t in titles if "\u5bfc\u8bba\u4e0e\u57fa\u7840\u77e5\u8bc6" in t) - 2
print(f"骨架起点 L{SK_START}，旧区 part 起点 L{OLD_PART}")

LEVEL_ORDER = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}
blocks = {}
for k, (ln, lv, t) in enumerate(titles):
    lvl = LEVEL_ORDER[lv]
    end = N
    for ln2, lv2, t2 in titles[k + 1:]:
        if LEVEL_ORDER[lv2] <= lvl:
            end = ln2
            break
    body = sum(1 for x in lines[ln:end - 1] if x.strip() and not x.strip().startswith("%"))
    blocks[ln] = (lv, t, end, body)


def norm(t):
    return re.sub(r"[\s\u3000]", "", t)


def norm2(t):
    """剥掉括号内容后再归一 —— 用于跨「（英文对照）」差异匹配。
    例：注释放「衰老科学与性健康」，实际标题是「衰老科学（Geroscience）与性健康」。"""
    t = re.sub(r"[（(][^（）()]*[）)]", "", t)
    return re.sub(r"[\s\u3000]", "", t)


old_idx = collections.defaultdict(list)
old_idx2 = collections.defaultdict(list)
for ln, lv, t in titles:
    if ln >= OLD_PART:
        old_idx[norm(t)].append((ln, lv, t))
        old_idx2[norm2(t)].append((ln, lv, t))


def resolve(title):
    key = norm(title)
    c = old_idx.get(key) or old_idx2.get(norm2(title)) or []
    if c:
        return c[0][0], c[0][1], blocks[c[0][0]][3], c
    return None, None, None, []


SRC_RE = re.compile(r"L(\d+)\s*(?:\u201c([^\u201d]+)\u201d|\"([^\"]+)\")?")

# ---- 归集骨架结构 ----
chapters = []      # [part, ch, line, items]
cur = None
for i in range(SK_START - 1, OLD_PART - 1):
    s = lines[i].strip()
    if not s:
        continue
    if s.startswith("%"):
        if chapters and cur:
            kind = "移入" if "移入" in s else ("去重" if "去重" in s else None)
            if kind:
                same = "同名" in s
                for m in SRC_RE.finditer(s):
                    t = m.group(2) or m.group(3)
                    if t:
                        chapters[-1][3].append((kind, t))
                if same:
                    chapters[-1][3].append((kind, "@同名:" + chapters[-1][1]))
        continue
    m = H.match(s)
    if not m:
        continue
    lv, t = m.group(1), get_title(s)
    if lv == "part":
        cur = t
    elif lv == "chapter":
        chapters.append([cur, t, i + 1, []])
    elif chapters and lv in ("section", "subsection", "subsubsection"):
        chapters[-1][3].append(("细目", t))

# ---- 逐章预算 ----
rows = []
for part, ch, cl, items in chapters:
    srcs = [x for x in items if x[0] in ("移入", "去重")]
    subs = [x for x in items if x[0] == "细目"]
    budget, details, missing = 0, [], []
    for kind, t in srcs:
        real = ch if t.startswith("@同名:") else t
        ln, lv, body, cands = resolve(real)
        if ln:
            budget += body
            details.append((kind, t, ln, lv, body, cands))
        else:
            missing.append((kind, t))
    rows.append(dict(part=part, ch=ch, cl=cl, budget=budget, nsrc=len(srcs),
                     nsub=len(subs), details=details, missing=missing))

# ---------- 报表 ----------
print()
print("=" * 96)
print("A. 各篇规模")
print("=" * 96)
bypart = collections.OrderedDict()
for r in rows:
    bypart.setdefault(r["part"], []).append(r)
for p, rs in bypart.items():
    tb = sum(x["budget"] for x in rs)
    nsub = sum(x["nsub"] for x in rs)
    nempty = sum(1 for x in rs if x["nsrc"] == 0 and x["nsub"] == 0)
    ndetail = sum(1 for x in rs if x["nsub"] > 0)
    print(f"\n【{p}】章 {len(rs)} 个 ｜ 来源预算 {tb} 行 ｜ 已细化 {ndetail} 章 ｜ 纯占位 {nempty} 章 ｜ 细目标题 {nsub} 个")
    for x in rs:
        flag = ""
        if x["nsub"] > 0:
            flag = f" [细目{x['nsub']}]"
        elif x["nsrc"] == 0:
            flag = " [占位]"
        print(f"   L{x['cl']:<6} {x['ch'][:40]:<42} 预算 {x['budget']:>6} 行  来源 {x['nsrc']} 条{flag}")

print()
print("=" * 96)
print("B. 章粒度失衡检查（预算排序）")
print("=" * 96)
srt = sorted(rows, key=lambda x: -x["budget"])
print("-- 预算最大的 15 章 --")
for x in srt[:15]:
    print(f"   {x['budget']:>6} 行  {x['part'][:16]:<18} {x['ch'][:44]}")
print("-- 预算最小的 20 章（已细化章除外）--")
tiny = [x for x in sorted(rows, key=lambda x: x["budget"]) if x["nsub"] == 0]
for x in tiny[:20]:
    print(f"   {x['budget']:>6} 行  {x['part'][:16]:<18} {x['ch'][:44]}")

print()
print("=" * 96)
print("C. 命名检查（按中文主体宽度 / 结构）")
print("=" * 96)
PAREN = re.compile(r"[（(]([^（）()]*)[）)]")


def cjk(s):
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


def W(s):
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def body(s):
    def rep(m):
        return "" if cjk(m.group(1)) == 0 else m.group(0)
    return W(PAREN.sub(rep, s).strip())


print("-- 中文主体宽 >= 18 的章标题 --")
for x in rows:
    b = body(x["ch"])
    if b >= 18:
        print(f"   {b:>3}  {x['ch']}")
print("-- 含 ≥2 个顿号的章标题 --")
for x in rows:
    if x["ch"].count("\u3001") >= 2:
        print(f"   顿号{x['ch'].count(chr(0x3001))}  {x['ch']}")
print("-- 带英文对照括号的章标题 --")
n = 0
for x in rows:
    if re.search(r"[（(][A-Za-z]", x["ch"]):
        n += 1
        print(f"   {x['ch']}")
print(f"   共 {n} 条")

print()
print("=" * 96)
print("D. 骨架内主题重叠（关键词聚类）")
print("=" * 96)
KEYS = ["未来", "资源", "误区", "性别", "文化", "法律", "数字", "教育", "检查", "避孕",
        "生殖", "性取向", "偏好", "心理", "年龄", "特殊", "中医", "整容", "沟通"]
for k in KEYS:
    hit = [x for x in rows if k in x["ch"]]
    if len(hit) >= 2:
        print(f"   「{k}」{len(hit)} 章： " + " ｜ ".join(f"{x['ch']}({x['part'][:4]})" for x in hit))

print()
print("=" * 96)
print("E. 未找到来源的引用")
print("=" * 96)
for x in rows:
    for kind, t in x["missing"]:
        print(f"   [{x['ch']}] {kind} 「{t}」")

print()
print("=" * 96)
print("F. 旧区 STI 篇内的 section 分布（第三篇 15 章的对应来源）")
print("=" * 96)
sti_part = next(ln for ln, lv, t in titles
                if lv == "part" and "性传播疾病" in t and ln > OLD_PART)
print(f"旧区 STI part 在 L{sti_part}")
for ln, lv, t in titles:
    if ln < sti_part:
        continue
    if ln > sti_part + 1300:
        break
    if lv in ("section", "chapter", "part"):
        print(f"   L{ln:<6} {lv:<8} {t[:44]:<46} {blocks[ln][3]:>5} 行")
