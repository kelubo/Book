# -*- coding: utf-8 -*-
"""r74 执行器：把数据层里的小节正文插入 book.tex（插在对应 \subsection 行之后）。
用法: python _r74_apply.py <data_module> [dry-run|apply]

安全规则（沿用历轮）：
  1. 锚行逐字全等断言（防文件被外部改动）
  2. 内容不含标题行（防重复标题）
  3. 内容洁净度：无 **、无未转义 %、花括号净 0
  4. 旧区 \part{old} 起逐字一致
  5. 幂等：若某小节已在文件中出现正文（锚行后紧跟空行+非空行），跳过
"""
import io, sys, importlib, re
sys.stdout.reconfigure(encoding="utf-8")

MOD_NAME = sys.argv[1]
MODE = sys.argv[2] if len(sys.argv) > 2 else "dry-run"
assert MODE in ("dry-run", "apply"), MODE

mod = importlib.import_module(MOD_NAME)
NEW = mod.NEW

F = "book.tex"
raw = io.open(F, encoding="utf-8", newline="").read()
assert raw.count("\r\n") == 0, "book.tex 应为纯 LF"
lines = raw.split("\n")

H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{(.*)\}\s*(%.*)?$")
OLD_IDX = next(i for i, l in enumerate(lines)
               if H.match(l) and H.match(l).group(1) == "part" and H.match(l).group(2) == "old")

# ── 定位每个待写小节的锚行（骨架区内，顶格 \subsection）──
# key 支持三种写法（分隔符 "|"）：
#   "小节标题"                  —— 全骨架区唯一时可用，取文档序最前匹配
#   "章标题|小节标题"            —— 章内唯一时可用
#   "章标题|节标题|小节标题"      —— 重名最严重时使用，可精确到节
KEYSEP = "|"
POS = {}          # key -> 行号(1-based)
RESOLVED = {}     # key -> 实际小节标题（用于打印与幂等）

# 扫描全部标题行号，供分层定位用
kind_at = {}      # (kind, 标题) -> [行号]
for i in range(OLD_IDX):
    m = H.match(lines[i])
    if m:
        kind_at.setdefault((m.group(1), m.group(2).strip()), []).append(i + 1)

chaplines = sorted(l for (k, _), v in kind_at.items() if k == "chapter" for l in v)
seclines = sorted(l for (k, _), v in kind_at.items() if k == "section" for l in v)


def span_of(kind, title, outer=None):
    """返回 (lo, hi)；outer 为 (lo, hi) 时限定在外层区间内。"""
    v = kind_at.get((kind, title), [])
    if outer:
        v = [l for l in v if outer[0] < l < outer[1]]
    assert len(v) == 1, "%s 标题 %s 命中 %d 处（应恰好 1 处）" % (kind, title, len(v))
    start = v[0]
    sib = chaplines if kind == "chapter" else seclines
    nxt = [l for l in sib if l > start]
    if outer:
        nxt = [l for l in nxt if l < outer[1]]
    return start, (nxt[0] if nxt else (outer[1] if outer else OLD_IDX + 1))


for key in NEW:
    parts = [p.strip() for p in key.split(KEYSEP)]
    if len(parts) == 1:
        if key in kind_at.get(("subsection", key), []):
            pass
        loc = kind_at.get(("subsection", parts[0]), [])
        if loc:
            POS[key] = loc[0]
            RESOLVED[key] = parts[0]
    elif len(parts) == 2:
        cn, st = parts
        lo, hi = span_of("chapter", cn)
        sub = [l for l in kind_at.get(("subsection", st), []) if lo < l < hi]
        assert len(sub) == 1, "章节键 %s 在章内命中 %d 处（应恰好 1 处）" % (key, len(sub))
        POS[key] = sub[0]
        RESOLVED[key] = st
    elif len(parts) == 3:
        cn, sn, st = parts
        clo, chi = span_of("chapter", cn)
        slo, shi = span_of("section", sn, (clo, chi))
        sub = [l for l in kind_at.get(("subsection", st), []) if slo < l < shi]
        assert len(sub) == 1, "章节节键 %s 在节内命中 %d 处（应恰好 1 处）" % (key, len(sub))
        POS[key] = sub[0]
        RESOLVED[key] = st
    else:
        raise AssertionError("key 层级过多: %s" % key)

