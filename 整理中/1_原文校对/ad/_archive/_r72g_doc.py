# -*- coding: utf-8 -*-
"""r72 文档生成：
  1. _r72_三卷目录分工总表_2026-09-22.md   —— 分工原则 + 逐项调整明细 + 三卷三层目录
  2. _r72_book目录_完整版_2026-09-22.md    —— book.tex 四层完整目录（替代 r69 版）
"""
import io
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
T = re.compile(r"\\(part|chapter|section|subsection)\*?\{([^{}]*)\}")
IND = {"part": "", "chapter": "\u3000\u3000", "section": "\u3000\u3000\u3000\u3000",
       "subsection": "\u3000\u3000\u3000\u3000\u3000\u3000"}


def skeleton(fn, start_anchor, end_kw):
    raw = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n")
    lines = raw.split("\n")
    si = next(i for i, l in enumerate(lines) if l.strip() == start_anchor)
    ei = next(i for i, l in enumerate(lines) if end_kw in l and l.strip().startswith("\\part"))
    ents, dead = [], False
    for i in range(si + 1, ei):
        s = lines[i].strip()
        if s.startswith("\\iffalse"):
            dead = True
        if s.startswith("%"):
            continue
        col0 = lines[i].startswith("\\")          # 骨架标题顶格；缩进的是正文标题
        m = T.match(s)
        if m:
            ents.append((m.group(1), m.group(2).strip(), dead, col0))
    return ents


book = skeleton("book.tex", "\\mainmatter", "\\part{old}")
fem = skeleton("female.tex", "\\mainmatter", "原始内容")
mal = skeleton("male.tex", "\\listoftables", "原始内容")


def count(ents, only_live=True):
    c = {}
    for k, _, dead, col0 in ents:
        if only_live and (dead or not col0):
            continue
        c[k] = c.get(k, 0) + 1
    return c


bkc, fcc, mlc = count(book), count(fem), count(mal)


def render(ents, maxlv=("part", "chapter", "section"), show_dead=False):
    """ents 为 4 元组序列；本函数只渲染标题。带跨卷标记的注释请在第二遍扫描里补。"""
    out = []
    cur_dead = False
    for k, t, dead, col0 in ents:
        if k not in maxlv:
            continue
        if dead and not show_dead:
            if not cur_dead:
                out.append("\u3000\u3000*（以下为 `\\iffalse` 停用区内的迁移过渡记录，不进目录 / 不编译）*")
                cur_dead = True
            continue
        out.append(IND[k] + t)
    out.append("")
    return out


MARKER = re.compile(r"^(⇒|⇐|分工|·|\[|移入|去重|合并|说明|注|注意|可选|改名|前移|降级|框架|待写)")


def render2(fn, anchor, endkw, maxlv=("part", "chapter", "section"), marks=True):
    """带跨卷标记的渲染：标题顶格列出，注释块按源码顺序以 › 缩进列出（仅列「有信息量」的块）。"""
    raw = io.open(os.path.join(BASE, fn), encoding="utf-8", newline="").read().replace("\r\n", "\n")
    lines = raw.split("\n")
    si = next(i for i, l in enumerate(lines) if l.strip() == anchor)
    ei = next(i for i, l in enumerate(lines) if endkw in l and l.strip().startswith("\\part"))
    out, dead, buf = [], False, []

    def tidy(c):
        b = re.sub(r"^%\s*", "", c)
        if b.startswith("框架成稿"):
            return "框架成稿（停用框架区已有本节成稿）"
        b = b.replace("（原始内容区，按标题搜索）", "（原始内容区）")
        return b

    def flush():
        if not buf or not marks:
            buf.clear()
            return
        if MARKER.match(re.sub(r"^%\s*", "", buf[0])):
            seen = set()
            for c in buf:
                t = tidy(c)
                if t in seen:
                    continue
                seen.add(t)
                out.append("\u3000\u3000\u3000\u3000› " + t)
        buf.clear()

    for i in range(si + 1, ei):
        s = lines[i].strip()
        if s.startswith("\\iffalse"):
            flush()
            dead = True
            out.append("")
            out.append("*（以下为 `\\iffalse` 停用区内的迁移过渡记录，不进目录 / 不编译）*")
            continue
        if s.startswith("%"):
            buf.append(s)
            continue
        if not s:
            flush()
            continue
        m = T.match(s)
        if not m:
            continue
        if m.group(1) not in maxlv:
            buf.clear()
            continue
        flush()
        if not dead:
            out.append(IND[m.group(1)] + m.group(2).strip())
    flush()
    out.append("")
    return out


