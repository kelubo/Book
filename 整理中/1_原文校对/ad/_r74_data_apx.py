# -*- coding: utf-8 -*-
r"""r74 附录 5 章内容（章级插入，内容自带 \section/\subsection 结构）。

原则：
  1) 只列真实、可核查的文献、机构与量表（不杜撰条目、不编造页码）。
  2) 与正文同一文风：散文段 + itemize + 粉色 tcolorbox 收尾。
  3) 本草为骨架区附录章，原无任何小节；内容自带层级以改善结构。
"""
APX = {}

# ═══════════════ 1. 术语表 ═══════════════
APX["术语表"] = r"""\section{使用说明}

本术语表按主题分区，收录全书反复出现的核心术语。每条只给最短的可理解定义，深入内容请按提示查阅对应章节。术语的中文译名在学界尚未完全统一，条目中同时给出常见英文原词，便于读者在检索学术文献时对照。

需要提醒的是，术语的价值在于沟通而非标签。同一个词在不同学科、不同年代的用法可能不同（例如"性欲"在临床评估、心理研究与日常语言中的含义各有偏重），遇到分歧时，回到定义本身比争论词汇更有效。

\begin{itemize}
  \item \keyword{分区归类}：按生理、功能、感染、心理社会、法律伦理五区排列。
  \item \keyword{中英对照}：给出常见英文原词，便于检索文献。
  \item \keyword{定义从简}：术语表给最短定义，深入内容见对应章节。
\end{itemize}

\begin{tcolorbox}[colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]
术语表最好用的方式不是通读，而是\keyword{在阅读遇到生词时查一次}。查过两三次之后，你会发现书中反复出现的核心概念就那么几十个——把它们弄懂，全书的门槛就降下了一大半。
\end{tcolorbox}

\section{生理与解剖}

\begin{itemize}
  \item \keyword{性（sex）}：可指生物学意义上的性别（染色体、性腺、激素、解剖特征），也可指性行为；使用时通常需依语境区分。相关概念见"性与性别的基本区分"。
  \item \keyword{性别（gender）}：社会与文化对男性气质与女性气质的建构与期待，与生物性别不完全对应。
  \item \keyword{性别认同（gender identity）}：个体对自身性别的内在体验，可能与出生时被指派的性别一致或不一致。
  \item \keyword{性取向（sexual orientation）}：个体在情感与性方面受到吸引的对象性别模式，包括异性恋、同性恋、双性恋、泛性恋等。
  \item \keyword{间性（intersex）}：出生时性染色体、性腺、激素或生殖器发育不符合典型男女模式的状态，属正常的人类生物学变异。
  \item \keyword{性腺（gonads）}：睾丸与卵巢的统称，负责产生配子与性激素。
  \item \keyword{睾酮（testosterone）}：主要的雄激素，参与性欲、勃起功能、肌肉与骨量维持等多种生理过程。
  \item \keyword{雌激素（estrogen）}：主要的女性性激素，参与女性生殖系统发育、月经周期调节与骨代谢等。
  \item \keyword{孕激素（progesterone）}：与月经周期、妊娠维持密切相关的激素。
  \item \keyword{性反应周期}：描述性唤起过程的经典模型（兴奋、平台、高潮、消退四期，由马斯特斯与约翰逊提出），现多采用更具个体差异的循环模型。见"性生理基础"。
  \item \keyword{阴道润滑（vaginal lubrication）}：性唤起时阴道壁渗出液体以降低摩擦，是唤起程度的生理指标之一。
  \item \keyword{勃起（erection）}：阴茎海绵体充血导致体积与硬度增加的过程，涉及血管、神经与心理多重机制。
  \item \keyword{射精（ejaculation）}：精液经尿道排出的反射过程，与高潮通常同时发生但属不同机制。
  \item \keyword{盆底肌（pelvic floor muscles）}：支撑盆腔器官、参与排尿与性功能的肌群，可通过凯格尔训练强化。
  \item \keyword{会阴（perineum）}：外生殖器与肛门之间的区域。
  \item \keyword{阴蒂（clitoris）}：女性主要的性敏感器官，可见的阴蒂头只是其一小部分，大部分结构位于体内。
  \item \keyword{前列腺（prostate）}：男性附属腺体，分泌精液成分，其增生与炎症常影响排尿与性功能。
\end{itemize}

\section{性功能与健康问题}

\begin{itemize}
  \item \keyword{性欲（sexual desire）}：对性活动的兴趣与动机，受激素、情绪、关系与情境多重影响。
  \item \keyword{性唤起（sexual arousal）}：性兴奋时的生理与主观反应，包括生殖器充血与主观兴奋感——两者可以不一致。
  \item \keyword{性高潮（orgasm）}：性反应的高峰体验，常伴随节律性的肌肉收缩。
  \item \keyword{勃起功能障碍（erectile dysfunction, ED）}：持续难以获得或维持足以完成性交的勃起，常为血管、神经、内分泌与心理因素共同作用。
  \item \keyword{早泄（premature ejaculation, PE）}：射精过早且难以控制，并造成本人或伴侣的困扰。
  \item \keyword{延迟射精（delayed ejaculation）}：射精显著延迟或无法射精，常与药物、神经因素或心理因素相关。
  \item \keyword{性交疼痛（dyspareunia）}：性交过程中的疼痛，女性与男性均可能发生，需排查器质性与心理性因素。
  \item \keyword{阴道痉挛（vaginismus）}：盆底肌不自主收缩导致插入困难或疼痛，现多归入盆底肌张力相关障碍。
  \item \keyword{性欲低下障碍（hypoactive sexual desire disorder）}：性欲持续低下并引起显著痛苦。
  \item \keyword{性别烦躁（gender dysphoria）}：性别认同与出生指派性别之间的不一致所带来的显著痛苦，注意诊断针对的是痛苦而非认同本身。
  \item \keyword{性感集中训练（sensate focus）}：马斯特斯与约翰逊提出的以非生殖器接触为主的伴侣练习，用于减少表现焦虑、重建亲密感受。
  \item \keyword{性治疗（sex therapy）}：以心理与行为方法处理性问题的专业领域，常需伴侣共同参与。
  \item \keyword{PLISSIT 模型}：性健康干预的分级框架（许可、有限信息、具体建议、强化治疗），用于指导临床沟通的深度。
\end{itemize}

\section{感染与防护}

\begin{itemize}
  \item \keyword{性传播感染（STI）}：主要经性接触传播的感染，涵盖细菌、病毒、原虫与寄生虫等多种病原体。
  \item \keyword{无症状感染}：感染后无明显症状却具传染性的状态，是性传播感染扩散的重要原因。
  \item \keyword{窗口期}：从感染到检测方法能够检出之间的时间间隔；窗口期内阴性结果不能排除感染。
  \item \keyword{核酸扩增检测（NAAT）}：通过扩增病原体核酸进行检测的方法，敏感度通常高于显微镜与培养。
  \item \keyword{血清学检测}：检测血液中抗体或抗原的方法，常用于 HIV、梅毒、乙肝等。
  \item \keyword{暴露前预防（PrEP）}：HIV 阴性者按医嘱规律服用药物以预防感染的方式。
  \item \keyword{暴露后预防（PEP）}：可能暴露于 HIV 后短期内（最好在 72 小时内）开始服用阻断药物的措施。
  \item \keyword{伴侣告知}：将感染情况告知性伴侣以便其检测与治疗，是切断传播链的关键环节。
  \item \keyword{伴侣同治}：对可治愈的性传播感染，双方同时治疗以避免再感染。
  \item \keyword{滴度}：血清中抗体或抗原的浓度水平，梅毒随访常以滴度变化评估疗效。
  \item \keyword{安全套（condom）}：物理屏障避孕与防病工具，是唯一同时具有避孕与防病作用的方式。
  \item \keyword{紧急避孕}：事后补救措施，包括口服药物与含铜宫内节育器，越早使用越有效。
  \item \keyword{长效可逆避孕方法（LARC）}：如宫内节育器与皮下埋植剂，失败率低且不依赖使用者操作。
  \item \keyword{人乳头瘤病毒（HPV）}：最常见性传播感染之一，部分型别与宫颈癌等恶性肿瘤相关，可通过疫苗预防。
\end{itemize}

\section{心理、关系与社会}

\begin{itemize}
  \item \keyword{依恋类型}：个体在亲密关系中的互动模式，通常分为安全型、焦虑型、回避型与混乱型（对应对焦虑与回避两个维度）。
  \item \keyword{同意（consent）}：在知情、自愿、无胁迫前提下对性行为的积极表示，可随时撤回；沉默与僵住不构成同意。
  \item \keyword{边界}：个人对可接受与不可接受行为的界限，需被明确表达与尊重。
  \item \keyword{同意的能力}：作出有效同意所需的理解与自主表达能力，受年龄、意识状态与认知功能影响。
  \item \keyword{亲密伴侣暴力}：现任或前任伴侣间的身体、性、精神或经济控制行为。
  \item \keyword{同意教育}与\keyword{旁观者干预}：性暴力预防的两个主要方向（见"暴力、安全与保护"）。
  \item \keyword{性少数}：性取向或性别认同属于少数群体者，包括同性恋、双性恋、跨性别、间性等（相关议题见"LGBTQ+ 性健康"）。
  \item \keyword{少数群体压力}：因处于少数地位而承受的偏见预期、身份管理与歧视经历所带来的持续压力，是理解性少数健康差异的核心框架。
  \item \keyword{交叉性（intersectionality）}：多重身份（性别、阶层、族裔、残障、性取向等）叠加影响个体处境的分析框架。
  \item \keyword{性脚本}：社会文化提供的关于"性应该如何发生"的默示模板，影响期待与行为。
  \item \keyword{污名}：对某类特征或行为的负面社会评价，及其导致的社会排斥与自我贬低。
  \item \keyword{去污名}：通过语言、制度与服务设计减少污名影响的实践。
  \item \keyword{性健康素养}：获取、理解、评估并运用性健康信息的能力，常体现为具体行为而非知识点数量。
  \item \keyword{性健康}：世界卫生组织将其定义为与性相关的身体、情感、精神与社会福祉状态，而不仅是没有疾病。
  \item \keyword{数字性暴力}：借助数字技术实施的性侵害形态，包括未经同意传播私密影像、深度伪造性内容、网络性骚扰与勒索。
  \item \keyword{深度伪造（deepfake）}：用人工智能合成或篡改的人脸与影像，被用于制作伪造的性内容时构成严重侵害。
\end{itemize}

\section{法律、伦理与权利}

\begin{itemize}
  \item \keyword{同意年龄}：法律认定可以作出有效性同意的年龄，低于该年龄的同意无效。
  \item \keyword{婚内强奸}：婚姻关系内的强制性行为；现代立法普遍承认婚姻不转移性同意权。
  \item \keyword{性骚扰}：具有性意味、不受欢迎的言语、肢体或视觉行为；含以工作利益交换的交换型与制造敌意环境的敌意型两类。
  \item \keyword{人身安全保护令}：依《反家庭暴力法》向法院申请的民事保护措施，可禁止接触、跟踪与骚扰。
  \item \keyword{家庭暴力告诫书}：公安机关对情节较轻的家暴行为出具的书面告诫，具有后续诉讼中的证据效力。
  \item \keyword{强制报告制度}：密切接触未成年人的单位与人员发现未成年人遭受或疑似遭受侵害时，负有向公安机关报告的法定义务。
  \item \keyword{性权利}：与性相关的各项基本权利的总称，包括身体自主、性自主、平等与非歧视、性健康权、隐私权与教育权等。参见《性权利宣言》。
  \item \keyword{人权法中的性权利}：通过既有国际人权条约（人身安全、健康权、平等与非歧视、私生活保护等条款）间接保障的性权利。
  \item \keyword{数据隐私}：性健康记录、性取向与检测结果等敏感个人信息的保护规则。
  \item \keyword{医学伦理四原则}：尊重自主、行善、不伤害与公正——性健康服务中的知情同意与保密义务均由此展开。
\end{itemize}

\begin{tcolorbox}[colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]
术语是工具，不是门槛。\keyword{若某个术语让你感到被冒犯（无论它用于你自己还是他人），你有权不接受它}——语言会变，而人对自身处境的判断权，始终属于自己。
\end{tcolorbox}
"""

