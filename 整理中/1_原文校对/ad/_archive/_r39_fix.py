# -*- coding: utf-8 -*-
"""r39：三卷 Markdown 格式修复
Pass0: 漏 % 的目录树注释行（行首 * 且含 ├└│）补 %
Pass1: **x** -> \\textbf{x}（全局，替换后验证零残留）
Pass2: 行首 bullet（- / *，含缩进层级）连续群 -> 嵌套 itemize + \\item
       （数字列表 N. 行与命令/正文行断组，保持原样；群内空行删除；跨空行前瞻合并）
Pass3: Markdown 表格（| ... |）连续段 -> tabular + \\hline
先备份到 _backup_r39，转换后输出详细统计。
"""
import io, os, re, shutil

BASE = r'D:\Git\Book\整理中\1_原文校对\ad'
CR = '\r\n'
BAK = os.path.join(BASE, '_backup_r39')
os.makedirs(BAK, exist_ok=True)

FILES = ['book.tex', 'female.tex', 'male.tex']
BULLET_RE = re.compile(r'^(\s*)[-*]\s+(\S.*)$')
NUM_RE = re.compile(r'^\s*\d{1,2}[.、)]\s')
BOLD_RE = re.compile(r'\*\*([^*]+?)\*\*')

def bullet_indent(line):
    m = BULLET_RE.match(line)
    if not m:
        return None
    return len(m.group(1))

def rel_level(indent, base):
    d = indent - base
    if d <= 0:
        return 1
    return 1 + (d + 2) // 3

def fix_pass0_tree(lines):
    n = 0
    for i, l in enumerate(lines):
        st = l.strip()
        if st.startswith('*') and ('├' in st or '└' in st or '│' in st):
            lines[i] = '%' + l
            n += 1
    return n

def fix_pass1_bold(lines):
    n = 0
    for i, l in enumerate(lines):
        if '**' in l:
            new, k = BOLD_RE.subn(r'\\textbf{\1}', l)
            if k:
                lines[i] = new
                n += k
    return n

def fix_pass2_bullets(lines):
    """v3：栈式相对层级法。
    - 奇数缩进先归偶（3→2、5→4…杂值归并）
    - 维护已开层缩进栈：更深→开层、相等→同级、更浅→回退
    - itemize 上限 4 层，超过的深层项平铺在第 4 层（内容不丢），记录警告
    - 数字列表 N. 行与其他非空行断组，保持原样
    """
    stats = dict(groups=0, items=0, maxdepth=0, overlimit=[])
    out = []
    i, N = 0, len(lines)
    while i < N:
        if BULLET_RE.match(lines[i]):
            # 收集组：bullet 行 / 可合并的空行（前瞻）
            items = []          # (indent, content)
            j = i
            while j < N:
                m = BULLET_RE.match(lines[j])
                if m:
                    ind = len(m.group(1))
                    if ind % 2 == 1:
                        ind -= 1
                    items.append((ind, m.group(2).rstrip()))
                    j += 1
                    continue
                if lines[j].strip() == '':
                    k = j
                    while k < N and lines[k].strip() == '':
                        k += 1
                    if k < N and BULLET_RE.match(lines[k]):
                        j = k
                        continue
                    break
                break
            stats['groups'] += 1
            stack = []          # 各打开层的缩进
            for ind, content in items:
                stats['items'] += 1
                if not stack:
                    stack.append(ind)
                    out.append(' ' * ind + '\\begin{itemize}')
                elif ind > stack[-1]:
                    if len(stack) < 4:
                        stack.append(ind)
                        out.append(' ' * ind + '\\begin{itemize}')
                    else:
                        stats['overlimit'].append(i + 1)
                elif ind < stack[-1]:
                    while stack and stack[-1] > ind:
                        out.append(' ' * stack.pop() + '\\end{itemize}')
                    if not stack or stack[-1] < ind:
                        # 夹在已开层之间的杂值缩进：视为当前层同级
                        if stack and stack[-1] < ind:
                            pass
                    if not stack:
                        stack.append(ind)
                        out.append(' ' * ind + '\\begin{itemize}')
                stats['maxdepth'] = max(stats['maxdepth'], len(stack))
                out.append(' ' * ind + '\\item ' + content)
            while stack:
                out.append(' ' * stack.pop() + '\\end{itemize}')
            i = j
        else:
            out.append(lines[i])
            i += 1
    return out, stats

