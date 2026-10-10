# -*- coding: utf-8 -*-
# r60: 过长标题优化——45 处改为短名词短语（book 42 + female 3）
import io, sys, os
from collections import Counter

D = os.path.dirname(os.path.abspath(__file__))
APPLY = 'apply' in sys.argv

EDITS = [
# --- book.tex ---
('book.tex', 'BDSM 后的情绪跌落（Sub Drop / Top Drop）：机制、识别与照护', 'BDSM后的情绪跌落（Sub Drop / Top Drop）'),
('book.tex', '依恋类型与性：为什么“越靠近越想逃、越爱越焦虑”', '依恋类型与性'),
('book.tex', '如何相处：把“回避--追逐”的死循环拆开', '回避与焦虑型的相处策略'),
('book.tex', '偶遇性行为（一夜情 / 419）的安全守则：从“约”到“事后”', '偶遇性行为（一夜情 / 419）的安全守则'),
('book.tex', '多人性行为（3P / 群交 / 换偶）的安全与协商：当伴侣数大于二', '多人性行为（3P / 群交 / 换偶）的安全与协商'),
('book.tex', '造口者的亲密与性重建：从“造口袋”到“重新靠近”', '造口者的亲密与性重建'),
('book.tex', '烧伤、毁容与截肢者的性重建：当身体图式被改变', '烧伤、毁容与截肢者的性重建'),
('book.tex', '性爱意愿不一致与“无性婚姻”：协商、排期与出路', '性爱意愿不一致与“无性婚姻”'),
('book.tex', '间性人群的成年期支持：从被治疗的对象到主体', '间性人群的成年期支持'),
('book.tex', '睡眠呼吸暂停与勃起功能障碍：一条被忽视的链条', '睡眠呼吸暂停与勃起功能障碍'),
('book.tex', '性欲的节律、波动与节制：兼谈“戒色”迷思', '性欲的节律与“戒色”迷思'),
('book.tex', '色情与勃起功能障碍：“色情诱导 ED”之争与使用自查', '色情与勃起功能障碍'),
('book.tex', '甲状腺功能异常与性欲：被忽视的“代谢--情绪--性”三角', '甲状腺功能异常与性欲'),
('book.tex', '皮肤可见疾病与性自信：银屑病、湿疹、白癜风与暴露焦虑', '皮肤可见疾病与性自信'),
('book.tex', '性拒绝的处理：被拒绝方与拒绝方的对话机制', '性拒绝的处理与对话机制'),
('book.tex', '先理解：哀伤是正常的，没有“标准进度表”', '哀伤的正常进程'),
('book.tex', '失独家庭：当亲密被巨大的丧失冻结', '失独家庭的亲密重建'),
('book.tex', '背叛创伤：出轨被发现后，被背叛者会经历什么', '背叛创伤与被背叛者的反应'),
('book.tex', '修复或不修复：可以从哪些证据判断可行性', '关系修复的可行性判断'),
('book.tex', '婚姻内的同意：结婚证不是“永久同意书”', '婚姻内的同意'),
('book.tex', '为什么老年人也会感染——以及为什么没人提醒他们', '老年HIV感染的漏检与沟通盲区'),
('book.tex', '停用之后还能怀上吗：各类避孕方法的生育力恢复', '停用避孕后的生育力恢复'),
('book.tex', '漏服之后怎么办：口服避孕药的差错处理', '漏服避孕药的差错处理'),
('book.tex', '女性更年期的阴道干燥、性欲下降等问题的解决方案', '更年期性问题的应对'),
('book.tex', '跨性别者就医流程实务：从挂号到复诊的每一步', '跨性别者的就医流程'),
('book.tex', '同性伴侣的法律事务：现行法框架下的可用工具', '同性伴侣的法律事务'),
('book.tex', '女同性恋者获取性健康服务的障碍：从“不用看医生”到看得上医生', '女同性恋者获取性健康服务的障碍'),
('book.tex', '女性性少数者的社群与支持资源：一份可用的清单', '女性性少数者的社群与支持资源'),
('book.tex', '熟人强奸与“强奸迷思”：为什么大多数受害者认识加害者', '熟人强奸与“强奸迷思”'),
('book.tex', '强奸创伤综合征与报案决策：受害者会经历什么', '强奸创伤综合征与报案决策'),
('book.tex', '性行为的法律界限（如年龄、consent等）', '性行为的法律界限'),
('book.tex', '性科技产品（如智能玩具、远程亲密工具）的发展', '性科技产品的发展'),
('book.tex', '性活动对心血管健康、免疫系统、睡眠质量的益处', '性活动的健康益处'),
('book.tex', '性与疼痛缓解（如偏头痛、关节炎疼痛）', '性与疼痛缓解'),
('book.tex', 'LGBTQ+人群面临的性健康挑战（如歧视、艾滋病风险）', 'LGBTQ+人群的性健康挑战'),
('book.tex', '数字性教育在不同年龄群体中的应用策略', '数字性教育的分龄应用'),
('book.tex', '数字时代维护性心理健康的实用建议', '数字时代的性心理健康'),
('book.tex', '性健康 App 与可穿戴设备：实用指南与陷阱', '性健康App与可穿戴设备'),
('book.tex', '为什么有的人性欲强，有的人性欲弱', '性欲的个体差异'),
('book.tex', '就医时如何开口，以及事后的心理恢复', '就医沟通与事后心理恢复'),
('book.tex', '传统功法的安全审视：铁裆功、气功导引与提肛', '传统功法的安全审视'),
('book.tex', '壮阳中药与西药的相互作用：同服之前必读', '壮阳中药与西药的相互作用'),
# --- female.tex ---
('female.tex', '经期还能做什么：口交、肛交、自慰与“高潮能缓解痛经吗”', '经期的其他性行为方式'),
('female.tex', '阴吹（阴道排气）：常见的“尴尬声音”，通常无害', '阴吹（阴道排气）'),
('female.tex', '拒绝的艺术：如何温柔而坚定地说“不”', '拒绝的艺术'),
]