# ═══════════════ 2. 参考文献 ═══════════════
APX["参考文献"] = r"""\section{使用说明}

本附录列出本书写作中参考的核心文献与权威资料，按类型分组，以便读者进一步查阅。所列条目均为真实、可公开检索的著作、标准或指导文件；\keyword{版本、页码与译本可能随时间变化，引用时请以最新版本为准}。

排列原则有三：经典奠基性著作优先（因其持续被引用与检验）、标准与指导文件单列（因其具有规范效力）、中文文献单列（便于国内读者获取）。

\begin{itemize}
  \item \keyword{只列真实可查条目}：不收录无法核实的资料来源。
  \item \keyword{分类排列}：奠基著作、标准与指南、中文文献、工具书与量表分别成组。
  \item \keyword{版本提示}：条目信息以出版时为准，引用须核对最新版本。
\end{itemize}

\begin{tcolorbox}[colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]
读文献的一个实用习惯：\keyword{先读综述（review），再读单篇研究}。综述会把某个议题上相互矛盾的研究摆在一起，告诉你哪里已经清楚、哪里还有争议——这比一篇孤立的"最新发现"更能帮你建立判断力。
\end{tcolorbox}

\section{奠基性著作}

\subsection{性学与性研究的奠基文献}

\begin{itemize}
  \item Kinsey AC, Pomeroy WB, Martin CE. \textit{Sexual Behavior in the Human Male}. Philadelphia: W. B. Saunders, 1948.
  \item Kinsey AC, Pomeroy WB, Martin CE, Gebhard PH. \textit{Sexual Behavior in the Human Female}. Philadelphia: W. B. Saunders, 1953.
  \item Masters WH, Johnson VE. \textit{Human Sexual Response}. Boston: Little, Brown, 1966.（性反应四期模型的原始出处）
  \item Masters WH, Johnson VE. \textit{Human Sexual Inadequacy}. Boston: Little, Brown, 1970.（性治疗与性感集中训练的开创性著作）
  \item Kaplan HS. \textit{The New Sex Therapy}. New York: Brunner/Mazel, 1974.（性欲—唤起—高潮三阶段模型）
  \item Annon JS. \textit{The Behavioral Treatment of Sexual Problems}. Honolulu: Kapiolani Health Services, 1974–1976.（PLISSIT 分级干预模型的出处）
  \item Basson R. The female sexual response: a different model. \textit{Journal of Sex \& Marital Therapy}, 2000, 26(1): 51–65.（女性性反应循环模型）
\end{itemize}

\subsection{依恋与关系研究}

\begin{itemize}
  \item Bowlby J. \textit{Attachment and Loss}（三卷）. London: Hogarth Press, 1969–1980.
  \item Ainsworth MDS, Blehar MC, Waters E, Wall S. \textit{Patterns of Attachment}. Hillsdale: Erlbaum, 1978.（陌生情境实验）
  \item Brennan KA, Clark CL, Shaver PR. Self-report measurement of adult attachment. In: Simpson JA, Rholes WS (eds). \textit{Attachment Theory and Close Relationships}. New York: Guilford Press, 1998.（ECR 量表）
\end{itemize}

\subsection{性取向与性别研究}

\begin{itemize}
  \item Klein F, Sepekoff B, Wolf TJ. Sexual orientation: a multi-variable dynamic process. \textit{Journal of Homosexuality}, 1985, 11(1–2): 35–49.（性取向多维网格 KSOG）
  \item Rubin G. The traffic in women: notes on the "political economy" of sex. In: Reiter RR (ed). \textit{Toward an Anthropology of Women}. New York: Monthly Review Press, 1975.（"性/性别系统"概念）
  \item Oakley A. \textit{Sex, Gender and Society}. London: Temple Smith, 1972.（社会性别与生理性别的区分）
\end{itemize}

\section{标准、指南与权威资料}

\subsection{分类标准与诊断系统}

\begin{itemize}
  \item World Health Organization. \textit{International Classification of Diseases, 11th Revision (ICD-11)}. Geneva: WHO, 2019/2022.（性健康相关章节与强迫性性行为障碍的收录）
  \item American Psychiatric Association. \textit{Diagnostic and Statistical Manual of Mental Disorders, Fifth Edition (DSM-5)}. Arlington: APA, 2013；\textit{DSM-5-TR}, 2022.（性功能失调与性别烦躁的诊断标准）
\end{itemize}

\subsection{公共卫生与性教育指导文件}

\begin{itemize}
  \item World Health Organization. \textit{Sexual health and its linkages to reproductive health: an operational approach}. Geneva: WHO, 2017.
  \item World Health Organization. \textit{Consolidated guidelines on HIV prevention, testing, treatment, service delivery and monitoring}. Geneva: WHO, 2021.
  \item UNESCO, UNAIDS, UNFPA, UNICEF, UN Women, WHO. \textit{International Technical Guidance on Sexuality Education: An evidence-informed approach}（修订版）. Paris: UNESCO, 2018.
  \item World Association for Sexual Health. \textit{Declaration of Sexual Rights}. 2014.（性权利的国际框架文件）
  \item United Nations. \textit{Convention on the Rights of Persons with Disabilities}. 2006.（残障者性与生殖健康权、家庭权的依据）
  \item United Nations. \textit{Convention on the Elimination of All Forms of Discrimination against Women (CEDAW)}. 1979.
\end{itemize}

\subsection{专业学会与其他权威来源}

\begin{itemize}
  \item 中华医学会相关分会（泌尿外科学分会、皮肤性病学分会、妇产科学分会等）发布的诊疗指南与专家共识。
  \item 中国疾病预防控制中心及其性病艾滋病预防控制中心发布的疫情报告、技术指南与防治规范。
  \item 国家卫生健康委员会及各级卫生行政部门发布的规范性文件与技术服务规范。
  \item 美国疾病控制与预防中心（CDC）发布的性传播感染治疗指南（\textit{STI Treatment Guidelines}），为国际常用参照。
  \item Cochrane Library 系统综述库：用于核查具体干预措施的证据强度。
  \item PubMed / MEDLINE、中国知网与万方数据：用于检索原始研究文献。
\end{itemize}

\section{中文文献}

\begin{itemize}
  \item 马王堆汉墓帛书整理小组.《马王堆汉墓帛书（肆）》. 北京：文物出版社，1985.（含《十问》《合阴阳》《天下至道谈》等古代性学文献）
  \item 孙思邈.《备急千金要方》（含《房中补益》篇）. 唐代。（现存最完整的医家房中论述之一）
  \item 高罗佩（R. H. van Gulik）.《中国古代房内考》. 中译本，上海：上海人民出版社，1990.（原书 \textit{Sexual Life in Ancient China}, Leiden: Brill, 1961）
  \item 刘达临.《中国古代性文化》. 银川：宁夏人民出版社，1993.
  \item 江晓原.《性张力下的中国人》. 上海：上海人民出版社，1995.
  \item 潘绥铭、黄盈盈.《性之变：21 世纪中国人的性生活》. 北京：中国人民大学出版社，2013.
  \item 李银河.《中国人的性爱与婚姻》. 河南人民出版社，1991（后有多个修订版本）.
\end{itemize}

\section{法律法规}

\begin{itemize}
  \item 《中华人民共和国反家庭暴力法》（2015 年通过，2016 年施行）——确立告诫书与人身安全保护令制度。
  \item 《中华人民共和国民法典》（2020 年通过）——人格权编规定性骚扰的界定、单位防治义务与隐私权保护。
  \item 《中华人民共和国妇女权益保障法》（2022 年修订）——细化性骚扰防治与用人单位义务。
  \item 《中华人民共和国未成年人保护法》（2020 年修订，2021 年施行）——确立强制报告制度与密切接触未成年人单位的义务。
  \item 《中华人民共和国刑法》及其修正案（含《刑法修正案（十一）》，2020 年）——强奸、强制猥亵、负有照护职责人员性侵等罪名。
  \item 《中华人民共和国传染病防治法》与《艾滋病防治条例》——免费咨询检测、免费抗病毒治疗与反歧视原则。
\end{itemize}

\begin{tcolorbox}[colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]
引用文献时有两条底线：\keyword{只引用你真正核对过的来源，不确定的条目注明"待核实"}。在性健康这类容易流传错误的领域，一份严谨的参考文献，本身就是对读者最实在的保护。
\end{tcolorbox}
"""

