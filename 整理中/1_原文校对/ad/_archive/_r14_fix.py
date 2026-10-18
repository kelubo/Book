# -*- coding: utf-8 -*-
"""Fix 1 stray end{itemize}->end{enumerate} at male.tex L2280; verify L2285 truncation;
compare brace deltas vs backup."""
import re

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
MALE = BASE + r"\male.tex"
BK_MALE = BASE + r"\_backup_术语替换" + r"\male.tex"
BK_BOOK = BASE + r"\_backup_术语替换" + r"\book.tex"
BOOK = BASE + r"\book.tex"

raw = open(MALE, "rb").read()
s = raw.decode("utf-8")
crlf = "\r\n" if b"\r\n" in raw else "\n"

# ---- full line 2285 ----
lines = s.split("\n")
print("L2285 repr:", repr(lines[2284]))

# ---- fix A: stray end{itemize} after the hypospadias enumerate ----
tgt = "射精功能障碍，影响生育" + crlf + "\\end{itemize}"
rep = "射精功能障碍，影响生育" + crlf + "\\end{enumerate}"
n = s.count(tgt)
print("fix A anchor count:", n)
if n == 1 and "射精功能障碍，影响生育" + crlf + "\\end{enumerate}" not in s:
    s = s.replace(tgt, rep, 1)
    open(MALE, "wb").write(s.encode("utf-8"))
    print("FIXED: end{itemize} -> end{enumerate} (male.tex)")
else:
    print("SKIP fix A (already fixed or anchor not unique)")

# ---- re-scan current male ----
def env_count(path):
    t = open(path, "rb").read().decode("utf-8")
    res = {}
    for e in ("itemize", "enumerate"):
        res[e] = (len(re.findall(r"\\begin\{" + e + r"\}", t)),
                  len(re.findall(r"\\end\{" + e + r"\}", t)))
    res["braces"] = (t.count("{"), t.count("}"))
    return res

for label, p in (("male current", MALE), ("male backup", BK_MALE),
                 ("book current", BOOK), ("book backup", BK_BOOK)):
    try:
        r = env_count(p)
        print("%-13s itemize=%s enumerate=%s braces=%s delta=%+d" % (
            label, r["itemize"], r["enumerate"], r["braces"],
            r["braces"][0] - r["braces"][1]))
    except FileNotFoundError:
        print(label, ": backup not found")
