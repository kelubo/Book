"""r64a：从 book.log 提取所有未定义控制序列，并核对 preamble 已有的宏定义。

用途：第 0 步（补齐 preamble 宏定义）前的完整清单，避免只补 \\keyword 又冒出别的。
"""
import io, re, os, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"


def read(p):
    return io.open(p, encoding="utf-8", errors="replace").read()


log = read(os.path.join(BASE, "book.log"))
lines = log.split("\n")

print("=" * 78)
print("1) 日志中的错误行汇总")
print("=" * 78)
errs = [l.strip() for l in lines if l.startswith("!")]
c = collections.Counter(errs)
for k, v in c.most_common(20):
    print("  %3d x  %s" % (v, k[:110]))
print("  合计 ! 行：%d" % len(errs))

print()
print("=" * 78)
print("2) Undefined control sequence 明细（命令名 + 出现行号）")
print("=" * 78)
undef = collections.Counter()
where = collections.defaultdict(list)
for i, l in enumerate(lines):
    if "Undefined control sequence" in l:
        # 后续 1-3 行通常给出 offenders
        ctx = "\n".join(lines[i + 1:i + 4])
        for m in re.finditer(r"\\([a-zA-Z@]+)\s*$", lines[i + 1] if i + 1 < len(lines) else ""):
            undef[m.group(1)] += 1
            where[m.group(1)].append(i + 1)
        # 另一种格式：<recently read> \keyword
        for m in re.finditer(r"\\([a-zA-Z@]+)", ctx):
            undef[m.group(1)] += 1
            where[m.group(1)].append(i + 1)
print("  按命令名统计：")
for k, v in undef.most_common(30):
    print("    %-28s %3d 次   log 行 %s" % (k, v, where[k][:5]))
if not undef:
    print("  （日志中未解析到命令名，改从源文件扫描）")

print()
print("=" * 78)
print("3) 源码中 \\keyword 使用分布（三卷）")
print("=" * 78)
for fn in ["book.tex", "female.tex", "male.tex"]:
    p = os.path.join(BASE, fn)
    if not os.path.exists(p):
        continue
    src = read(p)
    n = len(re.findall(r"\\keyword\s*\{", src))
    ln = [i + 1 for i, l in enumerate(src.split("\n")) if "\\keyword" in l]
    rng = "L%d-L%d" % (ln[0], ln[-1]) if ln else "-"
    print("  %-11s %3d 处   %s" % (fn, n, rng))

print()
print("=" * 78)
print("4) preamble 已有宏定义（L1-112）")
print("=" * 78)
src = read(os.path.join(BASE, "book.tex"))
head = "\n".join(src.split("\n")[:113])
for i, l in enumerate(head.split("\n")):
    if re.search(r"\\(newcommand|renewcommand|providecommand|def|DeclareRobustCommand|NewDocumentCommand)\b", l):
        print("  L%-4d %s" % (i + 1, l.strip()[:100]))