# ═══════════════ 3. 索引 ═══════════════
APX["索引"] = r"""\section{使用说明}

本索引按主题归类，指向相关章节，供读者按兴趣或问题定位内容。索引条目以\keyword{概念与主题词}为主，而非仅收录术语；同一主题下的多个相关条目集中排列，便于比较阅读。

需要说明的是，本索引采用\keyword{主题—章节}的形式，而非页码索引。原因有二：其一，本书的多处内容在不同章节中有交叉论述（如同一议题在生理、心理与社会层面各有章节），主题归类比页码罗列更便于查阅；其二，正式的页码索引需在排版定稿后由排版系统自动生成，届时会与本节互为补充。

\begin{itemize}
  \item \keyword{主题—章节定位}：按主题查，比按页码查更适合交叉论述的内容。
  \item \keyword{同主题集中}：相关条目并排，便于比较。
  \item \keyword{与页码索引互补}：定稿后可由排版系统自动生成页码索引。
\end{itemize}

\begin{tcolorbox}[colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]
索引最好的用法是\keyword{从一个问题出发}：你对什么困惑，就顺着相关主题把邻近章节一起读。亲密与性健康的问题很少是单一领域的——顺着一串相关条目读下去，常常比单点查阅更接近答案。
\end{tcolorbox}

\section{身体、发育与生理}

\begin{itemize}
  \item 生殖器官的解剖与个体差异 —— 见"生殖器官的个体差异与护理"。
  \item 男性生殖系统结构与功能 —— 见"男性解剖与生理"相关章；并见"男性性功能与男科疾病"。
  \item 女性生殖系统结构与功能 —— 见"女性解剖与生理"相关章；并见"女性性功能"相关章。
  \item 性发育与青春期（含初潮与遗精） —— 见"性发育与青春期"。
  \item 性反应周期与性别差异 —— 见"性生理基础"。
  \item 激素与性欲、月经周期 —— 见"性生理基础"；并见"月经与妇科健康"相关章。
  \item 盆底健康与性功能 —— 见"盆底健康与性功能"。
  \item 更年期与性 —— 见"性与年龄"；并见女性卷"更年期"相关章。
\end{itemize}

\section{性功能与性问题}

\begin{itemize}
  \item 勃起功能障碍 —— 见"性功能障碍"。
  \item 早泄与射精控制 —— 见"性功能障碍"；并见男科相关章。
  \item 性欲低下与性欲落差 —— 见"性功能障碍"；并见"情感亲密与沟通"。
  \item 性交疼痛与插入困难 —— 见"性功能障碍"；并见女性卷相关章。
  \item 性功能与慢性疾病、药物 —— 见"慢性疾病与性健康"；并见"性与物质使用"。
  \item 性治疗与性康复 —— 见"性治疗与性康复"。
  \item 性健康前沿研究 —— 见"性健康前沿研究"。
\end{itemize}

\section{避孕、生育与感染防护}

\begin{itemize}
  \item 避孕方法总览与选择 —— 见"避孕方法"。
  \item 紧急避孕 —— 见"避孕方法"；并见"紧急情况应对指南"。
  \item 备孕与优生 —— 见"备孕、优生与不孕不育"。
  \item 性传播感染的种类与防护 —— 见"STI 概述与预防"及细菌性、病毒性、寄生虫性 STI 各章。
  \item HIV 的预防（安全套、PrEP、PEP）与治疗 —— 见"病毒性 STI"；并见"紧急情况应对指南"。
  \item 筛查与伴侣告知 —— 见"STI 筛查与伴侣告知"。
  \item 疫苗接种（HPV、乙肝） —— 见"病毒性 STI"；并见"性与公共卫生"。
\end{itemize}

\section{心理、情感与关系}

\begin{itemize}
  \item 性心理的发展与性偏好形成 —— 见"性心理发展与性偏好"。
  \item 依恋类型与亲密关系 —— 见"依恋、爱情与择偶"。
  \item 情感沟通与性沟通 —— 见"情感亲密与沟通"；并见"性沟通的技巧与实践"。
  \item 前戏与爱抚、性技巧 —— 见"前戏与爱抚"与"性技巧与性辅助"。
  \item 体位与姿势（含怀孕、老年、残障的适配） —— 见"体位与姿势"。
  \item 自慰（含相关迷思） —— 见"自慰"。
  \item 婚姻与家庭性健康 —— 见"婚姻与家庭性健康"。
  \item 家庭形态的多样性（单亲、重组、多元家庭） —— 见"家庭形态的多样性"。
  \item 性偏好与多样性、BDSM 与安全框架 —— 见"性偏好与多样性"。
\end{itemize}

\section{人群与生命阶段}

\begin{itemize}
  \item 青少年性健康与性教育 —— 见"不同年龄段的性教育"；并见"性发育与青春期"。
  \item 中老年性健康 —— 见"性与年龄"。
  \item 残障人士的性健康 —— 见"性与特殊人群"。
  \item 性少数人群的健康需求 —— 见"LGBTQ+ 性健康"。
  \item 长期无伴侣与独居人群 —— 见"性与特殊人群"。
  \item 临终关怀与造口人群 —— 见"性与特殊人群"。
  \item 服刑人员与封闭环境中的性 —— 见"性与特殊人群"。
\end{itemize}

\section{安全、暴力与法律}

\begin{itemize}
  \item 同意与同意能力 —— 见"性行为的法律界限与同意"。
  \item 性骚扰（职场）与维权路径 —— 见"职场性骚扰与权力不对等"。
  \item 亲密伴侣暴力与约会暴力 —— 见"亲密伴侣暴力"与"约会暴力与尾随骚扰"。
  \item 儿童性侵害的识别与处置 —— 见"儿童性侵害的识别与应对"。
  \item 冲突与灾难情境中的性暴力 —— 见"冲突与灾难情境中的性暴力"。
  \item 安全计划与法律保护工具 —— 见"安全计划与自我保护"。
  \item 性工作、人口贩卖与色情监管 —— 见"性工作、人口贩卖与色情监管"。
  \item 性权利与人权法保障 —— 见"性权利与法律保障"。
\end{itemize}

\section{社会、文化与数字技术}

\begin{itemize}
  \item 性观念的历史演变与性解放 —— 见"性观念的历史演变"。
  \item 宗教与性 —— 见"宗教与性"。
  \item 媒体、艺术与性的呈现 —— 见"媒体、艺术与性的呈现"。
  \item 跨文化与全球化 —— 见"跨文化与全球化"。
  \item 中国古代性学经典与房中术 —— 见"中国古代性学经典"。
  \item 传统中医与性健康 —— 见"传统中医与性健康"。
  \item 性别社会学与性别平等 —— 见"性别社会学"与"性别平等与女权主义"。
  \item 在线约会与数字亲密 —— 见"在线约会与数字亲密"。
  \item 性隐私、私密影像与深度伪造 —— 见"性隐私与影像安全"。
  \item 网络色情与内容治理 —— 见"网络色情与内容治理"。
  \item 虚拟现实、人工智能与数字遗产 —— 见"虚拟现实、人工智能与数字遗产"。
\end{itemize}

\section{服务、制度与求助}

\begin{itemize}
  \item 性健康教育的目标与内容框架 —— 见"性教育的重要性与内容"。
  \item 学校、家庭、社区与媒体性教育 —— 见"性教育的方法"。
  \item 求助渠道（医疗、心理、公益、社群） —— 见"求助渠道"。
  \item 医院科室选择与就诊准备 —— 见"医疗机构与就诊导航"。
  \item 紧急情况应对（性暴力、避孕失败、暴露后阻断、心理危机） —— 见"紧急情况应对指南"。
  \item 公共卫生视角与服务体系 —— 见"性与公共卫生"。
  \item 医学检查与筛查 —— 见"定期检查与筛查"；并见"检查与随访流程"。
\end{itemize}

\begin{tcolorbox}[colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]
若你在索引里找不到想查的词，换个说法再找一次——\keyword{同一个现象常在书里用不同的概念层次表述}（"没感觉"可能是性欲、唤起、也可能是关系问题）。找到其中一个，顺着相关条目读过去，通常就能抵达你要找的地方。
\end{tcolorbox}
"""

