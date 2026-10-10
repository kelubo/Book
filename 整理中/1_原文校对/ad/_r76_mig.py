# -*- coding: utf-8 -*-
r"""r76 卷内正文迁移器：把「停用框架区」「原始内容区」「book.tex 骨架区」的正文块
按标题路径搬入「编译区 r72 骨架」的对应标题之下。

用法:
  python _r76_mig.py male report      # 只出解析报告（默认）
  python _r76_mig.py male dry-run     # 全量校验 + 预演，不写盘
  python _r76_mig.py male apply       # 写盘（自动备份）

机制：
  · 骨架锚 = 编译区骨架里的章/节路径（用 "章|节" 或 "篇|章|节" 指定，避免重名歧义）
  · 来源 = MAP 显式指定；未指定时按「标题归一化后唯一匹配」在 fw → old → book 三区中自动寻找
  · 只搬正文，不搬来源标题（骨架已有标题）；块 = 来源标题行之后、到下一个层级 <= 来源的标题之前
  · 锚下的「% 移入：…」「% 框架成稿：…」状态注释在迁入后删除（已过期）；
    其余说明性注释（% ⇐ book.tex / % ⇒ [统一] / % 分工 / % 去重 / % [改名] / % [合并]）保留。

不变量：CRLF 数按插入行数精确核对；\part*{原始内容} 起逐字一致；花括号 delta 不变。
"""
import io
import re
import shutil
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")

VOL = sys.argv[1] if len(sys.argv) > 1 else "male"
MODE = sys.argv[2] if len(sys.argv) > 2 else "report"
assert MODE in ("report", "dry-run", "apply"), MODE

LV = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}
H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{(.*)\}\s*$")
STATUS_CMT = re.compile(r"^%\s*(移入：|框架成稿：)")

# ─── 显式覆盖表：骨架锚路径 -> (来源区, 来源路径) ───
# 来源路径层级用 LV 名+标题交替书写，如 ("section","前列腺疾病","subsection","良性前列腺增生（BPH）")
MAP = {
    "male": {
        # 名称不一致 / 需从框架的节升级迁入
        "男性疾病与健康问题|前列腺疾病|前列腺增生":
            ("fw", ("section", "前列腺疾病", "subsection", "良性前列腺增生（BPH）")),
        "男性疾病与健康问题|前列腺疾病|前列腺癌筛查与 PSA":
            ("fw", ("section", "前列腺癌与PSA筛查",)),
        "男性保健与预防|盆底与射精控制|男性盆底训练与射精控制":
            ("fw", ("section", "男性盆底肌训练",)),
        "男性保健与预防|男性心理健康与性|男性产后抑郁（PPND）":
            ("fw", ("section", "男性产后抑郁（Paternal Postnatal Depression, PPND）",)),
        "男性疾病与健康问题|前列腺疾病|前列腺炎":
            ("fw", ("section", "前列腺疾病", "subsection", "前列腺炎")),
        "男性疾病与健康问题|前列腺疾病|前列腺癌":
            ("fw", ("section", "前列腺疾病", "subsection", "前列腺癌")),
        # 来源在 book.tex 旧区
        "男性疾病与健康问题|前列腺疾病|预防与健康管理":
            ("book", ("subsubsection", "前列腺疾病的预防与健康管理")),
        "男性保健与预防|定期检查与自检|男性生殖健康检查":
            ("book", ("@line", 75603)),      # book.tex 旧区有两份同名节，取后一份（含 5 个小节）
        # 来源为框架成稿（节内小节升为节）
        "男性手术与美学决策|男性外生殖器手术与美学决策|包皮环切":
            ("fw", ("subsubsection", "包皮环切术与HIV预防")),
        "男性手术与美学决策|男性外生殖器手术与美学决策|阴茎延长与增粗手术":
            ("fw", ("subsection", "阴茎延长增粗手术的风险与争议")),
    },
    "female": {},
}
# 暂无可迁来源、需新写的骨架节（保留 % 待写 标记）
PENDING = {
    "male": [
        "男性手术与美学决策|男性外生殖器手术与美学决策|男性外生殖器手术的美学决策",
        "男性手术与美学决策|男性外生殖器手术与美学决策|风险与常见误区",
        "传统中医与男性性健康|中医男科|中西医结合视角",
    ],
    "female": [],
}

fname = VOL + ".tex"
raw = io.open(fname, encoding="utf-8", newline="").read()
assert raw.count("\r\n") == raw.count("\n"), fname + " 应为纯 CRLF"
lines = raw.split("\n")


def body_of(i):
    return lines[i].rstrip("\r")


