"""r64d：生成「迁移映射表（标题锚版）」。

为什么：骨架注释里的 149 处行号引用，用户在 2026-09-20 重写文件后全部失效
（校验命中 0 条）。行号是易失锚，标题是稳定锚。本脚本把骨架注释转成
「来源标题 + 当前真实行号 + 块行数 + 重复候选」的结构化映射表。

关键：来源必然在旧区（L754 之后），所以只在旧区建索引，避免骨架自身同名章
造成"命中不唯一"的假未匹配。

输出：_迁移映射表_标题锚版_2026-09-20.md
每次迁移内容后重跑本脚本，行号自动刷新。
"""
import io, re, os, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
SRC = os.path.join(BASE, "book.tex")
OUT = os.path.join(BASE, "_迁移映射表_标题锚版_2026-09-20.md")

raw = io.open(SRC, encoding="utf-8", newline="").read().replace("\r\n", "\n")
lines = raw.split("\n")
N = len(lines)

SK_START, SK_END = 151, 745        # 骨架区切片
OLD_START = 754                    # 旧区起点

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

LEVEL_ORDER = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}
blocks = {}
for k, (ln, lv, t) in enumerate(titles):
    lvl = LEVEL_ORDER[lv]
    end = N
    for ln2, lv2, t2 in titles[k + 1:]:
        if LEVEL_ORDER[lv2] <= lvl:
            end = ln2
            break
    body = sum(1 for x in lines[ln:end - 1]
               if x.strip() and not x.strip().startswith("%"))
    blocks[ln] = (lv, t, end, body)


def norm(t):
    return re.sub(r"[\s\u3000]", "", t)


old_idx = collections.defaultdict(list)
all_idx = collections.defaultdict(list)
for ln, lv, t in titles:
    all_idx[norm(t)].append((ln, lv, t))
    if ln >= OLD_START:
        old_idx[norm(t)].append((ln, lv, t))


def resolve(title):
    """标题 -> (行号, 层级, 块行数, 候选列表)"""
    key = norm(title)
    pool = old_idx if key in old_idx else all_idx
    cands = pool.get(key, [])
    if not cands:
        # 模糊：唯一包含关系
        fuzzy = [(ln, lv, t) for ln, lv, t in titles
                 if ln >= OLD_START and key and (key in norm(t) or norm(t) in key) and len(key) >= 4]
        if len(fuzzy) == 1:
            norm_key = norm(fuzzy[0][2])
            cands = old_idx[norm_key]
        else:
            return None, None, None, []
    ln, lv, t = cands[0]
    lvl, tt, end, body = blocks[ln]
    return ln, lv, body, cands


SRC_RE = re.compile(r"L(\d+)\s*(?:\u201c([^\u201d]+)\u201d|\"([^\"]+)\")?")

# 归集：part -> chapter -> items
chapters = []
for i in range(SK_START, SK_END):
    s = lines[i].strip()
    if not s or s.startswith("%"):
        if s.startswith("%") and chapters:
            kind = "移入" if "移入" in s else ("去重" if "去重" in s else ("移出" if "\u2192" in s else None))
            if kind:
                scope = "整章" if "整章" in s else ("节" if "节" in s else "")
                for m in SRC_RE.finditer(s):
                    t = m.group(2) or m.group(3)
                    if t:
                        chapters[-1][3].append((kind, scope, t))
        continue
    m = H.match(s)
    if not m:
        continue
    lv, t = m.group(1), get_title(s)
    if lv == "part":
        chapters.append([t, None, None, []])
    elif lv == "chapter":
        if chapters and chapters[-1][1] is None:
            chapters[-1][1], chapters[-1][2] = t, i + 1
        else:
            part = chapters[-1][0] if chapters else None
            chapters.append([part, t, i + 1, []])
    else:
        if chapters and chapters[-1][1] and lv in ("section", "subsection", "subsubsection"):
            chapters[-1][3].append(("细目", "", t))