# ═══════════════ 4. 权威资源与数据来源 ═══════════════
APX["权威资源与数据来源"] = r"""\section{使用说明}

本附录汇总本书引用的权威机构、数据库与求助资源，供读者核实信息、获取服务或进一步研究。所列均为真实存在的机构、平台与服务渠道；\keyword{联系方式与政策可能变更，使用前请以官方最新公布为准}。

资源按功能分为四组：\keyword{国际组织与标准机构}（规范与数据来源）、\keyword{国内公共卫生与政府机构}（政策与服务）、\keyword{专业学会与学术数据库}（专业知识与文献）、以及\keyword{求助热线与服务渠道}（直接可用）。

\begin{itemize}
  \item \keyword{四组分类}：国际组织、国内机构、学术资源、求助渠道。
  \item \keyword{只列真实来源}：不收录无法核实的机构与渠道。
  \item \keyword{以官方公布为准}：联系方式与政策可能更新。
\end{itemize}

\begin{tcolorbox}[colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]
建议\keyword{把最可能用到的三个号码存进手机}：急救与报警、心理危机热线、法律援助热线。危机时刻搜索的效率极低——提前两分钟存好，可能省下最关键的十分钟。
\end{tcolorbox}

\section{国际组织与标准机构}

\begin{itemize}
  \item \keyword{世界卫生组织（WHO）}：发布性与生殖健康指南、ICD 分类标准与全球疾病负担数据；其官方网站提供多语言的技术文件与统计数据库。
  \item \keyword{联合国艾滋病规划署（UNAIDS）}：全球 HIV 疫情数据与防治策略的主要来源，发布年度全球艾滋病防治进展报告。
  \item \keyword{联合国人口基金（UNFPA）}：性与生殖健康、避孕与母婴健康领域的国际机构，负责发布相关技术标准与人道响应服务包。
  \item \keyword{联合国教科文组织（UNESCO）}：性教育技术指导文件的发布机构，其《国际性教育技术指导纲要》是各国课程设计的重要参照。
  \item \keyword{世界性健康学会（WAS）}：《性权利宣言》的发布机构，推动性健康与性权利的国际共识。
  \item \keyword{美国疾病控制与预防中心（CDC）}：其性传播感染治疗指南与 HIV 防治技术文件在国际上被广泛参照。
\end{itemize}

\section{国内公共卫生与政府机构}

\begin{itemize}
  \item \keyword{国家卫生健康委员会}：负责卫生健康政策、标准与技术服务规范的制定与发布；官方网站可查规范性文件与政策解读。
  \item \keyword{中国疾病预防控制中心（中国疾控中心）}：疾病监测、防控技术指导与数据发布；下设性病艾滋病预防控制中心，负责相关防治规划与技术指南。
  \item \keyword{各级疾病预防控制中心}：地方层面的疫情监测、检测服务与技术支持；其自愿咨询检测门诊提供 HIV 等检测与咨询。
  \item \keyword{各级卫生健康行政部门与妇幼保健机构}：孕产期保健、母婴阻断、避孕药具发放与生殖健康服务的执行端。
  \item \keyword{国家药品监督管理局}：药品、医疗器械与疫苗的审批信息查询，可用于核实保健产品与药品的合法性。
  \item \keyword{中国计划生育协会与各级妇联组织}：承担生殖健康宣传与家庭服务职能。
\end{itemize}

\section{专业学会与学术数据库}

\begin{itemize}
  \item \keyword{中华医学会及其专科分会}（泌尿外科、皮肤性病学、妇产科等）：发布国内诊疗指南与专家共识，是国内临床实践的主要依据。
  \item \keyword{中国性学会}：性学领域的学术团体，组织学术会议与科普活动。
  \item \keyword{Cochrane Library}：系统综述数据库，用于核查某项干预措施的证据强度，是"这个疗法到底有没有证据"的最佳查询入口。
  \item \keyword{PubMed / MEDLINE}：生物医学文献摘要数据库，覆盖国际主要同行评议期刊。
  \item \keyword{中国知网（CNKI）与万方数据}：中文学术文献数据库，适合检索国内研究与政策研究。
  \item \keyword{中国临床试验注册中心}：查询在中国开展的临床试验注册信息。
\end{itemize}

\section{求助热线与服务渠道}

\subsection{通用与紧急}

\begin{itemize}
  \item \keyword{110 报警服务}；\keyword{12110} 为公安机关短信报警号码，适用于不便出声的场景。
  \item \keyword{120 急救}：用于需要紧急医疗救助的情形。
  \item \keyword{12320} 卫生健康热线：卫生健康政策咨询与投诉举报渠道。
\end{itemize}

\subsection{维权与法律援助}

\begin{itemize}
  \item \keyword{12348} 公共法律服务热线：提供免费法律咨询，可就性侵、家暴、性骚扰等议题咨询维权路径。
  \item \keyword{12338} 妇女维权热线（各级妇联）：受理家暴、性骚扰、婚姻家庭权益相关咨询与求助。
  \item \keyword{12355} 青少年服务台（共青团）：面向青少年的心理与法律咨询渠道。
  \item \keyword{12351} 工会服务热线：涉及职场性骚扰与劳动权益时可使用。
\end{itemize}

\subsection{心理支持}

\begin{itemize}
  \item 各地\keyword{心理援助热线}（由卫生健康部门或精神卫生机构设立）：提供心理危机干预与情绪支持。
  \item 面向\keyword{性侵幸存者}的公益心理服务：由社会组织与专业机构提供，覆盖创伤后的心理干预。
  \item \keyword{医院精神科与心理科门诊}：需要诊断或药物治疗时的正规渠道。
\end{itemize}

\subsection{检测与医疗服务}

\begin{itemize}
  \item \keyword{自愿咨询检测门诊（VCT）}：各级疾控中心设置，提供 HIV 等检测与咨询，以保密与自愿为原则。
  \item \keyword{定点医疗机构}：承担 HIV 抗病毒治疗、性传播感染规范诊疗的医院；部分城市的指定医院提供性侵一站式接诊服务。
  \item \keyword{社区卫生服务中心}：避孕药具发放、基础咨询与常见问题的首诊入口。
  \item \keyword{互联网医院与在线咨询平台}：部分正规医疗机构的线上服务提供预约检测、报告查询与在线复诊，隐私友好度较高。
\end{itemize}

\begin{tcolorbox}[colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]
使用这些资源时请记住两点：\keyword{凡涉及性健康的正式渠道都有保密义务}；而\keyword{凡是要求你付费购买"疗程""秘方"的，都不是其中一员}。分不清时，先打一个上面列出的官方热线问一下——这一步永远不亏。
\end{tcolorbox}
"""