# ══════════════════ 文档 1 ══════════════════
d = []
w = d.append
w("# 三卷目录分工总表（book / female / male）")
w("")
w("> 日期：2026-09-22　｜　路径：`整理中/1_原文校对/ad/`　｜　轮次：r72")
w("> 本表说明三卷目录如何按「侧重点」切分、互不重复，并逐项列出跨卷转移。")
w("")

w("## 一、分工原则")
w("")
w("1. **三卷按读者性别定位分工**，同一章/节只出现在一卷的目录里：")
w("   - `book.tex` ＝ **两性共通卷**：共通的生理与心理、关系与技巧、STI、避孕、社会文化法律、教育、结语、附录。")
w("   - `female.tex` ＝ **女性专属卷**：女性解剖、月经、妇科疾病、女性性功能、生育与产后、更年期、妇科检查与手术、中医妇科。")
w("   - `male.tex` ＝ **男性专属卷**：男性解剖、男性性功能与男科疾病、男性保健与筛查、男性生殖器手术、中医男科。")
w("2. **凡性别专属的章/节一律归对应分卷**；`book.tex` 原位只留一行 `% ⇒ [已移出] …` 标记，指明去向，便于追溯。")
w("3. **分卷接收处在标题下标注 `% ⇐ book.tex`**，标明「这一节是从 book.tex 移来的」。")
w("4. **确实属于两性共通、但分卷里也出现过同名内容**（如技法、依恋、中医通论、生殖器常识），统一收敛到 `book.tex`，分卷只留 `% ⇒ [统一] …` 标记，不重复设节。")
w("5. **旧内容一律未动**：三卷 `\\part{old}` / `\\part*{原始内容}` 及其后的原有正文逐字保留，只在新目录与旧内容之间加了分隔。")
w("")

w("## 二、三卷规模（只统计新目录骨架区）")
w("")
w("| 卷 | 定位 | 篇 | 章 | 节 | 小节 |")
w("|---|---|---|---|---|---|")
w("| `book.tex` | 两性共通 | %d | %d | %d | %d |"
  % (bkc["part"], bkc["chapter"], bkc["section"], bkc["subsection"]))
w("| `female.tex` | 女性专属 | %d | %d | %d | %d |" % (fcc["part"], fcc["chapter"], fcc["section"], fcc.get("subsection", 0)))
w("| `male.tex` | 男性专属 | %d | %d | %d | %d |" % (mlc["part"], mlc["chapter"], mlc["section"], mlc.get("subsection", 0)))
w("")
w("> `book.tex` 的「篇」含独立的「结语」「附录」两篇；分卷的小节（学习要点）层待内容迁入时再补。")
w("> `book.tex` 由 r69 的「八篇 57 章」减为「八篇 53 章」——减少的 4 章即本轮移出的性别专属章。")
w("> 表内数字只计**顶格的骨架标题**并排除 `\\iffalse` 停用区；《两性研究导论》章已有正文，")
w("> 其正文内的 3 节 / 17 小节未计入表中，但在下方目录里一并列出。")
w("")

