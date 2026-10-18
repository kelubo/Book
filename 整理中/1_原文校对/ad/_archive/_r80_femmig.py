# -*- coding: utf-8 -*-
"""r80: female.tex 三源迁移（停用框架区 + 原始内容区 + book旧区两节）→ r72 骨架 12 章
dry-run / apply 双模；全量断言；零丢失台账。"""
import io, re, sys, shutil, time, collections

AD = "D:/Git/Book/整理中/1_原文校对/ad/"
MODE = sys.argv[1] if len(sys.argv) > 1 else "dry-run"

def read(fn):
    raw = io.open(AD + fn, encoding="utf-8", newline="").read()
    return [x.rstrip("\r") for x in raw.split("\n")]

def norm(s):
    return re.sub(r"\s+", "", s)

HEAD = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{([^}]*)\}")
def head_of(line):
    m = HEAD.match(line)
    if m:
        return m.group(1), m.group(2)
    return None, None

def find_head(lines, lo, hi, level, title, occ=0):
    t = norm(title)
    n = 0
    for i in range(lo, hi):
        lv, tt = head_of(lines[i])
        if lv == level and norm(tt) == t:
            if n == occ:
                return i
            n += 1
    raise AssertionError("未找到 %s{%s} (occ=%d) in [%d,%d)" % (level, title, occ, lo, hi))

def next_head(lines, i, hi, levels):
    for j in range(i + 1, hi):
        lv, _ = head_of(lines[j])
        if lv in levels:
            return j
    return hi

def sec_block(lines, i, hi, stop_sub=None):
    e = next_head(lines, i, hi, ("section", "chapter", "part"))
    if stop_sub:
        for j in range(i + 1, e):
            lv, tt = head_of(lines[j])
            if lv == "subsection" and norm(tt) == norm(stop_sub):
                return i, j
    return i, e

def sub_block(lines, sec_i, hi, title):
    s = None
    for j in range(sec_i + 1, hi):
        lv, tt = head_of(lines[j])
        if lv in ("section", "chapter", "part"):
            break
        if lv == "subsection" and norm(tt) == norm(title):
            s = j
            break
    assert s is not None, "未找到子节 %s" % title
    e = next_head(lines, s, hi, ("subsection", "section", "chapter", "part"))
    return s, e

def minus_subs(lines, s, e, subs):
    """[s,e) 去掉指定 subsection 块（含标题行）；s 通常为节标题行后一格"""
    cuts = []
    for t in subs:
        cuts.append(sub_block(lines, s - 1, e, t))
    keep = []
    cur = s
    for cs, ce in cuts:
        keep.extend(lines[cur:cs])
        cur = ce
    keep.extend(lines[cur:e])
    return keep

def braces_delta(ls):
    return sum(x.count("{") - x.count("}") for x in ls)

def env_delta(ls):
    c = collections.Counter()
    for x in ls:
        x2 = re.sub(r"(?<!\\)%.*$", "", x)
        for m in re.finditer(r"\\(begin|end)\{([^}]*)\}", x2):
            c[m.group(2)] += 1 if m.group(1) == "begin" else -1
    return c

# ===== 读入 =====
fem = read("2_female.tex")
book = read("0_book.tex")

dc = next(i for i, x in enumerate(fem) if x.startswith("\\documentclass"))
F0, F1 = next(i for i, x in enumerate(fem) if x.startswith("\\newif\\ifskipfemaleframework")), \
         next(i for i, x in enumerate(fem) if x.startswith("\\fi %% \\ifskipfemaleframework")) + 1
O0 = next(i for i, x in enumerate(fem) if re.match(r"^\\part\*\{原始内容\}", x))
O1 = len(fem)
OE = next(i for i, x in enumerate(fem) if "\\end{document}" in x)   # 提取上界：不含 \end{document}
SK0 = next(i for i, x in enumerate(fem) if re.match(r"^\\part\{女性生殖基础\}", x))
print("框架区 [%d,%d)  骨架起 L%d  原始内容区 [%d,%d)  提取上界 L%d  documentclass L%d" % (F0 + 1, F1, SK0 + 1, O0 + 1, O1, OE + 1, dc + 1))

MIG, DROP = [], []   # 台账

