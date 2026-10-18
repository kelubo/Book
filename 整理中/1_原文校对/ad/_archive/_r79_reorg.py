# -*- coding: utf-8 -*-
"""r79: 3_position.tex 结构重组 + 0_book.tex 两小节移入。

用法：
    python _r79_reorg.py dry-run    校验不改盘
    python _r79_reorg.py apply      备份后写盘

原则：
  1) 移动的正文行（非空/非注释/非标题）一条不丢（multiset 断言）；
  2) 标题行变化全部可枚举（改名/降级/删 old 与空节）；
  3) 新增正文仅限新写块（导语/男性前戏反应/Aftercare/边界导语）+ 自 0_book 移入的两节。
"""
import io, os, re, sys, shutil, time, collections

DIR = os.path.dirname(os.path.abspath(__file__))
MODE = sys.argv[1] if len(sys.argv) > 1 else "dry-run"

P_POS = os.path.join(DIR, "3_position.tex")
P_BOOK = os.path.join(DIR, "0_book.tex")

TITLE = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{")
LVL = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}

def read_lines(path):
    raw = io.open(path, encoding="utf-8", newline="").read()
    assert "\r" not in raw, path + " 应为纯 LF"
    return raw.split("\n")

def find_one(lines, pat, what):
    hits = [i for i, ln in enumerate(lines) if re.match(pat, ln)]
    assert len(hits) == 1, "锚「%s」命中 %d 处（应为 1）: %s" % (what, len(hits), [lines[i] for i in hits[:3]])
    return hits[0]

def block_end(lines, start, level):
    n = LVL[level]
    for j in range(start + 1, len(lines)):
        m = TITLE.match(lines[j])
        if m and LVL[m.group(1)] <= n:
            return j
    return len(lines)

def insert_after_title(lines, anchor_pat, what, block):
    i = find_one(lines, anchor_pat, what)
    return lines[:i + 1] + block + lines[i + 1:]

def insert_before(lines, anchor_pat, what, block):
    i = find_one(lines, anchor_pat, what)
    return lines[:i] + block + lines[i:]

def demote(block):
    out = []
    for ln in block:
        if re.match(r"^\\subsection\*?\{", ln):
            ln = ln.replace("\\subsection", "\\subsubsection", 1)
        out.append(ln)
    out2 = []
    for ln in out:
        if re.match(r"^\\section\*?\{", ln):
            ln = ln.replace("\\section", "\\subsection", 1)
        out2.append(ln)
    return out2

def body_counter(lines):
    c = collections.Counter()
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("%") or TITLE.match(ln):
            continue
        c[ln] += 1
    return c

def txt_body(text):
    return body_counter(text.strip().split("\n"))

# ---------- 新写文本 ----------
MALE_FOREPLAY = r"""\section{男性前戏反应与敏感带}

前戏并不是单方面为伴侣"做准备"的过程，男性自身同样需要被唤起、被探索。理解男性的反应节奏与身体敏感带，可以让前戏真正成为双方共同的事。

男性的唤起标志是阴茎勃起，但勃起并非"全有或全无"——在紧张、疲劳、饮酒或分心的状态下，勃起可能反复出现和消退，这属于正常现象，并不等于失去兴趣。把勃起程度的波动视为身体状态的晴雨表，而不是"表现"的评分，能显著减轻双方的焦虑。

男性的敏感带并不局限于生殖器。冠状沟与系带是阴茎上感觉最密集的区域；阴囊皮肤与会阴（肛门与阴囊之间的区域）对轻柔的触压也很敏感；此外，乳头、耳后、颈侧、大腿内侧等部位同样分布着大量触觉感受器。爱抚这些区域时，力度由轻到重、节奏由慢到快，通常比直接且持续的强刺激更容易积累兴奋。

节奏控制是前戏中男性最实用的技巧之一。按照性反应周期的模型，男性在平台期若感到接近射精的临界点，可以放慢动作、更换刺激方式或短暂停顿，让兴奋水平回落后再继续。这种"走走停停"的练习不仅有助于延长性行为的时间，也让双方对彼此的身体节律建立更细致的了解。

最后需要澄清一个常见误区：男性并非"随时可以、无需准备"。充分的唤起时间、足够的润滑和心理上的放松，对男性同样重要——润滑不足会造成包皮与黏膜的不适甚至微小损伤，而心理紧张则可能通过交感神经的兴奋直接干扰勃起与射精控制。把前戏当作双方共同享受的过程，而非进入前的"手续"，是更健康也更现实的心态。"""

