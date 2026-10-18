# -*- coding: utf-8 -*-
r"""r65：按 r63/r64 审查结论重建 book.tex 的前置目录骨架。

改动范围（仅两处，其余一切不动）：
  1) preamble：part/name={第,卷} -> {第,篇}（消除目录"第一卷 第一篇"双重编号）
  2) 骨架区：原说明注释 + 九篇 66 章骨架 -> 新的说明注释 + 九篇 53 章骨架
     - 《两性研究导论》全章正文（含 4 个 section）逐字保留
     - 各章来源注释由失效的 L#### 行号改为标题锚
     - 多来源合成的章补 \section 二级骨架
  3) backmatter / appendix / 附录 5 章 / 旧区（\part{old} 起）一字不动。

用法：python _r65_rebuild.py          # dry-run
      python _r65_rebuild.py apply    # 落盘
"""
import io, re, sys, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
P = BASE + r"\book.tex"
INTRO = "@@INTRO@@"

PART_OLD = "    part/name={第,卷},"
PART_NEW = "    part/name={第,篇},"

SKEL = r'''% ════════════════════════════════════════════════════════════════════════
%            全书目录结构（2026-09-20 重构版，供手动迁移内容用）
% ════════════════════════════════════════════════════════════════════════
% 使用说明：
%   1. 本结构为全书按主题去重后的目标目录，共九篇 53 章。
%   2. 每章下的注释标明该章的内容来源，一律以旧区的章节标题为锚——
%      直接搜索标题即可定位（旧版的 L#### 行号已随 9-20 的文件重写失效）。
%   3. 标注"去重"处存在两份以上近似内容，移入时择优保留一份。重复内容主要来自：
%      \part{旧内容}、\part{避孕与性健康}后半部分，
%      以及"生殖健康检查"章下的一批散落节。
%   4. 一个章下若列出多个 \section，表示该章由多份来源合成，按节对号入座。
%   5. 全部内容移入后：删除旧的 \part / \chapter / \section 标题行，
%      最后删除本骨架上方的说明注释。
% ════════════════════════════════════════════════════════════════════════

% ==================== 第一篇 ====================
\part{基础与生理}

@@INTRO@@

\chapter{性科学的沧桑}
% 移入："性科学的沧桑"整章

\chapter{性生理基础}
% 移入："性生理基础"整章（性反应周期 / 高潮差距 / 性激素 / 胚胎发育 / 梦交等）
% 去重："性生理反应"（与"性反应周期"重复，择优并入）

\chapter{生殖系统}
% 移入："男性生殖系统"、"女性生殖系统"、"生殖器官的额外知识"三节，升为章
%       （原挂在第七篇下，按主题应归本篇）
\section{男性生殖系统}
\section{女性生殖系统}
\section{生殖器官的额外知识}

\chapter{性取向与性别认同}
% 说明：原章名"性取向与性别认同的科学理解"已精简
\section{性取向}
\subsection{性取向的类型}
\subsection{性取向的生物学研究}
\subsection{性取向的心理社会研究}
\subsection{科学共识与争议}
\section{性别认同}
\subsection{性别认同的发展}
\subsection{跨性别与性别多元}
\subsection{性别焦虑}
\section{医疗与伦理}
\subsection{评估与诊断框架}
\subsection{激素治疗}
\subsection{性别肯定手术}
\subsection{心理支持与伦理争议}

% ==================== 第二篇 ====================
\part{性心理与情感}

\chapter{性心理与情感层面}
% 移入："性心理与情感层面"整章（性自尊 / 性焦虑 / 身体形象 / 性创伤 / 色情内容影响等）
% 可选："双相情感障碍"、"精神分裂症"、"自闭症谱系"三节亦可归第六篇"性功能障碍"章

\chapter{性心理发展与性偏好}
% 分工：本章讲"发展"与"偏好"；"性心理与情感层面"章讲情绪与自我认知，避免重叠
\section{性心理发展}
% 移入："性心理发展"（原在"婚姻与家庭性健康"章内）
\subsection{精神分析理论}
\subsection{现代发展理论}
\subsection{性脚本理论}
\section{性偏好与性幻想}
\subsection{常见性偏好}
\subsection{性幻想的功能}
\subsection{性偏好障碍}
\section{争议性诊断}
\subsection{性成瘾概念的历史}
\subsection{强迫性性行为}
\subsection{诊断争议与治疗}

\chapter{依恋、爱情与择偶}
\section{依恋理论}
\subsection{安全型依恋}
\subsection{焦虑型依恋}
\subsection{回避型依恋}
\subsection{混乱型依恋}
\section{爱情心理学}
\subsection{爱情类型理论}
\subsection{激情与亲密}
\subsection{承诺与维持}
\section{吸引力与择偶}
\subsection{外貌吸引力}
\subsection{相似性与互补性}
\subsection{择偶偏好}
\subsection{进化心理学解释及其争议}

\chapter{性与人际关系}
% 移入："性与人际关系"整章（依恋 / 无性婚姻 / 异地恋 / 多元关系 / 分手离婚等）
% 移入："性与亲密关系的维护"、"性沟通技巧的实践"（择优并入）
% 去重："性拒绝的处理与对话机制"

\chapter{情感亲密与沟通}
% 移入："情感亲密与沟通"节
% 移入："丁克家庭与亲密关系"节（或并入第三篇"婚姻与家庭性健康"）
% 区分：本章为伴侣间沟通；第八篇"性教育与沟通技巧"为教育场域的沟通

% ==================== 第三篇 ====================
\part{亲密关系与性实践}

\chapter{婚姻与家庭性健康}
% 移入："婚姻与家庭性健康"整章（通奸 / 非婚姻关系 / 育儿与夫妻关系 /
%       性幻想 / 助兴工具 / 充满性魅力的衣着等）
% 注意：该章内若干节按主题应移往别处——
%   "怀孕期间的性生活"        -> 第五篇"孕期与产后性健康"
%   "流产与避孕"              -> 第五篇"避孕方法"
%   "女性因绝经引起的症状"     -> 第六篇"性与年龄"
%   "性激素恢复方法"          -> 第六篇"性与年龄"（与更年期合并）
%   "性心理发展"              -> 第二篇"性心理发展与性偏好"

\chapter{新婚首夜}
% 移入："新婚首夜"节
% 去重："新婚首夜：心理、生理与实践"（择优合并）

\chapter{自慰}
% 移入："自慰"节
% 去重："自慰：生理、心理与健康"（择优合并）

\chapter{前戏与爱抚}
% 移入："前戏与爱抚"节（大块内容）
% 去重："前戏技巧"、"性生活的前奏曲"（两处重复，择优合并）

\chapter{性技巧与性辅助}
% 移入："性技巧与性辅助"整章（性敏感部位 / 亲吻抚摸 / 按摩 / 辅助工具）
% 说明：原列第一篇，按主题归本篇

\chapter{体位与姿势}
% 合并：体位基础 + 经典体位详解 + 变化与创新体位 + 特殊需求体位 + 体位与性体验
%       （原 5 章降为 5 节）
\section{体位基础}
\section{经典体位}
% 移入："经典体位详解"整章、"性交姿势"节（按体位拆分并入前两节）
% 去重："性交姿势与技巧"
\section{变化与创新体位}
\section{特殊需求体位}
\section{体位与性体验}
% 移入："体位与性体验"整章、"性高潮与满意度"
% 移入："影响性反应的因素与延长技巧"、"性爱过程的节奏"

\chapter{性爱的多样实践}
% 拆自原"性爱体验的深化与意外处理"，此为"实践"部分
% 移入："性爱体验的升华"、"口交的艺术与亲密意义"、"无插入性交"、"坦陀罗、密宗与慢爱"
%       （原挂第一篇"性生理基础"章下，按主题应移此）

\chapter{性爱中的意外与处理}
% 拆自原"性爱体验的深化与意外处理"，此为"问题与处理"部分
% 移入："性爱中的尴尬与意外"、"性行为中的意外损伤与家庭急救"、
%       "性交时长、频率与'正常'的标准"、"性爱前后的清洁与准备"
% 移入："性健康的其他重要方面"
% 去重："亲密关系中的性"

% ==================== 第四篇 ====================
\part{性传播疾病与防护}

\chapter{STI 概述与预防}
% 移入："STI 概述、流行现状与预防原则"（原直接挂在 part 下，升为章）

\chapter{细菌性 STI}
% 合并：梅毒 / 淋病 / 衣原体感染 / 软下疳（原 4 章降为 4 节）
\section{梅毒}
\section{淋病}
\section{衣原体感染}
% 原名"非淋病型尿道炎和衣原体感染"，已精简
\section{软下疳}

\chapter{病毒性 STI}
% 合并：艾滋病 / 生殖器疱疹 / 尖锐湿疣 / 乙型肝炎 / 丙型肝炎 / 猴痘 / COVID-19
%       （原 7 章降为 7 节）
\section{艾滋病}
\section{生殖器疱疹}
\section{尖锐湿疣}
% 含生殖器疣
\section{乙型肝炎}
\section{丙型肝炎}
\section{猴痘}
\section{COVID-19 与性健康}

\chapter{寄生虫性 STI}
% 合并：滴虫病 / 阴虱病（原 2 章降为 2 节）
\section{滴虫病}
\section{阴虱病}

\chapter{STI 筛查与伴侣告知}
% 移入："STI 筛查、检测与随访"、"性传播感染的检测与告知"（窗口期 / 伴侣告知 / 定期筛查）
% 去重：两个"性传播疾病与预防"章（与上面各病种节重复，择优并入对应病种）
% 去重："性传播疾病"节
% 移入："安全性行为与性健康防护"、"安全性行为教育"

% ==================== 第五篇 ====================
\part{避孕与生育}

\chapter{避孕方法}
% 合并：避孕方法总览 + 生殖健康与避孕的医学基础（避孕部分）
% 去重：两个"避孕方法"章（屏障 / 激素 / 紧急避孕 / 绝育 / 选择指南，择优合并为一份）
% 移入："流产与避孕"、"避孕方法与选择"
\section{激素避孕}
\section{屏障避孕}
\section{宫内节育器}
\section{永久避孕}
\section{紧急避孕}
\section{避孕效果与安全性比较}

\chapter{备孕、优生与不孕不育}
% 移入："备孕期间的性生活"、"优生优育与性健康的关系"、"不孕不育的原因与治疗选择"
\section{备孕与优生}
\section{不孕不育的原因}
\section{辅助生殖技术}
\section{代孕的伦理与法律}

\chapter{孕期与产后性健康}
% 移入："孕期与产后性健康"整章（含哺乳期性健康）、"怀孕期间的性生活"
% 去重："孕期与产后性健康"（旧内容，择优合并）

\chapter{流产与生殖伦理}
% 移入：流产的类型 / 医学处理 / 法律与伦理争议（原在"生殖健康与避孕的医学基础"章内）

% ==================== 第六篇 ====================
\part{性健康与医学}

\chapter{性健康核心要素}
% 移入："性健康核心要素与整体福祉"、"性欲与性渴望"
% 去重："性健康与整体福祉"、"性健康与整体健康"整章、"性健康与整体健康的关系"

\chapter{性功能障碍}
% 移入："性功能障碍"、"性功能障碍（续）"
% 移入："性心理障碍与治疗"、"性欲与性功能"
% 移入："性与心理健康的深度探讨"、"性与心理健康的专业干预"

\chapter{男性常见性健康问题}
% 移入："男性常见性健康问题"
% 去重：两处"男性常见性问题"（择优合并）

\chapter{女性常见性健康问题}
% 移入："女性常见性健康问题"
% 去重：两处"女性常见性问题"（择优合并）

\chapter{伴侣共同性问题}
% 移入："性健康自我评估问卷"、"夫妻共同性问题"、"性交后反应"、"精液过敏"、
%       "性心理问题与调适"

\chapter{性与物质使用}
% 移入："性与药物"、"性与饮酒"、"电子烟与性功能"、"物质使用障碍与性功能"
% 移入："药物与性功能速查"整章（抗抑郁药 / 降压药 / 激素类）

\chapter{慢性疾病与性健康}
% 移入："慢性疾病与性健康"（多发性硬化 / 糖尿病 / 心血管 / 肥胖 / 肝肾）
% 移入："肠道菌群-脑-性轴"、"衰老科学与性健康"、"表观遗传学与跨代遗传"、
%       "线粒体功能与性功能"、"精准医学在性医学中的应用"、"性健康药物与治疗"、
%       "性健康与衰老"
% 去重："性健康与慢性疾病"

\chapter{盆底健康与性功能}
% 移入："盆底健康与性功能"整章

\chapter{性与生活方式}
% 移入："性与生活方式"整章（饮食 / 运动 / 睡眠 / 压力 / 微塑料 / 光污染等）
% 移入："性与健康生活方式的关系"、"性与身体健康的关系"、"性与环境因素的关系"

\chapter{性与年龄}
% 移入："性与年龄"整章（青少年 / 成年 / 中年 / 老年，含老年 HIV）、
%       "老年期性健康"、"围绝经期与更年期健康"
% 去重："老年人的性需求"、"更年期与性健康"、"性健康与年龄相关变化的应对"、
%       "性与年龄发展的完整周期"

\chapter{定期检查与筛查}
% 移入："定期检查指南"、"年度性健康自查清单"
% 去重：三处"生殖健康检查"与"定期性健康检查"（择优合并为一份）
% 说明：与第四篇"STI 筛查与伴侣告知"分工——本章为全身/生殖系统常规体检，
%       该章专述 STI 筛查与伴侣告知

\chapter{私处整容}
% 移入："私处整容"节
% 去重："私处整容的考量"
% 说明：原列第七篇，属外科医学话题，按主题归本篇

\chapter{性健康误区与真相}
% 移入："性健康常见误区与真相"整章
% 去重：第一篇"两性研究导论"章内的"科学传播中的常见误区"（二者择一或明确分工）

% ==================== 第七篇 ====================
\part{社会、文化与多样性}

\chapter{性别社会学}
% 说明：本章为性别研究的社会学部分；学科史归第一篇"两性研究导论"，
%       平权运动与政策归本篇"性别平等与女权主义"
\section{性别社会化}
\subsection{家庭社会化}
\subsection{学校社会化}
\subsection{同伴社会化}
\subsection{媒体社会化}
\section{性别角色与刻板印象}
\subsection{传统性别角色}
\subsection{性别刻板印象}
\subsection{刻板印象的后果}
\section{家庭与婚姻制度}
\subsection{家庭结构变迁}
\subsection{婚姻制度类型}
\subsection{家务分工}
\section{劳动分工与性别}
\subsection{职场性别隔离}
\subsection{工资差距}
\subsection{职业发展障碍}
\section{教育与性别}
\subsection{教育机会差异}
\subsection{学科选择}
\subsection{教育成就}
\section{性别不平等与权力}
\subsection{权力理论}
\subsection{资源理论}
\subsection{父权制}
\section{交叉性理论}
\subsection{种族与性别}
\subsection{阶级与性别}
\subsection{性取向与性别}

\chapter{性别平等与女权主义}
\section{女权主义浪潮}
\subsection{第一次浪潮}
\subsection{第二次浪潮}
\subsection{第三次浪潮}
\subsection{第四次浪潮}
\section{女权主义理论流派}
\subsection{自由女权主义}
\subsection{激进女权主义}
\subsection{社会主义女权主义}
\subsection{后现代女权主义}
\subsection{交叉女权主义}
\section{性别平等指标}
\subsection{全球性别差距指数}
\subsection{性别发展指数}
\subsection{其他指标}
\section{男性运动与反性别运动}
\subsection{男性解放}
\subsection{父亲权利}
\subsection{反女权主义}
\subsection{争议与对话}

\chapter{LGBTQ+ 性健康}
% 移入："LGBTQ+ 性健康"节
% 去重：三处 LGBTQ+ 章（"LGBTQ+人群的性健康与权益"、"LGBTQ+人群的性健康"、
%       "LGBTQ+性健康"整章），择优合并
% 移入："性取向与性别认同"（旧内容）

\chapter{性偏好与多样性}
% 移入："性偏好与多样性"节（含 SM 的 SSC/RACK 框架）
% 去重："性偏好与性多样性"、"性偏好与性取向的亲密关系"
% 移入："初学者的SM指导"、"SM 是什么？"
% 说明：与第二篇"性心理发展与性偏好"分工——该章讲偏好如何形成，
%       本章讲偏好的类型与社群实践

\chapter{中国古代性学与传统中医}
% 移入："中国古代性学经典"节、"传统中医与性健康"整章
%       （理论基础 / 八益七损 / 中西医结合）、"中医与性健康"
% 去重："中国古代性学经典概述"

\chapter{性与文化、社会}
% 移入："性与文化、社会"整章（媒体 / 宗教 / 全球化 / 未来社会等）、"成人产业代表人物"
% 去重："性与文化"整章、"文化与性的探讨"整章
% 移入："性与文化、宗教的融合"、"性与艺术、媒体的表现"

\chapter{性与法律、伦理}
% 移入："性与法律、伦理"整章（性犯罪 / 性权利 / 性工作 / 战争性暴力 / 人口贩卖）
% 去重：三处"性与法律"（"性与法律：同意、权益与边界"、"性与法律"、"性与法律"）

\chapter{性与数字时代}
% 移入："性与数字时代"整章（在线约会 / 性隐私 / VR / 数字遗产等）、"性与科技的发展"
% 说明：数字技术对性的影响归本篇；第九篇"两性关系的未来"只留展望

% ==================== 第八篇 ====================
\part{特殊人群、教育与资源}

\chapter{性与特殊人群}
% 移入："性与特殊人群"整章（残障 / 视障听障 / 智力障碍 / 服刑 / 临终 / 造口等）
% 去重："残障人士的性健康"、"独居与长期无伴侣者的性需求"、"性少数群体的性需求"

\chapter{性教育与沟通技巧}
% 移入："性教育与沟通技巧"整章（性教育重要性 / 内容 / 方法 / 年龄段 / 沟通）
% 去重："性教育与青少年性健康"、"数字时代的性教育"、"数字技术在性教育中的应用"、
%       "性健康教育的全面覆盖"

\chapter{求助与资源导航}
% 移入：求助渠道 / 心理咨询 / 医疗机构导航
% 区分：与附录"权威资源与数据来源"分工——本章为求助渠道，附录为数据出处

% ==================== 第九篇 ====================
\part{未来与展望}

\chapter{两性关系的未来}
\section{技术变革}
\subsection{人工智能}
\subsection{虚拟现实}
\subsection{生物技术}
\section{家庭形态多样化}
\subsection{单身主义}
\subsection{丁克家庭}
\subsection{多元家庭}
\section{性别流动性}
\subsection{性别二元制的消解}
\subsection{性别多元认同}
\subsection{社会政策调整}
\section{全球化与本土化}
\subsection{全球性观念趋同}
\subsection{文化冲突}
\subsection{本土实践}
\section{政策展望}
\subsection{性别平等政策}
\subsection{家庭支持政策}
\subsection{性健康政策}
\section{研究前沿}
\subsection{神经科学}
\subsection{基因研究}
\subsection{社会网络分析}

\chapter{结语}
% 说明：原章名"结语：走向更平等与更健康的两性关系"已精简
\section{个体层面的建议}
\subsection{自我认知}
\subsection{沟通能力}
\subsection{尊重与边界}
\section{关系层面的建议}
\subsection{平等协商}
\subsection{情感支持}
\subsection{共同成长}
\section{社会层面的建议}
\subsection{制度保障}
\subsection{文化更新}
\subsection{教育普及}
\section{未来研究议题}
\subsection{理论整合}
\subsection{方法创新}
\subsection{政策评估}
'''


