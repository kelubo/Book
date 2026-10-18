# -*- coding: utf-8 -*-
"""r81: 四卷旧区内容并入新目录。用法: python _r81_merge.py report|dry-run|apply"""
import io, re, sys, time, shutil, collections

BASE = "D:/Git/Book/整理中/1_原文校对/ad/"
BOOK, MALE, FEM, POS = "0_book.tex", "1_male.tex", "2_female.tex", "3_position.tex"
HEAD = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{([^}]*)\}")
ENV = re.compile(r"^\\(begin|end)\{")
import importlib.util
spec = importlib.util.spec_from_file_location("tbl", BASE + "_r81_tbl.py")
T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)


def load(fn):
    raw = io.open(BASE + fn, encoding="utf-8", newline="").read()
    crlf = raw.count("\r\n")
    return [x.rstrip("\r") for x in raw.split("\n")], ("crlf" if crlf and crlf == raw.count("\n") else "lf")


def save(fn, lines, nl):
    s = "\n".join(lines)
    if nl == "crlf":
        s = re.sub(r"(?<!\r)\n", "\r\n", s)
    io.open(BASE + fn, "w", encoding="utf-8", newline="").write(s)


FWMAP = {"＋": "+", "－": "-", "（": "(", "）": ")", "［": "[", "］": "]",
         "｛": "{", "｝": "}", "：": ":", "；": ";", "，": ",", "．": ".",
         "／": "/", "＼": "\\", "％": "%", "＃": "#", "＆": "&", "＊": "*",
         "＝": "=", "？": "?", "！": "!", "～": "~", "＇": "'", "＂": '"',
         "–": "-", "—": "-", "−": "-", "‐": "-", "−": "-", "\u00a0": " "}


def norm(t):
    t = t.strip()
    t = re.sub(r"^(第[一二三四五六七八九十]+篇)[：:、]?", "", t)
    t = t.replace("\\&", "&").replace("\\_", "_").replace("\\%", "%")
    t = re.sub(r"\\([a-zA-Z]+)\s*", r"\1", t)
    t = t.replace("\u201c", '"').replace("\u201d", '"')
    t = t.replace("\u2018", "'").replace("\u2019", "'")
    t = "".join(FWMAP.get(ch, ch) for ch in t)
    return re.sub(r"\s+", "", t)


def pnorm(s):
    return re.sub(r"[\s\u3000\u00a0]+", "", s.strip())


def heads(lines, lo=0, hi=None):
    hi = len(lines) if hi is None else hi
    out = []
    for i in range(lo, hi):
        x = lines[i]
        if x.lstrip().startswith("%"):
            continue
        m = HEAD.match(x)
        if m:
            out.append((i, m.group(1), m.group(2).strip()))
    return out


def env_delta(lines):
    c = collections.Counter()
    for x in lines:
        s = re.sub(r"(?<!\\)%.*$", "", x)
        for m in re.finditer(r"\\(begin|end)\{([^}]*)\}", s):
            c[m.group(2)] += (1 if m.group(1) == "begin" else -1)
    return {k: v for k, v in c.items() if v}


def br(s):
    return s.count("{") - s.count("}")


book, bn = load(BOOK); male, mn = load(MALE); fem, fnl = load(FEM); pos, pn = load(POS)
assert bn == "lf" and mn == "crlf" and fnl == "crlf" and pn == "lf"
O = next(i for i, x in enumerate(book) if re.match(r"^\\part\{old\}", x))
mm = next(i for i, x in enumerate(book) if re.match(r"^\\mainmatter", x))
mdc = [i for i, x in enumerate(male) if x.startswith("\\documentclass")][-1]
mO = next(i for i, x in enumerate(male) if re.match(r"^\\part\*\{原始内容\}", x))
fdc = [i for i, x in enumerate(fem) if x.startswith("\\documentclass")][-1]

EXIST = set()
for lines, lo, hi in ((book, mm, O), (male, mdc, mO), (fem, fdc, len(fem)), (pos, 0, len(pos))):
    for x in lines[lo:hi]:
        s = x.strip()
        if not s or s.startswith("%") or HEAD.match(s) or ENV.match(s) or s in ("\\par", "\\\\", "\\noindent"):
            continue
        if len(pnorm(s)) >= 12:
            EXIST.add(pnorm(s))

