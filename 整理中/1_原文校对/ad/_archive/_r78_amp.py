# -*- coding: utf-8 -*-
"""r78: 扫描四卷标题行中未转义的 & （tabular 之外的坑）。report / apply."""
import re, sys, os

DIR = os.path.dirname(os.path.abspath(__file__))
FILES = ["book.tex", "female.tex", "male.tex", "position.tex"]

HEAD = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection|paragraph)\*?\{")
AMP = re.compile(r"(?<!\\)&")

def detect_nl(raw):
    crlf = raw.count("\r\n")
    lf = raw.count("\n")
    return "CRLF" if crlf > 0 and crlf == lf else ("LF" if crlf == 0 else "MIXED(crlf=%d/lf=%d)" % (crlf, lf))

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "report"
    for fn in FILES:
        p = os.path.join(DIR, fn)
        if not os.path.exists(p):
            print("[跳过] %s 不存在" % fn); continue
        raw = open(p, "r", encoding="utf-8", newline="").read()
        nl = detect_nl(raw)
        lines = raw.split("\n")
        hits = []
        for i, ln in enumerate(lines, 1):
            s = ln.rstrip("\r")
            # 剥掉注释部分
            code = re.sub(r"(?<!\\)%.*$", "", s)
            if HEAD.match(code) and AMP.search(code):
                hits.append((i, s))
        print("=== %s (%s, %d 行) 标题含未转义 & : %d 处 ===" % (fn, nl, len(lines), len(hits)))
        for i, s in hits:
            print("  L%d: %s" % (i, s))
        if mode == "apply" and hits:
            new = []
            for i, ln in enumerate(lines, 1):
                s = ln.rstrip("\r"); tail = "\r" if ln.endswith("\r") else ""
                # 只在标题行的 code 部分替换 & -> \&（不动 tabular，因为标题行不会含 tabular 分隔）
                if HEAD.match(re.sub(r"(?<!\\)%.*$", "", s)):
                    head_m = HEAD.match(re.sub(r"(?<!\\)%.*$", "", s))
                    # 找到注释起点
                    cm = re.search(r"(?<!\\)%", s)
                    stop = cm.start() if cm else len(s)
                    body, cmt = s[:stop], s[stop:]
                    body2 = AMP.sub(r"\\&", body)
                    new.append(body2 + cmt + tail)
                else:
                    new.append(ln)
            out = "\n".join(new)
            # 断言：花括号净值不变
            def braces(t): return t.count("{") - t.count("}")
            assert braces(out) == braces(raw), "花括号净值变了"
            assert detect_nl(out) == nl, "换行类型变了"
            assert out.count("\\begin{") == raw.count("\\begin{"), "环境数变了"
            # 幂等：再扫应无命中
            bak = p + ".r78bak"
            if not os.path.exists(bak):
                open(bak, "wb").write(raw.encode("utf-8"))
            open(p, "wb").write(out.encode("utf-8"))
            print("  -> 已写盘（备份 %s）" % os.path.basename(bak))

if __name__ == "__main__":
    main()