def load(p):
    raw = io.open(p, encoding="utf-8", newline="").read()
    crlf = raw.count("\r\n")
    return raw.replace("\r\n", "\n").split("\n"), crlf


def save(p, lines, crlf):
    nl = "\r\n" if crlf else "\n"
    io.open(p, "w", encoding="utf-8", newline="").write(nl.join(lines))


def main():
    apply = len(sys.argv) > 1 and sys.argv[1] == "apply"
    lines, crlf = load(P)
    n0 = len(lines)
    print("载入 %s：%d 行，换行 %s" % (os.path.basename(P), n0, "CRLF" if crlf else "LF"))

    # ---- 定位骨架区 ----
    anchor = "%                 新目录结构骨架（2026-09-19 生成，供手动迁移内容用）"
    assert lines.count(anchor) == 1, "骨架说明锚命中 %d 次" % lines.count(anchor)
    start = lines.index(anchor) - 1
    assert lines[start].strip().startswith("% ═"), "骨架起点不是分隔线：%r" % lines[start][:60]
    end = lines.index(r"\backmatter")
    assert end > start, "backmatter 位置异常"
    print("骨架区：L%d - L%d（%d 行）" % (start + 1, end, end - start))

    # ---- 提取《两性研究导论》正文（逐字保留）----
    i_intro = lines.index(r"\chapter{两性研究导论}")
    i_next = lines.index(r"\chapter{性科学的沧桑}")
    assert i_intro > start and i_next < end and i_intro < i_next
    intro = lines[i_intro:i_next]
    while intro and intro[-1].strip() == "":
        intro.pop()
    nsec = sum(1 for l in intro if l.strip().startswith(r"\section{"))
    nsub = sum(1 for l in intro if l.strip().startswith(r"\subsection{"))
    npar = sum(1 for l in intro if l.strip().startswith(r"\paragraph{"))
    print("导论章正文：%d 行（%d section / %d subsection / %d paragraph）"
          % (len(intro), nsec, nsub, npar))
    assert (nsec, nsub) == (4, 0) or nsec == 4, "导论章 section 数异常：%d" % nsec

    # ---- 组装新骨架 ----
    skel = SKEL.split("\n")
    assert skel.count(INTRO) == 1, "INTRO 占位符 %d 个" % skel.count(INTRO)
    out = []
    for l in skel:
        out.extend(intro if l == INTRO else [l])
    # 骨架与 \backmatter 之间留一空行
    while out and out[-1].strip() == "":
        out.pop()
    out.append("")

    new = lines[:start] + out + lines[end:]

    # ---- preamble 篇号 ----
    idx_p = [i for i, l in enumerate(new) if l == PART_OLD]
    assert len(idx_p) == 1, "preamble part/name 命中 %d 次" % len(idx_p)
    new[idx_p[0]] = PART_NEW

    # ---- 校验 ----
    k_old = lines.index(r"\part{old}")
    k_new = new.index(r"\part{old}")
    assert lines[k_old:] == new[k_new:], "旧区被改动！"
    print("旧区校验：L%d 起共 %d 行，逐字一致 ✓" % (k_old + 1, len(lines) - k_old))

    # 导论正文仍在
    j = new.index(r"\chapter{两性研究导论}")
    k = new.index(r"\chapter{性科学的沧桑}")
    assert new[j:j + len(intro)] == intro, "导论正文丢失（标题行后逐行比对失败）"
    print("导论正文校验：逐字保留 ✓")

    # 花括号配平（跳过注释行）
    def bal(ls):
        n = 0
        for l in ls:
            s = l.strip()
            if s.startswith("%"):
                continue
            n += s.count("{") - s.count("}")
        return n
    b0, b1 = bal(lines), bal(new)
    print("花括号净值：改前 %d -> 改后 %d" % (b0, b1))
    assert b0 == b1, "花括号配平被破坏"

    # 统计
    def cnt(ls, cmd):
        return sum(1 for l in ls[:ls.index(r"\backmatter")] if l.strip().startswith(cmd))
    for cmd in (r"\part{", r"\chapter{", r"\section{", r"\subsection{"):
        print("  骨架 %-14s %3d -> %3d" % (cmd, cnt(lines, cmd), cnt(new, cmd)))

    print("行数：%d -> %d（%+d）" % (n0, len(new), len(new) - n0))

    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        io.open(BASE + r"\_r65_preview.txt", "w", encoding="utf-8", newline="\n").write(
            "\n".join(new[start:start + len(out)]))
        print("预览已写入 _r65_preview.txt（%d 行）" % len(out))
        return

    if apply:
        save(P, new, crlf)
        print("已落盘。")
    else:
        print("[dry-run] 未写盘，加 apply 参数执行。")


if __name__ == "__main__":
    main()
