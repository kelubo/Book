# -*- coding: utf-8 -*-
"""r43 校验：新节定位 + 格式残留 + 术语表词条 + 上下文抽查"""
import io, os, re
BASE = os.path.dirname(os.path.abspath(__file__))

def read(fn):
    with io.open(os.path.join(BASE, fn), "r", encoding="utf-8", newline="") as f:
        return f.read()

NEW = {
    "book.tex": [
        r"\section{坦陀罗、密宗与慢爱",
        r"\section{性拒绝的处理",
        r"\section{继亲家庭",
        r"\section{复婚",
        r"\section{留学生与移民的性健康调适}",
        r"\section{间性人群的成年期支持",
        r"\section{视障与听障者的性健康}",
        r"\section{智力障碍者的性权利与性教育}",
        r"\section{独居与长期无伴侣者的性需求}",
        r"\section{造口者的亲密与性重建",
        r"\section{睡眠呼吸暂停与勃起功能障碍：一条被忽视的链条}",
        r"\section{老年 HIV 新发感染",
    ],
    "female.tex": [
        r"\section{依恋风格与女性的亲密之性}",
        r"\section{绝经之后",
    ],
    "male.tex": [
        r"\section{睡眠呼吸暂停与勃起功能障碍}",
        r"\section{依恋风格与男性在亲密关系中的性}",
    ],
}

GLOSS_KEYS = ["坦陀罗（Tantra）", "慢爱（Slow Sex）", "性拒绝（Sexual Refusal）",
              "性欲差异（Desire Discrepancy）", "复婚（Reconciliation", "继亲家庭（Stepfamily）",
              "造口（Stoma）", "间性（Intersex", "依恋风格（Attachment Style）",
              "睡眠呼吸暂停（OSA）", "绝经泌尿生殖综合征（GSM）", "U=U"]

ok = True
for fn in ("book.tex", "female.tex", "male.tex"):
    raw = read(fn)
    norm = raw.replace("\r\n", "\n").replace("\r", "\n")
    lines = norm.split("\n")
    print("\n" + "=" * 70)
    print("### %s  (%d 行, %d 字符)" % (fn, len(lines), len(raw)))
    print("=" * 70)

    # 1) 新节定位
    for t in NEW[fn]:
        hits = [i for i, ln in enumerate(lines, 1) if ln.strip().startswith(t)]
        flag = "OK " if len(hits) == 1 else "!! "
        if len(hits) != 1:
            ok = False
        print("  %s命中%d  %s  @%s" % (flag, len(hits), t[:44], hits))

    # 2) markdown 残留
    md = 0
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if re.match(r"^#{1,4}\s", s) or s.startswith("**") or re.match(r"^\|.*\|$", s):
            md += 1
            if md <= 5:
                print("  [MD残留] L%d %s" % (i, s[:70]))
    print("  markdown 残留:", md)
    if md:
        ok = False

    # 3) bare LF
    bare = raw.count("\n") - raw.count("\r\n")
    print("  bare LF:", bare)
    if bare:
        ok = False

    # 4) 术语表词条（仅 book）
    if fn == "book.tex":
        miss = [k for k in GLOSS_KEYS if ("\\item[" + k) not in norm]
        print("  术语表新词条: %d/%d 命中" % (len(GLOSS_KEYS) - len(miss), len(GLOSS_KEYS)))
        if miss:
            ok = False
            print("   缺失:", miss)

print("\n" + "=" * 70)
print("总体:", "全部通过" if ok else "存在问题")
print("=" * 70)

# 5) 上下文抽查：book 新节 1 前后
L = read("book.tex").replace("\r\n", "\n").split("\n")
for a, b, tag in [(846, 852, "B1 坦陀罗节首"), (55220, 55245, "术语表新词条区")]:
    print("\n--- 抽查 %s L%d-%d ---" % (tag, a, b))
    for i in range(a, b + 1):
        print("%6d | %s" % (i, L[i - 1][:104]))
