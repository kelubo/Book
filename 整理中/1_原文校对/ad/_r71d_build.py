# -*- coding: utf-8 -*-
"""r71d：给 female.tex / male.tex 生成并插入「新目录骨架」（篇/章/节 + 来源锚）。

用法：python _r71d_build.py          -> dry-run（只打印统计）
      python _r71d_build.py preview  -> 写 _r71_preview_female.txt / _r71_preview_male.txt
      python _r71d_build.py apply    -> 落盘

原则：
  * 只在编译区（\\documentclass 之后的正文）插入骨架 + 分隔；原内容一行不动。
  * 篇用 \\part*（不触发 preamble 里 part/name={。卷} 的可疑格式），加 addcontentsline。
  * 注释锚一律用标题锚，不写行号（r64 定版）。
"""
import io, re, sys

MODE = sys.argv[1] if len(sys.argv) > 1 else "dry"

FW_NOTE = '% 框架成稿：文件前部停用框架区（\\ifskip…\\fi）已有本节成稿，搜索同节名定位'
NOWNOTE = '% 待写：原始内容区与停用框架区暂无对应内容'


def S(n, orig=None, fw=False, extra=None):
    return {"n": n, "orig": orig, "fw": fw, "extra": extra or []}


# ══════════════════════════ female 数据 ══════════════════════════
F = [
    ("第一篇：女性生殖基础", [
        {"n": "女性生殖系统",
         "note": '% 移入："女性生殖系统"整章（原始内容区）——原为一整章近三十节，正逐节拆入本篇',
         "secs": [
             S("外生殖器（外阴 / 女阴）", "外生殖器", True),
             S("内生殖器", "内生殖器", True),
             S("乳房", "乳房", True,
               extra=['% 移入："乳房"整节在原始内容区出现两份（一处在"内生殖器"之后、一处在"妊娠与分娩"之后），择优合并']),
             S("生殖系统解剖与生理的综合解析", "生殖系统解剖与生理的综合解析"),
             S("发育与老化", "女性生殖系统的发育与老化", True),
             S("青春期生殖健康", "青春期生殖健康"),
             S("女性生殖健康与保健", "女性生殖健康与保健"),
         ]},
        {"n": "月经与周期健康管理", "note": None, "secs": [
            S("正常月经", None, True),
            S("常见月经问题", None, True),
            S("卫生用品与护理", None, True),
            S("经期性行为", None, True),
            S("月经贫困与经期平等", None, True),
        ]},
    ]),
    ("第二篇：妇科疾病与性问题", [
        {"n": "妇科常见疾病",
         "note": '% 移入："妇科常见疾病"整节（原始内容区）与"女性生殖系统的常见疾病"整节，两处同题材，'
                 '前者按器官分小节、后者为总览，合并时总览作章首导读',
         "secs": [
             S("阴道炎症", None, True),
             S("宫颈疾病", None, True),
             S("盆腔炎性疾病（PID）", None, True),
             S("子宫疾病", None, True),
             S("卵巢疾病", None, True),
             S("性传播疾病——女性角度", None, True),
             S("尿失禁与盆底功能障碍", None, True),
             S("其他", None, True),
         ]},
        {"n": "女性性问题与性健康", "note": None, "secs": [
            S("女性性欲与唤起", None, True),
            S("依恋风格与女性的亲密之性", None, True),
            S("性高潮障碍", None, True),
            S("性交疼痛", None, True),
            S("阴道干涩与萎缩", None, True),
            S("性健康与性生活指导", "性健康与性生活指导"),
            S("阴交技巧与体验", "阴交技巧与体验"),
            S("肛交技巧与体验", "肛交技巧与体验"),
            S("处女开苞与初次性体验", "处女开苞与初次性体验"),
        ]},
    ]),
    ("第三篇：生育、避孕与产后", [
        {"n": "生育与避孕", "note": None, "secs": [
            S("受孕原理与优生准备", None, True),
            S("不孕与辅助生殖", None, True),
            S("避孕方法（女性适用）", None, True),
            S("意外怀孕与流产", None, True),
            S("妊娠与分娩", "妊娠与分娩", True),
            S("生育生理与避孕", "生育生理与避孕"),
            S("生育问题与辅助生殖技术", "生育问题与辅助生殖技术"),
        ]},
        {"n": "孕期与产后性健康", "note": None, "secs": [
            S("孕期性生活指导", None, True),
            S("产后恢复与性需求变化", None, True),
            S("哺乳期性健康", None, True),
        ]},
    ]),
    ("第四篇：更年期、检查与日常保健", [
        {"n": "更年期健康管理",
         "note": '% 移入："更年期健康管理"整节（原始内容区）作为本章主体，框架区各节与之互补',
         "secs": [
             S("围绝经期生理变化", None, True),
             S("激素替代治疗（HRT）", None, True),
             S("非激素替代方案", None, True),
             S("绝经之后的亲密与再婚", None, True),
             S("更年期后长期健康管理", None, True),
         ]},
        {"n": "妇科检查与筛查",
         "note": '% 移入："妇科检查与筛查指南"整节（原始内容区）作为本章主体',
         "secs": [
             S("常规检查项目", None, True),
             S("不同年龄段的筛查建议", None, True),
             S("检查前的准备", None, True),
         ]},
        {"n": "女性日常保健", "note": None, "secs": [
            S("外阴护理常识", None, True),
            S("性交后的身体护理与清洁", None, True),
            S("饮食与营养", "饮食与营养", True,
              extra=['% 注意：原始内容区 \\begin{document} 之后、目录页之前有一处游离的"饮食与营养"节，迁入时并入本节']),
            S("运动与盆底肌", None, True),
            S("心理健康", None, True),
            S("营养与生殖健康", "营养与生殖健康"),
            S("环境因素对生殖健康的影响", "环境因素对生殖健康的影响"),
            S("心理健康与生殖健康的关系", "心理健康与生殖健康的关系"),
        ]},
        {"n": "妇科手术与康复",
         "note": '% 移入："妇科手术与康复"整节（原始内容区）作为本章主体',
         "secs": [
             S("常见手术简介", None, True),
             S("术后护理与康复", None, True),
             S("女性生殖器美容手术", None, True),
         ]},
        {"n": "生殖健康专题",
         "note": '% 本章为新增章，四节全部来自原始内容区，无框架成稿',
         "secs": [
             S("儿童与青少年妇科健康", "儿童与青少年妇科健康"),
             S("生殖权利与医疗资源获取", "生殖权利与医疗资源获取"),
             S("女性割礼（FGM）的全球健康议题", "女性割礼（FGM）的全球健康议题"),
             S("新兴技术在生殖健康中的应用", "新兴技术在生殖健康中的应用"),
         ]},
    ]),
    ("第五篇：传统中医与女性性健康", [
        {"n": "中医妇科", "note": None, "secs": [
            S("中医妇科学基础", None, True),
            S("常见妇科病的中医调理", None, True),
            S("食疗与养生", None, True),
            S("附录：幼女性健康常见问题解答", None, True),
            S("传统中医与女性性健康", "传统中医与女性性健康"),
        ]},
    ]),
]