DECL = set()
for x in book[mm:O]:
    for m in re.finditer(r"\\(keyword|textbf|item)\{", x):
        DECL.add(m.group(1))
ADDED = set()          # 本轮已并入的内容行（跨文件全局去重）


# ---------- 旧区拆解 ----------
def parse_zone(lines, zstart, sec_route, ch_route):
    hs = heads(lines, zstart, len(lines))
    bound = [i for i, lv, t in hs if lv in ("part", "chapter", "section")]
    bound += [i for i in range(zstart, len(lines))
              if "\\end{document}" in lines[i] or lines[i].strip() == "\\backmatter"]
    bound = sorted(set(bound))
    owners = [(i, t) for i, lv, t in hs if lv in ("part", "chapter")]
    secs = [(i, t) for i, lv, t in hs if lv == "section"]
    plans, missing, seen = [], [], set()
    cnt = collections.Counter()
    for k, (i, t) in enumerate(secs):
        e = len(lines)
        for b in bound:
            if b > i:
                e = b; break
        owner = None
        for p, ot in owners:
            if p <= i:
                owner = ot
            else:
                break
        n = norm(t)
        tgt = sec_route.get(n) or ch_route.get(owner)
        if tgt is None:
            missing.append((i, t, owner, repr(n))); continue
        if tgt == "__DROP__":
            cnt["drop"] += 1; continue
        kind = "sec"
        if tgt == "__TAIL__":
            tgt2 = sec_route.get(norm(owner)) or ch_route.get(owner)
            if tgt2 is None or tgt2 == "__DROP__":
                cnt["drop"] += 1; continue
            tgt = tgt2; kind = "tail"
        if n in seen:
            cnt["dup"] += 1          # 旧区同名副本：内容仍并入，靠全局去重防重复
        seen.add(n)
        body = lines[i + 1:e]
        if "|" in tgt:
            tgt, rename = tgt.split("|", 1)
        else:
            rename = None
        plans.append((tgt, rename or t, body, kind))
    # 章/篇 前导言（标题与首个 section 之间）
    for idx, t in owners:
        e2 = len(lines)
        for b in bound:
            if b > idx:
                e2 = b; break
        known = [i for i, l2, t2 in hs if l2 == "section" and idx < i < e2]
        stop = known[0] if known else e2
        intro = lines[idx + 1:stop]
        if sum(1 for x in intro if x.strip() and not x.lstrip().startswith("%")) >= 1:
            tt = t
            n2 = norm(tt)
            tgt = sec_route.get(n2) or ch_route.get(t) or ch_route.get(owner_of_in(owners, idx))
            if tgt and tgt != "__DROP__" and "|" not in tgt:
                plans.append((tgt, "__INTRO__", intro, "intro"))
    seen = seen
    return plans, missing, cnt


def owner_of_in(owners, idx):
    cur = None
    for p, t in owners:
        if p <= idx:
            cur = t
    return cur


SEC_N = {norm(k): v for k, v in T.SEC_ROUTE.items()}
CH_N = {norm(k): v for k, v in T.CH_ROUTE.items()}
MSEC_N = {norm(k): v for k, v in T.MALE_SEC_ROUTE.items()}
MCH_N = {norm(k): v for k, v in T.MALE_CH_ROUTE.items()}

book_plans, book_miss, book_cnt = parse_zone(book, O, SEC_N, CH_N)
male_plans, male_miss, male_cnt = parse_zone(male, mO, MSEC_N, MCH_N)

# 体位块过滤凑数小节
FILLER = re.compile("最大化|身体分离|身体接触|极简|极繁|未来式|复古式|庆祝|协作式|独立式|混合式|平衡式|"
                    "探索式|梦幻式|模仿动物|杂技|舞蹈|冥想|定制式|自由式|动作变化组合|多感官|"
                    "视觉刺激|听觉刺激|嗅觉刺激|触觉刺激|三重刺激|多角度刺激")