chs = [c for c in chapters if c[1]]

out = []
A = out.append
A("# 迁移映射表（标题锚版）")
A("")
A("> 生成：2026-09-20 ｜ 由 `_r64d_migmap.py` 自动生成，**迁移内容后重跑即可刷新行号**。")
A(">")
A("> **为什么换标题锚**：原骨架注释里的行号（如 `L1587`）是生成时记录的，"
  "2026-09-20 文件重写后 **149 处引用命中 0 条、全部失效**。标题是稳定锚，行号只作辅助。")
A(">")
A("> **列义**：`块` = 该标题到下一个同级/更高级标题之间的正文行数（不含空行/注释），"
  "用于粗估迁移量；`⚠N处` = 旧区有 N 个同名标题，需择优（通常取行数大者为主版本）。")
A(">")
A("> **状态**：⬜ 纯占位 ｜ ◐ 已登记来源待汇 ｜ ✅ 已有正文/细目")
A("")

total_budget = 0
A("## 一、骨架 ↔ 来源 映射")
A("")
last_part = "__INIT__"
for part, ch, cl, items in chs:
    if part != last_part:
        A("")
        A(f"### {part or '(无篇)'}")
        A("")
        A("| 骨架章 | 行 | 来源 | 当前行 | 块 | 状态 |")
        A("|---|---|---|---|---|---|")
        last_part = part
    srcs = [x for x in items if x[0] in ("移入", "去重")]
    subs = [x for x in items if x[0] == "细目"]
    resolved = []
    budget = 0
    for kind, scope, t in srcs:
        ln, lv, body, cands = resolve(t)
        resolved.append((kind, scope, t, ln, lv, body, cands))
        if body:
            budget += body
    total_budget += budget
    if subs and not srcs:
        status = "✅ 已细化"
    elif not srcs:
        status = "⬜ 占位"
    elif budget >= 1200:
        status = f"✅ 大章({budget}行)"
    elif budget > 0:
        status = f"◐ 待汇({budget}行)"
    else:
        status = "⬜ 占位"
    if not resolved:
        A(f"| **{ch}** | L{cl} | （无来源注释） | - | - | {status} |")
        continue
    for k, (kind, scope, t, ln, lv, body, cands) in enumerate(resolved):
        name = f"**{ch}**" if k == 0 else ""
        cls = f"L{cl}" if k == 0 else ""
        st = status if k == 0 else ""
        if ln:
            loc = f"L{ln}"
            blk = str(body)
            if len(cands) > 1:
                lvls = "/".join(f"L{c[0]}" for c in cands[:4])
                loc += f" ⚠{len(cands)}处({lvls})"
        else:
            loc, blk = "**未找到**", "?"
        tag = f"{kind}{'·'+scope if scope else ''}"
        A(f"| {name} | {cls} | {tag} {t} | {loc} | {blk} | {st} |")

A("")
A(f"**骨架来源预算合计：约 {total_budget} 行**（旧区正文总量见下）")
A("")
A("## 二、旧区当前清单（迁移源）")
A("")
A("| 行号 | 层级 | 标题 | 块行数 |")
A("|---|---|---|---|")
old_total = 0
for ln, lv, t in titles:
    if ln < OLD_START or lv not in ("part", "chapter"):
        continue
    lvl, tt, end, body = blocks[ln]
    if lv == "chapter":
        old_total += body
    A(f"| L{ln} | {lv} | {t} | {body} |")
A("")
A(f"**旧区 chapter 正文合计：{old_total} 行**")
A("")

io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("written", OUT)
print("骨架章数", len(chs))
print("来源引用", sum(len([x for x in c[3] if x[0] in ('移入', '去重')]) for c in chs))
un = [(c[1], x[2]) for c in chs for x in c[3] if x[0] in ('移入', '去重')
      and not resolve(x[2])[0]]
print("未找到来源", len(un))
for u in un:
    print("   ", u)