# ══════════════════════════ male 数据 ══════════════════════════
M = [
    ("第一篇：男性生殖基础", [
        {"n": "男性生殖系统",
         "note": '% 移入："男性生殖系统"整章（原始内容区）——原为一整章，逐节拆入本篇',
         "secs": [
             S("解剖与生理", "男性生殖系统解剖与生理", True,
               extra=['% 注意：原始内容区该节 1800 余行，仅五个小节（阴阜／阴茎／阴囊／男性内生殖器官／男性性感区），迁入时按器官拆小节']),
             S("男性性感区", None, True,
               extra=['% 移入：原始内容区"男性性感区"现为"男性生殖系统解剖与生理"节下的小节，升为独立节']),
             S("男性的性反应", "男性的性反应",
               extra=['% 移入：含兴奋期／平台期／高潮期／消退期四小节（原始内容区）']),
         ]},
    ]),
    ("第二篇：男性疾病与健康问题", [
        {"n": "常见疾病", "note": None, "secs": [
            S("男性的性功能障碍概述", None, True),
            S("勃起功能障碍（ED，旧称阳痿）", None, True),
            S("糖尿病性ED的机制与治疗", None, True),
            S("早泄（PE）", None, True),
            S("不射精或迟缓射精", None, True),
            S("性欲低下（性欲减退）", None, True),
            S("性欲衰退", None, True),
            S("男性性欲的波动与节律", None, True),
            S("前列腺疾病", None, True,
               extra=['% 分工：本节讲诊断与治疗；筛查与预防见第三篇「前列腺疾病」']),
            S("男性不育", None, True),
            S("男性避孕技术新进展", None, True),
            S("男性生殖系统感染", None, True),
            S("其他男科问题", None, True),
        ]},
    ]),
    ("第三篇：男性保健与预防", [
        {"n": "日常保健", "note": None, "secs": [
            S("定期自检指南", None, True),
            S("男科体检：查什么、何时查", None, True),
            S("前列腺疾病", None, True,
               extra=['% 分工：本节讲 PSA 筛查与预防；诊断与治疗见第二篇「前列腺疾病」']),
            S("生活方式与性健康", None, True),
            S("男性盆底肌训练", None, True),
            S("内分泌干扰物与生殖健康", None, True),
            S("年龄相关的性健康变化", None, True),
            S("前列腺癌与PSA筛查", None, True),
            S("睾丸癌与自检", None, True),
            S("男性乳腺癌（Male Breast Cancer）", None, True),
            S("睡眠呼吸暂停与勃起功能障碍", None, True),
            S("男性更年期（LOH）", None, True),
            S("男性骨质疏松与睾酮的关系", None, True),
            S("依恋风格与性", None, True),
            S("男性心理健康与性功能", None, True),
            S("男性产后抑郁（Paternal Postnatal Depression, PPND）", None, True),
        ]},
    ]),
    ("第四篇：传统中医与男性性健康", [
        {"n": "中医男科", "note": None, "secs": [
            S("中医男科理论基础", None, True),
            S("性健康调养", None, True),
            S("中西医结合视角", None, True),
            S("传统中医与男性性健康", "传统中医与男性性健康",
               extra=['% 移入：含男性生理特点／男性"四至"／男性"五常"之说／性健康调养／常见男性生殖系统感染五个小节']),
        ]},
    ]),
]