w("## 三、跨卷调整明细")
w("")
w("### 3.1 `book.tex` 移出 / 拆分（原位留标记）")
w("")
w("| # | 原位置 | 处理 | 去向 |")
w("|---|---|---|---|")
rows = [
    ("第一篇《生殖系统》章", "改名 + 拆出两节",
     "章名改《生殖器官的个体差异与护理》，只留共通 3 节；男性生殖系统 → `male`《男性生殖系统》；女性生殖系统 → `female`《女性生殖系统》"),
    ("第二篇《性与人际关系》章", "接收", "`male` 原「依恋风格与性」节并回（两性共通）"),
    ("第三篇《性爱的多样实践》章", "接收", "`female` 原「阴交技巧与体验」「肛交技巧与体验」两节并回"),
    ("第三篇《新婚首夜》章", "接收", "`female` 原「处女开苞与初次性体验」节并回"),
    ("第五篇《避孕方法》章", "接收 + 分工",
     "`female` 原「避孕方法（女性适用）」并回；避孕通论只在 book，分卷不另设避孕章（`male` 只留「男性避孕技术新进展」）"),
    ("第五篇《孕期与产后性健康》章", "整章移出", "`female`《孕期与产后性健康》（同名章，避免两卷重复）"),
    ("第六篇《男性常见性健康问题》章", "整章移出",
     "`male`，拆为《男性性功能障碍》《性欲异常》《前列腺疾病》《男性生殖健康问题》"),
    ("第六篇《女性常见性健康问题》章", "整章移出",
     "`female`，拆入《妇科常见疾病》《女性性功能与性问题》"),
    ("第六篇《外生殖器手术与美学决策》章", "整章移出",
     "男 → `male`《男性外生殖器手术与美学决策》；女 → `female`《妇科手术与康复》"),
    ("第六篇《定期检查与筛查》章", "拆节",
     "保留共通 3 节；男性生殖健康检查 → `male`《定期检查与自检》；女性生殖健康检查 → `female`《妇科检查与筛查》"),
    ("第六篇《盆底健康与性功能》章", "拆节",
     "保留共通 4 节；男性盆底训练与射精控制 → `male`《盆底与射精控制》；女性盆底训练与性感受 → `female`《女性日常保健》"),
    ("第六篇《性与年龄》章·中年期与围绝经期", "改名 + 拆节",
     "改为《中年期的性变化》；女性围绝经期 → `female`《更年期健康管理》；男性更年期（LOH） → `male`《男性生命周期与中老年性健康》"),
    ("第六篇《传统中医与性健康》章", "分工声明", "只讲共通中医性医学理论；妇科 → `female`《中医妇科》；男科 → `male`《中医男科》"),
    ("第六篇《精神健康与性》章", "分工声明", "共通机制留 book；男性特有议题见 `male`《男性心理健康与性》"),
    ("第六篇《性与生活方式》章", "分工声明", "共通因素留 book；男性特有因素见 `male`《生活方式与性健康》"),
    ("第四篇《STI 概述与预防》章", "分工声明", "共通 STI 知识留 book；女性感染特点见 `female`《妇科常见疾病·性传播疾病——女性角度》"),
]
for i, (a, b, c) in enumerate(rows, 1):
    w("| %d | %s | %s | %s |" % (i, a, b, c))
w("")

w("### 3.2 `female.tex` 调整")
w("")
w("| # | 处理 | 说明 |")
w("|---|---|---|")
frows = [
    ("章《女性性问题与性健康》→《女性性功能与性问题》", "改名；并接收 `book`《女性常见性健康问题》的性功能各节"),
    ("新增 4 节", "女性性欲低下 / 性唤起障碍 / 阴道痉挛 / 性厌恶（`⇐ book.tex`）"),
    ("删 3 节", "阴交技巧与体验 / 肛交技巧与体验 / 处女开苞与初次性体验 → 统一至 `book`"),
    ("章《生育与避孕》→《女性生育与生殖健康》", "改名；避孕通论统一至 `book`"),
    ("删 3 节", "避孕方法（女性适用）→ `book`；生育生理与避孕、生育问题与辅助生殖技术 → 与本章其余节重复，已合并"),
    ("章《孕期与产后性健康》", "保留；新增「孕期性生理变化」节（`⇐ book.tex`）"),
    ("章《更年期健康管理》", "新增「围绝经期症状与性」节（`⇐ book.tex`）"),
    ("章《妇科检查与筛查》", "新增「女性生殖健康检查」节（`⇐ book.tex`）"),
    ("章《女性日常保健》", "「运动与盆底肌」→「运动与盆底训练」，吸收 `book` 女性盆底训练节"),
    ("章《妇科手术与康复》", "新增「女性外生殖器手术」「女性外生殖器手术的美学决策」两节（`⇐ book.tex`）"),
    ("章《中医妇科》", "删「传统中医与女性性健康」节 → 统一至 `book`《传统中医与性健康》"),
    ("删「生殖器官的个体差异与护理」节", "属两性共通常识，统一至 `book` 同名章"),
    ("篇三改名", "「生育、避孕与产后」→「生育与产后」（避孕已统一至 book）"),
]
for i, (a, b) in enumerate(frows, 1):
    w("| %d | %s | %s |" % (i, a, b))
