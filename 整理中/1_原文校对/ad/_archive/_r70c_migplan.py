# -*- coding: utf-8 -*-
"""r70c：迁移作业清单生成器（只读）。

产出：把 book.tex 的新骨架目录 + 旧区内容对起来，回答两个问题
  A. 目录 -> 旧区：每个 % 移入： 锚是否能在旧区命中？（命中行号 + 旧块规模）
  B. 旧区 -> 目录：旧区的 chapter / section 有多少还没被任何锚引用？（孤儿内容）
"""
import re, collections, io

SRC = "book.tex"
raw = open(SRC, encoding="utf-8").read()
lines = raw.split("\n")

i_main = next(i for i, l in enumerate(lines) if l.strip() == r"\mainmatter")
i_old = next(i for i, l in enumerate(lines) if l.strip() == r"\part{old}")
skel_all = lines[i_main + 1: i_old]

# 剔除 \iffalse ... \fi 区间（内含 3 章过渡记录，不属于当前目录）
skel, in_hide = [], False
for ln in skel_all:
    if ln.strip().startswith(r"\iffalse"):
        in_hide = True
        continue
    if in_hide:
        if ln.strip().startswith(r"\fi"):
            in_hide = False
        continue
    skel.append(ln)
n_hidden = len(skel_all) - len(skel)

old = lines[i_old:]