texts = {}
for f in ('book.tex', 'female.tex'):
    raw = io.open(os.path.join(D, f), encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in raw else '\n'
    texts[f] = [raw, nl, raw.split(nl), 0]

log = []
def norm(s):
    for q in ('“', '”', '„'):
        s = s.replace(q, '"')
    return s

for f, old, new in EDITS:
    lines = texts[f][2]
    oldsuf = norm('{%s}' % old)
    hits = [i for i, ln in enumerate(lines) if norm(ln.strip()).endswith(oldsuf) and ln.strip().startswith('\\')]
    if len(hits) != 1:
        sys.exit('%s 中 %r 命中 %d 次' % (f, old[:30], len(hits)))
    i = hits[0]
    # 保留行首命令，整体换标题（统一用全角弯引号）
    stripped = lines[i].strip()
    head = stripped[:stripped.index('{')]
    lines[i] = head + '{%s}' % new
    texts[f][3] += 1

for f in ('book.tex', 'female.tex'):
    raw, nl, lines, n = texts[f]
    ca = Counter(io.open(os.path.join(D, f), encoding='utf-8', newline='').read().split(nl))
    cb = Counter(lines)
    d = (cb - ca) + (ca - cb)
    exp = Counter()
    for ff, old, new in EDITS:
        if ff == f:
            for full in (old, new):
                for c in ('section', 'subsection', 'subsubsection'):
                    exp['\\%s{%s}' % (c, full)] += 0  # 占位，不计
    # 宽松校验：新旧行数一致，且每个旧标题行消失、新标题行出现
    if len(ca) != len(cb) or sum(ca.values()) != sum(cb.values()):
        sys.exit('%s 行数变化' % f)
    log.append('%s：替换 %d 处，行数 %d 不变' % (f, n, sum(cb.values())))
    for ff, old, new in EDITS:
        if ff == f:
            if any('{%s}' % old in ln for ln in lines if ln.strip().startswith('\\')):
                sys.exit('旧标题残留：%r' % old[:30])
            for bad in ('**', '？', '?'):
                if bad in new:
                    sys.exit('新标题含 %r：%r' % (bad, new))

if APPLY:
    for f in ('book.tex', 'female.tex'):
        raw, nl, lines, n = texts[f]
        io.open(os.path.join(D, f), 'w', encoding='utf-8', newline='').write(nl.join(lines))
    log.append('>>> 已写盘 book.tex / female.tex')
else:
    log.append('(dry-run；加 apply 落盘)')

io.open(os.path.join(D, '_r60_long_out.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(log))
print('\n'.join(log))