# ─── 区域边界 ───
ifm = next(i for i, l in enumerate(lines) if re.match(r"^\\ifskip\w*framework", body_of(i)))
els = next(i for i in range(ifm, len(lines)) if body_of(i).strip() == "\\else")
end = next(i for i in range(els, len(lines)) if body_of(i).strip().startswith("\\fi"))
dc = next(i for i, l in enumerate(lines) if body_of(i).strip().startswith("\\documentclass"))
oi = next(i for i, l in enumerate(lines) if body_of(i).strip().startswith("\\part*{原始内容}"))
REG = {"fw": (fname, els + 1, end), "old": (fname, oi, len(lines))}

# 第三来源：book.tex 旧区（男性手术/筛查类内容在此）
_bk = io.open("book.tex", encoding="utf-8", newline="").read().split("\n")
_bko = next(i for i, l in enumerate(_bk) if l.strip() == "\\part{old}")
REG["book"] = ("book.tex", _bko, len(_bk))

_LINES = {fname: lines, "book.tex": _bk}


def parse(fn, lo, hi):
    """返回 [(idx, level, title, path)]，path 为 (level, title) 交替的元组。"""
    src = _LINES[fn]
    out, stack = [], []
    for i in range(lo, hi):
        m = H.match(src[i].rstrip("\r"))
        if not m:
            continue
        lvl, t = m.group(1), m.group(2).strip()
        while stack and LV[stack[-1][0]] >= LV[lvl]:
            stack.pop()
        path = tuple(x for lv, tt in stack for x in (lv, tt)) + (lvl, t)
        out.append((i, lvl, t, path))
        stack.append((lvl, t))
    return out


def norm(t):
    t = re.sub(r"（[^）]*）", "", t)
    t = re.sub(r"\([^)]*\)", "", t)
    t = re.sub(r"[A-Za-z]+", "", t)
    t = re.sub(r"[\s、，,。·・\-—–：:；;／/+＆&]", "", t)
    return t.strip()


TREES = {k: parse(v[0], v[1], v[2]) for k, v in REG.items()}
SKEL = parse(fname, dc, oi)


def find(region, spec):
    """spec = (level,title,level,title,...) 后缀匹配；或 ("@line", N) 精确行号。"""
    if spec[0] == "@line":
        ln = spec[1]
        hits = [x for x in TREES[region] if x[0] + 1 == ln]
        return hits
    n = len(spec)
    return [x for x in TREES[region] if x[3][-n:] == spec]


def norm_index(region):
    d = {}
    for x in TREES[region]:
        if x[1] in ("section", "subsection"):
            d.setdefault(norm(x[2]), []).append(x)
    return d


NORM_IDX = {k: norm_index(k) for k in TREES}


def block_of(region, idx, lvl):
    """来源块的正文行（不含来源标题行，不含其后的状态注释）。"""
    src = _LINES[REG[region][0]]
    hi = REG[region][2]
    nxt = hi
    for j in range(idx + 1, hi):
        m = H.match(src[j].rstrip("\r"))
        if m and LV[m.group(1)] <= LV[lvl]:
            nxt = j
            break
    out = src[idx + 1:nxt]
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return [x if x.endswith("\r") else x + "\r" for x in out]


# ─── 解析计划 ───
plan, unresolved, notes = [], [], []
PEND = set(PENDING.get(VOL, []))
for i, lvl, t, path in SKEL:
    if lvl not in ("section", "subsection"):
        continue
    skel_key = "|".join(path[k] for k in range(1, len(path), 2))
    if skel_key in PEND:
        notes.append("标为待写：%s（%s）" % (t, skel_key))
        continue
    src = None
    why = ""
    ov = MAP.get(VOL, {}).get(skel_key)
    if ov:
        region, spec = ov
        hits = find(region, spec)
        if len(hits) == 1:
            src, why = hits[0], "覆盖表/" + region
        else:
            notes.append("覆盖表命中 %d 处：%s" % (len(hits), skel_key))
    if src is None:
        n = norm(t)
        for region in ("fw", "old"):
            hits = NORM_IDX[region].get(n, [])
            if len(hits) == 1:
                src, why = hits[0], "自动/" + region
                break
    if src is None:
        unresolved.append((skel_key, t))
    else:
        plan.append((i, lvl, t, skel_key, src, why))

print("=" * 96)
print("%s 骨架 节/小节 %d 个 → 解析 %d，待写 %d，未解析 %d"
      % (fname, sum(1 for x in SKEL if x[1] in ("section", "subsection")),
         len(plan), len(PEND), len(unresolved)))