# ═══════════════ 5. 常用问卷与量表 ═══════════════
APX["常用问卷与量表"] = r"""\section{使用说明}

本附录介绍性健康与亲密关系研究中常用的问卷与量表，说明其用途、适用对象与局限。它们主要用于\keyword{研究与临床筛查}，而非自我诊断工具。

使用前必须明确三点。第一，\keyword{量表是筛查与评估工具，不是诊断}：得分高提示"值得进一步评估"，不构成任何疾病的诊断，诊断需由专业人员结合临床访谈作出。第二，\keyword{量表测量的是主观报告}：受理解方式、社会期待与当时的情绪状态影响，单次测量不宜过度解读。第三，\keyword{中文版的适用性需要验证}：量表在跨文化使用时需做翻译与信效度检验，直接使用未经检验的译本可能失真。

\begin{itemize}
  \item \keyword{用途限定}：筛查与评估，不用于自我诊断。
  \item \keyword{主观报告的局限}：单次得分不宜过度解读。
  \item \keyword{中文版需验证}：跨文化使用须核实信效度。
\end{itemize}

\begin{tcolorbox}[colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]
网上随手能搜到的"自测表"多为简化或改编版本，常删去了原量表的计分规则与适用条件。\keyword{把它当作"我该不该去看医生"的提示可以，当作结论不行}——真正需要判断时，专业评估才是最省时间的方式。
\end{tcolorbox}

\section{性功能评估量表}

\subsection{男性性功能}

\begin{itemize}
  \item \keyword{国际勃起功能指数（IIEF）}：评估勃起功能的标准化量表，涵盖勃起、射精、性欲、性交满意度与总体满意度五个维度；由 Rosen 等人在 1997 年发表，是临床研究中最常用的工具之一。
  \item \keyword{IIEF-5（又称 SHIM，性健康问卷简版）}：由 IIEF 简化而来的五题版本，便于快速筛查，常用于门诊初筛与流行病学调查。
  \item \keyword{早泄诊断工具（PEDT）}：由 Symonds 等人于 2007 年发表的五题量表，用于评估早泄相关的主观困扰与控制困难。
  \item \keyword{男性性健康问卷（如 MSHQ）}：评估射精功能、性欲与总体满意度，用于射精障碍研究。
\end{itemize}

\subsection{女性性功能}

\begin{itemize}
  \item \keyword{女性性功能指数（FSFI）}：由 Rosen 等人于 2000 年发表，包含性欲、唤起、润滑、高潮、满意度与疼痛六个维度，是女性性功能研究中最广泛使用的量表。
  \item \keyword{女性性困扰量表（FSDS-R）}：测量与性功能相关的个人困扰程度，常与 FSFI 联合使用——因为临床关注的是"困扰"而非单纯的得分高低。
  \item \keyword{女性性功能问卷（如 SFQ）}：另一套多维评估工具，侧重性反应各阶段的主观体验。
  \item \keyword{盆底功能相关量表}：评估盆底症状（如疼痛、脱垂、排尿排便相关困扰）对性生活的影响。
\end{itemize}

\subsection{通用与跨性别群体}

\begin{itemize}
  \item \keyword{亚利桑那性体验量表（ASEX）}：五个条目快速评估性欲、唤起、勃起或润滑、高潮与满意度，常用于药物（如抗抑郁药）对性功能影响的筛查。
  \item \keyword{戈隆博克—鲁斯特性满意度量表（GRISS）}：包含自评与伴侣评两部分，评估性关系中的多个问题维度，适合伴侣研究。
  \item \keyword{性欲量表（如 Sexual Desire Inventory）}：由 Spector 等人于 1996 年发表，区分个体性与伴侣性性欲两个维度，用于性欲研究。
\end{itemize}

\section{性取向、性别与关系量表}

\begin{itemize}
  \item \keyword{克莱因性取向网格（KSOG）}：由 Klein 等人提出，从性吸引、性行为、性幻想、情感偏好、社会偏好、生活方式与自我认同七个维度分别评估过去、现在与理想状态下的性取向，体现了性取向的多维与动态特征。
  \item \keyword{性别认同相关量表}：用于评估性别认同的一致性、性别烦躁的程度与相关困扰；临床评估通常结合结构化访谈，量表仅作辅助。
  \item \keyword{成人依恋量表（ECR / ECR-R）}：由 Brennan 等人开发，从依恋焦虑与依恋回避两个维度测量成人依恋风格，是亲密关系研究中最常用的工具之一。
  \item \keyword{关系满意度量表}：如关系评估量表（RAS）与二元调适量表（DAS），用于评估伴侣关系的满意度与调适程度。
  \item \keyword{性沟通量表}：评估伴侣间讨论性议题的自在程度与频率，常用于性治疗研究中的过程评估。
\end{itemize}

\begin{tcolorbox}[colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]
这类量表最实际的用途是\keyword{给沟通提供一个把手}：把"我们之间不太好说"变成"这里有一份清单，我们一起看看哪些像我们"。工具本身不解决问题，但它能让对话开始——而对话，才是改变真正发生的地方。
\end{tcolorbox}
"""
