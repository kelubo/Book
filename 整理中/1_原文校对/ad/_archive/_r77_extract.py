# -*- coding: utf-8 -*-
"""r77 执行层：把已迁入 position.tex 的内容从 book.tex / female.tex 原位移出，留 % ⇒ [已移出] 标记。

用法：
    python _r77_extract.py dry-run
    python _r77_extract.py apply

零丢失证明：对每个待删区间，其"实质行"（非空、非注释）必须 100% 被本次提取的块覆盖；
区间内未被覆盖的残留行只允许是 空行 / 注释行 / \\chapter 或 \\part 标题行。
"""
import io, re, sys, shutil, time
import _r77_plan as P

MODE = sys.argv[1] if len(sys.argv) > 1 else "dry-run"

H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{(.*)\}\s*$")
CH_PART = re.compile(r"^\\chapter\*?\{")   # r77 教训：只允许 \chapter 作为可重建的结构残留；\part 绝不允许被丢弃
LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}


def load(fn):
    raw = io.open(fn, encoding="utf-8", newline="").read()
    crlf = raw.count("\r\n")
    lines = raw.split("\n")
    if crlf:
        lines = [x[:-1] if x.endswith("\r") else x for x in lines]
    return raw, lines, crlf


RAW = {}
LNS = {}
for fn in ("book.tex", "female.tex"):
    RAW[fn], LNS[fn], crlf = load(fn)
    print("%-11s 行 %-6d CRLF %-6d 花括号 delta %+d" % (fn, len(LNS[fn]), crlf,
          RAW[fn].count("{") - RAW[fn].count("}")))

# ── 生成删除计划 ─────────────────────────────────────────────────────────
def blocks_of():
    """返回 [(file, region, a, b_exclusive, kind, title)]，与 _r77_build 的提取完全一致。"""
    out = []
    for part, chaps in P.STRUCT:
        for ctitle, blocks in chaps:
            for spec in blocks:
                if spec[0] == "BIGPOS":
                    continue        # 单独处理
                region, a, b = spec[0], spec[1], spec[2]
                fn = P.FILE_OF[region]
                L = LNS[fn]
                if b is None:
                    m0 = H.match(L[a - 1])
                    lv0 = LV[m0.group(1)]
                    b = P.REGION[region][1]
                    for j in range(a, P.REGION[region][1]):
                        m = H.match(L[j])
                        if m and LV[m.group(1)] <= lv0:
                            b = j + 1
                            break
                # r77 教训：块尾若紧邻 \part（篇分隔），必须截断，不得把它一起删掉
                for k in range(a - 1, b - 1):
                    if L[k].lstrip().startswith("\\part"):
                        print("   [截断] %s L%d 处遇 \\part，块尾由 L%d 收至 L%d" % (region, a, b - 1, k))
                        b = k + 1
                        break
                m = H.match(L[a - 1])
                out.append((fn, region, a, b, m.group(1), m.group(2).strip()))
    # BIGPOS 逐小节
    BA, BB = 59372, 66080
    toks = []
    for i in range(BA - 1, BB):
        m = H.match(LNS["book.tex"][i])
        if m:
            toks.append((i, m.group(1), m.group(2).strip()))
    toks.append((BB, None, None))
    pos = {}
    for k in range(len(toks) - 1):
        i, lvl, t = toks[k]
        if lvl == "subsection":
            pos.setdefault(t, (i + 1, toks[k + 1][0]))
    for bucket in ("base", "classic", "variation", "special"):
        for t in P.BIG_POS[bucket]:
            a, b = pos[t]
            out.append(("book.tex", "BIG", a, b, "subsection", t))
    return out


BLOCKS = blocks_of()
print("提取块 %d 个" % len(BLOCKS))

# ── 合并成"待删区间"（把连续的块并成一段） ────────────────────────────────
def merge(fn, ivs):
    ivs = sorted(ivs)
    res = []
    for a, b, lvl, t in ivs:
        if res and a <= res[-1][1]:
            pa, pb, plvl, pt = res[-1]
            res[-1] = (pa, max(pb, b), plvl, pt)
        else:
            res.append((a, b, lvl, t))
    return res


per_file = {}
for fn in ("book.tex", "female.tex"):
    per_file[fn] = merge(fn, [(a, b, lvl, t) for f, r, a, b, lvl, t in BLOCKS if f == fn])

# ── book.tex：整章搬迁（8 章）+ P4 整篇 + 巨块片段 ────────────────────────
CHAP_RANGES = [
    (3867, 4221, "chapter", "新婚首夜"),
    (4221, 4618, "chapter", "自慰"),
    (4618, 4906, "chapter", "情感亲密与沟通"),
    (4906, 5582, "chapter", "前戏与爱抚"),
    (5582, 5871, "chapter", "性技巧与性辅助"),
    (5871, 6264, "chapter", "体位与姿势"),
    (6264, 6797, "chapter", "性爱的多样实践"),
    (7110, 7440, "chapter", "性爱中的意外与处理"),
    (27245, 27842, "part", "第四篇：性交体位与姿势艺术"),
]
# 撤掉这些整章/整篇后，其内部块已全部被提取 → 用整块区间替换
# r77：章级区间若尾部紧邻 \part，同样要截断（否则会连带删掉下一篇的 \part 行）
CHAP_RANGES2 = []
for a, b, lvl, t in CHAP_RANGES:
    if lvl != "part":
        for k in range(a - 1, b - 1):
            if LNS["book.tex"][k].lstrip().startswith("\\part"):
                print("   [截断] CHAP_RANGES %s 块尾由 L%d 收至 L%d" % (t, b - 1, k))
                b = k + 1
                break
    CHAP_RANGES2.append((a, b, lvl, t))