w("")

w("### 3.3 `male.tex` 调整")
w("")
w("| # | 处理 | 说明 |")
w("|---|---|---|")
mrows = [
    ("篇章细化：4 篇 4 章 → 5 篇 12 章", "原《常见疾病》《日常保健》两章各含 13–16 节，章粒度太粗；按主题拆章"),
    ("章《常见疾病》→ 拆为 4 章", "《男性性功能障碍》《性欲异常》《前列腺疾病》《男性生殖健康问题》"),
    ("章《日常保健》→ 拆为 4 章 + 1 章", "《定期检查与自检》《生活方式与性健康》《盆底与射精控制》《男性心理健康与性》"),
    ("新增章《男性生命周期与中老年性健康》", "年龄相关的性健康变化 / 男性更年期（LOH）/ 男性骨质疏松与睾酮的关系；并接收 `book`《性与年龄》的男性更年期（`⇐ book.tex`）"),
    ("新增章《男性外生殖器手术与美学决策》", "整章 `⇐ book.tex`《外生殖器手术与美学决策》男性部分"),
    ("章《性功能障碍》→《男性性功能障碍》", "加「男性」前缀，避免与 `book`《性功能障碍》章同名"),
    ("合并两处「前列腺疾病」", "原第二篇（诊治）与第三篇（筛查）合并为一章《前列腺疾病》，5 节"),
    ("新增 2 节", "男性生殖健康检查（`⇐ book`）；男性盆底训练与射精控制（`⇐ book`）"),
    ("删 2 节", "依恋风格与性 → 统一至 `book`《性与人际关系》；传统中医与男性性健康 → 统一至 `book`《传统中医与性健康》"),
]
for i, (a, b) in enumerate(mrows, 1):
    w("| %d | %s | %s |" % (i, a, b))
w("")

w("### 3.4 三卷各有侧重、互不重复的对照")
w("")
w("| 主题 | `book.tex`（共通） | `female.tex`（女性） | `male.tex`（男性） |")
w("|---|---|---|---|")
w("| 生殖系统解剖 | 生殖器官的个体差异与护理（常识） | 女性生殖系统 | 男性生殖系统 |")
w("| 性功能障碍 | 性功能障碍（机制与治疗框架） | 女性性功能与性问题 | 男性性功能障碍 |")
w("| 常见疾病 | — | 妇科常见疾病 | 前列腺疾病等男科疾病 |")
w("| 定期检查 | 定期检查与筛查（共通框架） | 妇科检查与筛查 | 定期检查与自检 |")
w("| 盆底 | 盆底健康与性功能（解剖与评估） | 女性日常保健·运动与盆底训练 | 盆底与射精控制 |")
w("| 更年期 / 年龄 | 性与年龄（两性共通变化） | 更年期健康管理 | 男性生命周期与中老年性健康 |")
w("| 避孕 | 避孕方法（通论，含女用方式） | —（只讲女性生育生理） | 男性生殖健康问题·男性避孕技术 |")
w("| 孕期产后 | — | 孕期与产后性健康 | — |")
w("| 生殖器手术 | — | 妇科手术与康复 | 男性外生殖器手术与美学决策 |")
w("| 中医 | 传统中医与性健康（通论） | 中医妇科 | 中医男科 |")
w("| 性爱技巧 | 前戏与爱抚 / 体位与姿势 / 性爱的多样实践 | —（已统一至 book） | — |")
w("| STI | STI 全篇 | 妇科常见疾病·性传播疾病——女性角度 | — |")
w("")