def fix_pass3_tables(lines):
    stats = dict(tables=0, rows=0, skipped=0, warnings=[])
    out = []
    i, N = 0, len(lines)
    ROW = re.compile(r'^\s*\|(.*)\|\s*$')
    SEP = re.compile(r'^:?-{2,}:?$')
    while i < N:
        m = ROW.match(lines[i])
        if m and i + 1 < N:
            m2 = ROW.match(lines[i+1])
            if m2:
                sep_cells = [c.strip() for c in m2.group(1).split('|')]
                if sep_cells and all(SEP.match(c) for c in sep_cells if c != ''):
                    header = [c.strip() for c in m.group(1).split('|')]
                    ncol = len(sep_cells)
                    # 收集数据行
                    j = i + 2
                    data = []
                    while j < N and ROW.match(lines[j]):
                        cells = [c.strip() for c in ROW.match(lines[j]).group(1).split('|')]
                        if len(cells) < ncol:
                            cells += [''] * (ncol - len(cells))
                        elif len(cells) > ncol:
                            stats['warnings'].append('L%d cell overflow %d>%d' % (j+1, len(cells), ncol))
                            cells = cells[:ncol-1] + [' '.join(cells[ncol-1:])]
                        data.append(cells)
                        j += 1
                    # 输出 tabular
                    stats['tables'] += 1
                    stats['rows'] += len(data)
                    out.append('\\begin{tabular}{' + 'l' * ncol + '}')
                    out.append('\\hline')
                    out.append(' & '.join('\\textbf{%s}' % c for c in header) + ' \\\\')
                    out.append('\\hline')
                    for cells in data:
                        cells = [c.replace('&', '\\&') for c in cells]
                        out.append(' & '.join(cells) + ' \\\\')
                        out.append('\\hline')
                    out.append('\\end{tabular}')
                    i = j
                    continue
        out.append(lines[i])
        i += 1
    return out, stats

total_stat = {}
for fn in FILES:
    p = os.path.join(BASE, fn)
    shutil.copy2(p, os.path.join(BAK, fn))
    lines = io.open(p, encoding='utf-8', newline='').read().split(CR)
    old_n = len(lines)

    n0 = fix_pass0_tree(lines)
    n1 = fix_pass1_bold(lines)
    residue_bold = sum(l.count('**') for l in lines)

    lines, s2 = fix_pass2_bullets(lines)

    residue_bullet = 0
    for l in lines:
        st = l.strip()
        if st and not st.startswith('%') and BULLET_RE.match(st):
            residue_bullet += 1

    lines, s3 = fix_pass3_tables(lines)
    residue_table = sum(1 for l in lines if l.strip().startswith('|') and not l.strip().startswith('%'))

    new_n = len(lines)
    io.open(p, 'w', encoding='utf-8', newline='').write(CR.join(lines))
    total_stat[fn] = (old_n, new_n)
    print('=== %s ===' % fn)
    print('  Pass0 漏%%注释补%%: %d' % n0)
    print('  Pass1 bold 转换: %d 对, ** 残留 = %d' % (n1, residue_bold))
    print('  Pass2 bullet 群: %d 组 / %d 项 / 最大层级 %d, bullet 残留 = %d, 超限截断行 = %d' % (
        s2['groups'], s2['items'], s2['maxdepth'], residue_bullet, len(s2['overlimit'])))
    if s2['overlimit']:
        print('    超限组起始行:', s2['overlimit'][:10])
    print('  Pass3 表格: %d 个 / %d 数据行, | 残留 = %d, 警告 %s' % (
        s3['tables'], s3['rows'], residue_table, s3['warnings'][:5]))
    print('  行数: %d -> %d' % (old_n, new_n))

print()
print('ALL DONE')
