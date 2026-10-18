# -*- coding: utf-8 -*-
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

files = [
    r"D:\Git\Book\整理中\1_原文校对\ad\0_book.tex",
    r"D:\Git\Book\整理中\1_原文校对\ad\1_male.tex",
    r"D:\Git\Book\整理中\1_原文校对\ad\2_female.tex",
]

begin_re = re.compile(r'\\begin\{([^}]*)\}')
end_re   = re.compile(r'\\end\{([^}]*)\}')

for f in files:
    text = open(f, encoding='utf-8').read()
    lines = text.split('\n')
    # strip comments (unescaped %)
    stripped = []
    for ln in lines:
        out = []
        i = 0
        while i < len(ln):
            c = ln[i]
            if c == '\\' and i+1 < len(ln):
                out.append(ln[i:i+2]); i += 2; continue
            if c == '%':
                break
            out.append(c); i += 1
        stripped.append(''.join(out))
    s = '\n'.join(stripped)

    # brace balance
    bal = 0; minbal = 0
    for c in s:
        if c == '{': bal += 1
        elif c == '}':
            bal -= 1
            if bal < minbal: minbal = bal

    # environments
    from collections import Counter
    bc = Counter(begin_re.findall(s))
    ec = Counter(end_re.findall(s))
    env_issues = []
    for env in set(bc) | set(ec):
        if bc[env] != ec[env]:
            env_issues.append((env, bc[env], ec[env]))

    # iffalse/fi
    iffalse = len(re.findall(r'\\iffalse\b', s))
    fi = len(re.findall(r'\\fi\b', s))

    # structure
    chapters = re.findall(r'\\chapter(?:\[[^\]]*\])?\{([^}]*)\}', s)
    n_sec = len(re.findall(r'\\section(?:\[[^\]]*\])?\{', s))
    n_sub = len(re.findall(r'\\subsection(?:\[[^\]]*\])?\{', s))
    n_subsub = len(re.findall(r'\\subsubsection(?:\[[^\]]*\])?\{', s))

    print("="*70)
    print(f.split('\\')[-1], f"  lines={len(lines)}")
    print(f"  brace balance: final={bal} min={minbal}  (0/0 = OK)")
    print(f"  envs mismatch : {env_issues if env_issues else 'none'}")
    print(f"  \\iffalse={iffalse}  \\fi={fi}")
    print(f"  chapters={len(chapters)} sections={n_sec} subsections={n_sub} subsubsections={n_subsub}")
    print("  chapter list:")
    for c in chapters:
        print("    -", c[:40])
