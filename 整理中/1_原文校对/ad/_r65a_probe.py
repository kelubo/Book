"""r65a：探测 book.tex 骨架区精确边界与逐章内容量。只读，不改文件。"""
import io, re, collections

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
P = BASE + r"\book.tex"

raw = io.open(P, encoding="utf-8", newline="").read()
lines = raw.replace("\r\n", "\n").split("\n")
N = len(lines)

HEAD = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{")
ANY_H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{")

def strip_tex(s):
    """取出 {..} 内的标题文本"""
    i = s.index("{")
    d = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            d += 1
        elif s[j] == "}":
            d -= 1
            if d == 0:
                return s[i + 1:j]
    return s[i + 1:]

# ---- 1) 找 backmatter / 旧区起点 ----
print("=== 关键分界行 ===")
for i, l in enumerate(lines):
    s = l.strip()
    if s in (r"\frontmatter", r"\mainmatter", r"\backmatter", r"\tableofcontents", r"\appendix"):
        print("L%-6d %s" % (i + 1, s))
for i, l in enumerate(lines):
    s = l.strip()
    if s.startswith(r"\part{") and re.search(r"(old|旧内容|旧)", s):
        print("L%-6d 旧区 part: %s" % (i + 1, s[:70]))
        if i > 700:
            break

# ---- 2) 骨架区 part/chapter 明细 ----
print("\n=== 骨架区（首章之前到旧区之前）逐章内容量 ===")
# 找第一个骨架 part
first_part = None
for i, l in enumerate(lines):
    if l.strip().startswith(r"\part{") and not re.search(r"(old|旧)", l.strip()):
        first_part = i
        break
# 找旧区起点
old_start = None
for i, l in enumerate(lines):
    if i > 700 and l.strip().startswith(r"\part{") and re.search(r"(old|旧)", l.strip()):
        old_start = i
        break
print("骨架起始 L%d，旧区起始 L%d" % (first_part + 1, (old_start + 1) if old_start else -1))

# 逐行扫描骨架区
struct = []  # (lineno, level, title)
for i in range(first_part, old_start if old_start else N):
    s = lines[i].strip()
    if s.startswith("%"):
        continue
    m = ANY_H.match(s)
    if m:
        struct.append((i, m.group(1), strip_tex(s)))

# 逐章正文统计
print("\n%-6s %-9s %-42s %6s %6s %7s %6s" % ("章行", "层级", "标题", "总行", "正文行", "注释行", "子节"))
part_cur = ""
rows = []
for k, (ln, lv, t) in enumerate(struct):
    if lv == "part":
        part_cur = t
        continue
    if lv != "chapter":
        continue
    end = struct[k + 1][0] if k + 1 < len(struct) else (old_start or N)
    seg = lines[ln + 1:end]
    body = [x for x in seg if x.strip() and not x.strip().startswith("%")]
    comments = [x for x in seg if x.strip().startswith("%")]
    subs = sum(1 for x in seg if re.match(r"^\s*\\(section|subsection)\*?\{", x))
    rows.append((ln, part_cur, t, end - ln, len(body), len(comments), subs))
    print("L%-5d %-9s %-42s %6d %6d %7d %6d" % (
        ln + 1, "ch", t[:40], end - ln, len(body), len(comments), subs))

print("\n骨架章数:", len(rows))
print("有正文的章:", sum(1 for r in rows if r[4] > 0), " / 纯占位:", sum(1 for r in rows if r[4] == 0))
print("骨架正文总行:", sum(r[4] for r in rows))
