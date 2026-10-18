# -*- coding: utf-8 -*-
"""r43 执行器：纯锚点行级插入（before 型）
用法：
  python _r43_insert.py          # dry-run：只校验锚点，不写盘
  python _r43_insert.py apply    # 实际写盘
"""
import io, os, sys, importlib.util

BASE = os.path.dirname(os.path.abspath(__file__))

def load_mod(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(BASE, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

BK1 = load_mod("_r43_bk1").NEW
BK2 = load_mod("_r43_bk2").NEW
BK3 = load_mod("_r43_bk3").NEW
FMM = load_mod("_r43_fm")
GLS = load_mod("_r43_gloss").GLOSS

CONT = {"book.tex": {}, "female.tex": {}, "male.tex": {}}
for d in (BK1, BK2, BK3):
    CONT["book.tex"].update(d)
CONT["book.tex"]["gloss"] = GLS
CONT["female.tex"] = dict(FMM.FEM)
CONT["male.tex"] = dict(FMM.MAL)

# (锚行号, 锚行原文(须与本行 strip 后全等), 内容 key)
PLAN = {
    "book.tex": [
        (847,   r"\section{性反应的个体差异与常见问题}",              "b1_tantra"),
        (21348, r"\section{性心理障碍与治疗}",                        "b2_refusal"),
        (25024, r"\section{周末夫妻与两地分居：维系性亲密的策略}",      "b3_stepfamily"),
        (25242, r"\section{年龄差伴侣：忘年恋的亲密与挑战}",            "b4_remarriage"),
        (25331, r"\section{性与多元关系}",                             "b5_migrant"),
        (27720, r"\section{残疾人的性需求与解决方案}",                  "b6_intersex"),
        (27724, r"\subsection{不同类型残疾人群的性健康特点}",           "b7_sensory"),
        (28052, r"\subsection{联合国 CRPD 公约与残疾人性权利}",         "b8_id_sexuality"),
        (28481, r"\section{服刑人员的性需求}",                         "b9_solitary"),
        (28811, r"\section{临终关怀与性亲密}",                         "b10_stoma"),
        (29269, r"\subsection{睡眠建议}",                              "b11_osa"),
        (52927, r"\subsection{老年期性传播感染的预防}",                 "b12_elderly_hiv"),
        (54142, r"\end{description}",                                  "gloss"),
    ],
    "female.tex": [
        (3649,  r"\section{性高潮障碍}",                  "f1_attach"),
        (4573,  r"\section{更年期后长期健康管理}",         "f2_postmeno"),
    ],
    "male.tex": [
        (4871,  r"\section{男性更年期（迟发性性腺功能减退症，LOH）}", "m1_osa"),
        (5066,  r"\section{男性心理健康与性功能}",                   "m2_attach"),
    ],
}

APPLY = len(sys.argv) > 1 and sys.argv[1] == "apply"
report = []

for fn in ("book.tex", "female.tex", "male.tex"):
    path = os.path.join(BASE, fn)
    with io.open(path, "r", encoding="utf-8", newline="") as f:
        raw = f.read()
    norm = raw.replace("\r\n", "\n").replace("\r", "\n")
    lines = [x.rstrip() for x in norm.split("\n")]
    plist = PLAN[fn]
    cdict = CONT[fn]

    # ---- 前置校验：锚唯一 + 锚行全等 + 内容存在 ----
    problems = []
    for lineno, anchor, key in plist:
        if key not in cdict:
            problems.append("内容缺失: %s" % key)
            continue
        hits = [i for i, ln in enumerate(lines, 1) if ln.strip() == anchor]
        if len(hits) != 1:
            problems.append("锚命中 %d 次(应=1): L%d %s -> %s" % (len(hits), lineno, anchor[:40], hits[:6]))
        if lines[lineno - 1].strip() != anchor:
            problems.append("行号与锚不匹配: L%d 实际=%r 期望=%r" % (lineno, lines[lineno - 1].strip()[:60], anchor[:60]))
    if problems:
        print("[ABORT] %s 校验失败：" % fn)
        for p in problems:
            print("   -", p)
        sys.exit(1)

    before = len(lines)
    # ---- 倒序插入 ----
    for lineno, anchor, key in sorted(plist, key=lambda x: -x[0]):
        content = cdict[key].replace("\r\n", "\n").replace("\r", "\n")
        clines = [x.rstrip() for x in content.rstrip("\n").split("\n")]
        lines[lineno - 1:lineno - 1] = [""] + clines + [""]

    out = "\r\n".join(lines)
    msg = "[%s] %d 处插入，%d -> %d 行 (+%d)" % (
        "WRITE" if APPLY else "DRY", len(plist), before, len(lines), len(lines) - before)
    print(msg)
    report.append(msg)

    if APPLY:
        with io.open(path, "w", encoding="utf-8", newline="") as f:
            f.write(out)

print("\n".join(report))
print("模式:", "已写盘" if APPLY else "dry-run（未改动文件）")
