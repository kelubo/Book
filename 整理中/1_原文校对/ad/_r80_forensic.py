# -*- coding: utf-8 -*-
"""核对：book@26ed24f 被移除的孕产章内容 vs female框架孕产章 + book旧区孕产章 的覆盖度"""
import io, re, subprocess

def norm_set(text):
    out = set()
    for x in text.split("\n"):
        s = re.sub(r"\s+", "", re.sub(r"(?<!\\)%.*$", "", x))
        s = s.strip("\\")
        if len(s) >= 6:  # 忽略过短的行（标题片段/符号）
            out.add(s)
    return out

def get(p):
    return subprocess.run(["git", "-C", "D:/Git/Book", "show", p],
                          capture_output=True, text=True, encoding="utf-8").stdout

b26 = get("26ed24f:整理中/1_原文校对/ad/book.tex").split("\n")
# 孕产章范围
a = next(i for i, x in enumerate(b26) if x.startswith("\\chapter{孕期与产后性健康}"))
b = next(i for i, x in enumerate(b26) if x.startswith("\\chapter{") and i > a + 5)
chap = "\n".join(b26[a:b])
print("被移除的孕产章: %d 行 (L%d-%d)" % (b - a, a + 1, b))

# female 框架孕产章 (L4244-4403)
fem = io.open("D:/Git/Book/整理中/1_原文校对/ad/2_female.tex", encoding="utf-8").read()
feml = fem.split("\n")
fw = "\n".join(feml[4243:4403])

# book 旧区孕产章
cur = io.open("D:/Git/Book/整理中/1_原文校对/ad/0_book.tex", encoding="utf-8").read()
curl = cur.split("\n")
oa = next(i for i, x in enumerate(curl) if x.startswith("\\chapter{孕期与产后性健康}"))
ob = next(i for i, x in enumerate(curl) if re.match(r"^\\chapter\{", x) and i > oa + 5)
old = "\n".join(curl[oa:ob])
print("book 旧区孕产章: %d 行 (L%d-%d)" % (ob - oa, oa + 1, ob))

S_chap = norm_set(chap)
cov = norm_set(fw) | norm_set(old)
uniq = [x for x in S_chap if x not in cov]
print("孕产章非空正文行(规范化): %d, 两来源未覆盖: %d" % (len(S_chap), len(uniq)))
for x in uniq[:25]:
    print("   " + x[:90])