print("-" * 96)
plan2 = []
for i, lvl, t, key, src, why in plan:
    region = why.split("/")[-1] if "/" in why else ("fw" if "fw" in why else "old")
    b = block_of(region, src[0], src[1])
    plan2.append((i, lvl, t, key, region, src, b))
    print("  L%-6d %-9s %-44s ← %-8s L%-6d %-9s %-28s 正文 %d 行"
          % (i + 1, lvl, t[:44], region, src[0] + 1, src[1], src[2][:28], len(b)))
if notes:
    print("-" * 96)
    for n in notes:
        print("  ! " + n)
if unresolved:
    print("-" * 96)
    print("未解析：")
    for key, t in unresolved:
        print("   · %-44s  %s" % (t[:44], key))
print("=" * 96)
print("待插入块 %d 个，合计 %d 行" % (len(plan2), sum(len(x[6]) for x in plan2)))


# ══════════════════════════════════════════════════════════════════════════
#  执行：插入 / 幂等检查 / 不变量断言
# ══════════════════════════════════════════════════════════════════════════
KEY2ANCHOR = {}
for _i, _l, _t, _p in SKEL:
    KEY2ANCHOR["|".join(_p[k] for k in range(1, len(_p), 2))] = (_i, _l, _t)
pend_anchors = [KEY2ANCHOR[k] for k in PEND if k in KEY2ANCHOR]
assert len(pend_anchors) == len(PEND), "待写锚未全部定位"

anchors = sorted([(x[0], x[6], False, x[2]) for x in plan2] + [(x[0], None, True, x[2]) for x in pend_anchors],
                 key=lambda z: z[0])

skip, insert_at, done, empty = set(), {}, 0, []
for anchor, blk, pend, title in anchors:
    j = anchor + 1
    kept = 0
    while j < oi and lines[j].rstrip("\r").strip().startswith("%"):
        if STATUS_CMT.match(lines[j].rstrip("\r").strip()):
            skip.add(j)
        else:
            kept += 1
        j += 1
    # 幂等：锚后到下一个标题之间若已有正文，跳过插入
    k = j
    has = False
    while k < oi and not H.match(lines[k].rstrip("\r")):
        s2 = lines[k].rstrip("\r").strip()
        if s2 and not s2.startswith("%"):
            has = True
            break
        k += 1
    if has:
        done += 1
        continue
    if pend:
        insert_at[j - kept] = ["% 待写：三区均无对应成稿，需新写。原《外生殖器手术与美学决策》相关内容散见 book.tex 旧区。\r"]
        continue
    if not blk:
        empty.append(title)
        continue
    insert_at[j - kept] = ["\r"] + blk + ["\r"]

out = []
for i, l in enumerate(lines):
    if i in skip:
        continue
    out.append(l)
    if i in insert_at:
        out.extend(insert_at[i])

print("=" * 96)
print("插入 %d 个锚点，跳过（已有正文）%d 个，来源为空 %d 个，删除过期状态注释 %d 行"
      % (len(insert_at), done, len(empty), len(skip)))
for t in empty:
    print("   ! 来源块为空：%s" % t)

ns = "\n".join(out)
assert "\n" not in ns.replace("\r\n", ""), fname + " 出现裸 \\n"
exp_crlf = raw.count("\r\n") + sum(len(v) for v in insert_at.values()) - len(skip)
assert ns.count("\r\n") == exp_crlf, "%s CRLF 数异常：%d vs %d" % (fname, ns.count("\r\n"), exp_crlf)
assert raw.count("{") - raw.count("}") == ns.count("{") - ns.count("}"), fname + " 花括号 delta 变"
oi0 = next(i for i, l in enumerate(lines) if l.rstrip("\r").strip().startswith("\\part*{原始内容}"))
oi1 = next(i for i, l in enumerate(out) if l.rstrip("\r").strip().startswith("\\part*{原始内容}"))
assert lines[oi0:] == out[oi1:], fname + " 原始内容区被改动"
print("不变量：CRLF %d->%d  delta 不变  原始内容区逐字一致  [OK]" % (raw.count("\r\n"), ns.count("\r\n")))
print("行数 %d -> %d" % (len(lines), len(out)))

if MODE == "report":
    print("REPORT 模式，未写盘。")
elif MODE == "dry-run":
    print("DRY-RUN 完成，未写盘。")
else:
    st = time.strftime("%Y%m%d_%H%M%S")
    shutil.copy2(fname, fname + ".migbak_" + st)
    io.open(fname, "w", encoding="utf-8", newline="").write(ns)
    print("已写盘（备份 %s.migbak_%s）" % (fname, st))
