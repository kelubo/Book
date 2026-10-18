# -*- coding: utf-8 -*-
"""r61b 探测：剥离"英文对照括号"后，按层级统计中文主体标题宽度。
判定：括号内容不含 CJK 汉字 -> 视为英文对照注，剥离并单独计宽；
      含汉字 -> 中文补充说明，保留计入主体。
"""
import os, re, unicodedata

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FILES = ["book.tex", "female.tex", "male.tex"]
LV = ["chapter", "section", "subsection", "subsubsection"]
HEAD_RE = re.compile(r"^\\(chapter|section|subsection|subsubsection)\*?\{")
CMD_RE = re.compile(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?(\{[^{}]*\})?")
PAREN_RE = re.compile(r"[（(]([^（）()]*)[）)]")


def cjk(s):
    return sum(1 for ch in s if "\u4e00" <= ch <= "\u9fff")


def width(s):
    w = 0
    for ch in s:
        w += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return w


def strip_cmd(s):
    for _ in range(6):
        new = CMD_RE.sub(lambda m: (m.group(2) or ""), s)
        if new == s:
            break
        s = new
    return s.replace("\\", "")


def split_title(txt):
    """返回 (中文主体, 被剥离的英文注拼接)"""
    notes = []
    def rep(m):
        inner = m.group(1)
        if cjk(inner) == 0:          # 纯英文/ASCII -> 英文对照注
            notes.append(m.group(0))
            return ""
        return m.group(0)
    body = PAREN_RE.sub(rep, txt)
    return body.strip(), " ".join(notes)


def scan(path):
    with open(path, encoding="utf-8", newline="") as f:
        lines = f.read().replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out = []
    for i, ln in enumerate(lines, 1):
        if not HEAD_RE.match(ln):
            continue
        head = ln.strip()
        pos = head.index("{")
        depth = 0
        for j in range(pos, len(head)):
            if head[j] == "{":
                depth += 1
            elif head[j] == "}":
                depth -= 1
                if depth == 0:
                    raw = head[pos + 1:j]
                    break
        else:
            raw = head[pos + 1:]
        level = head[1:head.index("{")].rstrip("*")
        txt = strip_cmd(raw)
        body, notes = split_title(txt)
        out.append(dict(ln=i, lv=level, raw=raw, txt=txt, body=body,
                        nw=width(notes), bw=width(body), tw=width(txt),
                        has_note=bool(notes)))
    return out


def main():
    allr = []
    for f in FILES:
        rows = scan(os.path.join(BASE, f))
        allr.append((f, rows))
        print("=" * 78)
        print(f, "总标题", len(rows))
        for lv in LV:
            sub = [r for r in rows if r["lv"] == lv]
            if not sub:
                continue
            bw = sorted(r["bw"] for r in sub)
            n = len(bw)
            def q(p):
                return bw[min(n - 1, int(n * p))]
            print("  %-14s n=%-5d 中文主体宽度 中位=%-3d p75=%-3d p90=%-3d p95=%-3d max=%d  带英文注=%d" % (
                lv, n, q(.5), q(.75), q(.9), q(.95), bw[-1],
                sum(1 for r in sub if r["has_note"])))
    print("=" * 78)
    TH = {"chapter": 18, "section": 16, "subsection": 17, "subsubsection": 15}
    for f, rows in allr:
        print("#### %s" % f)
        for lv in LV:
            cand = [r for r in rows if r["lv"] == lv and r["bw"] > TH[lv]]
            cand.sort(key=lambda x: -x["bw"])
            print("-- %s 中文主体>%d：%d 条" % (lv, TH[lv], len(cand)))
            for r in cand:
                tag = " [+英注%d]" % r["nw"] if r["has_note"] else ""
                print("   L%-6d bw=%-3d%s %s" % (r["ln"], r["bw"], tag, r["raw"]))
    print("=" * 78)
    # 中文主体最长 top 60（不分层）
    flat = []
    for f, rows in allr:
        for r in rows:
            flat.append((r["bw"], f, r))
    flat.sort(key=lambda x: -x[0])
    print("##### 三卷中文主体最长 top 60")
    for w, f, r in flat[:60]:
        tag = " [+英注%d]" % r["nw"] if r["has_note"] else ""
        print("  %-8s L%-6d %-13s bw=%-3d%s %s" % (f, r["ln"], r["lv"], w, tag, r["raw"]))


if __name__ == "__main__":
    main()