def filter_filler(body):
    out, skip, n = [], False, 0
    for x in body:
        m = re.match(r"^\\(subsection|subsubsection)\{", x)
        if m:
            tm = re.match(r"^\\(?:subsection|subsubsection)\{([^}]*)\}", x)
            skip = bool(FILLER.search(tm.group(1)))
            if skip:
                n += 1; continue
        if skip and re.match(r"^\\(part|chapter|section)\{", x):
            skip = False
        if not skip:
            out.append(x)
    return out, n


tot_filler = 0
fixed = []
for tgt, t, body, kind in book_plans:
    if tgt.startswith("P:经典体位详解"):
        body, n = filter_filler(body); tot_filler += n
    fixed.append((tgt, t, body, kind))
book_plans = fixed

print("book 旧区：section %d 纳入 %d（旧区同名跳 %d / 丢弃 %d / 体位凑数弃 %d）"
      % (len(book_plans) + book_cnt["dup"] + book_cnt["drop"], len(book_plans), book_cnt["dup"], book_cnt["drop"], tot_filler))
print("male 老区：section %d 纳入 %d（同名跳 %d / 丢弃 %d）"
      % (len(male_plans) + male_cnt["dup"] + male_cnt["drop"], len(male_plans), male_cnt["dup"], male_cnt["drop"]))
for i, t, o, _n in book_miss:
    print("   [book 无路由] L%-6d %s (%s) n=%s" % (i + 1, t, o, _n))
for i, t, o in male_miss:
    print("   [male 无路由] L%-6d %s (%s)" % (i + 1, t, o))

BUCK = {k: collections.OrderedDict() for k in "BMFP"}
for tgt, t, body, kind in book_plans:
    k, c = tgt.split(":", 1)
    BUCK[k].setdefault(c, []).append((t, body, kind))
for tgt, t, body, kind in male_plans:
    k, c = tgt.split(":", 1)
    BUCK[k].setdefault(c, []).append((t, body, kind))

print("\n=== 目标分布 ===")
for k, lab in (("B", "book"), ("M", "male"), ("F", "female"), ("P", "position")):
    print("[%s] %d 章 / %d 节" % (lab, len(BUCK[k]), sum(len(v) for v in BUCK[k].values())))
    for c, lst in sorted(BUCK[k].items(), key=lambda kv: -len(kv[1])):
        print("    %-26s <- %2d 节" % (c, len(lst)))

if len(sys.argv) < 2 or sys.argv[1] == "report":
    sys.exit(0)
MODE = sys.argv[1]