# 重名标题 -> 该标题在骨架区的全部行号（用于歧义告警）
ALLLOC = {}
for i in range(OLD_IDX):
    m = H.match(lines[i])
    if m and m.group(1) == "subsection":
        ALLLOC.setdefault(m.group(2).strip(), []).append(i + 1)

print("=== 校验 1：锚行定位 ===")
missing = [t for t in NEW if t not in POS]
for t in missing:
    print("  [X] 未定位:", t)
print("  目标 %d 个，定位 %d 个，缺失 %d 个" % (len(NEW), len(POS), len(missing)))
assert not missing, "有标题未在骨架区定位到"

# 歧义告警：无前缀且标题在全骨架区出现多次 => 有误命中风险
sub_at = {t: v for (k, t), v in kind_at.items() if k == "subsection"}
amb = {t: sub_at[t] for t in NEW
       if KEYSEP not in t and t in sub_at and len(sub_at[t]) > 1}
if amb:
    print("  [!] 重名且未加前缀 %d 个（取文档序最前行号，注意核对）:" % len(amb))
    for t in sorted(amb, key=lambda x: amb[x][0]):
        print("      %-24s 行号 %s" % (t, amb[t]))

# ── 校验 2：锚行逐字 + 是否已有正文（幂等）──
print()
print("=== 校验 2：锚行逐字 + 已有正文检测 ===")
plan = []
already = []
for t, ln in sorted(POS.items(), key=lambda x: x[1]):
    st = RESOLVED[t]
    anchor = "\\subsection{%s}" % st
    actual = lines[ln - 1].strip()
    if actual != anchor:
        # 允许行尾带注释
        if not actual.startswith(anchor):
            print("  [X] L%d 锚行不符: |%s|" % (ln, actual))
            raise AssertionError("锚行不符 L%d" % ln)
    # 检查是否已插入正文：锚行之后跳过空行与注释行，若遇非空非注释行则已有正文
    j = ln
    while j < OLD_IDX and (not lines[j].strip() or lines[j].strip().startswith("%")):
        j += 1
    if j < OLD_IDX and not lines[j].startswith("\\"):
        already.append(t)
    else:
        plan.append((ln, t))
print("  待插入 %d 个，已有正文（跳过）%d 个" % (len(plan), len(already)))
for t in already[:10]:
    print("    - 跳过:", t)
if already:
    print("    [!] 出现跳过通常意味着该标题的'文档序最前空槽'已被填，本批目标槽不是它。")
    print("        请改用 '章标题|小节标题' 形式的 key 精确锁定。")