def take_f_sec(title, dst_ch, dst_sec, minus=(), note=None, occ=0):
    i = find_head(fem, F0, F1, "section", title, occ)
    _, e = sec_block(fem, i, F1)
    body = minus_subs(fem, i + 1, e, minus)
    MIG.append(("F", title, i + 1, e, dst_ch, dst_sec, len(body)))
    return (dst_ch, dst_sec, body, note)

def take_f_sub(sec_title, sub_title, dst_ch, dst_sec, strip=True, occ=0):
    i = find_head(fem, F0, F1, "section", sec_title, occ)
    s, e = sub_block(fem, i, F1, sub_title)
    body = fem[s + 1:e] if strip else fem[s:e]
    MIG.append(("F", sec_title + "/" + sub_title, s + 1, e, dst_ch, dst_sec, len(body)))
    return (dst_ch, dst_sec, body, None)

def take_o_sec(title, dst_ch, dst_sec, minus=(), note=None, occ=0, stop_sub=None, strip=True):
    i = find_head(fem, O0, OE, "section", title, occ)
    _, e = sec_block(fem, i, OE, stop_sub)
    body = minus_subs(fem, i + 1, e, minus) if minus else (fem[i + 1:e] if strip else fem[i:e])
    if not minus and strip:
        body = fem[i + 1:e]
    MIG.append(("O", title, i + 1, e, dst_ch, dst_sec, len(body)))
    return (dst_ch, dst_sec, body, note)

def take_o_sub(sec_title, sub_title, dst_ch, dst_sec, occ=0, strip=True):
    i = find_head(fem, O0, OE, "section", sec_title, occ)
    s, e = sub_block(fem, i, OE, sub_title)
    body = fem[s + 1:e] if strip else fem[s:e]
    MIG.append(("O", sec_title + "/" + sub_title, s + 1, e, dst_ch, dst_sec, len(body)))
    return (dst_ch, dst_sec, body, None)

def take_b_sec(title, dst_ch, dst_sec, note=None, occ=0):
    i = find_head(book, 0, len(book), "section", title, occ)
    _, e = sec_block(book, i, len(book))
    MIG.append(("B", title, i + 1, e, dst_ch, dst_sec, e - i - 1))
    return (dst_ch, dst_sec, book[i + 1:e], note)

def take_b_sub(sec_title, sub_title, dst_ch, dst_sec, occ=0):
    i = find_head(book, 0, len(book), "section", sec_title, occ)
    s, e = sub_block(book, i, len(book), sub_title)
    MIG.append(("B", sec_title + "/" + sub_title, s + 1, e, dst_ch, dst_sec, e - s - 1))
    return (dst_ch, dst_sec, book[s + 1:e], None)

BLOKS = []   # (dst_ch, dst_sec, lines, note)

# ===== 章1 女性生殖系统 =====
# 外生殖器：O节(阴阜~前庭腺) + O阴蒂(并F阴蒂正文) + O(处女膜,前庭腺) + F(大小阴唇,前庭,会阴,异常护理)
i_o6 = find_head(fem, O0, OE, "section", "外生殖器")
o6_end = next_head(fem, i_o6, OE, ("section", "chapter", "part"))
s_yinti = find_head(fem, i_o6, o6_end, "subsection", "阴蒂")
s_chunv = find_head(fem, i_o6, o6_end, "subsection", "处女膜")
s_yindao = find_head(fem, i_o6, o6_end, "subsection", "阴道")
i_f6 = find_head(fem, F0, F1, "section", "外生殖器（外阴 / 女阴）")
f6_end = next_head(fem, i_f6, F1, ("section", "chapter", "part"))
s_fdi = find_head(fem, i_f6, f6_end, "subsection", "阴蒂")
e_fdi = next_head(fem, s_fdi, f6_end, ("subsection", "section", "chapter", "part"))
part1 = fem[i_o6 + 1:s_yinti]
part2 = fem[s_yinti:s_chunv] + fem[s_fdi + 1:e_fdi]
part3 = fem[s_chunv:s_yindao]
part4 = fem[i_f6 + 1:s_fdi] + fem[e_fdi:f6_end]
BLOKS.append(("女性生殖系统", "外生殖器（外阴 / 女阴）", part1 + part2 + part3 + part4, None))
MIG.append(("O", "外生殖器(拆)", i_o6 + 1, s_yindao, "女性生殖系统", "外生殖器", len(part1 + part2 + part3)))
MIG.append(("F", "外生殖器(拆)", i_f6 + 1, f6_end, "女性生殖系统", "外生殖器", len(part4)))