# ---------- 插入器 ----------
def insert_chapter(lines, chap_title, payloads, stat):
    hs = heads(lines)
    ch = next((i for i, lv, t in hs if lv == "chapter" and norm(t) == norm(chap_title)), None)
    if ch is None:
        return None
    end = next((i for i, lv, t in hs if i > ch and lv in ("chapter", "part")), len(lines))
    insec = [(i, t) for i, lv, t in hs if ch < i < end and lv == "section"]
    sec_end = {i: (insec[k + 1][0] if k + 1 < len(insec) else end) for k, (i, _) in enumerate(insec)}
    sec_head = {norm(t): i for i, t in insec}
    # 章内所有二级标题位置
    sub_loc = {}
    for j in range(ch + 1, end):
        m = re.match(r"^\\(subsection|subsubsection)\{([^}]*)\}", lines[j])
        if m:
            k2 = j + 1
            while k2 < end and not HEAD.match(lines[k2]):
                k2 += 1
            sub_loc[norm(m.group(2))] = (j, k2)
    ch_sub = set(sub_loc)

    appends = collections.defaultdict(list)
    subapp = collections.defaultdict(list)
    tail = []
    tail_by_name = {}
    ch_tail = []
    for t, body, kind in payloads:
        # 内容行去重（已在四卷新目录出现过、或本轮已并入过的整行，不再重复搬入）
        kept = []
        for x in body:
            s = x.strip()
            if s and not s.startswith("%") and not HEAD.match(s) and not ENV.match(s) \
               and s not in ("\\par", "\\\\", "\\noindent") and len(pnorm(s)) >= 12 \
               and (pnorm(s) in EXIST or pnorm(s) in ADDED):
                stat["line_dup"] += 1
                continue
            kept.append(x)
        for x in kept:
            s = x.strip()
            if s and not HEAD.match(s) and not ENV.match(s) and len(pnorm(s)) >= 12:
                ADDED.add(pnorm(s))
        if kind == "intro":
            if kept:
                appends[ch].append([x for x in kept if x.strip()])
                stat["intro_lines"] += len(kept); stat["intro"] += 1
            continue
        if kind == "tail":
            if kept:
                ch_tail.append(["", "% ⇒ [r81 并入] 自旧区（本章小结）"] + [x for x in kept if x.strip()])
                stat["tail_lines"] += len(kept); stat["tail"] += 1
            continue
        n = norm(t)
        cross, buf, i2 = [], [], 0
        while i2 < len(kept):
            m = re.match(r"^\\(subsection|subsubsection)\{([^}]*)\}", kept[i2])
            if m:
                nm = norm(m.group(2))
                j = i2 + 1
                while j < len(kept) and not re.match(r"^\\(section|subsection|chapter|part)\{", kept[j]):
                    j += 1
                if nm in sec_head:            # 与章内某 section 同名 → 并入该节
                    cross.append((sec_head[nm], kept[i2 + 1:j])); stat["cross"] += 1
                    i2 = j; continue
                if nm in sub_loc:             # 同名小节 → 内容并入该小节（不重复标题）
                    subapp[sub_loc[nm][1] - 1].append([x for x in kept[i2 + 1:j] if x.strip()])
                    stat["sub_merge"] += 1
                    i2 = j; continue
                ch_sub.add(nm)
            buf.append(kept[i2]); i2 += 1
        while buf and not buf[0].strip():
            buf.pop(0)
        cur = sec_head.get(n)
        if cur is not None:
            if buf:
                appends[cur].append(buf); stat["merge_lines"] += len(buf); stat["merge"] += 1
        elif n in tail_by_name:
            tail_by_name[n][0].extend([x for x in buf if x.strip()])
            stat["new_merge"] += 1
        elif buf:
            blk = ["", "\\section{%s}" % t, "% ⇒ [r81 并入] 自旧区"] + buf
            tail_by_name[n] = [blk]
            tail.append(blk)
            stat["new_lines"] += len(buf); stat["new"] += 1
            ch_sub.add(n)
        for h, b in cross:
            b = [x for x in b if x.strip()]
            if b:
                appends[h].append(b); stat["cross_lines"] += len(b)
    edits = []
    for h, chunks in appends.items():
        if h == ch:
            edits.append((h, ["", "% ⇒ [r81 并入] 自旧区（章前导言）"] + [x for c in chunks for x in c]))
        else:
            edits.append((sec_end.get(h, end) - 1, [x for c in chunks for x in c]))
    for h, chunks in subapp.items():
        edits.append((h, [x for c in chunks for x in c]))
    if ch_tail:
        edits.append((end - 1, [x for c in ch_tail for x in c]))
    if tail:
        edits.append((end - 1, [x for b in tail for x in b]))
    edits.sort(key=lambda k: -k[0])
    for pos_, ins in edits:
        if ins:
            lines = lines[:pos_ + 1] + ins + lines[pos_ + 1:]
    return lines


# ---------- book ----------
new_book = book[:O]
sb = collections.Counter()
for chap, lst in BUCK["B"].items():
    r = insert_chapter(new_book, chap, lst, sb)
    print("  !! book 缺章 %s" % chap) if r is None else None
    if r is not None:
        new_book = r
new_book += ["", "\\nocite{*}", "\\bibliography{references}", "", "\\end{document}", ""]
print("book 插入统计:", dict(sb))

# ---------- male ----------
new_male = male
sm = collections.Counter()
for chap, lst in BUCK["M"].items():
    r = insert_chapter(new_male, chap, lst, sm)
    print("  !! male 缺章 %s" % chap) if r is None else None
    if r is not None:
        new_male = r