# ── 校验 3：内容洁净度 ──
# 允许出现的英文词（专有名词、缩写、命令名等白名单）
ALLOW_EN = set("""
STI STD HIV AIDS HPV HSV HBV HCV WHO COVID PrEP PEP CD4 RNA DNA
DAA IUD PID VCT TPPA RPR VDRL HBsAg HBs anti HBeAg
Masters Johnson
SSRI SNRI ADHD PDE MAOI TCA SGLT GLP
PLISSIT AASECT ESSM LGBTQ CBT BDSM SSC RACK ICD DSM
Permission Limited Information Specific Suggestions Intensive Therapy
Bondage Discipline Dominance Submission Sadism Masochism
Risk Aware Consensual Kink Safe Sane
sensate focus sex therapy
rRNA ATP DNA RNA NAD mRNA ROS
""".split())
# LaTeX 命令名 / tcolorbox 参数键（不是"混入的英文词"）
ALLOW_LATEX = set("""
itemize enumerate item textbf textit emph keyword texttt center flushleft
tcolorbox tcbox begin end hspace vspace par smallskip medskip bigskip
textbf title colback colframe colbacktitle coltitle fonttitle boxrule
arc rounded corners width height breakable left right top bottom
separator enhanced skin sharpish title
""".split())
print()
print("=== 校验 3：内容洁净度 ===")
for t in NEW:
    v = NEW[t]
    assert "**" not in v, t + " 含 **"
    assert not v.lstrip().startswith("\\subsection"), t + " 内容自带标题行！"
    assert not v.lstrip().startswith("\\section"), t + " 内容自带 section 标题！"
    d = v.count("{") - v.count("}")
    assert d == 0, "%s 花括号不配平 delta=%d" % (t, d)
    # 非法控制字符（r74 教训：0x1C 混入导致 xelatex "invalid character"）
    for ch in v:
        o = ord(ch)
        if (o < 32 and ch != "\n") or o == 127 or 0x80 <= o <= 0x9F:
            raise AssertionError("%s 含非法控制字符 U+%04X" % (t, o))
    # 混入的英文单词（r74 教训：正文里残留 "imagined" 这类未翻译词）
    for m in re.finditer(r"(?<![A-Za-z\\{])([A-Za-z]{3,})(?![A-Za-z}])", v):
        w = m.group(1)
        if w in ALLOW_EN or w in ALLOW_LATEX:
            continue
        # tcolorbox 参数键：形如 键名=值 且键名含 col/title/font 等（如 colback=pink!5!white）
        if re.match(r"^[A-Za-z]*(col|title|font|rule|skin|arc|width|height)[A-Za-z]*$", w):
            continue
        if w.startswith("col") or w.endswith("title"):
            continue
        # xcolor 颜色名 / 混合表达式里的颜色词
        if w in ("pink","white","black","red","blue","green","gray","grey","yellow",
                 "orange","purple","brown","cyan","magenta","teal","violet","lime",
                 "olive","navy","maroon","light","dark","lightgray","darkgray"):
            continue
        raise AssertionError("%s 疑似混入英文词: %s（若为专有名词请加入 ALLOW_EN）" % (t, w))
    # 行首孤立反斜杠控制序列（如 \r 被解释成回车）
    for i, l in enumerate(v.split("\n")):
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
            raise AssertionError("%s 第%d行未转义 %%: %s" % (t, i + 1, l))
    # 列表环境首行必须是 \item（r74 教训：首行漏写 \item → "missing \item" 报错；
    # 注意 \item 之后的续行是合法的，不能一律禁止）
    depth = 0
    started = False
    for i, l in enumerate(v.split("\n")):
        s = l.strip()
        if re.match(r"^\\begin\{(itemize|enumerate)\}", s):
            depth += 1
            if depth == 1:
                started = False
            continue
        if re.match(r"^\\end\{(itemize|enumerate)\}", s):
            depth = max(0, depth - 1)
            continue
        if depth > 0 and s and not s.startswith("%"):
            if not started and not s.startswith("\\item"):
                raise AssertionError("%s 第%d行列表首行缺 \\item: %s" % (t, i + 1, s[:60]))
            started = True
print("  [OK] %d 条内容全部通过（%d 行）" % (len(NEW), sum(len(v.split("\n")) for v in NEW.values())))

# ── 预演插入 ──
out = list(lines)
for ln, t in sorted(plan, key=lambda x: -x[0]):
    body = NEW[t].split("\n")
    # 裁首尾空行
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

# 旧区一致
n_old = out.index("\\part{old}")
print("  旧区逐字一致:", lines[OLD_IDX:] == out[n_old:])
assert lines[OLD_IDX:] == out[n_old:]

# 正文行多重集：新增行必须都来自 NEW
old_c = {}
for l in lines:
    old_c[l] = old_c.get(l, 0) + 1
new_c = {}
for l in out:
    new_c[l] = new_c.get(l, 0) + 1
removed = {k: v - new_c.get(k, 0) for k, v in old_c.items() if v - new_c.get(k, 0) > 0}
print("  删除行种类:", len(removed), "（应只含空行与骨架注释）")
for k, v in list(removed.items())[:10]:
    print("    - [x%d] %s" % (v, k[:80]))

if MODE == "dry-run":
    print()
    print("DRY-RUN 完成，未写盘。")
else:
    io.open(F, "w", encoding="utf-8", newline="").write(new_text)
    print()
    print("已写盘: %s  %d 行 %d 字节" % (F, len(out), len(new_text.encode("utf-8"))))