JOBS = {
    "female.tex": {
        "data": F,
        "after": "\\mainmatter",
        "boundary": "\\chapter{女性生殖系统}",
        "switch": "\\ifskipfemaleframework",
        "pos": "女性专属内容（解剖、妇科疾病、生育、保健、中医妇科）",
        "other": "male.tex",
    },
    "male.tex": {
        "data": M,
        "after": "\\listoftables",
        "boundary": "\\chapter{男性生殖系统}",
        "switch": "\\ifskipmaleframework",
        "pos": "男性专属内容（解剖、疾病、保健、中医男科）",
        "other": "female.tex",
    },
}


def collect_orig_sections(lines, begin_idx):
    """编译区（\\begin{document} 之后，含目录前的游离节）的全部 section 名"""
    names = []
    for i in range(begin_idx + 1, len(lines)):
        m = re.match(r"^\s*\\section\*?\s*\{", lines[i])
        if m:
            e = lines[i].index("}", m.end())
            names.append(lines[i][m.end():e].strip())
    return names


def collect_framework_sections(lines, switch):
    """停用框架区 = \\ifskip… 行 到 \\fi 行 之间"""
    a = next(i for i, l in enumerate(lines) if l.strip() == switch)
    b = next(i for i, l in enumerate(lines) if l.strip().startswith("\\fi"))
    names = []
    for l in lines[a:b]:
        m = re.match(r"^\s*\\section\*?\s*\{", l)
        if m:
            e = l.index("}", m.end())
            names.append(l[m.end():e].strip())
    return names