TITLE = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection|paragraph)\*?\s*\{")
LEVEL = {"part": 0, "chapter": 1, "section": 2, "subsection": 3,
         "subsubsection": 4, "paragraph": 5}


def tname(ln):
    m = TITLE.match(ln)
    if not m:
        return None, None, None
    cmd = m.group(1)
    s = ln[m.end():]
    # 取到匹配的右花括号
    depth, buf = 1, []
    i = 0
    while i < len(s) and depth:
        c = s[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                break
        buf.append(c)
        i += 1
    return cmd, "".join(buf).strip(), m.end() + i + 1


def norm(s):
    s = s.replace("\u201c", '"').replace("\u201d", '"').replace("\u2018", "'").replace("\u2019", "'")
    return re.sub(r"\s+", "", s)


Q = re.compile(r'"([^"]{2,60})"')

# ---------- A. 解析骨架 ----------
parts = []
cur_part = cur_ch = cur_sec = None
skel_titles = []
for ln in skel:
    cmd, name, _ = tname(ln)
    if cmd:
        rec = {"lv": LEVEL[cmd], "cmd": cmd, "name": name, "notes": []}
        skel_titles.append(rec)
        if cmd == "part":
            rec["chapters"] = []
            cur_part = rec
            parts.append(cur_part)
        elif cmd == "chapter":
            rec["sections"] = []
            cur_ch = rec
            if cur_part is not None:
                cur_part["chapters"].append(cur_ch)
        elif cmd == "section":
            rec["subs"] = []
            cur_sec = rec
            if cur_ch is not None:
                cur_ch["sections"].append(cur_sec)
        elif cmd == "subsection":
            if cur_sec is not None:
                cur_sec["subs"].append(name)
        continue
    t = ln.strip()
    if t.startswith("%") and skel_titles:
        skel_titles[-1]["notes"].append(t)

# ---------- B. 旧区标题索引 ----------
old_titles = []
for i, ln in enumerate(old):
    cmd, name, _ = tname(ln)
    if cmd:
        old_titles.append({"lv": LEVEL[cmd], "cmd": cmd, "name": name, "ln": i + i_old + 1})

for k, t in enumerate(old_titles):
    end = len(old)
    for t2 in old_titles[k + 1:]:
        if t2["lv"] <= t["lv"]:
            end = t2["ln"] - i_old - 1
            break
    t["span"] = end - (t["ln"] - i_old - 1)

old_idx = collections.defaultdict(list)
for t in old_titles:
    old_idx[norm(t["name"])].append(t)

# ---------- C. 锚命中 ----------
skel_title_set = set(norm(t["name"]) for t in skel_titles)
old_title_set = set(norm(t["name"]) for t in old_titles)

def base(s):
    """去掉结尾的括号注（中英文），用于宽松匹配"""
    s = norm(s)
    s = re.sub(r"[（(][^（）()]*[）)]$", "", s)
    return s


old_base = collections.defaultdict(list)
for t in old_titles:
    old_base[base(t["name"])].append(t)

skel_norm_names = [norm(t["name"]) for t in skel_titles]

used = set()
miss, dup, fuzzy = [], [], []
n_anchor = n_ref = 0
SRC_KINDS = ("移入", "去重", "合并", "拆分", "并入")
for rec in skel_titles:
    rec["hits"] = []
    rec["miss"] = []
    for note in rec["notes"]:
        m = re.match(r"^%\s*([^：:]{0,6})[：:]", note)
        kind = m.group(1).strip() if m else ""
        is_src = kind in SRC_KINDS
        quotes = Q.findall(note)
        if is_src and not quotes:
            # 合并类注释常写成 甲 + 乙 + 丙，没有引号
            body = note.split("：", 1)[1] if "：" in note else note
            quotes = [t.strip() for t in re.split(r"[+＋、／/]", body) if len(t.strip()) >= 2]
        for q in quotes:
            if is_src:
                n_anchor += 1
            else:
                n_ref += 1
            nq = norm(q)
            cands, how = old_idx.get(nq), "精确"
            if not cands:
                cands, how = old_base.get(base(q)), "去括注"
            if not cands:
                cs = [t for t in old_titles
                      if len(nq) >= 4 and (nq in norm(t["name"]) or norm(t["name"]) in nq)]
                if cs:
                    cands, how = cs, "包含"
                    if is_src:
                        fuzzy.append((q, rec["name"], [(c["cmd"], c["ln"], c["name"]) for c in cs]))
            if cands:
                b = max(cands, key=lambda x: x["span"])
                if is_src:
                    rec["hits"].append((q, b, how))
                used.add(id(b))
                if is_src and len(cands) > 1:
                    dup.append((q, [(c["cmd"], c["ln"], c["span"]) for c in cands]))
            elif is_src:
                k2 = "骨架内自指" if any(nq in s for s in skel_norm_names) else "旧区与骨架均无"
                rec["miss"].append((q, k2))
                miss.append((q, k2, rec["cmd"], rec["name"]))

# 把命中的锚算到 chapter 上（便于逐章报进度）
for p in parts:
    for ch in p["chapters"]:
        ch["anchor_hits"] = list(ch["hits"])
        ch["anchor_miss"] = list(ch["miss"])
        for s in ch["sections"]:
            ch["anchor_hits"] += s["hits"]
            ch["anchor_miss"] += s["miss"]

# ---------- D. 孤儿旧标题（chapter / section 级） ----------
orph = [t for t in old_titles if t["lv"] in (1, 2) and id(t) not in used]
orph_ch = [t for t in orph if t["lv"] == 1]
orph_sec = [t for t in orph if t["lv"] == 2]

# ---------- E. 每章正文状态 ----------
def chapter_has_body(idx):
    """骨架中该章是否已有正文（非标题、非注释的可读行）"""
    nxt = len(skel_titles)
    for k in range(idx + 1, len(skel_titles)):
        if skel_titles[k]["lv"] <= 1:
            nxt = k
            break
    n = 0
    started = False
    for ln in skel:
        pass
    return None


# 逐行扫描骨架，按 chapter 归段统计正文行
ch_stats = []
cur = None
for ln in skel:
    cmd, name, _ = tname(ln)
    if cmd == "chapter":
        cur = {"name": name, "body": 0}
        ch_stats.append(cur)
        continue
    if cmd in ("part", "section", "subsection", "subsubsection", "paragraph"):
        continue
    t = ln.strip()
    if cur and t and not t.startswith("%"):
        cur["body"] += 1

named = {}
for p in parts:
    for ch in p["chapters"]:
        named.setdefault(ch["name"], ch)
ch_body = {}
for s in ch_stats:
    ch_body[s["name"]] = ch_body.get(s["name"], 0) + s["body"]

# ---------- F. 输出 ----------
out = []
w = out.append
w("# book.tex 迁移作业清单")
w("")
w("生成时间：2026-09-21　｜　源文件：`book.tex`（纯 LF，%d 行）" % len(lines))
w("骨架区：L%d（`\\mainmatter`）— L%d（`\\part{old}` 前）　｜　旧区：L%d — 文末" % (i_main + 1, i_old, i_old + 1))
w("")
w("## 0. 总览")
w("")
tot_ch = sum(len(p["chapters"]) for p in parts)
tot_sec = sum(len(c["sections"]) for p in parts for c in p["chapters"])
tot_sub = sum(len(s["subs"]) for p in parts for c in p["chapters"] for s in c["sections"])
w("| 指标 | 数值 |")
w("|---|---|")
w("| 骨架篇 / 章 / 节 / 小节 | %d / %d / %d / %d |" % (len(parts), tot_ch, tot_sec, tot_sub))
w("| 移入／去重／合并锚引用的标题数 | %d |" % n_anchor)
w("| 　其中在旧区**命中** | %d |" % (n_anchor - len(miss)))
w("| 　其中**未命中** | %d |" % len(miss))
w("| 说明性注释里顺带提到的标题（不计入来源锚） | %d |" % n_ref)
w("| 旧区 chapter / section 总数 | %d / %d |" % (
    len([t for t in old_titles if t["lv"] == 1]), len([t for t in old_titles if t["lv"] == 2])))
w("| 旧区**孤儿** chapter（未被任何锚引用） | %d |" % len(orph_ch))
w("| 旧区**孤儿** section（未被任何锚引用） | %d |" % len(orph_sec))
w("")

w("## 1. 逐篇进度")
w("")
w("| 篇 | 章数 | 已有正文 | 待迁章数 | 锚命中 | 锚未命中 |")
w("|---|---|---|---|---|---|")
for p in parts:
    nb = sum(1 for c in p["chapters"] if ch_body.get(c["name"], 0) > 0)
    h = sum(len(c["anchor_hits"]) for c in p["chapters"])
    m = sum(len(c["anchor_miss"]) for c in p["chapters"])
    w("| %s | %d | %d | %d | %d | %d |" % (p["name"], len(p["chapters"]), nb, len(p["chapters"]) - nb, h, m))
w("")

w("## 2. 逐章明细")
w("")
for p in parts:
    w("### %s" % p["name"])
    w("")
    w("| 章 | 节 | 小节 | 正文行 | 待迁锚（命中 / 未命中） |")
    w("|---|---|---|---|---|")
    for c in p["chapters"]:
        ns = len(c["sections"])
        nsub = sum(len(s["subs"]) for s in c["sections"])
        nb = ch_body.get(c["name"], 0)
        h, m = len(c["anchor_hits"]), len(c["anchor_miss"])
        flag = " **有正文**" if nb > 0 else ""
        w("| %s%s | %d | %d | %d | %d / %d |" % (c["name"], flag, ns, nsub, nb, h, m))
    w("")

if miss:
    w("## 3. 未命中的锚（%d）" % len(miss))
    w("")
    w("三类：**骨架内自指**＝该内容已在新骨架里，属说明性引用，可忽略；")
    w("**旧区与骨架均无**＝需另写，或该内容已并入别处。")
    w("")
    w("| 锚标题 | 类型 | 所属层级 | 所属标题 |")
    w("|---|---|---|---|")
    for q, kind, lv, nm in miss:
        w("| %s | %s | %s | %s |" % (q, kind, lv, nm))
    w("")

if fuzzy:
    w("### 3.1 靠“包含关系”匹配上的锚（%d，标题措辞不完全一致，迁移时按名搜索）" % len(fuzzy))
    w("")
    w("| 锚标题 | 所属标题 | 实际匹配到的旧标题 |")
    w("|---|---|---|")
    for q, nm, cs in fuzzy:
        w("| %s | %s | %s |" % (q, nm, " ／ ".join("%s@L%d（%s）" % c for c in cs)))
    w("")

if dup:
    seen, rows = set(), []
    for q, cs in dup:
        key = (q, tuple(cs))
        if key in seen:
            continue
        seen.add(key)
        rows.append((q, cs))
    w("## 4. 一个锚对到多个旧标题（%d 组，需择优保留）" % len(rows))
    w("")
    w("| 锚标题 | 候选（类型@行号，块行数） | 建议保留（块最大） |")
    w("|---|---|---|")
    for q, cs in rows:
        best = max(cs, key=lambda c: c[2])
        w("| %s | %s | %s@L%d |" % (
            q, " ／ ".join("%s@L%d（%d行）" % c for c in cs), best[0], best[1]))
    w("")

w("## 5. 旧区孤儿内容（目录里还没给位置）")
w("")
w("孤儿不等于废弃。这里把每个孤儿章先归类，便于判断该留、该删还是该改标注。")
w("")
w("### 5.1 孤儿 chapter（%d）" % len(orph_ch))
w("")
skel_part_names = set(norm(t["name"]) for t in skel_titles if t["lv"] == 0)
orph_by_name = collections.Counter(norm(t["name"]) for t in orph_ch)
AUX = {"术语表": "旧区尾部辅助材料 → 对应附录「术语表」",
       "索引": "旧区尾部辅助材料 → 对应附录「索引」",
       "参考文献": "旧区尾部辅助材料 → 对应附录「参考文献」",
       "求助与资源导航": "骨架同名列标了 [待写]，但旧区 L58237 有现成 196 行 → 建议撤销该标注"}
for t in sorted(orph_ch, key=lambda x: -x["span"]):
    kids = [x for x in old_titles if x["lv"] == 2 and t["ln"] < x["ln"] < t["ln"] + t["span"]]
    nk = len([x for x in kids if id(x) in used])
    if t["name"] in AUX:
        why = AUX[t["name"]]
    elif orph_by_name[norm(t["name"])] > 1:
        why = "旧区内部重复副本：同名章在本区出现 %d 次，择优保留一份" % orph_by_name[norm(t["name"])]
    elif norm(t["name"]) in skel_part_names:
        why = "与骨架某**篇**同名：旧区分章，内容已分散到该篇各章，搬完后删章标题"
    elif norm(t["name"]) in skel_norm_names:
        why = "与骨架同名 → 重复副本，迁移时择优保留一份"
    elif nk:
        why = "容器章：其下 %d/%d 节已被目录引用，迁移后删章标题即可" % (nk, len(kids))
    else:
        why = "需人工判断归属"
    w("- L%d　**%s**　（%d 行）　→ %s" % (t["ln"], t["name"], t["span"], why))
w("")
w("### 5.2 孤儿 section（%d，按体积前 60）" % len(orph_sec))
w("")
for t in sorted(orph_sec, key=lambda x: -x["span"])[:60]:
    w("- L%d　%s　（%d 行）" % (t["ln"], t["name"], t["span"]))
w("")

w("## 6. 迁移优先级建议（旧区 chapter 块体积降序前 20）")
w("")
w("先搬大块：块越大，搬完对成书的贡献越明显，也越早暴露结构问题。")
w("")
w("| 序 | 旧区行号 | 章名 | 块行数 | 已被锚引用 |")
w("|---|---|---|---|---|")
for k, t in enumerate(sorted([x for x in old_titles if x["lv"] == 1],
                             key=lambda x: -x["span"])[:20], 1):
    w("| %d | L%d | %s | %d | %s |" % (
        k, t["ln"], t["name"], t["span"], "是" if id(t) in used else "否（孤儿）"))
w("")

open("_r70_迁移作业清单_2026-09-21.md", "w", encoding="utf-8", newline="\n").write("\n".join(out))
print("锚 %d：命中 %d / 未命中 %d" % (n_anchor, n_anchor - len(miss), len(miss)))
print("旧区章节：chapter %d / section %d" % (
    len([t for t in old_titles if t["lv"] == 1]), len([t for t in old_titles if t["lv"] == 2])))
print("孤儿：chapter %d / section %d" % (len(orph_ch), len(orph_sec)))
print("骨架：%d 篇 %d 章 %d 节 %d 小节" % (len(parts), tot_ch, tot_sec, tot_sub))
print("写出 _r70_迁移作业清单_2026-09-21.md")