w("## 四、三卷目录（三层）")
w("")
w("### 4.1 `book.tex`　两性共通卷")
w("")
w("　".replace("　", "") + "```text")
d.extend(render2("book.tex", r"\mainmatter", r"\part{old}", ("part", "chapter", "section")))
w("```")
w("")
w("### 4.2 `female.tex`　女性专属卷")
w("")
w("```text")
d.extend(render2("female.tex", r"\mainmatter", "原始内容", ("part", "chapter", "section")))
w("```")
w("")
w("### 4.3 `male.tex`　男性专属卷")
w("")
w("```text")
d.extend(render2("male.tex", r"\listoftables", "原始内容", ("part", "chapter", "section")))
w("```")
w("")

w("## 五、验证与遗留")
w("")
w("**验证口径**")
w("- 旧内容零改动：`book.tex` 的 `\\part{old}`、两卷的 `\\part*{原始内容}` 及其后内容与备份 `_backup_r72/` **逐字一致**；")
w("  锚点之前（前言与基础结构）亦逐字一致。")
w("- 只动注释与标题：`book.tex` 正文行多重集 **43023 → 43023**（消失 0 / 新增 0）。")
w("- 换行保持：`book.tex` 纯 LF；`female.tex` / `male.tex` CRLF 数 21195 → 21233、8126 → 8189（新增行同为 CRLF）。")
w("- 静态校验三卷：花括号净值 delta＝0，环境栈无错配。")
w("- 跨卷查重：章级、节级重名 **0**（脚本 `_r72h_final.py`）。")
w("- XeLaTeX 编译 **0 错误**：`book.tex` 2010 页、`female.tex` 435 页、`male.tex` 117 页。")
w("- 新增/移动的标题行由执行器逐条 log，可对照 `_r72_apply.py` 的输出复核。")
w("")
w("**遗留（待授权）**")
w("- 两卷 preamble 的 `part/name={。卷}`、`chapter/name={。章}` 是损坏格式（应为 `{第,卷}` / `{第,章}`）。")
w("  新骨架的「篇」用 `\\part*` 规避了它，但**章/节编号在编译出来的目录里会显示成「。章一」「。节1」**，已在 PDF 目录中可见，建议尽快修正。")
w("- 分卷的小节（学习要点）层尚未铺开——待内容迁入时按需补。")
w("- `book.tex` 旧区 10 个 part 名仍带编号（「第九篇　old」等），待统一去编号。")
w("- `_r70_迁移作业清单_2026-09-21.md` 的行号锚基于 r69 骨架（`\\part{old}` L2308），本轮骨架缩短 140 行，需重跑脚本刷新。")
w("")

io.open(os.path.join(BASE, "_r72_三卷目录分工总表_2026-09-22.md"), "w", encoding="utf-8", newline="\n") \
    .write("\n".join(d))
print("写 _r72_三卷目录分工总表_2026-09-22.md  %d 行" % len(d))

# ══════════════════ 文档 2：book 四层完整目录 ══════════════════
d2 = []
w = d2.append
w("# book.tex 目录框架（四层完整版）")
w("")
w("> 日期：2026-09-22（r72 三卷分工后重新生成）　｜　路径：`整理中/1_原文校对/ad/book.tex`")
w("> 本卷为「两性共通卷」；性别专属的章/节已按卷拆到 `female.tex` / `male.tex`。")
w("> 标注 `⇒`、`⇐` 的注释行即跨卷转移标记，详见《三卷目录分工总表》。")
w("")
w("```text")
d2.extend(render2("book.tex", r"\mainmatter", r"\part{old}", ("part", "chapter", "section", "subsection"), marks=False))
w("```")
io.open(os.path.join(BASE, "_r72_book目录_完整版_2026-09-22.md"), "w", encoding="utf-8", newline="\n") \
    .write("\n".join(d2))
print("写 _r72_book目录_完整版_2026-09-22.md  %d 行" % len(d2))