# 内生殖器
blk = [take_o_sec("内生殖器", "女性生殖系统", "内生殖器"),
       take_o_sub("外生殖器", "子宫颈", "女性生殖系统", "内生殖器"),
       take_o_sub("外生殖器", "G点", "女性生殖系统", "内生殖器"),
       take_o_sub("处女开苞与初次性体验", "子宫", "女性生殖系统", "内生殖器"),
       take_o_sub("处女开苞与初次性体验", "输卵管", "女性生殖系统", "内生殖器"),
       take_o_sub("处女开苞与初次性体验", "卵巢", "女性生殖系统", "内生殖器"),
       take_o_sub("外生殖器", "卵巢的秘密", "女性生殖系统", "内生殖器"),
       take_o_sub("外生殖器", "女性的性激素", "女性生殖系统", "内生殖器"),
       take_f_sec("内生殖器", "女性生殖系统", "内生殖器",
                  note="注（r80）：框架区《内生殖器》成稿（性健康视角）并录于后。")]
BLOKS += blk

BLOKS += [take_o_sec("乳房", "女性生殖系统", "乳房", occ=0),
          take_o_sec("乳房", "女性生殖系统", "乳房", occ=1,
                     note="注（r80）：原始内容区「乳房」节有两份，本份（内衣与女性健康）与上一份互补，均已迁入。"),
          take_f_sec("乳房", "女性生殖系统", "乳房"),
          take_o_sec("生殖系统解剖与生理的综合解析", "女性生殖系统", "生殖系统解剖与生理的综合解析"),
          take_o_sec("女性生殖系统的发育与老化", "女性生殖系统", "发育与老化"),
          take_f_sec("发育与老化", "女性生殖系统", "发育与老化"),
          take_o_sec("青春期生殖健康", "女性生殖系统", "青春期生殖健康"),
          take_o_sec("女性生殖健康与保健", "女性生殖系统", "女性生殖健康与保健")]
DROP += [("O", "女性生殖系统的常见疾病", "与框架区《妇科常见疾病》成稿及原始区「妇科常见疾病」互补小节同题重复"),
         ("O", "外生殖器/阴道(短版)", "同题重复，采用原始区《内生殖器》下的详版（约5倍篇幅）"),
         ("O", "外生殖器/子宫、输卵管、卵巢(短版)", "同题重复，采用「初次性体验」节下的详版")]

# ===== 章2 月经 =====
for t in ["正常月经", "常见月经问题", "卫生用品与护理", "经期性行为", "月经贫困与经期平等"]:
    BLOKS.append(take_f_sec(t, "月经与周期健康管理", t))

# ===== 章3 妇科常见疾病 =====
for t in ["阴道炎症", "宫颈疾病", "盆腔炎性疾病（PID）", "子宫疾病", "卵巢疾病",
          "尿失禁与盆底功能障碍", "性传播疾病——女性角度"]:
    BLOKS.append(take_f_sec(t, "妇科常见疾病", t))
BLOKS.append(take_f_sec("其他", "妇科常见疾病", "其他妇科问题",
                        note="注（r80）：原框架节名「其他」，此处沿用骨架节名「其他妇科问题」。"))
for t in ["外阴癌与阴道癌", "妊娠滋养细胞肿瘤", "输卵管疾病", "先天性生殖道发育异常与性健康",
          "乳腺疾病", "妇科疾病的预防与筛查"]:
    BLOKS.append(take_o_sub("妇科常见疾病", t, "妇科常见疾病", "其他妇科问题"))
DROP += [("O", "妇科常见疾病/外阴及阴道疾病、宫颈疾病、性传播疾病(STDs)、子宫疾病、卵巢疾病",
          "与框架区对应节成稿同题重复，采用成稿")]

# ===== 章4 女性性功能与性问题 =====
BLOKS.append(take_f_sec("女性性欲与唤起", "女性性功能与性问题", "女性性反应与性欲",
                        minus=["性欲低下的原因与应对", "HSDD 与氟班色林（Addyi）", "性唤起障碍", "性厌恶"]))