for a, b, lvl, t in CHAP_RANGES2:
    per_file["book.tex"].append((a, b, lvl, t))
per_file["book.tex"] = merge("book.tex", [(a, b, lvl, t) for a, b, lvl, t in per_file["book.tex"]])

# ── 覆盖度校验（零丢失证明） ──────────────────────────────────────────────
def covered_idx(fn):
    s = set()
    for f, r, a, b, lvl, t in BLOCKS:
        if f == fn:
            s |= set(range(a, b))          # 半开 [a, b-1] → 0-based [a-1, b-1)
    return s


print("=" * 96)
ok = True
for fn in ("book.tex", "female.tex"):
    cov = covered_idx(fn)
    for a, b, lvl, t in per_file[fn]:
        resid = []
        for i in range(a - 1, b - 1):
            if i + 1 in cov:
                continue
            s = LNS[fn][i].rstrip()
            if not s.strip() or s.lstrip().startswith("%") or CH_PART.match(s):
                continue
            if lvl == "part" and s.lstrip().startswith("\\part"):
                continue        # 整篇移出：该 \part 行本身即预期删除

            resid.append((i + 1, s[:100]))
        flag = "OK " if not resid else "!! "
        if resid:
            ok = False
        print("%s%-11s L%-6d~L%-6d %-11s 「%s」 残留非结构行 %d" % (
            flag, fn, a, b - 1, lvl, t[:28], len(resid)))
        for ln, s in resid[:5]:
            print("        L%d | %s" % (ln, s))
assert ok, "存在未被提取覆盖的实质行，拒绝执行"

# 额外护栏（r77 教训）：\part 清单的增减必须精确等于预期
def _parts(L):
    return [x.strip() for x in L if x.strip().startswith("\\part")]


EXPECT_PART_DEL = {"\\part{第四篇：性交体位与姿势艺术}"}
for fn in ("book.tex", "female.tex"):
    L = LNS[fn]
    keep = [l for i, l in enumerate(L, 1) if not any(a <= i < b for a, b, _, _ in per_file[fn])]
    gone = [p for p in _parts(L) if p not in _parts(keep)]
    unexpected = [p for p in gone if p not in EXPECT_PART_DEL]
    assert not unexpected, "%s 有非预期删除的 \\part：%s" % (fn, unexpected)
    print("%s \\part 清单校验 OK（删除 %d 个，均为预期）" % (fn, len(gone)))

# ── 生成标记并执行删除（倒序） ───────────────────────────────────────────
MARK = {"chapter": "章", "part": "篇", "section": "节", "subsection": "小节"}
newlines = {fn: list(LNS[fn]) for fn in LNS}
stat = []
for fn in ("book.tex", "female.tex"):
    for a, b, lvl, t in sorted(per_file[fn], key=lambda x: -x[0]):
        marker = "%% ⇒ [已移出] %s「%s」→ position.tex" % (MARK[lvl], t)
        newlines[fn][a - 1:b - 1] = [marker]
        stat.append((fn, a, b, b - a, marker))

# book.tex：在篇三标题后补一条说明
for i, l in enumerate(newlines["book.tex"]):
    if l.strip() == "\\part{亲密关系与性实践}":
        note = ("% 注（r77）：本篇的性爱实践类章节已整体移出至 position.tex（性爱实践卷）——"
                "新婚首夜 / 自慰 / 情感亲密与沟通 / 前戏与爱抚 / 性技巧与性辅助 / 体位与姿势 / "
                "性爱的多样实践 / 性爱中的意外与处理。原位留 % ⇒ [已移出] 标记。"
                "本篇现含「婚姻与家庭性健康」「家庭形态的多样性」两章；"
                "篇名中的「性实践」二字已不贴切，建议改为「婚姻、家庭与亲密关系」（待定）。")
        newlines["book.tex"].insert(i + 1, note)
        print("已在 \\part{亲密关系与性实践} 后补注释")
        break

# ── 写盘 + 不变量断言 ────────────────────────────────────────────────────
print("=" * 96)
print("%-11s %-8s %-8s %-6s %s" % ("文件", "原行数", "新行数", "删除", "标记"))
for fn in ("book.tex", "female.tex"):
    old = LNS[fn]
    new = newlines[fn]
    ns = "\n".join(new) if fn == "book.tex" else "\r\n".join(new)
    print("%-11s %-8d %-8d %-6d %d 个" % (fn, len(old), len(new),
          len(old) - len(new) + len(per_file[fn]), len(per_file[fn])))

    if fn == "book.tex":
        assert "\r" not in ns, "book.tex 出现 CR"
        assert ns.count("\\part{old}") == 1
        assert ns.rstrip().endswith("\\end{document}")
    else:
        assert ns.count("\r\n") == len(new) - 1, "female.tex 不是纯 CRLF：%d vs %d" % (ns.count("\r\n"), len(new) - 1)
    assert (RAW[fn].count("{") - RAW[fn].count("}")) == (ns.count("{") - ns.count("}")), fn + " 花括号 delta 变化"
    print("        不变量 OK（换行类型 / \\part{old} / 结尾 / 花括号 delta %+d）"
          % (ns.count("{") - ns.count("}")))

if MODE == "apply":
    st = time.strftime("%Y%m%d_%H%M%S")
    for fn in ("book.tex", "female.tex"):
        shutil.copy2(fn, fn + ".r77bak_" + st)
        new = newlines[fn]
        ns = "\n".join(new) if fn == "book.tex" else "\r\n".join(new)
        io.open(fn, "w", encoding="utf-8", newline="").write(ns)
    print("已写盘（备份后缀 .r77bak_%s）" % st)
else:
    print("%s 模式，未写盘。" % MODE)