AFTERCARE = r"""\chapter{拥抱与情感交流（Aftercare）}

亲密行为结束后的拥抱、交谈与照顾，在英文里被称为 Aftercare（事后照顾）。这个概念最早来自 BDSM 社群——强调高强度活动结束后必须有一段安抚期；但对普通伴侣而言，它同样是值得学习的实践：性高潮之后的几分钟，是关系里少有的"双方都卸下防备"的时刻，用得好，它对亲密感的滋养不亚于性行为本身。

\section{为什么事后温存如此重要}

从生理上看，男性和女性在高潮后进入消退期的速度并不同步。男性在射精后因催乳素升高而普遍感到困倦与放松，出现"事后只想睡"的倾向；而女性的消退较为平缓，且在持续刺激下可以再次进入平台期，因此往往更期待延续身体的亲密。这种节奏差如果没有被理解，很容易变成"他转身就睡、她心里失落"的隔阂。事后温存的意义，正是给这段节奏差一个缓冲：让快的一方慢下来，陪慢的一方走完回落的过程。

从情感上看，性行为后是心理防御最低的时刻。此时的一个拥抱、一句肯定，传递的安全感远超日常言语；反之，立刻翻身看手机、起身离开，则可能被解读为"对方只要性、不要我"。大量伴侣咨询的案例显示，事后几分钟的态度，会影响双方对整个性经历的满意度评价。

\section{身体层面的照顾}

事后的身体照顾并不复杂：一起休息几分钟后起身排尿（尤其对女性，有助于预防尿路感染），补充一小杯水，用温水清洁外阴与生殖器；若使用了情趣用品或安全套，及时清理与收纳；出汗较多时换一套干爽的床品，避免着凉。这些动作本身就是照顾的表达，不必被视为扫兴的"收尾工序"。

\section{情感层面的照顾}

情感层面的温存更简单，也更容易被忽略：

\begin{itemize}
  \item \keyword{保持身体接触}：拥抱、依偎、轻抚后背或头发，持续几分钟而不是几秒钟；
  \item \keyword{说几句肯定的话}："刚才很好""我喜欢你现在的样子"，具体的肯定比沉默更让人安心；
  \item \keyword{轻量交谈}：聊聊刚才的感受、聊聊无关紧要的日常，让情绪平稳回落；
  \item \keyword{避免立即抽离}：不马上看手机、起身工作或评价表现，若有事必须离开，先说明并给出补偿性的亲密动作。
\end{itemize}

事后温存没有标准流程，它的核心只有一件事：让双方都感到"这段经历被珍视"。随着彼此了解加深，每对伴侣都会形成自己的事后仪式。"""

BOUNDARY_INTRO = r"""同意与边界是一切亲密行为的底线，也是高质量性生活的前提。本章从实践角度讨论：如何表达与确认同意、如何沟通各自的偏好与边界。这些内容与技术同样重要——技巧决定体验的上限，而同意与边界决定关系的安全感。"""

CORE_INTRO = r"""本章聚焦各类性行为的核心技巧，涵盖阴交、肛交、口交与非插入式行为。技巧的目标是增进双方的舒适与愉悦，而非追求难度或数量；所有实践都应以自愿、安全、卫生为前提，出现疼痛或不适时应立即停止并调整。"""

AIDS_INTRO = r"""多样化的实践方式与情趣用品可以为性生活增添新的可能，前提是了解各自的安全须知、正确的使用与清洁方法，并对彼此的边界保持尊重。本章先概述常见实践形式的要点，再介绍情趣玩具的选购、使用与养护。"""

# 预期新增正文（供 apply 断言）
EXPECTED_NEW = (txt_body(MALE_FOREPLAY) + txt_body(AFTERCARE) + txt_body(BOUNDARY_INTRO)
                + txt_body(CORE_INTRO) + txt_body(AIDS_INTRO))