st = next(i for i, x in enumerate(new_male) if re.match(r"^\\part\*\{原始内容\}", x))
new_male = new_male[:st] + ["", "% 注（r81）：原「原始内容区」已按骨架并各章，旧区已删除。", "", "\\end{document}", ""]
print("male 插入统计:", dict(sm))

# ---------- female ----------
new_fem = fem
sf = collections.Counter()
for chap, lst in BUCK["F"].items():
    r = insert_chapter(new_fem, chap, lst, sf)
    print("  !! female 缺章 %s" % chap) if r is None else None
    if r is not None:
        new_fem = r
print("female 插入统计:", dict(sf))

# ---------- position ----------
new_pos = pos
bm = [i for i, x in enumerate(new_pos) if x.strip() == "\\backmatter"]
if len(bm) == 1:
    i = bm[0]
    j = next(k for k, x in enumerate(new_pos) if x.startswith("\\chapter{参考文献}"))
    if i < j:
        new_pos = new_pos[:i] + new_pos[i + 1:]
        j = next(k for k, x in enumerate(new_pos) if x.startswith("\\chapter{参考文献}"))
        new_pos = new_pos[:j] + ["\\backmatter", ""] + new_pos[j:]
sp = collections.Counter()
for chap, lst in BUCK["P"].items():
    r = insert_chapter(new_pos, chap, lst, sp)
    print("  !! position 缺章 %s" % chap) if r is None else None
    if r is not None:
        new_pos = r
print("position 插入统计:", dict(sp))


# ---------- 校验 ----------
if MODE == "dry-run":
    for nm, a, nl_ in (("book", new_book, bn), ("male", new_male, mn),
                       ("female", new_fem, fnl), ("position", new_pos, pn)):
        with io.open(BASE + "_r81pv_" + nm + ".tex", "w", encoding="utf-8", newline="") as f:
            s = "\n".join(a)
            f.write(s.replace("\n", "\r\n") if nl_ == "crlf" else s)


def check(name, old, new, gone=None):
    o, n = "\n".join(old), "\n".join(new)
    assert br(o) == br(n), "%s 花括号净值 %+d" % (name, br(n) - br(o))
    assert "\ufffd" not in n, name + " 替换字符"
    assert "**" not in n, name + " markdown 粗体"
    assert n.count("\\end{document}") == 1, name + " end{document}=%d @%s" % (
        n.count("\\end{document}"), [i + 1 for i, x in enumerate(new) if "end{document}" in x])
    for k, v in env_delta(new).items():
        assert v == 0, "%s 环境 %s 差 %d" % (name, k, v)
    if gone:
        assert not any(gone(x) for x in new), name + " 旧区未删净"


check("book", book, new_book, lambda x: re.match(r"^\\part\{old\}", x))
check("male", male, new_male, lambda x: re.match(r"^\\part\*\{原始内容\}", x))
check("female", fem, new_fem)
check("position", pos, new_pos)
print("\n校验通过：book %d->%d / male %d->%d / female %d->%d / position %d->%d"
      % (len(book), len(new_book), len(male), len(new_male), len(fem), len(new_fem), len(pos), len(new_pos)))

if MODE == "dry-run":
    for nm, a, nl_ in (("book", new_book, bn), ("male", new_male, mn),
                       ("female", new_fem, fnl), ("position", new_pos, pn)):
        with io.open(BASE + "_r81pv_" + nm + ".tex", "w", encoding="utf-8", newline="") as f:
            s = "\n".join(a)
            f.write(s.replace("\n", "\r\n") if nl_ == "crlf" else s)
    print("（dry-run，预览写 _r81pv_*.tex，未动源文件）")
    sys.exit(0)
ts = time.strftime("%Y%m%d_%H%M%S")
for f in (BOOK, MALE, FEM, POS):
    shutil.copy2(BASE + f, BASE + f + ".r81bak_" + ts)
save(BOOK, new_book, bn); save(MALE, new_male, mn); save(FEM, new_fem, fnl); save(POS, new_pos, pn)
print("已写盘（备份 .r81bak_%s）" % ts)