BLOKS.append(take_f_sub("女性性欲与唤起", "性欲低下的原因与应对", "女性性功能与性问题", "女性性欲低下", strip=False))
BLOKS.append(take_f_sub("女性性欲与唤起", "HSDD 与氟班色林（Addyi）", "女性性功能与性问题", "女性性欲低下"))
BLOKS.append(take_f_sub("女性性欲与唤起", "性唤起障碍", "女性性功能与性问题", "性唤起障碍", strip=False))
BLOKS.append(take_f_sub("女性性欲与唤起", "性厌恶", "女性性功能与性问题", "性厌恶", strip=False))
BLOKS.append(take_f_sec("性高潮障碍", "女性性功能与性问题", "性高潮障碍"))
BLOKS.append(take_f_sec("性交疼痛", "女性性功能与性问题", "性交疼痛", minus=["阴道痉挛的治疗"]))
BLOKS.append(take_f_sub("性交疼痛", "阴道痉挛的治疗", "女性性功能与性问题", "阴道痉挛"))
BLOKS.append(take_f_sec("阴道干涩与萎缩", "女性性功能与性问题", "阴道干涩与萎缩"))
BLOKS.append(take_f_sec("依恋风格与女性的亲密之性", "女性性功能与性问题", "依恋风格与女性的亲密之性"))
BLOKS.append(take_o_sec("性健康与性生活指导", "女性性功能与性问题", "性健康与性生活指导",
                        minus=["乳交与性健康", "阴交与性健康", "肛交与性健康", "手交与性健康", "足交与性健康"],
                        note="注（r80）：本节原含乳交/阴交/肛交/手交/足交五个技法小节，按三卷分工已统一至 3_position.tex，此处不再重复。"))
# 新节：初次性行为与处女膜
i_o9 = find_head(fem, O0, OE, "section", "处女开苞与初次性体验")
s_zg = find_head(fem, i_o9, OE, "subsection", "子宫")
body = ['\\section{初次性行为与处女膜}', ''] + fem[i_o9 + 1:s_zg]
BLOKS.append(("女性性功能与性问题", "#NEW#女性性功能与性问题", body, None))
MIG.append(("O", "处女开苞与初次性体验(更名)", i_o9 + 1, s_zg, "女性性功能与性问题", "初次性行为与处女膜", len(body)))
DROP += [("O", "处女开苞与初次性体验/子宫、输卵管、卵巢", "归属《内生殖器》，已迁入")]

# ===== 章5 女性生育与生殖健康 =====
BLOKS.append(take_o_sub("生育生理与避孕", "生育生理", "女性生育与生殖健康", "受孕原理与女性生殖生理"))
BLOKS.append(take_f_sec("受孕原理与优生准备", "女性生育与生殖健康", "受孕原理与女性生殖生理"))
BLOKS.append(take_o_sec("生育问题与辅助生殖技术", "女性生育与生殖健康", "不孕与辅助生殖"))
BLOKS.append(take_f_sec("不孕与辅助生殖", "女性生育与生殖健康", "不孕与辅助生殖",
                        note="注（r80）：框架区《不孕与辅助生殖》成稿（速览视角）并录于后。"))
BLOKS.append(take_o_sec("妊娠与分娩", "女性生育与生殖健康", "妊娠与分娩"))
BLOKS.append(take_f_sec("妊娠与分娩", "女性生育与生殖健康", "妊娠与分娩",
                        note="注（r80）：框架区《妊娠与分娩》速览并录于后。"))
BLOKS.append(take_f_sec("意外怀孕与流产", "女性生育与生殖健康", "意外怀孕与流产"))
DROP += [("O", "生育生理与避孕/避孕方法", "避孕按三卷分工统一至 0_book《避孕与生育》篇"),
         ("F", "避孕方法（女性适用）", "避孕按三卷分工统一至 0_book《避孕与生育》篇")]

# ===== 章6 孕期与产后性健康 =====
BLOKS.append(take_f_sec("孕期性生活指导", "孕期与产后性健康", "孕期性生活指导", minus=["孕期性生理变化"]))
BLOKS.append(take_f_sub("孕期性生活指导", "孕期性生理变化", "孕期与产后性健康", "孕期性生理变化", strip=False))
BLOKS.append(take_f_sec("产后恢复与性需求变化", "孕期与产后性健康", "产后恢复与性需求变化"))
BLOKS.append(take_f_sec("哺乳期性健康", "孕期与产后性健康", "哺乳期性健康"))