def build_block(fn, job, lines, after_idx):
    begin_idx = next(i for i, l in enumerate(lines) if l.strip() == r"\begin{document}")
    orig_secs = collect_orig_sections(lines, begin_idx)
    fw_secs = collect_framework_sections(lines, job["switch"])
    out = []
    w = out.append
    w("% ════════════════════════════════════════════════════════════════════════")
    w("%            全书目录结构（2026-09-21 新增，供逐步迁移内容用）")
    w("% ════════════════════════════════════════════════════════════════════════")
    w("% 使用说明：")
    w("%%   1. 本文件定位：%s。" % job["pos"])
    w("%%      两性共通内容见 book.tex，%s。" % ("女性专属内容见 female.tex" if fn == "male.tex" else "男性专属内容见 male.tex"))
    w("%   2. 本骨架为目录层（篇 / 章 / 节），供把下方「原始内容」逐步迁入；")
    w("%      小节（学习要点）层暂未铺开，待内容迁入时按需补。")
    w("%   3. 每节下注释标明来源：")
    w('%      「移入」＝原始内容区（\\part*{原始内容} 之后）的同名节，按标题搜索即可定位；')
    w("%%      「框架成稿」＝文件前部停用框架区（%s…\\fi）已有成稿，" % job["switch"])
    w("%      把开关改为 false 即可编译查看，或直接复制其内容；")
    w('%      「待写」＝两处都暂无对应内容。')
    w("%   4. 篇一律用 \\part*（不带编号），避免触发 preamble 中 part/name={。卷} 的可疑格式；")
    w("%      建议后续（待授权）把 {。卷}/{。章} 修正为 {第,卷}/{第,章}。")
    w("%   5. 原始内容区末尾的「参考资料」类章不在本目录内，最终并入卷尾。")
    w("%   6. 全部迁完后：删除 \\part*{原始内容} 及以下旧标题行，再删除本说明。")
    w("% ════════════════════════════════════════════════════════════════════════")
    nsec = 0
    for pname, chapters in job["data"]:
        w("")
        w("\\part*{%s}" % pname)
        w("\\addcontentsline{toc}{part}{%s}" % pname)
        for ch in chapters:
            w("")
            w("\\chapter{%s}" % ch["n"])
            if ch["note"]:
                w(ch["note"])
            for s in ch["secs"]:
                w("")
                w("\\section{%s}" % s["n"])
                nsec += 1
                if s["orig"]:
                    assert s["orig"] in orig_secs, "%s: 原始内容区找不到节「%s」" % (fn, s["orig"])
                    w('%% 移入："%s"整节（原始内容区，按标题搜索）' % s["orig"])
                if s["fw"]:
                    assert s["n"] in fw_secs, "%s: 停用框架区找不到节「%s」" % (fn, s["n"])
                    w(FW_NOTE)
                if not s["orig"] and not s["fw"]:
                    w(NOWNOTE)
                for e in s["extra"]:
                    w(e)
    w("")
    w("% ════════════════════════════════════════════════════════════════════════")
    w("%            ▼ 原始内容开始（保留原样，逐步迁入上方新目录） ▼")
    w("% ════════════════════════════════════════════════════════════════════════")
    w("")
    w("\\part*{原始内容}")
    w("\\addcontentsline{toc}{part}{原始内容（待迁移，保留原样）}")
    return out, nsec


def process(fn, job):
    raw = io.open(fn, encoding="utf-8", newline="").read()
    # female/male 为纯 CRLF（book.tex 才是纯 LF），先探测再保持一致
    pure_crlf = raw.count("\r\n") == raw.count("\n") == raw.count("\r") and raw.count("\n") > 0
    assert pure_crlf, fn + " 不是纯 CRLF"
    EOL = "\r\n"
    lines = raw.split(EOL)
    after_idx = next(i for i, l in enumerate(lines) if l.strip() == job["after"])
    b_idx = next(i for i in range(after_idx + 1, len(lines))
                 if lines[i].strip() == job["boundary"])
    block, nsec = build_block(fn, job, lines, after_idx)
    nch = sum(1 for _, chs in job["data"] for c in chs)
    print("%s: 在 L%d（%s 之后）插入；原始内容章 L%d；篇 %d / 章 %d / 节 %d；插入 %d 行"
          % (fn, after_idx + 1, job["after"], b_idx + 1, len(job["data"]), nch, nsec, len(block)))
    if MODE == "preview":
        io.open("_r71_preview_" + fn.split(".")[0] + ".txt", "w", encoding="utf-8", newline="") \
            .write(EOL.join(block))
    if MODE == "apply":
        new = lines[: after_idx + 1] + block + lines[after_idx + 1:]
        # 断言：插入点之前 + 插入点之后逐字不变
        assert new[: after_idx + 1] == lines[: after_idx + 1]
        assert new[len(new) - (len(lines) - after_idx - 1):] == lines[after_idx + 1:]
        io.open(fn, "w", encoding="utf-8", newline="").write(EOL.join(new))
        print("  已落盘 %d -> %d 行（保持 CRLF）" % (len(lines), len(new)))


for fn, job in JOBS.items():
    process(fn, job)
