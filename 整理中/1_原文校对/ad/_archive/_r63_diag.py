# -*- coding: utf-8 -*-
"""r63 诊断：book.tex 迁移期目录问题量化"""

import io, re, os, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
P = os.path.join(BASE, "book.tex")
lines = io.open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")

LV = re.compile(r"^\\(part|chapter|section|subsection)\*?\{")


def title(s):
    t = s[s.index("{") + 1:]
    return t[:t.rindex("}")] if "}" in t else t


ents = []  # (line, level, title)
for i, l in enumerate(lines):
    s = l.strip()
    if s.startswith("%"):
        continue
    m = LV.match(s)
    if m:
        ents.append((i + 1, m.group(1), title(s)))

# 骨架区边界：第一个 \part 到 \part{old}
first_part = next(ln for ln, lv, _ in ents if lv == "part")
old_part = next((ln for ln, lv, t in ents if lv == "part" and t.strip().lower() == "old"), None)
print("骨架区：L%d ~ L%d" % (first_part, old_part))
sk = [e for e in ents if first_part <= e[0] < old_part]
lg = [e for e in ents if old_part <= e[0]]
print("骨架区：part=%d chapter=%d section=%d subsection=%d" % (
    sum(1 for e in sk if e[1] == "part"), sum(1 for e in sk if e[1] == "chapter"),
    sum(1 for e in sk if e[1] == "section"), sum(1 for e in sk if e[1] == "subsection")))
print("旧区：part=%d chapter=%d section=%d subsection=%d" % (
    sum(1 for e in lg if e[1] == "part"), sum(1 for e in lg if e[1] == "chapter"),
    sum(1 for e in lg if e[1] == "section"), sum(1 for e in lg if e[1] == "subsection")))

# 骨架章：正文行数（去注释、去空行）与是否有 section
skch = [e for e in sk if e[1] == "chapter"]
bounds = [(skch[k][0], skch[k + 1][0] if k + 1 < len(skch) else old_part) for k in range(len(skch))]
empty, withsec, filled = [], [], []
for (ln, lv, t), (a, b) in zip(skch, bounds):
    body = [x for x in lines[a:b - 1] if x.strip() and not x.strip().startswith("%")]
    secs = sum(1 for x in lines[a:b - 1] if re.match(r"^\s*\\(section|subsection)\*?\{", x))
    if not body:
        empty.append((ln, t))
    else:
        filled.append((ln, t, len(body), secs))
print("\n骨架章 %d 个：纯占位（无正文行）%d 个；有正文 %d 个" % (len(skch), len(empty), len(filled)))
print("  有正文的骨架章（行数/节数）：")
for ln, t, n, s in filled:
    print("    L%-5d %-28s 正文%3d 行, 节 %d" % (ln, t[:28], n, s))
print("  纯占位章（前 40）：")
for ln, t in empty[:40]:
    print("    L%-5d %s" % (ln, t[:60]))

# 骨架中的空节
sksec = [(ln, t) for ln, lv, t in sk if lv == "section"]
print("\n骨架区 section 级标题 %d 个（会进目录）：%s" % (len(sksec), [t[:14] for _, t in sksec][:20]))

# 全篇号清单与重号
print("\n全部 \\part（按出现顺序）：")
for ln, lv, t in ents:
    if lv == "part":
        n = sum(1 for e in ents if e[1] == "chapter" and e[0] > ln)
        print("  L%-6d %s   （其后还有 %d 章）" % (ln, t[:44], n))

# 重名章
ch = [(ln, t) for ln, lv, t in ents if lv == "chapter"]
c = collections.Counter(t for _, t in ch)
dups = {k: [ln for ln, t in ch if t == k] for k, v in c.items() if v > 1}
print("\n重名章 %d 组（共 %d 个标题）：" % (len(dups), len(ch)))
for k, v in sorted(dups.items(), key=lambda x: -len(x[1])):
    print("  ×%d %-34s %s" % (len(v), k[:34], v))

# 旧区裸节
print("\n旧区各 part 下的“裸节”（part 下直接挂 section，无 chapter）：")
cur = None
cnt = collections.Counter()
bare = collections.defaultdict(list)
for ln, lv, t in lg:
    if lv == "part":
        cur = t
    elif lv == "section":
        cnt[cur] += 1
        bare[cur].append((ln, t))
    elif lv == "chapter":
        pass
for k, v in cnt.items():
    print("  %-26s 裸节 %2d 个：例 %s" % (k[:26], v, [x[1][:16] for x in bare[k][:4]]))

# toc 文件
for f in ["book.toc", "book.pdf", "book.log"]:
    p = os.path.join(BASE, f)
    if os.path.exists(p):
        import time
        print("\n%s  mtime=%s  size=%d" % (f, time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(p))), os.path.getsize(p)))