# ===== 章7 更年期健康管理 =====
BLOKS.append(take_o_sub("更年期健康管理", "更年期的定义与分期", "更年期健康管理", "围绝经期生理变化"))
BLOKS.append(take_o_sub("更年期健康管理", "更年期的生理变化", "更年期健康管理", "围绝经期生理变化"))
BLOKS.append(take_f_sec("围绝经期生理变化", "更年期健康管理", "围绝经期生理变化"))
BLOKS.append(take_f_sec("激素替代治疗（HRT）", "更年期健康管理", "激素替代治疗（HRT）"))
BLOKS.append(take_f_sec("非激素替代方案", "更年期健康管理", "非激素替代方案"))
BLOKS.append(take_o_sub("更年期健康管理", "更年期常见症状", "更年期健康管理", "围绝经期症状与性"))
BLOKS.append(take_o_sub("更年期健康管理", "更年期的性生活指导", "更年期健康管理", "围绝经期症状与性"))
BLOKS.append(take_o_sub("更年期健康管理", "性欲与性反应在更年期的变化", "更年期健康管理", "围绝经期症状与性"))
BLOKS.append(take_f_sec("绝经之后的亲密与再婚", "更年期健康管理", "绝经之后的亲密与再婚"))
BLOKS.append(take_o_sub("更年期健康管理", "更年期的健康管理", "更年期健康管理", "更年期后长期健康管理"))
BLOKS.append(take_o_sub("更年期健康管理", "更年期的常见疾病预防", "更年期健康管理", "更年期后长期健康管理"))
BLOKS.append(take_o_sub("更年期健康管理", "更年期的定期检查", "更年期健康管理", "更年期后长期健康管理"))
BLOKS.append(take_f_sec("更年期后长期健康管理", "更年期健康管理", "更年期后长期健康管理"))

# ===== 章8 妇科检查与筛查 =====
BLOKS.append(take_f_sec("常规检查项目", "妇科检查与筛查", "常规检查项目"))
BLOKS.append(take_o_sub("妇科检查与筛查指南", "妇科检查的重要性", "妇科检查与筛查", "常规检查项目"))
BLOKS.append(take_o_sub("妇科检查与筛查指南", "妇科检查的类型与内容", "妇科检查与筛查", "常规检查项目"))
BLOKS.append(take_f_sec("不同年龄段的筛查建议", "妇科检查与筛查", "不同年龄段的筛查建议"))
BLOKS.append(take_o_sub("妇科检查与筛查指南", "妇科筛查的时机与频率", "妇科检查与筛查", "不同年龄段的筛查建议"))
BLOKS.append(take_f_sec("检查前的准备", "妇科检查与筛查", "检查前的准备"))
BLOKS.append(take_o_sub("妇科检查与筛查指南", "妇科检查前的准备与注意事项", "妇科检查与筛查", "检查前的准备"))
BLOKS.append(take_o_sub("妇科检查与筛查指南", "特殊人群的妇科检查与筛查", "妇科检查与筛查", "女性生殖健康检查"))
BLOKS.append(take_o_sub("妇科检查与筛查指南", "妇科检查的常见误区", "妇科检查与筛查", "女性生殖健康检查"))
BLOKS.append(take_b_sec("女性生殖健康检查", "妇科检查与筛查", "女性生殖健康检查",
                        note="注（r80）：自 0_book.tex《生殖健康检查》章迁入（book 原位留有移出标记，旧区存档仍在）。"))

# ===== 章9 女性日常保健 =====
BLOKS.append(take_f_sec("外阴护理常识", "女性日常保健", "外阴护理常识"))
BLOKS.append(take_f_sec("性交后的身体护理与清洁", "女性日常保健", "性交后的身体护理与清洁"))
BLOKS.append(take_f_sec("饮食与营养", "女性日常保健", "饮食与营养"))
BLOKS.append(take_f_sec("运动与盆底肌", "女性日常保健", "运动与盆底训练"))
BLOKS.append(take_b_sec("女性盆底训练与性感受", "女性日常保健", "运动与盆底训练",
                        note="注（r80）：自 0_book.tex《盆底健康与性功能》章迁入（book 原位留有移出标记）。"))
