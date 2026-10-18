# -*- coding: utf-8 -*-
r"""r74 附录执行器：把附录章内容插到对应 \chapter 行之后（内容自带 \section/\subsection）。

用法: python _r74_apx.py <data_module> [dry-run|apply]
数据模块需定义 APX = { "章标题": r'''正文...''' }

安全规则：
  1) 锚行逐字全等（\chapter{标题} 在骨架区恰好 1 处）
  2) 该章当前必须无正文（其后紧跟空行/注释，直到下一个 chapter/part）
  3) 内容不得自带 \chapter；不得含 **、非法控制字符、未转义 %
  4) 内容内 \section/\subsection 标题在章内唯一，且不与既有标题重复
  5) 花括号净值不变；旧区 \part{old} 起逐字一致
  6) 幂等：若该章已有正文则跳过
"""
import io, sys, importlib, re

sys.stdout.reconfigure(encoding="utf-8")

MOD_NAME = sys.argv[1]
MODE = sys.argv[2] if len(sys.argv) > 2 else "dry-run"
assert MODE in ("dry-run", "apply"), MODE

mod = importlib.import_module(MOD_NAME)
APX = mod.APX

F = "book.tex"
raw = io.open(F, encoding="utf-8", newline="").read()
assert raw.count("\r\n") == 0, "book.tex 应为纯 LF"
lines = raw.split("\n")

H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{(.*?)\}(\[.*?\])?\s*(%.*)?$")
OLD_IDX = next(i for i, l in enumerate(lines)
               if H.match(l) and H.match(l).group(1) == "part" and H.match(l).group(2) == "old")

# 骨架区所有标题（含层级）
titles = {}
for i in range(OLD_IDX):
    m = H.match(lines[i])
    if m:
        titles.setdefault((m.group(1), m.group(2).strip()), []).append(i + 1)

# 参考文献章为书目性质，含外文原题，豁免"混入英文词"检查
EN_CHECK_EXEMPT = {"参考文献"}
# 术语表按设计含"中文（English）"对照：仅豁免括号内的英文，括号外的仍严格检查
EN_CHECK_PAREN_OK = {"术语表", "常用问卷与量表"}
ALLOW_EN = set("""
STI HIV HPV HSV HBV WHO UNESCO UNAIDS UNFPA UNICEF CEDAW PrEP PEP VCT
ICD DSM GRISS IIEF FSFI FSDS PEDT ASEX ECR RAS DAS KSOG SHIM MSHQ SFQ
CDC CNKI NAAT LARC ED PE
Cochrane Library PubMed MEDLINE BDSM LGBTQ WAS
Rosen Symonds Klein Brennan Spector
""".split())

print("=== 校验 1：锚行定位 + 空章检测 ===")
plan, already = [], []
for ch, body in APX.items():
    loc = titles.get(("chapter", ch), [])
    assert len(loc) == 1, "章标题 %s 在骨架区命中 %d 处（应恰好 1 处）" % (ch, len(loc))
    ln = loc[0]
    actual = lines[ln - 1]
    assert actual.strip() == "\\chapter{%s}" % ch, "锚行不符 L%d: %s" % (ln, actual)
    # 该章是否已有正文：跳过空行与注释，下一个非空行应为 \chapter / \part / \iffalse
    j = ln
    has_body = False
    while j < OLD_IDX:
        s = lines[j].strip()
        if not s or s.startswith("%"):
            j += 1
            continue
        if s.startswith(("\\chapter", "\\part", "\\iffalse", "\\fi")):
            break
        has_body = True
        break
    if has_body:
        already.append((ln, ch))
    else:
        plan.append((ln, ch))
print("  目标 %d 章，待插入 %d，已有正文（跳过）%d" % (len(APX), len(plan), len(already)))
for ln, ch in already:
    print("    - 跳过:", ch)
for ln, ch in plan:
    print("    + 插入:", ch, "@L%d" % ln)