def reorganize():
    lines = read_lines(P_POS)
    src_body = body_counter(lines)

    def rm_line(lines, pat, what):
        i = find_one(lines, pat, what)
        return lines[:i] + lines[i + 1:]

    def move(lines, src_pat, src_what, src_level, dst_fn, new_title=None, dem=False, dem_ch=False):
        i = find_one(lines, src_pat, src_what)
        e = block_end(lines, i, src_level)
        blk = lines[i:e]
        lines = lines[:i] + lines[e:]
        if dem_ch:
            assert blk[0].startswith("\\chapter"), blk[0]
            tm = re.match(r"^\\chapter\*?\{(.*)\}\s*$", blk[0])
            tname = tm.group(1)
            # 块内（首行之外）与章同名的 \section 行 → 删除（块内其余正文直接挂在节下）
            for k in range(1, len(blk)):
                if re.match(r"^\\section\*?\{%s\}\s*$" % re.escape(tname), blk[k]):
                    del blk[k]
                    break
            blk[0] = blk[0].replace("\\chapter", "\\section", 1)
        if new_title:
            blk[0] = re.sub(r"\{.*\}\s*$", "{%s}" % new_title, blk[0])
        if dem:
            blk = demote(blk)
        return dst_fn(lines, blk)

    # ===== A. 删 12 个 old 残留行（逐个循环删，直到删净） =====
    n_old = 0
    while True:
        hits = [i for i, ln in enumerate(lines) if re.match(r"^\\(?:sub)?section\{old\}$", ln)]
        if not hits:
            break
        i = hits[0]
        lines = lines[:i] + lines[i + 1:]
        n_old += 1
    assert n_old == 12, "old 行应恰为 12 个，实删 %d" % n_old

    # ===== B. 删全部空壳节行（移块前，避免重名冲突） =====
    for t in ["前戏的重要性与身心反应", "前戏的时机与节奏掌控", "节奏、主导权与伴侣互动",
              "呼吸、吟叫与身体扭动", "女性高潮的多样性",
              "身体敏感带探索", "爱抚的手技与口技", "情欲按摩与感官唤醒", "亲密技法进阶",
              "阴交技巧详解", "肛交技巧详解", "口交与性健康", "非插入式性行为",
              "情趣玩具与用品的使用与安全", "性爱的多样实践"]:
        lines = rm_line(lines, r"^\\section\{%s\}$" % re.escape(t), "空节「%s」" % t)

    # ===== C. 第三篇重组 =====
    # 逆序插到章标题后，最终顺序：阴交→肛交→口交→非插入式
    lines = move(lines, r"^\\chapter\{非插入式性行为与情趣用品\}$", "章·非插入式", "chapter",
                 lambda L, b: insert_after_title(L, r"^\\chapter\{性爱核心技巧\}$", "章·性爱核心技巧", b),
                 dem_ch=True)
    lines = move(lines, r"^\\chapter\{口交与性健康\}$", "章·口交", "chapter",
                 lambda L, b: insert_after_title(L, r"^\\chapter\{性爱核心技巧\}$", "章·性爱核心技巧", b),
                 dem_ch=True)
    lines = move(lines, r"^\\chapter\{肛交技巧详解\}$", "章·肛交", "chapter",
                 lambda L, b: insert_after_title(L, r"^\\chapter\{性爱核心技巧\}$", "章·性爱核心技巧", b),
                 dem_ch=True)
    lines = move(lines, r"^\\chapter\{阴交技巧详解\}$", "章·阴交", "chapter",
                 lambda L, b: insert_after_title(L, r"^\\chapter\{性爱核心技巧\}$", "章·性爱核心技巧", b),
                 dem_ch=True)
    lines = move(lines, r"^\\chapter\{性爱的多样实践\}$", "章·多样实践", "chapter",
                 lambda L, b: insert_after_title(L, r"^\\chapter\{情趣辅助与多元探索\}$", "章·情趣辅助", b),
                 dem_ch=True, dem=True)
    lines = move(lines, r"^\\section\{性玩具的使用与安全\}$", "节·性玩具", "section",
                 lambda L, b: insert_before(L, r"^\\part\{性交体位与姿势\}$", "part·体位", b),
                 new_title="情趣玩具与用品的使用与安全")
    lines = move(lines, r"^\\section\{情趣用品与辅助工具\}$", "节·情趣用品辅助", "section",
                 lambda L, b: insert_before(L, r"^\\part\{性交体位与姿势\}$", "part·体位", b))
    lines = move(lines, r"^\\section\{使用安全与清洁\}$", "节·使用安全", "section",
                 lambda L, b: insert_before(L, r"^\\part\{性交体位与姿势\}$", "part·体位", b))
    lines = move(lines, r"^\\section\{性敏感部位\}$", "节·性敏感部位", "section",
                 lambda L, b: insert_before(L, r"^\\chapter\{前戏中的生理反应与高潮铺垫\}$", "章·生理反应", b))
    lines = move(lines, r"^\\section\{亲吻与抚摸\}$", "节·亲吻抚摸", "section",
                 lambda L, b: insert_before(L, r"^\\chapter\{前戏中的生理反应与高潮铺垫\}$", "章·生理反应", b))
    lines = rm_line(lines, r"^\\chapter\{性玩具的使用与安全\}$", "章·性玩具标题")
    # 章导语（新增正文）：插在章标题行后
    i = find_one(lines, r"^\\chapter\{性爱核心技巧\}$", "章·性爱核心技巧")
    lines[i + 1:i + 1] = ["", CORE_INTRO]
    i = find_one(lines, r"^\\chapter\{情趣辅助与多元探索\}$", "章·情趣辅助")
    lines[i + 1:i + 1] = ["", AIDS_INTRO]

    # ===== D. 第二篇重组 =====
    lines = move(lines, r"^\\section\{前戏的重要性\}$", "节·前戏重要性", "section",
                 lambda L, b: insert_after_title(L, r"^\\chapter\{前戏的认知与氛围营造\}$", "章·前战认知", b),
                 new_title="前戏的重要性与身心反应")
    lines = move(lines, r"^\\section\{前戏的方式和技巧\}$", "节·前戏方式", "section",
                 lambda L, b: insert_after_title(L, r"^\\section\{前戏的重要性与身心反应\}$", "节·前戏重要性(新)", b),
                 new_title="前戏的时机与节奏掌控")
    lines = move(lines, r"^\\section\{节奏与主导权\}$", "节·节奏主导权", "section",
                 lambda L, b: insert_after_title(L, r"^\\section\{前戏的时机与节奏掌控\}$", "节·前戏时机(新)", b),
                 new_title="节奏、主导权与伴侣互动")
    lines = move(lines, r"^\\section\{吟叫与扭动\}$", "节·吟叫扭动", "section",
                 lambda L, b: insert_after_title(L, r"^\\chapter\{前戏中的生理反应与高潮铺垫\}$", "章·生理反应", b),
                 new_title="呼吸、吟叫与身体扭动")
    lines = move(lines, r"^\\section\{女性高潮的多样性与阴蒂\}$", "节·女性高潮", "section",
                 lambda L, b: insert_after_title(L, r"^\\section\{呼吸、吟叫与身体扭动\}$", "节·吟叫扭动(新)", b),
                 new_title="女性高潮的多样性")
    # 核心爱抚技法 4 节改名
    for old_t, new_t in [("敏感区域的爱抚技巧", "身体敏感带探索"),
                         ("爱抚的手技", "爱抚的手技与口技"),
                         ("情欲按摩与感官按摩", "情欲按摩与感官唤醒"),
                         ("爱抚与亲密技法", "亲密技法进阶")]:
        i = find_one(lines, r"^\\section\{%s\}$" % re.escape(old_t), "节·" + old_t)
        lines[i] = "\\section{%s}" % new_t
    # 男性前戏反应：空节行替换为新写整节
    i = find_one(lines, r"^\\section\{男性前戏反应与敏感带\}$", "节·男性前戏")
    lines[i:i + 1] = MALE_FOREPLAY.split("\n")

    # ===== E. 体位篇：找回被切走的节 =====
    for t in ["侧卧位", "后入式体位", "女上男下体位", "传教士体位（男上女下）"]:
        lines = move(lines, r"^\\section\{%s\}$" % re.escape(t), "节·" + t, "section",
                     lambda L, b: insert_before(L, r"^\\section\{坐位与站位\}$", "节·坐位站位", b))
    for t in ["后入式的变体", "女上位的变体", "传教士体位的变体"]:
        lines = move(lines, r"^\\section\{%s\}$" % re.escape(t), "节·" + t, "section",
                     lambda L, b: insert_before(L, r"^\\section\{组合式体位\}$", "节·组合式", b))
    lines = move(lines, r"^\\section\{第一次的身心调适\}$", "节·第一次身心调适", "section",
                 lambda L, b: insert_before(L, r"^\\part\{前戏与爱抚\}$", "part·前戏", b))

    # ===== F. 事后温存 + 安全与应对 =====
    lines = move(lines, r"^\\section\{性爱前后的清洁与准备\}$", "节·清洁准备", "section",
                 lambda L, b: insert_after_title(L, r"^\\chapter\{事后清洁与身体护理\}$", "章·事后清洁", b))
    lines = move(lines, r"^\\section\{性交后的不适与处理\}$", "节·性交后不适", "section",
                 lambda L, b: insert_after_title(L, r"^\\chapter\{疲惫与不适的应对\}$", "章·疲惫不适", b))
    # Aftercare：空章行替换为新写整章
    i = find_one(lines, r"^\\chapter\{拥抱与情感交流（Aftercare）\}$", "章·Aftercare")
    lines[i:i + 1] = AFTERCARE.split("\n")

    # ===== G. 0_book 侧切出两小节；边界章 = 导语 + 两节 =====
    blines = read_lines(P_BOOK)
    a = find_one(blines, r"^\\subsection\{性同意的表达与确认\}$", "0book·性同意节")
    _, e1 = None, block_end(blines, a, "subsection")
    b = find_one(blines, r"^\\subsection\{性偏好与边界的沟通\}$", "0book·性偏好节")
    blk2_end = block_end(blines, b, "subsection")
    assert e1 == b, "0_book 中两小节应相邻: e1=%d b=%d" % (e1, b)
    moved_body = body_counter(blines[a:blk2_end])
    moved = []
    for ln in blines[a:blk2_end]:
        if re.match(r"^\\subsection\{", ln):
            ln = ln.replace("\\subsection", "\\section", 1)
        moved.append(ln)
    # 0_book 原位留标记
    mark = ["% ⇒ [已移出] 小节「性同意的表达与确认」「性偏好与边界的沟通」→ 3_position.tex《性爱中的边界、沟通与同意》章（r79）"]
    blines = blines[:a] + mark + blines[blk2_end:]
    # 边界章：章行后先插两节，再插导语（导语紧贴章标题）
    i = find_one(lines, r"^\\chapter\{性爱中的边界、沟通与同意\}$", "章·边界同意")
    lines[i + 1:i + 1] = moved
    lines[i + 1:i + 1] = ["", BOUNDARY_INTRO]

    # ===== 校验 =====
    out_body = body_counter(lines)
    src_titles = title_counter_orig = body_counter.__class__  # noqa (占位，下面真正比较)
    gone = src_body - out_body
    add = out_body - src_body
    # 预期新增 = 新写正文 + 0_book 移入正文
    expected_add = EXPECTED_NEW + moved_body
    unplanned_add = add - expected_add
    missing_new = expected_add - add
    print("--- 花括号净值: 改前 %d / 改后 %d" % (
        sum(x.count("{") - x.count("}") for x in read_lines(P_POS)),
        sum(x.count("{") - x.count("}") for x in lines)))
    print("--- 正文行: 原 %d 种/%d 行 -> 新 %d 种/%d 行" % (
        len(src_body), sum(src_body.values()), len(out_body), sum(out_body.values())))
    print("--- 消失正文行 %d 种（必须为 0）:" % len(gone))
    for s in list(gone)[:10]:
        print("    -", s[:120])
    print("--- 计划外新增正文行 %d 种（必须为 0）:" % len(unplanned_add))
    for s in list(unplanned_add)[:10]:
        print("    +", s[:120])
    print("--- 新写/移入正文未全部落盘: %d 种（必须为 0）" % len(missing_new))
    # 标题行变化（打印供人工核对）
    raw_old = read_lines(P_POS)
    t_old = collections.Counter(ln for ln in raw_old if TITLE.match(ln))
    t_new = collections.Counter(ln for ln in lines if TITLE.match(ln))
    print("--- 标题行变化 %d 种:" % len((t_old - t_new) + (t_new - t_old)))
    for s in sorted(t_old - t_new):
        print("    -", s[:110])
    for s in sorted(t_new - t_old):
        print("    +", s[:110])
    # 环境配对（剥注释）
    def env_check(ls):
        noc = "\n".join(re.sub(r"(?<!\\)%.*$", "", x) for x in ls)
        bad = []
        for env in ["itemize", "enumerate", "description", "center", "table", "tabular",
                    "tabularx", "longtable", "tcolorbox", "quote", "figure", "minipage"]:
            bb, ee = noc.count("\\begin{%s}" % env), noc.count("\\end{%s}" % env)
            if bb != ee:
                bad.append("%s b=%d e=%d" % (env, bb, ee))
        return bad
    print("--- 3_position 环境配对:", env_check(lines) or "OK")
    print("--- 0_book 环境配对:", env_check(blines) or "OK")

    if MODE == "apply":
        assert not gone, "存在消失的正文行!"
        assert not unplanned_add, "存在计划外新增正文行!"
        assert not missing_new, "新写/移入正文未全部落盘!"
        assert not env_check(lines) and not env_check(blines), "环境配对失败"
        st = time.strftime("%Y%m%d_%H%M%S")
        for p in (P_POS, P_BOOK):
            shutil.copy2(p, p + ".r79bak_" + st)
        io.open(P_POS, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
        io.open(P_BOOK, "w", encoding="utf-8", newline="\n").write("\n".join(blines))
        print("已写盘 3_position.tex + 0_book.tex（备份 .r79bak_%s）" % st)
    else:
        print("[dry-run] 未写盘")

reorganize()