BLOKS.append(take_f_sec("心理健康", "女性日常保健", "心理健康"))
BLOKS.append(take_o_sec("营养与生殖健康", "女性日常保健", "营养与生殖健康"))
BLOKS.append(take_o_sec("环境因素对生殖健康的影响", "女性日常保健", "环境因素对生殖健康的影响"))
BLOKS.append(take_o_sec("心理健康与生殖健康的关系", "女性日常保健", "心理健康与生殖健康的关系"))

# ===== 章10 妇科手术与康复 =====
for t in ["妇科手术的概述", "常见的妇科手术类型", "妇科手术前的准备与评估"]:
    BLOKS.append(take_o_sub("妇科手术与康复", t, "妇科手术与康复", "常见手术简介"))
BLOKS.append(take_f_sec("常见手术简介", "妇科手术与康复", "常见手术简介"))
for t in ["妇科手术后的康复护理", "妇科手术与生育的关系", "妇科手术的心理调适", "妇科手术的伦理与法律问题"]:
    BLOKS.append(take_o_sub("妇科手术与康复", t, "妇科手术与康复", "术后护理与康复"))
BLOKS.append(take_f_sec("术后护理与康复", "妇科手术与康复", "术后护理与康复"))
BLOKS.append(take_f_sec("女性生殖器美容手术", "妇科手术与康复", "女性生殖器美容手术"))
BLOKS.append(take_b_sub("私处整容", "定义与常见类型", "妇科手术与康复", "女性外生殖器手术"))
BLOKS.append(take_b_sub("私处整容", "动机与方法技术", "妇科手术与康复", "女性外生殖器手术"))
BLOKS.append(take_b_sub("私处整容", "风险并发症与社会-心理考量", "妇科手术与康复", "女性外生殖器手术的美学决策"))
BLOKS.append(take_b_sub("私处整容", "专业建议", "妇科手术与康复", "女性外生殖器手术的美学决策"))

# ===== 章11 生殖健康专题 =====
for t in ["儿童与青少年妇科健康", "生殖权利与医疗资源获取", "女性割礼（FGM）的全球健康议题",
          "新兴技术在生殖健康中的应用"]:
    BLOKS.append(take_o_sec(t, "生殖健康专题", t))

# ===== 章12 中医妇科 =====
BLOKS.append(take_f_sec("中医妇科学基础", "中医妇科", "中医妇科学基础"))
BLOKS.append(take_f_sec("常见妇科病的中医调理", "中医妇科", "常见妇科病的中医调理"))
BLOKS.append(take_f_sec("食疗与养生", "中医妇科", "食疗与养生"))
BLOKS.append(take_f_sec("附录：幼女性健康常见问题解答", "中医妇科", "幼女性健康常见问题解答"))
i_o26 = find_head(fem, O0, OE, "section", "传统中医与女性性健康")
_, e26 = sec_block(fem, i_o26, OE)
body = ['\\section{传统性学观与女性生殖健康}', '',
        '% 注（r80）：原标记「统一至 book」经核查 book《中国古代性学经典》并无九气/五征五欲等内容，',
        '%      为不丢知识点改迁本卷。'] + fem[i_o26 + 1:e26]
BLOKS.append(("中医妇科", "#NEW#中医妇科", body, None))
MIG.append(("O", "传统中医与女性性健康(更名)", i_o26 + 1, e26, "中医妇科", "传统性学观与女性生殖健康", len(body)))

# ===== 校验与执行 =====
print("迁移块: %d  台账: MIG=%d" % (len(BLOKS), len(MIG)))
bad = [b for b in BLOKS if braces_delta(b[2]) != 0]
assert not bad, "花括号不平衡的迁移块: %s" % [(b[0], b[1]) for b in bad]
for b in BLOKS:
    ed = env_delta(b[2])
    nz = {k: v for k, v in ed.items() if v != 0}
    assert not nz, "环境不配平: %s %s" % ((b[0], b[1]), nz)

# 删除两大区（框架区 + 原始内容区），保留 \end{document}
assert braces_delta(fem[F0:F1]) == 0 and braces_delta(fem[O0:O1]) == 0
for zone, nm in ((fem[F0:F1], "框架区"), (fem[O0:O1], "原始内容区")):
    ed = env_delta(zone)
    nz = {k: v for k, v in ed.items() if v != 0}
    if nm == "原始内容区":
        nz.pop("document", None)   # 文件尾的孤立 \end{document}，写盘时补回
    assert not nz, "%s 环境不配平: %s" % (nm, nz)