print()
print("=== 校验 2：内容洁净度 + 标题唯一性 ===")
for ch, body in APX.items():
    assert not body.lstrip().startswith("\\chapter"), ch + " 内容自带章标题！"
    assert "**" not in body, ch + " 含 **"
    d = body.count("{") - body.count("}")
    assert d == 0, "%s 花括号不配平 delta=%d" % (ch, d)
    for c in body:
        o = ord(c)
        if (o < 32 and c != "\n") or o == 127 or 0x80 <= o <= 0x9F:
            raise AssertionError("%s 含非法控制字符 U+%04X" % (ch, o))
    # 未转义 %
    for i, l in enumerate(body.split("\n")):
        s = l.strip()
        if s.startswith("%"):
            continue
        j = 0
        while True:
            p = l.find("%", j)
            if p < 0:
                break
            if p > 0 and l[p - 1] == "\\":
                j = p + 1
                continue
            raise AssertionError("%s 第%d行未转义 %%: %s" % (ch, i + 1, l))
    # 自带标题唯一性（章内）+ 全骨架区不重名
    seen = {}
    for i, l in enumerate(body.split("\n")):
        m = H.match(l)
        if m and m.group(1) in ("section", "subsection"):
            t = m.group(2).strip()
            seen.setdefault(t, 0)
            seen[t] += 1
            cnt = len(titles.get((m.group(1), t), []))
            assert cnt == 0, "%s 内新标题 %s(%s) 与骨架区既有标题重名" % (ch, t, m.group(1))
    dup = [t for t, c in seen.items() if c > 1]
    assert not dup, "%s 内标题重复: %s" % (ch, dup)
    # 英文词检查（书目章豁免；术语表仅豁免括号内）
    if ch not in EN_CHECK_EXEMPT:
        scan = body
        if ch in EN_CHECK_PAREN_OK:
            scan = re.sub(r"（[^）]*）", "", body)   # 去掉中文全角括号内的内容
        for m in re.finditer(r"(?<![A-Za-z\\{])([A-Za-z]{3,})(?![A-Za-z}])", scan):
            w = m.group(1)
            if w in ALLOW_EN:
                continue
            if re.match(r"^[A-Za-z]*(col|title|font|rule|skin|arc|width|height)[A-Za-z]*$", w):
                continue
            if w in ("pink", "white", "black", "red", "blue", "green"):
                continue
            raise AssertionError("%s 疑似混入英文词: %s" % (ch, w))
print("  [OK] %d 章内容通过（%d 行）" % (len(APX), sum(len(v.split("\n")) for v in APX.values())))

# ── 预演插入（倒序）──
out = list(lines)
for ln, ch in sorted(plan, key=lambda x: -x[0]):
    body = APX[ch].split("\n")
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    out[ln:ln] = [""] + body

new_text = "\n".join(out)
print()
print("=== 预演统计 ===")
print("  原行数 %d -> 新行数 %d（净增 %d）" % (len(lines), len(out), len(out) - len(lines)))
bd = raw.count("{") - raw.count("}")
nd = new_text.count("{") - new_text.count("}")
print("  花括号 delta: %d -> %d" % (bd, nd))
assert bd == nd, "花括号净值被改变"

n_old = out.index("\\part{old}")
print("  旧区逐字一致:", lines[OLD_IDX:] == out[n_old:])
assert lines[OLD_IDX:] == out[n_old:]

old_c = {}
for l in lines:
    old_c[l] = old_c.get(l, 0) + 1
new_c = {}
for l in out:
    new_c[l] = new_c.get(l, 0) + 1
removed = {k: v - new_c.get(k, 0) for k, v in old_c.items() if v - new_c.get(k, 0) > 0}
print("  删除行种类:", len(removed))
for k, v in list(removed.items())[:10]:
    print("    - [x%d] %s" % (v, k[:80]))

if MODE == "dry-run":
    print()
    print("DRY-RUN 完成，未写盘。")
else:
    io.open(F, "w", encoding="utf-8", newline="").write(new_text)
    print()
    print("已写盘: %s  %d 行 %d 字节" % (F, len(out), len(new_text.encode("utf-8"))))