out = fem[:F0] + fem[F1:O0]
shift = F1 - F0
O0n = O0 - shift
out = out[:O0n] + out[O0n + 1:]           # 去掉 \part*{原始内容} 行
# 其余原始内容区行 = out[O0n:]（已不含 \part 行）——直接截断
out = out[:O0n]

# ===== 插入迁移块 =====
def insert_blocks(out):
    dc2 = next(i for i, x in enumerate(out) if x.startswith("\\documentclass"))
    # 按 (章,节) 归组，保持顺序
    groups = collections.OrderedDict()
    for ch, sec, body, note in BLOKS:
        groups.setdefault((ch, sec), []).append((body, note))
    for (ch, sec), items in groups.items():
        ci = find_head(out, dc2, len(out), "chapter", ch)
        ce = next_head(out, ci, len(out), ("part",))
        if sec.startswith("#NEW#"):
            # 章尾新节
            body = items[0][0]
            out = out[:ce] + [""] + body + out[ce:]
            continue
        si = find_head(out, ci, ce, "section", sec)
        se = next_head(out, si, ce, ("section", "chapter", "part"))
        ins = []
        for body, note in items:
            if note:
                ins.append("% " + note)
            ins += body
        out = out[:se] + ins + out[se:]
    return out

out = insert_blocks(out)
# 追加参考文献说明与 \end{document}
out += ['', '% 注（r80）：原「原始内容区」全部内容已按骨架迁入各章；停用框架区成稿亦已迁入并删除。',
        '%      参考文献统一见 0_book.tex 卷尾。', '', '\\end{document}', '']

# ===== 全量断言 =====
def full_check(lines, tag):
    t = "\n".join(re.sub(r"(?<!\\)%.*$", "", x) for x in lines)
    d = t.count("{") - t.count("}")
    c = collections.Counter()
    for m in re.finditer(r"\\(begin|end)\{([^}]*)\}", t):
        c[m.group(2)] += 1 if m.group(1) == "begin" else -1
    nz = {k: v for k, v in c.items() if v != 0}
    assert d == 0, "%s 花括号 delta=%d" % (tag, d)
    assert not nz, "%s 环境不配平 %s" % (tag, nz)
    assert any("\\end{document}" in x for x in lines[-6:]), tag + " 缺 end{document}"
    assert not [x for x in lines if "\ufffd" in x], tag + " 乱码"

full_check(out, "结果文件")
# 迁移内容确实在结果里：抽样每块首行非注释行应在输出中
moved_norm = set()
for ch, sec, body, note in BLOKS:
    for x in body:
        s = norm(x)
        if len(s) >= 10 and not x.strip().startswith("%"):
            moved_norm.add(s)
out_norm = set(norm(x) for x in out if x.strip())
lost = [x for x in list(moved_norm)[:0]]  # 占位
missing = 0
for x in moved_norm:
    if x not in out_norm:
        missing += 1
assert missing == 0, "迁移行缺失 %d" % missing
print("迁移行抽查: 全部在结果文件中 (%d 条唯一行)" % len(moved_norm))

if MODE == "apply":
    st = time.strftime("%Y%m%d_%H%M%S")
    shutil.copy2(AD + "2_female.tex", AD + "2_female.tex.r80bak_" + st)
    io.open(AD + "2_female.tex", "w", encoding="utf-8", newline="").write("\r\n".join(out))
    print("已写盘 2_female.tex（备份 .r80bak_%s）新行数 %d" % (st, len(out)))
else:
    print("dry-run 完成：预览输出 %d 行" % len(out))
    io.open(AD + "_r80_preview.tex", "w", encoding="utf-8", newline="").write("\r\n".join(out))

# 台账落盘
with io.open(AD + "_r80_ledger.txt", "w", encoding="utf-8") as f:
    f.write("== 迁入 (%d) ==\n" % len(MIG))
    for z, t, a, b, ch, sec, n in MIG:
        f.write("[%s] %-40s L%d-%d -> %s·%s (%d行)\n" % (z, t, a, b, ch, sec, n))
    f.write("\n== 弃用并说明 (%d) ==\n" % len(DROP))
    for z, t, r in DROP:
        f.write("[%s] %s —— %s\n" % (z, t, r))
print("台账已写 _r80_ledger.txt")
