const BASE_DATE = new Date("2026-07-06T00:00:00");

const STORAGE_KEYS = {
  prep: "gensight.prepChecklist",
  daily: "gensight.dailyLog",
  week: "gensight.weekProgress",
  inquiries: "gensight.inquiries",
  reviews: "gensight.eveningReview",
  clientId: "gensight.clientId",
  handoffs: "gensight.handoffs",
  handoffSeq: "gensight.handoffSeq",
  workItems: "gensight.workItems",
  workItemSeq: "gensight.workItemSeq",
  recentDocs: "gensight.recentDocs",
  finalizedAssets: "gensight.finalizedAssets",
};

const DEFAULT_FINALIZED_ASSETS = [
  {
    id: "intro-copy",
    title: "企业介绍文案",
    version: "v2",
    status: "done",
    date: "2026-07-06",
    docId: "standards",
    docFile: "12-company-profile-delivery-standards.md",
    note: "四版本文案、团队背书、案例索引已定稿",
  },
  {
    id: "intro-ppt",
    title: "企业介绍 PPT / 介绍图",
    version: "v1",
    status: "pending",
    date: null,
    docId: "standards",
    docFile: "12-company-profile-delivery-standards.md",
    docSection: "§1.3 私聊转发版",
    note: "文案已定，待Brian做私聊转发图 + 标准版介绍图",
    expectedOutputs: ["私聊转发图", "标准版介绍图"],
  },
  {
    id: "public-pricing",
    title: "对外公开报价图",
    version: "v1",
    status: "pending",
    date: null,
    docId: "public",
    docFile: "03-public-pricing.md",
    note: "价格与交付标准校验中，待做报价图",
    expectedOutputs: ["对外报价图 v1"],
  },
  {
    id: "platform-bio",
    title: "平台简介（小红书等）",
    version: "v1",
    status: "pending",
    date: null,
    docId: "standards",
    docFile: "12-company-profile-delivery-standards.md",
    docSection: "§1.2 超短版",
    note: "依赖企业介绍 v2，用超短版裁切",
    expectedOutputs: ["小红书简介图"],
  },
];

const docs = [
  { id: "readme", group: "总览", title: "总入口", subtitle: "文件导航与执行纪律", file: "README.md" },
  { id: "foundation", group: "校验", title: "基础校验", subtitle: "企业介绍·业务范围·报价", file: "00-foundation-review.md" },
  { id: "startup", group: "启动", title: "启动准备", subtitle: "账号、收款、素材库", file: "00-startup-checklist.md" },
  { id: "business", group: "业务", title: "业务规划", subtitle: "90 天目标与收入线", file: "01-business-plan.md" },
  { id: "channel", group: "定价", title: "渠道内部价", subtitle: "合作广告公司专用", file: "02-channel-internal-pricing.md" },
  { id: "public", group: "定价", title: "对外报价", subtitle: "自媒体直客公开口径", file: "03-public-pricing.md" },
  { id: "social", group: "内容", title: "自媒体规划", subtitle: "平台分工与栏目", file: "04-social-media-plan.md" },
  { id: "calendar", group: "执行", title: "90 天执行表", subtitle: "2026-07-06 起", file: "05-90-day-execution-calendar.md" },
  { id: "cases", group: "案例", title: "案例包装库", subtitle: "收费案例与策略型案例", file: "06-case-packaging-library.md" },
  { id: "content", group: "内容", title: "首月内容", subtitle: "选题、脚本与图文", file: "07-content-first-month.md" },
  { id: "sop", group: "销售", title: "询盘 SOP", subtitle: "报价、收款、交付", file: "08-sales-and-intake-sop.md" },
  { id: "duomiao", group: "协作", title: "多淼联合", subtitle: "联合业务与宣传策略", file: "09-duomiao-partnership.md" },
  { id: "twoperson", group: "执行", title: "双人推进", subtitle: "Howard + Brian日计划", file: "10-two-person-execution-plan.md" },
  { id: "xianyu", group: "渠道", title: "闲鱼试点", subtitle: "14 天体验款获客", file: "11-xianyu-channel-pilot.md" },
  { id: "standards", group: "业务", title: "企业介绍", subtitle: "对外介绍与交付标准", file: "12-company-profile-delivery-standards.md" },
  { id: "proposal", group: "高阶", title: "商业方案", subtitle: "崇明案例与 BP 服务", file: "13-commercial-proposal-service.md" },
  { id: "placement", group: "案例", title: "案例归类", subtitle: "小马 / Teddy / 茶养", file: "14-strategy-case-placement.md" },
  { id: "registration", group: "公司", title: "注册路线图", subtitle: "8 月后公司化", file: "15-company-registration-roadmap.md" },
];

const docFileToId = Object.fromEntries(docs.map((doc) => [doc.file, doc.id]));

const foundationCategories = [
  {
    title: "企业介绍",
    owner: "两人",
    items: [
      { id: "E1", text: "一句话介绍：内核「策略先于执行，专业驾驭效能」，专业判断×策略深度×AI应用" },
      { id: "E2", text: "目标客户：覆盖常规设计采购、快速比稿、内容视觉化；AI 进阶型为差异化细分，非唯一客群" },
      { id: "E3", text: "全国线上交付 vs 多淼苏州本地边界表述清楚" },
      { id: "E4", text: "私聊转发短版可直接使用" },
      { id: "E5", text: "各产品交付标准「包含/不包含」已写清" },
    ],
  },
  {
    title: "业务范围定位",
    owner: "Howard主导",
    items: [
      { id: "B1", text: "主推 5 类确认：Logo/VI、广告创意、PPT、效果图、全案" },
      { id: "B2", text: "企业 AI 落地、政务传播已从首屏移除" },
      { id: "B3", text: "纯设计类全国线上可独立承接" },
      { id: "B4", text: "多淼联合边界清楚：谁主导、谁报价、谁收款" },
      { id: "B5", text: "策略型方案（崇明/BP）不与标准设计报价混排" },
      { id: "B6", text: "渠道单 vs 自媒体直客两条线产品清楚" },
    ],
  },
  {
    title: "报价合理性",
    owner: "两人",
    items: [
      { id: "P1", text: "对外公开价逐项核对（Logo/PPT/效果图/全案）" },
      { id: "P2", text: "用已收费案例反推：价格与实际项目是否匹配" },
      { id: "P3", text: "公开价与渠道内部价严格隔离、不混用" },
      { id: "P4", text: "与广告公司核对渠道内部价是否符合合作实际" },
      { id: "P5", text: "修改轮次、付款节点、月结规则可执行" },
      { id: "P6", text: "联合项目价是否需拆设计费/制作费/安装费" },
      { id: "P7", text: "定稿报价 v1：记录需调整的产品和价格" },
    ],
  },
];

const prepCategories = [
  {
    title: "收款",
    owner: "Howard",
    items: [
      { id: "R1", text: "确认个人微信收款可用于直客 50% 预付 + 50% 尾款" },
      { id: "R2", text: "确认个人支付宝收款备用" },
      { id: "R3", text: "渠道单继续走朋友广告公司结算" },
      { id: "R4", text: "每笔直客收款后留聊天记录和交付确认截图" },
    ],
  },
  {
    title: "合同与话术",
    owner: "Howard",
    items: [
      { id: "C1", text: "写个人服务协议简版" },
      { id: "C2", text: "写询盘首次沟通 7 问话术" },
      { id: "C3", text: "写报价后确认话术（预付、尾款、不包含事项）" },
      { id: "C4", text: "明确不提供发票的说明口径" },
    ],
  },
  {
    title: "账号开通",
    owner: "Brian",
    items: [
      { id: "A1", text: "注册小红书账号「元晟传媒」并完成基础资料" },
      { id: "A2", text: "注册抖音账号并完成基础资料" },
      { id: "A3", text: "注册视频号并完成基础资料" },
      { id: "A4", text: "注册闲鱼账号并可上架商品" },
      { id: "A5", text: "朋友圈发布口径确认（Howard个人号）" },
    ],
  },
  {
    title: "素材库",
    owner: "Brian",
    items: [
      { id: "M1", text: "建立总目录「案例资产/」" },
      { id: "M2", text: "7 个收费项目各建子文件夹" },
      { id: "M3", text: "填写案例素材缺口表" },
      { id: "M4", text: "统一水印和封面模板 v0.1" },
    ],
  },
  {
    title: "渠道确认",
    owner: "Howard",
    items: [
      { id: "CH1", text: "与现有广告公司确认近期可交付项目和排期" },
      { id: "CH2", text: "确认渠道内部价和结算规则是否可执行" },
      { id: "CH3", text: "锁定渠道单交付时间，避免和自媒体建设抢时间" },
      { id: "CH4", text: "记录渠道联系人、结算周期、修改轮次约定" },
    ],
  },
  {
    title: "多淼协作",
    owner: "Howard",
    items: [
      { id: "D1", text: "发出可公开案例边界确认清单" },
      { id: "D2", text: "确认联合报价分工：谁报价、谁收款、谁交付" },
      { id: "D3", text: "确认哪些案例可实名、脱敏、暂不发" },
      { id: "D4", text: "确认线上询盘分流规则" },
    ],
  },
  {
    title: "办公协作",
    owner: "两人",
    items: [
      { id: "O1", text: "固定 09:30 今日对齐（只看工作台 1-3 件事）" },
      { id: "O2", text: "固定 10:00-12:00 深工时段" },
      { id: "O3", text: "固定 14:00-17:30 修改成型时段" },
      { id: "O4", text: "固定 18:00 晚间五问复盘" },
      { id: "O5", text: "日内不讨论战略方向（方向只在周一/周五）" },
    ],
  },
  {
    title: "工作台",
    owner: "Howard",
    items: [
      { id: "W1", text: "通过协同服务器打开工作台（python3 server.py --port 8025）" },
      { id: "W2", text: "每天在工作台勾选今日任务" },
      { id: "W3", text: "启动准备清单逐项打勾" },
      { id: "W4", text: "询盘和报价记录进工作台表格" },
    ],
  },
];

const weeklyPlans = [
  {
    week: 1,
    range: "2026-07-06 至 2026-07-12",
    goal: "先完成基础校验（企业介绍、业务范围、报价合理性），定稿 v1 后再出报价图和启动账号。",
    acceptance: [
      "基础校验三项两人确认，结论模板有 v1 决定",
      "企业介绍 + 业务范围 + 对外报价定稿 v1",
      "渠道内部价与广告公司核对完成",
      "对外报价图至少完成 v1",
      "多淼可公开案例边界清单已发出",
      "7 个收费项目素材缺口表已建立",
    ],
    days: [
      {
        date: "2026-07-06",
        focus: "基础校验：企业介绍 + 业务范围",
        huang: ["两人审阅企业介绍，标出需改处", "确认 5 类主推业务 + 多淼联合边界", "发出多淼/飞书评论确认清单"],
        li: ["从客户视角审阅企业介绍", "整理已收费案例与公开报价对照表", "记录报价图待修改清单"],
        deliverable: "基础校验记录、业务范围确认结论、案例报价对照表",
      },
      {
        date: "2026-07-07",
        focus: "基础校验：报价合理性",
        huang: ["逐项验证对外公开价与交付标准", "与广告公司核对渠道内部价", "汇总校验结论，改正文"],
        li: ["用案例反推报价是否合理", "做报价合理性对照草稿", "预备报价图版式（不出终稿）"],
        deliverable: "报价校验结论、渠道价反馈、待调整价格清单",
      },
      {
        date: "2026-07-08",
        focus: "定稿 v1 + 启动准备",
        huang: ["定稿企业介绍+报价口径 v1", "写个人收款话术和服务协议简版", "定闲鱼体验款边界"],
        li: ["完成对外报价图 v1", "注册小红书/抖音/闲鱼账号", "建立案例素材文件夹"],
        deliverable: "介绍+报价 v1、报价图 v1、3 个账号已注册",
      },
      {
        date: "2026-07-09",
        focus: "多淼 PPT 案例",
        huang: ["写多淼 PPT 案例小红书长文初稿", "写朋友圈短文", "写闲鱼 Logo 商品文案"],
        li: ["选 6-9 张 PPT 案例图", "做半间茶舍 / 汇泽万帮商品图"],
        deliverable: "多淼 PPT 小红书初稿、短视频 v1、闲鱼第 2 个商品草稿",
      },
      {
        date: "2026-07-10",
        focus: "发布第一批内容",
        huang: ["审稿发布 1 篇小红书长文 + 1 条短视频 + 朋友圈", "设置闲鱼站内回复话术"],
        li: ["做小红书封面 2 张、视频号封面 1 张", "补报价图和闲鱼商品图细节"],
        deliverable: "1 篇小红书长文、1 条短视频、2 篇小红书笔记、2 个闲鱼商品可上架",
      },
      {
        date: "2026-07-11",
        focus: "渠道沟通和熟人转化",
        huang: ["联系多淼和广告公司确认渠道价", "检查闲鱼曝光和私信"],
        li: ["根据反馈修改报价图、案例图和闲鱼主图"],
        deliverable: "渠道反馈记录、朋友圈转化文案、报价图 v2",
      },
      {
        date: "2026-07-12",
        focus: "周复盘",
        huang: ["检查启动准备完成率", "统计本周物料、发布、询盘", "确定第 2 周主案例"],
        li: ["整理本周最终素材包", "列下周缺素材清单"],
        deliverable: "启动准备复盘、第 1 周复盘表、第 2 周任务清单",
      },
    ],
  },
  {
    week: 2,
    range: "2026-07-13 至 2026-07-19",
    goal: "完成 7 个已收费项目的基础案例卡，并开始稳定发布。",
    acceptance: [
      "7 个已收费项目都有基础案例卡",
      "至少发布 1 篇小红书长文、2 篇笔记、2 条短视频",
      "文家姑娘、Logo、PPT 三条内容线都形成可复用素材",
      "多淼联合业务有一张「对外能力卡」草稿",
    ],
    days: [
      { date: "2026-07-13", focus: "案例库结构", huang: ["按 7 个收费项目补客户背景和可公开边界"], li: ["每个案例选 3-5 张图，做统一水印和封面模板"], deliverable: "7 个案例卡文字框架、案例封面模板" },
      { date: "2026-07-14", focus: "文家姑娘酸奶", huang: ["写文家姑娘案例初稿", "复盘闲鱼前 7 天数据"], li: ["做文家姑娘案例长图和 mockup"], deliverable: "文家姑娘小红书初稿、闲鱼第 1 轮优化" },
      { date: "2026-07-15", focus: "Logo 案例", huang: ["写半间茶舍 + 汇泽万帮 Logo 合并案例提纲"], li: ["做 2 组 Logo 前后对比和应用图"], deliverable: "Logo 案例提纲、2 组案例图" },
      { date: "2026-07-16", focus: "PPT 案例矩阵", huang: ["整理多淼、田文华、讲宪法 PPT 方法论"], li: ["做 PPT 前后对比短视频素材 2 条"], deliverable: "PPT 方法论短文、短视频素材 2 条" },
      { date: "2026-07-17", focus: "发布和分发", huang: ["发布文家姑娘内容", "朋友圈发案例快照"], li: ["做小红书封面、视频号封面"], deliverable: "1 篇小红书长文、2 篇笔记、1-2 条短视频" },
      { date: "2026-07-18", focus: "多淼联合内容", huang: ["写联合承接说明短文"], li: ["做联合服务流程图和多淼协作能力卡"], deliverable: "多淼联合服务图文 v1" },
      { date: "2026-07-19", focus: "周复盘", huang: ["检查 7 个案例卡是否齐全"], li: ["整理已发布素材和剩余缺图"], deliverable: "7 个基础案例卡、第 2 周复盘表" },
    ],
  },
  {
    week: 3,
    range: "2026-07-20 至 2026-07-26",
    goal: "用 Logo/VI 形成搜索获客内容，同时把多淼联合业务讲清楚。",
    acceptance: [
      "Logo/VI 形成 2 个案例内容和 1 篇报价科普",
      "多淼联合业务说明可以发给潜在客户",
      "小红书布局 Logo/VI 关键词",
    ],
    days: [
      { date: "2026-07-20", focus: "Logo/VI 主题周规划", huang: ["确认本周标题和内容排期"], li: ["做 Logo/VI 主题视觉模板"], deliverable: "本周内容排期、主题封面模板" },
      { date: "2026-07-21", focus: "半间茶舍案例", huang: ["写半间茶舍案例正文"], li: ["做半间茶舍 Logo 应用图、短视频过程图"], deliverable: "半间茶舍案例初稿、短视频 v1" },
      { date: "2026-07-22", focus: "汇泽万帮案例", huang: ["写汇泽万帮案例短文"], li: ["做汇泽万帮 Logo 应用图和小红书封面"], deliverable: "汇泽万帮案例短文、小红书 v1" },
      { date: "2026-07-23", focus: "Logo 报价科普", huang: ["写 Logo 基础版和标准版区别"], li: ["做报价对比图和 3 张解释卡"], deliverable: "Logo 报价科普图文" },
      { date: "2026-07-24", focus: "多淼联合服务", huang: ["写联合承接说明"], li: ["做联合业务流程图 v2 和服务卡"], deliverable: "多淼联合业务说明 v1" },
      { date: "2026-07-25", focus: "发布和客户触达", huang: ["发布 Logo/VI 内容", "私聊触达潜在线索"], li: ["按平台尺寸导出封面和图文"], deliverable: "本周发布包、触达记录" },
      { date: "2026-07-26", focus: "周复盘", huang: ["统计 Logo/VI 内容反馈"], li: ["整理 Logo/VI 素材库"], deliverable: "第 3 周复盘表、下周选题" },
    ],
  },
  {
    week: 4,
    range: "2026-07-27 至 2026-08-02",
    goal: "用米兰坊和铺宝宝切入店面/装修效果图，同时复盘第一个月执行效果。",
    acceptance: [
      "米兰坊案例形成长文、短视频、小红书三种版本",
      "效果图产品价格和交付边界讲清楚",
      "7 月发布、询盘、报价、成交形成一张复盘表",
    ],
    days: [
      { date: "2026-07-27", focus: "效果图主题周规划", huang: ["确认效果图基础包/标准包话术"], li: ["做效果图主题封面模板"], deliverable: "本周内容排期、效果图封面模板" },
      { date: "2026-07-28", focus: "米兰坊案例", huang: ["写米兰坊案例正文"], li: ["做米兰坊前后对比、场景图、短视频素材"], deliverable: "米兰坊案例初稿、短视频 v1" },
      { date: "2026-07-29", focus: "铺宝宝测试案例", huang: ["写铺宝宝脱敏案例短文"], li: ["做铺宝宝效果图对比图和小红书封面"], deliverable: "铺宝宝小红书图文" },
      { date: "2026-07-30", focus: "效果图报价科普", huang: ["写店面效果图报价科普"], li: ["做基础包/标准包对比图"], deliverable: "效果图报价科普图文" },
      { date: "2026-07-31", focus: "发布和触达", huang: ["发布效果图主题内容", "联系门店潜在线索"], li: ["导出发布素材，补朋友圈图"], deliverable: "本周发布包、触达记录" },
      { date: "2026-08-01", focus: "月度数据整理", huang: ["统计 7 月内容数、询盘数、报价数、成交数"], li: ["整理 7 月所有视觉素材和发布截图"], deliverable: "7 月数据表、素材归档" },
      { date: "2026-08-02", focus: "月度复盘会", huang: ["判断下月主推产品"], li: ["输出月度案例作品集 v1"], deliverable: "7 月复盘结论、8 月重点" },
    ],
  },
];

const phases = [
  { maxWeek: 1, label: "基础校验", desc: "企业介绍、业务范围、报价合理性定稿 v1。" },
  { maxWeek: 4, label: "生存启动", desc: "报价图、案例包装、小红书内容发布。" },
  { maxWeek: 9, label: "产品验证", desc: "固定内容节奏，验证效果图和全案产品线。" },
  { maxWeek: 99, label: "转化提升", desc: "复盘线索，提高直客占比。" },
];

const WORK_ITEM_STATUS_LABELS = {
  backlog: "待开始",
  in_progress: "进行中",
  waiting_handoff: "待接手",
  waiting_review: "待确认",
  blocked: "待补充",
  done: "已完成",
};

const WORK_ITEM_TYPES = {
  copy_to_visual: "文案定稿 → 视觉制作",
  pricing_visual: "报价口径 → 报价图",
  case_visual: "案例文稿 → 案例图/封面",
  publish_pack: "发布包 → 多平台导出",
  copy_revision: "需文案/口径补充",
  visual_review: "视觉稿待确认",
  general: "一般任务",
};

const PINNED_DOCS = [
  { id: "standards", label: "企业介绍与交付标准" },
  { id: "public", label: "对外报价" },
  { id: "twoperson", label: "双人日计划" },
  { id: "cases", label: "案例包装库" },
  { id: "sop", label: "询盘 SOP" },
  { id: "xianyu", label: "闲鱼试点" },
];

const DOC_LOOKUP_GROUPS = {
  执行: ["twoperson", "calendar", "startup", "xianyu"],
  口径: ["standards", "public", "channel", "business", "sop"],
  规划归档: ["readme", "foundation", "social", "content", "duomiao", "proposal", "placement", "registration"],
};

const SYNC = {
  enabled: false,
  saving: false,
  updatedAt: null,
  error: null,
  saveTimer: null,
  pollTimer: null,
  clientId: "",
};

const workItemDialogState = { mode: "create", editingId: null };

const state = {
  activeDoc: docs.find((doc) => doc.id === "twoperson") || docs[0],
  mode: "read",
  markdown: "",
  search: "",
  cache: new Map(),
  drafts: new Map(),
  prep: {},
  daily: {},
  week: {},
  foundation: {},
  foundationNote: "",
  inquiries: [],
  reviews: [],
  handoffs: [],
  handoffSeq: 0,
  workItems: [],
  workItemSeq: 0,
  recentDocs: [],
  finalizedAssets: [],
  workboardFilter: "all",
  perspective: "huang",
  laneCollapsed: false,
  splitPaneOpen: false,
  splitDoc: null,
};

function init() {
  SYNC.clientId = getClientId();
  bindEvents();
  bootstrap().catch(() => {
    loadStorage();
    afterLoad();
    renderSyncStatus();
  });
}

async function bootstrap() {
  await loadFromServer();
  afterLoad();
  startSyncPolling();
  openDocFromQuery();
}

function afterLoad() {
  migrateHandoffsToWorkItems();
  seedWorkItems();
  renderAll();
  refreshIcons();
  setInquiryDateDefault();
  populateWorkItemFormDefaults();
  showSection("workboard");
}

function openDocFromQuery() {
  const params = new URLSearchParams(window.location.search);
  const docParam = params.get("doc");
  if (!docParam) return;
  const docId = resolveDocLink(docParam);
  if (docId) openSplitDoc(docId);
  window.history.replaceState({}, "", window.location.pathname);
}

function getClientId() {
  let id = localStorage.getItem(STORAGE_KEYS.clientId);
  if (!id) {
    id = `user-${Math.random().toString(36).slice(2, 8)}`;
    localStorage.setItem(STORAGE_KEYS.clientId, id);
  }
  return id;
}

function packState() {
  return {
    prep: state.prep,
    daily: state.daily,
    week: state.week,
    foundation: state.foundation,
    foundationNote: state.foundationNote,
    inquiries: state.inquiries,
    reviews: state.reviews,
    handoffs: state.handoffs,
    handoffSeq: state.handoffSeq,
    workItems: state.workItems,
    workItemSeq: state.workItemSeq,
    recentDocs: state.recentDocs,
    finalizedAssets: state.finalizedAssets,
  };
}

function getFinalizedAssets() {
  return state.finalizedAssets.length ? state.finalizedAssets : DEFAULT_FINALIZED_ASSETS;
}

function applyRemoteData(data) {
  state.prep = data.prep || {};
  state.daily = data.daily || {};
  state.week = data.week || {};
  state.foundation = data.foundation || {};
  state.foundationNote = data.foundationNote || "";
  state.inquiries = Array.isArray(data.inquiries) ? data.inquiries : [];
  state.reviews = Array.isArray(data.reviews) ? data.reviews : [];
  state.handoffs = Array.isArray(data.handoffs) ? data.handoffs : [];
  state.handoffSeq = Number(data.handoffSeq) || 0;
  state.workItems = Array.isArray(data.workItems) ? data.workItems : [];
  state.workItemSeq = Number(data.workItemSeq) || 0;
  state.recentDocs = Array.isArray(data.recentDocs) ? data.recentDocs : [];
  state.finalizedAssets = Array.isArray(data.finalizedAssets) ? data.finalizedAssets : [];
  if (!state.finalizedAssets.length) state.finalizedAssets = structuredClone(DEFAULT_FINALIZED_ASSETS);
  cacheToLocalStorage();
}

function isRemoteEmpty(data) {
  return (
    !Object.keys(data.prep || {}).length &&
    !Object.keys(data.daily || {}).length &&
    !Object.keys(data.week || {}).length &&
    !Object.keys(data.foundation || {}).length &&
    !(data.foundationNote || "").trim() &&
    !(data.inquiries || []).length &&
    !(data.reviews || []).length &&
    !(data.handoffs || []).length &&
    !(data.workItems || []).length &&
    !(data.finalizedAssets || []).length
  );
}

function hasLocalData() {
  return (
    Object.keys(readJSON(STORAGE_KEYS.prep, {})).length > 0 ||
    Object.keys(readJSON(STORAGE_KEYS.daily, {})).length > 0 ||
    Object.keys(readJSON(STORAGE_KEYS.week, {})).length > 0 ||
    Object.keys(readJSON("gensight.foundation", {})).length > 0 ||
    (readJSON("gensight.foundationNote", "") || "").trim().length > 0 ||
    readJSON(STORAGE_KEYS.inquiries, []).length > 0 ||
    readJSON(STORAGE_KEYS.reviews, []).length > 0 ||
    readJSON(STORAGE_KEYS.handoffs, []).length > 0 ||
    readJSON(STORAGE_KEYS.workItems, []).length > 0 ||
    readJSON(STORAGE_KEYS.finalizedAssets, []).length > 0
  );
}

async function loadFromServer() {
  const response = await fetch("/api/data", { cache: "no-store" });
  if (!response.ok) throw new Error("无法读取共享数据");
  const data = await response.json();
  SYNC.enabled = true;
  SYNC.error = null;
  SYNC.updatedAt = data.updatedAt || null;

  if (isRemoteEmpty(data) && hasLocalData()) {
    loadStorage();
    await saveToServer(true);
    return;
  }

  applyRemoteData(data);
  renderSyncStatus();
}

async function saveToServer(force = false) {
  if (!SYNC.enabled && !force) {
    cacheToLocalStorage();
    return;
  }

  SYNC.saving = true;
  renderSyncStatus();

  try {
    const response = await fetch("/api/data", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...packState(), clientId: SYNC.clientId }),
    });
    if (!response.ok) throw new Error("保存失败");
    const data = await response.json();
    SYNC.enabled = true;
    SYNC.error = null;
    SYNC.updatedAt = data.updatedAt || null;
    cacheToLocalStorage();
  } catch (error) {
    SYNC.error = error.message;
    cacheToLocalStorage();
  }

  SYNC.saving = false;
  renderSyncStatus();
}

function persistState() {
  cacheToLocalStorage();
  clearTimeout(SYNC.saveTimer);
  SYNC.saveTimer = setTimeout(() => saveToServer(), 350);
}

function cacheToLocalStorage() {
  writeJSON(STORAGE_KEYS.prep, state.prep);
  writeJSON(STORAGE_KEYS.daily, state.daily);
  writeJSON(STORAGE_KEYS.week, state.week);
  writeJSON("gensight.foundation", state.foundation);
  writeJSON("gensight.foundationNote", state.foundationNote);
  writeJSON(STORAGE_KEYS.inquiries, state.inquiries);
  writeJSON(STORAGE_KEYS.reviews, state.reviews);
  writeJSON(STORAGE_KEYS.handoffs, state.handoffs);
  writeJSON(STORAGE_KEYS.handoffSeq, state.handoffSeq);
  writeJSON(STORAGE_KEYS.workItems, state.workItems);
  writeJSON(STORAGE_KEYS.workItemSeq, state.workItemSeq);
  writeJSON(STORAGE_KEYS.recentDocs, state.recentDocs);
  writeJSON(STORAGE_KEYS.finalizedAssets, state.finalizedAssets);
}

async function pollServer() {
  if (!SYNC.enabled || SYNC.saving) return;
  try {
    const response = await fetch("/api/data", { cache: "no-store" });
    if (!response.ok) return;
    const data = await response.json();
    if (data.updatedAt && data.updatedAt !== SYNC.updatedAt) {
      SYNC.updatedAt = data.updatedAt;
      applyRemoteData(data);
      renderAll();
      renderSyncStatus();
    }
  } catch {
    /* silent */
  }
}

function startSyncPolling() {
  if (SYNC.pollTimer) clearInterval(SYNC.pollTimer);
  if (!SYNC.enabled) return;
  SYNC.pollTimer = setInterval(pollServer, 5000);
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") pollServer();
  });
}

function renderSyncStatus() {
  const el = document.querySelector("#syncStatusText");
  const box = document.querySelector("#syncStatus");
  if (!el || !box) return;

  box.classList.remove("sync-on", "sync-off", "sync-saving", "sync-error");

  if (SYNC.saving) {
    box.classList.add("sync-saving");
    el.textContent = "正在保存到共享文件…";
    return;
  }

  if (SYNC.enabled) {
    box.classList.add("sync-on");
    const time = SYNC.updatedAt ? formatSyncTime(SYNC.updatedAt) : "刚刚";
    el.textContent = SYNC.error ? `已保存（离线缓存）· ${time}` : `双人协同已开启 · ${time}`;
    if (SYNC.error) box.classList.add("sync-error");
    return;
  }

  box.classList.add("sync-off");
  el.textContent = "仅本机模式（请用 server.py 启动）";
}

function formatSyncTime(iso) {
  try {
    const date = new Date(iso);
    return date.toLocaleString("zh-CN", { month: "numeric", day: "numeric", hour: "2-digit", minute: "2-digit" });
  } catch {
    return iso;
  }
}

function loadStorage() {
  state.prep = readJSON(STORAGE_KEYS.prep, {});
  state.daily = readJSON(STORAGE_KEYS.daily, {});
  state.week = readJSON(STORAGE_KEYS.week, {});
  state.foundation = readJSON("gensight.foundation", {});
  state.foundationNote = readJSON("gensight.foundationNote", "") || "";
  state.inquiries = readJSON(STORAGE_KEYS.inquiries, []);
  state.reviews = readJSON(STORAGE_KEYS.reviews, []);
  state.handoffs = readJSON(STORAGE_KEYS.handoffs, []);
  state.handoffSeq = readJSON(STORAGE_KEYS.handoffSeq, 0);
  state.workItems = readJSON(STORAGE_KEYS.workItems, []);
  state.workItemSeq = readJSON(STORAGE_KEYS.workItemSeq, 0);
  state.recentDocs = readJSON(STORAGE_KEYS.recentDocs, []);
  state.finalizedAssets = readJSON(STORAGE_KEYS.finalizedAssets, []);
  if (!state.finalizedAssets.length) state.finalizedAssets = structuredClone(DEFAULT_FINALIZED_ASSETS);
}

function readJSON(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function writeJSON(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function renderAll() {
  renderWorkboard();
  renderWorkBadges();
  renderSidebarPhase();
  renderDocLookup();
  renderInquiries();
  renderReview();
  renderSettings();
}

function showSection(sectionId) {
  document.querySelectorAll("[data-view]").forEach((el) => {
    el.hidden = el.dataset.view !== sectionId;
  });
  document.querySelectorAll(".nav-item[data-section]").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.section === sectionId);
  });
  refreshIcons();
}

function getToday() {
  const now = new Date();
  now.setHours(0, 0, 0, 0);
  return now;
}

function formatDate(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

function parseDate(str) {
  return new Date(`${str}T00:00:00`);
}

function daysBetween(a, b) {
  return Math.floor((b - a) / 86400000);
}

function getCalendar() {
  const today = getToday();
  const dayOffset = Math.max(0, daysBetween(BASE_DATE, today));
  const weekNum = Math.min(4, Math.floor(dayOffset / 7) + 1);
  const weekPlan = weeklyPlans.find((w) => w.week === weekNum) || weeklyPlans[0];
  const dayIndex = dayOffset % 7;
  const dayPlan = weekPlan.days[dayIndex] || weekPlan.days[0];
  const phase = phases.find((p) => weekNum <= p.maxWeek) || phases[phases.length - 1];
  const weekdayNames = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"];

  return {
    today,
    todayStr: formatDate(today),
    dayOffset,
    weekNum,
    weekPlan,
    dayPlan,
    dayIndex,
    phase,
    weekdayName: weekdayNames[today.getDay()],
  };
}

function getPrepStats() {
  const all = prepCategories.flatMap((c) => c.items);
  const done = all.filter((item) => state.prep[item.id]?.done).length;
  const percent = all.length ? Math.round((done / all.length) * 100) : 0;
  return { total: all.length, done, percent };
}

function getFoundationStats() {
  const all = foundationCategories.flatMap((c) => c.items);
  const done = all.filter((item) => state.foundation[item.id]?.done).length;
  const percent = all.length ? Math.round((done / all.length) * 100) : 0;
  return { total: all.length, done, percent };
}

function renderSidebarPhase() {
  const cal = getCalendar();
  const prepStats = getPrepStats();
  const foundationStats = getFoundationStats();
  const label = document.querySelector("#phaseLabel");
  const desc = document.querySelector("#phaseDesc");
  const progressText = document.querySelector("#prepProgressText");
  const fill = document.querySelector("#prepProgressFill");
  if (label) label.textContent = cal.phase.label;
  if (desc) desc.textContent = cal.phase.desc;
  const sidebarPct = foundationStats.percent < 100 ? foundationStats.percent : prepStats.percent;
  if (progressText) {
    progressText.textContent =
      foundationStats.percent < 100
        ? `基础校验 ${foundationStats.percent}% · 启动准备 ${prepStats.percent}%`
        : `基础校验完成 · 启动准备 ${prepStats.percent}%`;
  }
  if (fill) fill.style.width = `${sidebarPct}%`;
}

function nextWorkItemId() {
  state.workItemSeq += 1;
  const cal = getCalendar();
  return `wi-${cal.todayStr.replace(/-/g, "")}-${String(state.workItemSeq).padStart(3, "0")}`;
}

function findWorkItem(id) {
  return state.workItems.find((w) => w.id === id);
}

function workItemStatusClass(status) {
  const map = {
    backlog: "handoff-status-draft",
    in_progress: "handoff-status-in_progress",
    waiting_handoff: "handoff-status-ready",
    waiting_review: "handoff-status-ready",
    blocked: "handoff-status-blocked",
    done: "handoff-status-done",
  };
  return `handoff-status ${map[status] || ""}`;
}

function migrateHandoffsToWorkItems() {
  if (state.workItems.length || !state.handoffs.length) return;

  state.handoffs.forEach((h) => {
    if (h.status === "draft") return;
    state.workItems.push(handoffToWorkItem(h));
  });
  state.workItemSeq = Math.max(state.workItemSeq, state.handoffSeq);
  persistState();
}

function handoffToWorkItem(h) {
  let category = "handoff";
  let status = "in_progress";
  let reviewTarget = null;

  if (h.direction === "huang_to_li") {
    category = "handoff";
    if (h.status === "ready") status = "waiting_handoff";
    else if (h.status === "in_progress") status = "in_progress";
    else if (h.status === "done") status = "done";
    else if (h.status === "blocked") status = "blocked";
  } else if (h.direction === "li_to_huang") {
    category = "handoff";
    status = h.status === "blocked" ? "blocked" : h.status === "done" ? "done" : "blocked";
  }

  return {
    id: h.id.replace(/^ho-/, "wi-"),
    title: h.title,
    owner: h.owner === "li" ? "li" : "huang",
    category,
    status,
    priority: "p1",
    dueDate: h.date,
    source: "migrated_handoff",
    type: h.type || "general",
    linkedTaskKey: h.linkedTaskKey || null,
    linkedAssetId: h.linkedAssetId || null,
    docFile: h.docFile || "",
    docSection: h.docSection || "",
    brief: h.brief || "",
    expectedOutputs: h.expectedOutputs || [],
    outputNote: h.liNote || "",
    reviewTarget,
    direction: h.direction,
    parentId: h.parentHandoffId || null,
    createdAt: h.huangReadyAt || new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    completedAt: h.liDoneAt || null,
  };
}

function createSeedItem({ title, owner, dueDate, linkedTaskKey, source, docFile, brief, priority, type, expectedOutputs }) {
  const now = new Date().toISOString();
  return {
    id: nextWorkItemId(),
    title,
    owner,
    category: "own",
    status: "backlog",
    priority: priority || "p1",
    dueDate: dueDate || getCalendar().todayStr,
    source: source || "seed",
    type: type || "general",
    linkedTaskKey: linkedTaskKey || null,
    linkedAssetId: null,
    docFile: docFile || "",
    docSection: "",
    brief: brief || "",
    expectedOutputs: expectedOutputs || [],
    outputNote: "",
    reviewTarget: null,
    direction: null,
    parentId: null,
    createdAt: now,
    updatedAt: now,
    completedAt: null,
  };
}

function seedWorkItems() {
  const existingKeys = new Set(state.workItems.map((w) => w.linkedTaskKey).filter(Boolean));
  const existingAssetIds = new Set(state.workItems.map((w) => w.linkedAssetId).filter(Boolean));
  const cal = getCalendar();
  let changed = false;

  weeklyPlans.forEach((week) => {
    week.days.forEach((day) => {
      if (parseDate(day.date) > parseDate(cal.todayStr) && week.week > cal.weekNum) return;
      day.huang.forEach((text, idx) => {
        const key = `${day.date}-huang-${idx}`;
        if (state.workItems.some((w) => w.linkedTaskKey === key)) return;
        state.workItems.push(createSeedItem({ title: text, owner: "huang", dueDate: day.date, linkedTaskKey: key, source: "weekly_plan" }));
        existingKeys.add(key);
        changed = true;
      });
      day.li.forEach((text, idx) => {
        const key = `${day.date}-li-${idx}`;
        if (state.workItems.some((w) => w.linkedTaskKey === key)) return;
        state.workItems.push(createSeedItem({ title: text, owner: "li", dueDate: day.date, linkedTaskKey: key, source: "weekly_plan" }));
        existingKeys.add(key);
        changed = true;
      });
    });
  });

  prepCategories.forEach((cat) => {
    const owner = cat.owner.includes("Brian") ? "li" : cat.owner.includes("Howard") ? "huang" : null;
    if (!owner) return;
    cat.items.forEach((item) => {
      const key = `prep-${item.id}`;
      if (state.workItems.some((w) => w.linkedTaskKey === key)) return;
      state.workItems.push(
        createSeedItem({
          title: item.text,
          owner,
          dueDate: cal.todayStr,
          linkedTaskKey: key,
          source: "prep",
          priority: owner === "li" && /^[AM]/.test(item.id) ? "p1" : "p2",
        }),
      );
      existingKeys.add(key);
      changed = true;
    });
  });

  foundationCategories.forEach((cat) => {
    cat.items.forEach((item) => {
      const key = `foundation-${item.id}`;
      if (state.workItems.some((w) => w.linkedTaskKey === key)) return;
      state.workItems.push(
        createSeedItem({
          title: `[校验] ${item.text}`,
          owner: "huang",
          dueDate: cal.todayStr,
          linkedTaskKey: key,
          source: "foundation",
          priority: "p0",
          docFile: "00-foundation-review.md",
        }),
      );
      existingKeys.add(key);
      changed = true;
    });
  });

  getFinalizedAssets()
    .filter((a) => a.status === "pending")
    .forEach((asset) => {
      if (existingAssetIds.has(asset.id)) return;
      const hasHandoff = state.workItems.some(
        (w) => w.linkedAssetId === asset.id && w.category === "handoff" && w.status !== "done",
      );
      if (hasHandoff) return;
      state.workItems.push({
        ...createSeedItem({
          title: `${asset.title}（建议推送Brian）`,
          owner: "huang",
          dueDate: cal.todayStr,
          source: "finalized",
          priority: "p1",
          docFile: asset.docFile || "",
          brief: asset.note || "",
          expectedOutputs: asset.expectedOutputs || [],
          type: asset.id.includes("pricing") ? "pricing_visual" : "copy_to_visual",
        }),
        linkedAssetId: asset.id,
        category: "own",
        status: "backlog",
      });
      existingAssetIds.add(asset.id);
      changed = true;
    });

  if (changed) persistState();
}

function getWorkItemStats() {
  const active = state.workItems.filter((w) => w.status !== "done");
  const liWaiting = state.workItems.filter((w) => w.category === "handoff" && w.direction === "huang_to_li" && w.status === "waiting_handoff").length;
  const liWorking = state.workItems.filter((w) => w.category === "handoff" && w.direction === "huang_to_li" && w.status === "in_progress").length;
  const huangReview = state.workItems.filter((w) => w.category === "review" && w.status === "waiting_review").length;
  const huangBlocked = state.workItems.filter((w) => w.status === "blocked" && w.owner === "huang").length;
  const todayDone = state.workItems.filter((w) => w.status === "done" && w.completedAt?.startsWith(getCalendar().todayStr)).length;
  return { liWaiting, liWorking, huangReview, huangBlocked, todayDone, active: active.length };
}

function matchesFilter(item) {
  const f = state.workboardFilter;
  if (f === "all") return item.status !== "done" || isRecentDone(item);
  if (f === "active") return ["backlog", "in_progress", "waiting_handoff", "waiting_review", "blocked"].includes(item.status);
  if (f === "done") return item.status === "done";
  const p = state.perspective;
  if (f === "mine") return needsActionFrom(item, p);
  if (f === "theirs") return waitingOnOther(item, p);
  return true;
}

function isRecentDone(item) {
  if (!item.completedAt) return false;
  const days = daysBetween(parseDate(item.completedAt.slice(0, 10)), getToday());
  return days <= 7;
}

function needsActionFrom(item, person) {
  if (item.status === "done") return false;
  if (person === "huang") {
    if (item.category === "review" && item.status === "waiting_review") return true;
    if (item.status === "blocked" && item.direction === "li_blocked_huang") return true;
    if (item.category === "own" && item.owner === "huang") return true;
    if (item.category === "handoff" && item.direction === "huang_to_li" && item.status === "waiting_handoff" && item.owner === "huang") return false;
  }
  if (person === "li") {
    if (item.category === "handoff" && item.direction === "huang_to_li" && ["waiting_handoff", "in_progress"].includes(item.status)) return true;
    if (item.category === "own" && item.owner === "li") return true;
    if (item.status === "blocked" && item.owner === "li") return true;
  }
  return false;
}

function waitingOnOther(item, person) {
  if (item.status === "done") return false;
  if (person === "huang") {
    if (item.category === "review" && item.owner === "li" && item.status === "waiting_review") return true;
    if (item.category === "handoff" && item.direction === "huang_to_li" && item.owner === "li" && item.status === "in_progress") return true;
    if (item.status === "blocked" && item.owner === "li") return true;
  }
  if (person === "li") {
    if (item.category === "review" && item.status === "waiting_review") return true;
    if (item.status === "blocked" && item.direction === "li_blocked_huang") return true;
  }
  return false;
}

function renderWorkBadges() {
  const stats = getWorkItemStats();
  const navBadge = document.querySelector("#workboardNavBadge");
  const sideBadges = document.querySelector("#sideWorkBadges");
  const total = stats.liWaiting + stats.huangReview + stats.huangBlocked;
  if (navBadge) {
    navBadge.hidden = total <= 0;
    navBadge.textContent = String(total);
  }
  if (sideBadges) {
    sideBadges.innerHTML = `
      <span>Brian待接手 ${stats.liWaiting}</span>
      <span>Howard待确认 ${stats.huangReview}</span>
      <span>Howard待补充 ${stats.huangBlocked}</span>
    `;
  }
}

function renderWorkboard() {
  const cal = getCalendar();
  const day = cal.dayPlan;
  const stats = getWorkItemStats();

  const titleEl = document.querySelector("#workboardTitle");
  const subtitleEl = document.querySelector("#workboardSubtitle");
  if (titleEl) titleEl.textContent = `协同工作台 · ${cal.todayStr}`;
  if (subtitleEl) {
    subtitleEl.textContent = `${cal.weekdayName} · ${day.focus}。第 ${cal.weekNum} 周 · ${day.deliverable}`;
  }

  const meta = document.querySelector("#workboardMeta");
  if (meta) {
    meta.innerHTML = `
      <article><b>今日重点</b><span>${escapeHtml(day.focus)}</span></article>
      <article><b>本周交付物</b><span>${escapeHtml(cal.weekPlan.acceptance[0] || day.deliverable)}</span></article>
      <article><b>工作项进度</b><span>进行中 ${stats.active} · 今日完成 ${stats.todayDone}</span></article>
      <article><b>视角</b><span>${state.perspective === "huang" ? "Howard" : "Brian"} · 筛选 ${filterLabel(state.workboardFilter)}</span></article>
    `;
  }

  renderPersonZone("huang");
  renderPersonZone("li");
  renderWorkboardLane();
  renderWorkboardFooter(day);
  renderWorkBadges();

  document.querySelectorAll(".filter-chip").forEach((chip) => {
    chip.classList.toggle("active", chip.dataset.filter === state.workboardFilter);
  });
}

function filterLabel(f) {
  return { all: "全部", active: "进行中", mine: "待我处理", theirs: "待对方", done: "已完成" }[f] || f;
}

function renderPersonZone(person) {
  const zone = document.querySelector(person === "huang" ? "#huangZone" : "#liZone");
  if (!zone) return;

  const items = state.workItems.filter(matchesFilter);
  const name = person === "huang" ? "Howard" : "Brian";
  const role = person === "huang" ? "策略 / 文案 / 口径" : "视觉 / 素材 / 完稿";

  let blocks = [];
  if (person === "huang") {
    const own = items.filter((w) => w.category === "own" && w.owner === "huang" && w.status !== "done");
    const review = items.filter((w) => w.category === "review" && w.status === "waiting_review");
    const blocked = items.filter((w) => w.status === "blocked" && (w.direction === "li_blocked_huang" || w.owner === "huang"));
    const sent = items.filter((w) => w.category === "handoff" && w.direction === "huang_to_li");
    const suggestions = getFinalizedAssets().filter(
      (a) => a.status === "pending" && !state.workItems.some((w) => w.linkedAssetId === a.id && w.category === "handoff" && w.status !== "done"),
    );

    blocks = [
      ["我的任务", own],
      ["待我确认（Brian视觉稿）", review],
      ["待我补充", blocked],
      ["我发起的交接", sent.filter((w) => w.status !== "done")],
    ];

    if (suggestions.length) {
      blocks.push([
        "已定稿资产 · 建议推送",
        suggestions.map((a) => ({ _suggest: true, asset: a })),
      ]);
    }
  } else {
    const own = items.filter((w) => w.category === "own" && w.owner === "li" && w.status !== "done");
    const handoffs = items.filter((w) => w.category === "handoff" && w.direction === "huang_to_li");
    const waiting = handoffs.filter((w) => w.status === "waiting_handoff");
    const working = handoffs.filter((w) => w.status === "in_progress");
    const reviews = items.filter((w) => w.category === "review" && w.owner === "li" && w.status === "waiting_review");
    const blocked = items.filter((w) => w.status === "blocked" && w.owner === "li");

    blocks = [
      ["我的任务", own],
      ["来自Howard的交接（待接手）", waiting],
      ["制作中", working],
      ["待Howard确认", reviews],
      ["需Howard补充", blocked],
    ];
  }

  const doneOwn = state.workItems.filter((w) => w.category === "own" && w.owner === person && w.status === "done").length;

  zone.innerHTML = `
    <div class="collab-zone-head">
      <h3>${name}工作区</h3>
      <span>${role} · 已完成 ${doneOwn} 项自有任务</span>
    </div>
    ${blocks
      .map(([title, list]) => {
        if (!list.length) {
          return `<div class="collab-block"><h4>${escapeHtml(title)}</h4><p class="handoff-lane-empty">暂无</p></div>`;
        }
        const cards = list
          .map((entry) => (entry._suggest ? renderSuggestCard(entry.asset) : renderWorkItemCard(entry, person)))
          .join("");
        return `<div class="collab-block"><h4>${escapeHtml(title)}</h4>${cards}</div>`;
      })
      .join("")}
  `;
}

function renderSuggestCard(asset) {
  const docBtn = asset.docFile
    ? `<button type="button" class="action-button wi-doc-button" data-open-doc="${escapeHtml(asset.docId || resolveDocLink(asset.docFile) || "")}">查看文档：${escapeHtml(asset.title)}</button>`
    : "";
  return `
    <article class="handoff-card suggest-card">
      <div class="handoff-card-head">
        <h5>${escapeHtml(asset.title)}</h5>
        <span class="handoff-status handoff-status-ready">建议推送</span>
      </div>
      ${docBtn ? `<div class="wi-doc-strip">${docBtn}</div>` : ""}
      <p>${escapeHtml(asset.note)}</p>
      <div class="handoff-card-actions">
        <button type="button" class="action-button" data-suggest-push="${escapeHtml(asset.id)}">推送给Brian</button>
      </div>
    </article>
  `;
}

function resolveWorkItemDoc(item) {
  if (item.docFile) return item.docFile;
  const title = item.title || "";
  if (item.source === "foundation" || /校验/.test(title)) return "00-foundation-review.md";
  if (item.source === "prep" || /账号|素材库|收款/.test(title)) return "00-startup-checklist.md";
  if (/企业介绍|私聊|介绍图|平台简介/.test(title)) return "12-company-profile-delivery-standards.md";
  if (/报价/.test(title)) return "03-public-pricing.md";
  if (/闲鱼/.test(title)) return "11-xianyu-channel-pilot.md";
  if (/多淼/.test(title)) return "09-duomiao-partnership.md";
  if (/案例/.test(title)) return "06-case-packaging-library.md";
  if (/询盘|话术|协议/.test(title)) return "08-sales-and-intake-sop.md";
  if (item.source === "weekly_plan") return "10-two-person-execution-plan.md";
  return "";
}

function getWorkItemDocMeta(item) {
  const file = resolveWorkItemDoc(item);
  if (!file) return null;
  const doc = docs.find((d) => d.file === file);
  return { file, doc, title: doc?.title || file.split("/").pop() };
}

function renderWorkItemDocStrip(item) {
  const meta = getWorkItemDocMeta(item);
  if (!meta) {
    return `<div class="wi-doc-strip"><span class="wi-no-doc">暂无关联文档（可在新建/推送时绑定）</span></div>`;
  }
  const section = item.docSection ? ` · ${escapeHtml(item.docSection)}` : "";
  return `
    <div class="wi-doc-strip">
      <button type="button" class="action-button wi-doc-button" data-open-wi-doc="${escapeHtml(item.id)}">
        查看文档：${escapeHtml(meta.title)}${section}
      </button>
      <button type="button" class="text-button" data-download-wi-doc="${escapeHtml(item.id)}">下载 MD</button>
    </div>
  `;
}

function renderWorkItemCard(item, viewPerson) {
  const statusLabel = WORK_ITEM_STATUS_LABELS[item.status] || item.status;
  const outputs = (item.expectedOutputs || []).join("、") || "—";
  const priorityTag = item.priority === "p0" ? "P0" : item.priority === "p1" ? "P1" : "P2";
  const due = item.dueDate ? item.dueDate.slice(5) : "—";
  const docStrip = renderWorkItemDocStrip(item);

  let actions = "";

  if (viewPerson === "huang") {
    if (item.category === "own" && item.owner === "huang" && item.status !== "done") {
      actions = `
        ${item.status === "backlog" ? `<button type="button" class="text-button" data-wi-start="${escapeHtml(item.id)}">开始</button>` : ""}
        <button type="button" class="text-button" data-wi-push="${escapeHtml(item.id)}">推送给Brian</button>
        <button type="button" class="action-button" data-wi-done="${escapeHtml(item.id)}">完成</button>
      `;
    }
    if (item.category === "review" && item.status === "waiting_review") {
      actions = `
        <button type="button" class="action-button primary" data-wi-confirm="${escapeHtml(item.id)}">确认通过</button>
        <button type="button" class="text-button" data-wi-reject="${escapeHtml(item.id)}">打回修改</button>
      `;
    }
    if (item.status === "blocked" && (item.direction === "li_blocked_huang" || item.owner === "huang")) {
      actions = `<button type="button" class="action-button" data-wi-resolve-block="${escapeHtml(item.id)}">已补充</button>`;
    }
    if (item.category === "handoff" && item.direction === "huang_to_li" && item.status === "waiting_handoff") {
      actions = `<button type="button" class="text-button" data-wi-cancel-handoff="${escapeHtml(item.id)}">撤回</button>`;
    }
    if (item.category === "handoff" && item.direction === "huang_to_li" && item.status === "in_progress") {
      actions = `<span class="handoff-status handoff-status-in_progress">Brian制作中</span>`;
    }
  }

  if (viewPerson === "li") {
    if (item.category === "own" && item.owner === "li" && item.status !== "done") {
      actions = `
        ${item.status === "backlog" ? `<button type="button" class="text-button" data-wi-start="${escapeHtml(item.id)}">开始</button>` : ""}
        <button type="button" class="text-button" data-wi-submit-review="${escapeHtml(item.id)}">提交视觉稿</button>
        <button type="button" class="action-button" data-wi-done="${escapeHtml(item.id)}">完成</button>
      `;
    }
    if (item.category === "handoff" && item.direction === "huang_to_li") {
      if (item.status === "waiting_handoff") {
        actions = `<button type="button" class="action-button primary" data-wi-ack="${escapeHtml(item.id)}">已接手，开始制作</button>`;
      }
      if (item.status === "in_progress") {
        actions = `
          <button type="button" class="text-button" data-wi-block="${escapeHtml(item.id)}">需Howard补充</button>
          <button type="button" class="text-button" data-wi-submit-review="${escapeHtml(item.id)}">提交视觉稿</button>
          <button type="button" class="action-button primary" data-wi-done="${escapeHtml(item.id)}">确认完成</button>
        `;
      }
    }
    if (item.category === "review" && item.status === "waiting_review") {
      actions = `<span class="handoff-status handoff-status-ready">等待Howard确认</span>`;
    }
    if (item.status === "blocked" && item.owner === "li") {
      actions = `<span class="handoff-status handoff-status-blocked">等待Howard补充</span>`;
    }
  }

  return `
    <article class="handoff-card wi-card" data-priority="${escapeHtml(item.priority)}">
      <div class="handoff-card-head">
        <h5>${escapeHtml(item.title)}</h5>
        <span class="${workItemStatusClass(item.status)}">${escapeHtml(statusLabel)}</span>
      </div>
      ${docStrip}
      <p>${escapeHtml(item.brief || "")}</p>
      <div class="handoff-card-meta">
        <span class="wi-priority">${priorityTag}</span>
        <span>截止 ${due}</span>
        <span>产出：${escapeHtml(outputs)}</span>
      </div>
      ${item.outputNote ? `<p><b>备注：</b>${escapeHtml(item.outputNote)}</p>` : ""}
      ${actions ? `<div class="handoff-card-actions">${actions}</div>` : ""}
    </article>
  `;
}

function renderWorkboardLane() {
  const body = document.querySelector("#workboardLaneBody");
  const lane = document.querySelector("#workboardLane");
  if (!body || !lane) return;
  lane.classList.toggle("lane-collapsed", state.laneCollapsed);
  body.hidden = state.laneCollapsed;

  const chains = state.workItems
    .filter((w) => w.category === "handoff" || w.category === "review")
    .filter((w) => w.status !== "done")
    .slice(0, 12);

  if (!chains.length) {
    body.innerHTML = `<p class="handoff-lane-empty">暂无活跃交接链路。</p>`;
    return;
  }

  body.innerHTML = `
    <table class="handoff-lane-table">
      <thead><tr><th>Howard侧</th><th>Brian侧</th><th>文档</th><th>状态</th></tr></thead>
      <tbody>
        ${chains
          .map((w) => {
            const huangSide =
              w.direction === "huang_to_li"
                ? escapeHtml(w.title)
                : w.direction === "li_blocked_huang"
                  ? `待补充：${escapeHtml(w.brief || w.title)}`
                  : w.category === "review"
                    ? `待确认：${escapeHtml(w.title)}`
                    : "—";
            const liSide =
              w.direction === "huang_to_li"
                ? escapeHtml((w.expectedOutputs || []).join("、") || "视觉制作")
                : w.category === "review"
                  ? `已提交：${escapeHtml(w.title)}`
                  : escapeHtml(w.title);
            const docBtn = w.docFile
              ? `<button type="button" class="text-button" data-open-wi-doc="${escapeHtml(w.id)}">${escapeHtml(w.docFile)}</button>`
              : "—";
            return `<tr><td>${huangSide}</td><td>${liSide}</td><td>${docBtn}</td><td><span class="${workItemStatusClass(w.status)}">${escapeHtml(WORK_ITEM_STATUS_LABELS[w.status])}</span></td></tr>`;
          })
          .join("")}
      </tbody>
    </table>
  `;
}

function renderWorkboardFooter(day) {
  const footer = document.querySelector("#workboardFooter");
  if (!footer) return;
  const cal = getCalendar();
  const blocker = state.daily[`${cal.todayStr}-blocker`] || "";
  const tomorrow = state.daily[`${cal.todayStr}-tomorrow`] || day.deliverable;
  footer.innerHTML = `
    <h3>共同推进</h3>
    <label><span>今日卡点</span><textarea id="dailyBlocker" rows="2" placeholder="写真实问题">${escapeHtml(blocker)}</textarea></label>
    <label><span>明日第一件事</span><input type="text" id="dailyTomorrow" value="${escapeHtml(tomorrow)}" /></label>
  `;
}

function populateWorkItemFormDefaults() {
  const docSelect = document.querySelector("#wiDocFile");
  if (docSelect && docSelect.options.length <= 1) {
    docSelect.innerHTML =
      `<option value="">不关联文档</option>` +
      docs.map((doc) => `<option value="${escapeHtml(doc.file)}">${escapeHtml(doc.title)} · ${escapeHtml(doc.file)}</option>`).join("");
  }
  const due = document.querySelector("#wiDueDate");
  if (due && !due.value) due.value = getCalendar().todayStr;
}

function openWorkItemDialog(options = {}) {
  populateWorkItemFormDefaults();
  const dialog = document.querySelector("#workItemDialog");
  if (!dialog) return;

  document.querySelector("#wiMode").value = options.mode || "create";
  document.querySelector("#wiEditingId").value = options.editingId || "";
  document.querySelector("#wiCategory").value = options.category || "own";
  document.querySelector("#wiDirection").value = options.direction || "";
  document.querySelector("#wiLinkedTaskKey").value = options.linkedTaskKey || "";
  document.querySelector("#wiLinkedAssetId").value = options.linkedAssetId || "";
  document.querySelector("#wiParentId").value = options.parentId || "";
  document.querySelector("#wiTitle").value = options.title || "";
  document.querySelector("#wiOwner").value = options.owner || "huang";
  document.querySelector("#wiPriority").value = options.priority || "p1";
  document.querySelector("#wiDueDate").value = options.dueDate || getCalendar().todayStr;
  if (options.docFile) document.querySelector("#wiDocFile").value = options.docFile;
  document.querySelector("#wiDocSection").value = options.docSection || "";
  document.querySelector("#wiBrief").value = options.brief || "";
  document.querySelector("#wiOutputs").value = (options.expectedOutputs || []).join(", ");

  const titleEl = document.querySelector("#workItemDialogTitle");
  const submitBtn = document.querySelector("#workItemSubmitButton");
  if (titleEl) {
    titleEl.textContent =
      options.category === "handoff"
        ? "推送给Brian"
        : options.category === "review"
          ? "提交视觉稿"
          : "新建工作项";
  }
  if (submitBtn) submitBtn.textContent = options.category === "handoff" ? "确认推送" : "保存";

  dialog.showModal();
}

function closeWorkItemDialog() {
  document.querySelector("#workItemDialog")?.close();
}

function saveWorkItemFromForm() {
  const mode = document.querySelector("#wiMode").value;
  const title = document.querySelector("#wiTitle").value.trim();
  const brief = document.querySelector("#wiBrief").value.trim();
  if (!title) return;

  const payload = {
    title,
    owner: document.querySelector("#wiOwner").value,
    category: document.querySelector("#wiCategory").value,
    direction: document.querySelector("#wiDirection").value || null,
    priority: document.querySelector("#wiPriority").value,
    dueDate: document.querySelector("#wiDueDate").value,
    docFile: document.querySelector("#wiDocFile").value,
    docSection: document.querySelector("#wiDocSection").value.trim(),
    brief,
    expectedOutputs: document
      .querySelector("#wiOutputs")
      .value.split(/[,，]/)
      .map((s) => s.trim())
      .filter(Boolean),
    linkedTaskKey: document.querySelector("#wiLinkedTaskKey").value || null,
    linkedAssetId: document.querySelector("#wiLinkedAssetId").value || null,
    parentId: document.querySelector("#wiParentId").value || null,
  };

  if (mode === "edit") {
    const item = findWorkItem(document.querySelector("#wiEditingId").value);
    if (item) Object.assign(item, payload, { updatedAt: new Date().toISOString() });
  } else {
    const now = new Date().toISOString();
    let status = "backlog";
    let category = payload.category;
    let direction = payload.direction;

    if (category === "handoff" || direction === "huang_to_li") {
      category = "handoff";
      direction = "huang_to_li";
      status = "waiting_handoff";
      payload.owner = "li";
    }

    state.workItems.push({
      id: nextWorkItemId(),
      ...payload,
      category,
      direction,
      status,
      type: "general",
      source: "manual",
      outputNote: "",
      reviewTarget: null,
      createdAt: now,
      updatedAt: now,
      completedAt: null,
    });
  }

  persistState();
  closeWorkItemDialog();
  renderAll();
}

function startWorkItem(id) {
  const item = findWorkItem(id);
  if (!item) return;
  item.status = "in_progress";
  item.updatedAt = new Date().toISOString();
  persistState();
  renderAll();
}

function completeWorkItem(id) {
  const item = findWorkItem(id);
  if (!item) return;
  item.status = "done";
  item.completedAt = new Date().toISOString();
  item.updatedAt = item.completedAt;

  if (item.linkedAssetId) {
    const asset = state.finalizedAssets.find((a) => a.id === item.linkedAssetId);
    if (asset) {
      asset.status = "done";
      asset.date = getCalendar().todayStr;
    }
  }

  persistState();
  renderAll();
}

function ackHandoffWorkItem(id) {
  const item = findWorkItem(id);
  if (!item) return;
  item.status = "in_progress";
  item.updatedAt = new Date().toISOString();
  persistState();
  renderAll();
}

function pushFromOwnItem(id) {
  const item = findWorkItem(id);
  if (!item) return;
  openWorkItemDialog({
    category: "handoff",
    direction: "huang_to_li",
    title: `${item.title} → 视觉制作`,
    brief: item.brief || item.title,
    docFile: item.docFile,
    docSection: item.docSection,
    expectedOutputs: item.expectedOutputs,
    linkedTaskKey: item.linkedTaskKey,
    linkedAssetId: item.linkedAssetId,
    parentId: item.id,
  });
}

function suggestPushFromAsset(assetId) {
  const asset = getFinalizedAssets().find((a) => a.id === assetId);
  if (!asset) return;
  openWorkItemDialog({
    category: "handoff",
    direction: "huang_to_li",
    title: `${asset.title} → 视觉制作`,
    brief: asset.note || "",
    docFile: asset.docFile || "",
    docSection: asset.docSection || "",
    expectedOutputs: asset.expectedOutputs || [],
    linkedAssetId: asset.id,
    type: asset.id.includes("pricing") ? "pricing_visual" : "copy_to_visual",
  });
}

function submitVisualReview(id) {
  const item = findWorkItem(id);
  if (!item) return;
  const now = new Date().toISOString();
  state.workItems.push({
    id: nextWorkItemId(),
    title: `视觉稿：${item.title}`,
    owner: "li",
    category: "review",
    status: "waiting_review",
    priority: item.priority,
    dueDate: item.dueDate,
    source: "review",
    type: "visual_review",
    linkedTaskKey: item.linkedTaskKey,
    linkedAssetId: item.linkedAssetId,
    docFile: item.docFile,
    docSection: item.docSection,
    brief: item.brief,
    expectedOutputs: item.expectedOutputs,
    outputNote: "",
    reviewTarget: "huang",
    direction: "li_to_huang",
    parentId: item.id,
    createdAt: now,
    updatedAt: now,
    completedAt: null,
  });
  if (item.category === "handoff") item.status = "waiting_review";
  else item.status = "waiting_review";
  item.updatedAt = now;
  persistState();
  renderAll();
}

function confirmReview(id) {
  const item = findWorkItem(id);
  if (!item) return;
  item.status = "done";
  item.completedAt = new Date().toISOString();
  item.updatedAt = item.completedAt;
  if (item.parentId) {
    const parent = findWorkItem(item.parentId);
    if (parent) completeWorkItem(parent.id);
    return;
  }
  persistState();
  renderAll();
}

function openRejectDialog(id) {
  document.querySelector("#rejectWorkItemId").value = id;
  document.querySelector("#rejectNote").value = "";
  document.querySelector("#rejectDialog")?.showModal();
}

function rejectReviewFromForm() {
  const id = document.querySelector("#rejectWorkItemId").value;
  const note = document.querySelector("#rejectNote").value.trim();
  if (!note) return;
  const item = findWorkItem(id);
  if (!item) return;
  item.status = "in_progress";
  item.outputNote = note;
  item.updatedAt = new Date().toISOString();
  if (item.parentId) {
    const parent = findWorkItem(item.parentId);
    if (parent) {
      parent.status = "in_progress";
      parent.outputNote = note;
      parent.updatedAt = item.updatedAt;
    }
  }
  document.querySelector("#rejectDialog")?.close();
  persistState();
  renderAll();
}

function blockForCopy(id) {
  const item = findWorkItem(id);
  if (!item) return;
  const note = window.prompt("需要Howard补充什么？（简短说明）", item.outputNote || "");
  if (note === null) return;

  const now = new Date().toISOString();
  item.status = "blocked";
  item.outputNote = note;
  item.updatedAt = now;

  state.workItems.push({
    id: nextWorkItemId(),
    title: `需补充：${item.title}`,
    owner: "huang",
    category: "handoff",
    status: "blocked",
    priority: item.priority,
    dueDate: item.dueDate,
    source: "blocked",
    type: "copy_revision",
    linkedTaskKey: item.linkedTaskKey,
    linkedAssetId: item.linkedAssetId,
    docFile: item.docFile,
    docSection: item.docSection,
    brief: note,
    expectedOutputs: [],
    outputNote: note,
    reviewTarget: null,
    direction: "li_blocked_huang",
    parentId: item.id,
    createdAt: now,
    updatedAt: now,
    completedAt: null,
  });

  persistState();
  renderAll();
}

function resolveBlock(id) {
  const blocked = findWorkItem(id);
  if (!blocked) return;
  blocked.status = "done";
  blocked.updatedAt = new Date().toISOString();
  if (blocked.parentId) {
    const parent = findWorkItem(blocked.parentId);
    if (parent) {
      parent.status = parent.category === "handoff" ? "in_progress" : "in_progress";
      parent.outputNote = "";
      parent.updatedAt = blocked.updatedAt;
    }
  }
  persistState();
  renderAll();
}

function cancelHandoffWorkItem(id) {
  const item = findWorkItem(id);
  if (!item || item.status !== "waiting_handoff") return;
  item.status = "done";
  item.outputNote = "已撤回";
  item.completedAt = new Date().toISOString();
  persistState();
  renderAll();
}

function recordRecentDoc(file) {
  if (!file) return;
  state.recentDocs = [file, ...state.recentDocs.filter((f) => f !== file)].slice(0, 8);
  persistState();
}

async function openSplitDoc(docIdOrFile) {
  const doc = docs.find((d) => d.id === docIdOrFile) || docs.find((d) => d.file === docIdOrFile);
  if (!doc) return;

  state.splitDoc = doc;
  state.activeDoc = doc;
  state.splitPaneOpen = true;

  const pane = document.querySelector("#docSplitPane");
  const backdrop = document.querySelector("#docBackdrop");
  if (pane) {
    pane.hidden = false;
    pane.setAttribute("aria-hidden", "false");
  }
  if (backdrop) {
    backdrop.hidden = false;
    backdrop.setAttribute("aria-hidden", "false");
  }

  document.querySelector("#splitDocTitle").textContent = doc.title;
  document.querySelector("#splitDocPath").textContent = doc.file;

  try {
    if (!state.cache.has(doc.file)) {
      state.cache.set(doc.file, await fetchMarkdownText(doc.file));
    }
    const original = state.cache.get(doc.file);
    const draft = state.drafts.get(doc.file) || original;
    document.querySelector("#splitDraftEditor").value = draft;
    state.markdown = original;
    setSplitMode("read");
    recordRecentDoc(doc.file);
    renderDocLookup();
    refreshIcons();
  } catch (error) {
    document.querySelector("#splitRenderedMarkdown").innerHTML = `<div class="empty-state"><p>${escapeHtml(error.message)}</p></div>`;
  }
}

async function fetchMarkdownText(file) {
  const endpoints = [
    `/api/doc?file=${encodeURIComponent(file)}`,
    `./${file}`,
  ];
  let lastError = new Error("无法加载文档");
  for (const url of endpoints) {
    try {
      const response = await fetch(url, { cache: "no-store", redirect: "follow" });
      if (!response.ok) {
        lastError = new Error(`无法加载（HTTP ${response.status}）`);
        continue;
      }
      const text = await response.text();
      if (looksLikeHtmlPage(text)) {
        lastError = new Error("文档读取失败：服务把工作台页面当成了 Markdown。请重启 server.py 后硬刷新（Cmd+Shift+R）。");
        continue;
      }
      return text;
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));
    }
  }
  throw lastError;
}

function looksLikeHtmlPage(text) {
  const head = String(text || "").slice(0, 400).toLowerCase();
  return head.includes("<!doctype html") || head.includes("<html") || head.includes('<section class="workspace"');
}

function closeSplitPane() {
  const pane = document.querySelector("#docSplitPane");
  const backdrop = document.querySelector("#docBackdrop");
  if (pane) {
    pane.hidden = true;
    pane.setAttribute("aria-hidden", "true");
  }
  if (backdrop) {
    backdrop.hidden = true;
    backdrop.setAttribute("aria-hidden", "true");
  }
  state.splitPaneOpen = false;
  state.search = "";
  const lookupSearch = document.querySelector("#doclookupSearch");
  if (lookupSearch) lookupSearch.value = "";
}

function setSplitMode(mode) {
  state.mode = mode;
  const layout = document.querySelector(".doc-split-body");
  layout?.classList.toggle("compare", mode === "compare");
  layout?.classList.toggle("edit", mode === "edit");
  document.querySelectorAll("[data-split-mode]").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.splitMode === mode);
  });
  const original = state.cache.get(state.splitDoc?.file) || state.markdown;
  const draft = state.drafts.get(state.splitDoc?.file) || original;
  document.querySelector("#splitDraftEditor").value = draft;
  state.markdown = mode === "read" ? original : draft;
  renderSplitMarkdown();
}

function renderSplitMarkdown() {
  const el = document.querySelector("#splitRenderedMarkdown");
  if (!el) return;
  const html = markdownToHtml(state.markdown);
  el.innerHTML = state.search ? highlight(html, state.search) : html;
}

async function openWorkItemDoc(id) {
  const item = findWorkItem(id);
  const file = item ? resolveWorkItemDoc(item) : "";
  if (!file) return;
  const docId = resolveDocLink(file);
  if (docId) await openSplitDoc(docId);
}

async function downloadWorkItemDoc(id) {
  const item = findWorkItem(id);
  const file = item ? resolveWorkItemDoc(item) : "";
  if (!file) return;
  try {
    const text = state.cache.get(file) || (await fetchMarkdownText(file));
    const blob = new Blob([text], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = file;
    anchor.click();
    URL.revokeObjectURL(url);
  } catch {
    window.alert("无法下载 Markdown 文件。请重启 server.py 后重试。");
  }
}

function renderDocLookup() {
  const pinned = document.querySelector("#doclookupPinned");
  if (pinned) {
    pinned.innerHTML = `
      <h3>固定入口</h3>
      <div class="doclookup-pinned-grid">
        ${PINNED_DOCS.map(
          (p) => `<button type="button" class="doc-pin-button" data-open-doc="${p.id}">${escapeHtml(p.label)}</button>`,
        ).join("")}
      </div>
    `;
  }

  const recent = document.querySelector("#doclookupRecent");
  if (recent) {
    recent.innerHTML = state.recentDocs.length
      ? `<h3>最近打开</h3><div class="doclookup-recent-list">${state.recentDocs
          .map((file) => {
            const doc = docs.find((d) => d.file === file);
            return doc
              ? `<button type="button" class="doc-pin-button" data-open-doc="${doc.id}">${escapeHtml(doc.title)}</button>`
              : "";
          })
          .join("")}</div>`
      : `<h3>最近打开</h3><p class="handoff-lane-empty">从工作项打开文档后会出现在这里。</p>`;
  }

  const nav = document.querySelector("#doclookupNav");
  if (nav) {
    nav.innerHTML = Object.entries(DOC_LOOKUP_GROUPS)
      .map(([group, ids]) => {
        const buttons = ids
          .map((id) => {
            const doc = docs.find((d) => d.id === id);
            return doc
              ? `<button type="button" class="doc-button" data-open-doc="${doc.id}"><strong>${escapeHtml(doc.title)}</strong><span>${escapeHtml(doc.subtitle)}</span></button>`
              : "";
          })
          .join("");
        return `<section class="doclookup-group"><h4>${escapeHtml(group)}</h4>${buttons}</section>`;
      })
      .join("");
  }
}

function renderInquiries() {
  const body = document.querySelector("#inquiryBody");
  if (!body) return;
  if (!state.inquiries.length) {
    body.innerHTML = `<tr><td colspan="7" class="empty-cell">暂无询盘记录</td></tr>`;
    return;
  }

  body.innerHTML = state.inquiries
    .slice()
    .reverse()
    .map(
      (item, idx) => `
      <tr>
        <td>${escapeHtml(item.date)}</td>
        <td>${escapeHtml(item.source)}</td>
        <td>${escapeHtml(item.product)}</td>
        <td>${escapeHtml(item.price || "—")}</td>
        <td><span class="status-badge status-${statusClass(item.status)}">${escapeHtml(item.status)}</span></td>
        <td>${escapeHtml(item.note || "")}</td>
        <td><button class="text-button" data-delete-inquiry="${state.inquiries.length - 1 - idx}">删除</button></td>
      </tr>
    `,
    )
    .join("");
}

function statusClass(status) {
  if (status === "已成交") return "done";
  if (status === "已报价" || status === "询盘中") return "progress";
  return "pending";
}

function renderReview() {
  const cal = getCalendar();
  const todayReview = state.reviews.find((r) => r.date === cal.todayStr);

  ["reviewQ1", "reviewQ2", "reviewQ3", "reviewQ4", "reviewQ5"].forEach((id, idx) => {
    const el = document.querySelector(`#${id}`);
    if (el) el.value = todayReview?.answers?.[idx] || "";
  });

  const history = state.reviews
    .filter((r) => r.date !== cal.todayStr)
    .slice(-5)
    .reverse();

  document.querySelector("#reviewHistory").innerHTML = history.length
    ? `<h3>近期复盘</h3>${history
        .map(
          (r) => `
        <article class="review-card">
          <header><strong>${escapeHtml(r.date)}</strong></header>
          <p><b>明日优先：</b>${escapeHtml(r.answers[4] || "—")}</p>
          <p><b>成果：</b>${escapeHtml((r.answers[0] || "—").slice(0, 80))}</p>
        </article>
      `,
        )
        .join("")}`
    : "";

  const stats = getWorkItemStats();
  const doneToday = state.workItems.filter((w) => w.status === "done" && w.completedAt?.startsWith(cal.todayStr));
  const reviews = state.workItems.filter((w) => w.category === "review" && w.completedAt?.startsWith(cal.todayStr));
  const handoffs = state.workItems.filter((w) => w.category === "handoff" && w.status === "done" && w.completedAt?.startsWith(cal.todayStr));
  const summaryEl = document.querySelector("#reviewWorkSummary");
  if (summaryEl) {
    summaryEl.textContent = `今日工作项：完成 ${doneToday.length} 项 · 确认通过 ${reviews.length} 项 · 交接完成 ${handoffs.length} 项 · 待确认 ${stats.huangReview} · 待接手 ${stats.liWaiting}`;
  }
}

function renderSettings() {
  const grid = document.querySelector("#settingsGrid");
  if (!grid) return;
  const cal = getCalendar();
  const prepStats = getPrepStats();
  const foundationStats = getFoundationStats();
  const data = packState();

  grid.innerHTML = `
    <article class="settings-card">
      <h3>协同同步</h3>
      <p>${SYNC.enabled ? "已连接 server.py，data.json 双人同步。" : "未连接，请运行 python3 server.py --port 8025"}</p>
      <p>最近更新：${SYNC.updatedAt ? formatSyncTime(SYNC.updatedAt) : "—"}</p>
    </article>
    <article class="settings-card">
      <h3>当前阶段</h3>
      <p><strong>${escapeHtml(cal.phase.label)}</strong> — ${escapeHtml(cal.phase.desc)}</p>
      <p>第 ${cal.weekNum} 周 · 基础校验 ${foundationStats.percent}% · 启动准备 ${prepStats.percent}%</p>
    </article>
    <article class="settings-card">
      <h3>工作项统计</h3>
      <p>共 ${state.workItems.length} 项 · 进行中 ${getWorkItemStats().active} · 已完成 ${state.workItems.filter((w) => w.status === "done").length}</p>
    </article>
    <article class="settings-card">
      <h3>数据导出</h3>
      <button type="button" class="action-button" id="exportDataButton">导出 JSON 快照</button>
      <button type="button" class="action-button" id="exportCsvButton">导出本周工作项 CSV</button>
    </article>
    <article class="settings-card">
      <h3>开发文档</h3>
      <p>v2 规格见 <code>docs/workbench-spec-v2.md</code></p>
      <button type="button" class="text-button" data-open-doc="readme">打开 README</button>
    </article>
  `;
}

function exportDataJson() {
  const blob = new Blob([JSON.stringify(packState(), null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `gensight-data-${getCalendar().todayStr}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

function exportWorkItemsCsv() {
  const cal = getCalendar();
  const weekStart = cal.weekPlan.days[0]?.date || cal.todayStr;
  const rows = [["id", "title", "owner", "category", "status", "dueDate", "source", "completedAt"]];
  state.workItems
    .filter((w) => !w.dueDate || w.dueDate >= weekStart)
    .forEach((w) => {
      rows.push([w.id, w.title, w.owner, w.category, w.status, w.dueDate, w.source, w.completedAt || ""]);
    });
  const csv = rows.map((r) => r.map((c) => `"${String(c).replace(/"/g, '""')}"`).join(",")).join("\n");
  const blob = new Blob(["\ufeff" + csv], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `workitems-week${cal.weekNum}-${cal.todayStr}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

function setInquiryDateDefault() {
  const el = document.querySelector("#inquiryDate");
  if (el) el.value = formatDate(getToday());
}

function bindEvents() {
  document.querySelectorAll(".nav-item[data-section]").forEach((button) => {
    button.addEventListener("click", () => showSection(button.dataset.section));
  });

  document.querySelector("#newWorkItemButton")?.addEventListener("click", () => openWorkItemDialog({ owner: "huang" }));
  document.querySelector("#workItemForm")?.addEventListener("submit", (e) => {
    e.preventDefault();
    saveWorkItemFromForm();
  });
  document.querySelector("#workItemCancelButton")?.addEventListener("click", closeWorkItemDialog);
  document.querySelector("#workItemDialogClose")?.addEventListener("click", closeWorkItemDialog);

  document.querySelector("#rejectForm")?.addEventListener("submit", (e) => {
    e.preventDefault();
    rejectReviewFromForm();
  });
  document.querySelector("#rejectCancelButton")?.addEventListener("click", () => document.querySelector("#rejectDialog")?.close());
  document.querySelector("#rejectDialogClose")?.addEventListener("click", () => document.querySelector("#rejectDialog")?.close());

  document.querySelector("#workboardFilters")?.addEventListener("click", (e) => {
    const chip = e.target.closest("[data-filter]");
    if (chip) {
      state.workboardFilter = chip.dataset.filter;
      renderWorkboard();
      return;
    }
    const perspectiveBtn = e.target.closest("[data-perspective]");
    if (perspectiveBtn) {
      state.perspective = perspectiveBtn.dataset.perspective;
      document.querySelectorAll("[data-perspective]").forEach((btn) => {
        btn.classList.toggle("active", btn.dataset.perspective === state.perspective);
      });
      renderWorkboard();
    }
  });

  document.querySelector("#toggleLaneButton")?.addEventListener("click", () => {
    state.laneCollapsed = !state.laneCollapsed;
    renderWorkboardLane();
    const btn = document.querySelector("#toggleLaneButton");
    if (btn) btn.textContent = state.laneCollapsed ? "展开" : "收起";
  });

  document.querySelector("#splitCloseButton")?.addEventListener("click", (event) => {
    event.preventDefault();
    event.stopPropagation();
    closeSplitPane();
  });
  document.querySelector("#docBackdrop")?.addEventListener("click", closeSplitPane);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && state.splitPaneOpen) closeSplitPane();
  });
  document.querySelector("#docSplitPane")?.addEventListener("click", (event) => event.stopPropagation());
  document.querySelectorAll("[data-split-mode]").forEach((btn) => {
    btn.addEventListener("click", () => setSplitMode(btn.dataset.splitMode));
  });
  document.querySelector("#splitCopyButton")?.addEventListener("click", async () => {
    await navigator.clipboard.writeText(document.querySelector("#splitDraftEditor").value);
  });
  document.querySelector("#splitDownloadButton")?.addEventListener("click", () => {
    const text = document.querySelector("#splitDraftEditor").value;
    const blob = new Blob([text], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = state.splitDoc?.file || "draft.md";
    a.click();
    URL.revokeObjectURL(url);
  });

  document.querySelector("#splitRenderedMarkdown")?.addEventListener("click", (event) => {
    const docLink = event.target.closest("[data-doc-link]");
    if (docLink) {
      event.preventDefault();
      openSplitDoc(docLink.dataset.docLink);
    }
  });

  document.querySelector("#splitDraftEditor")?.addEventListener("input", () => {
    if (!state.splitDoc) return;
    state.drafts.set(state.splitDoc.file, document.querySelector("#splitDraftEditor").value);
    if (state.mode === "edit") {
      state.markdown = document.querySelector("#splitDraftEditor").value;
      renderSplitMarkdown();
    }
  });

  document.querySelector("#doclookupSearch")?.addEventListener("keydown", async (e) => {
    if (e.key !== "Enter") return;
    state.search = e.target.value.trim();
    if (!state.search) return;
    showSection("doclookup");
    for (const doc of docs) {
      if (!state.cache.has(doc.file)) {
        try {
          state.cache.set(doc.file, await fetchMarkdownText(doc.file));
        } catch {
          /* skip */
        }
      }
      const text = state.cache.get(doc.file) || "";
      if (text.includes(state.search)) {
        await openSplitDoc(doc.id);
        renderSplitMarkdown();
        break;
      }
    }
  });

  document.body.addEventListener("click", async (event) => {
    const openDoc = event.target.closest("[data-open-doc]");
    if (openDoc) {
      await openSplitDoc(openDoc.dataset.openDoc);
      return;
    }

    const suggest = event.target.closest("[data-suggest-push]");
    if (suggest) {
      suggestPushFromAsset(suggest.dataset.suggestPush);
      return;
    }

    const actions = {
      "data-wi-start": (el) => startWorkItem(el.dataset.wiStart),
      "data-wi-done": (el) => completeWorkItem(el.dataset.wiDone),
      "data-wi-ack": (el) => ackHandoffWorkItem(el.dataset.wiAck),
      "data-wi-push": (el) => pushFromOwnItem(el.dataset.wiPush),
      "data-wi-submit-review": (el) => submitVisualReview(el.dataset.wiSubmitReview),
      "data-wi-confirm": (el) => confirmReview(el.dataset.wiConfirm),
      "data-wi-reject": (el) => openRejectDialog(el.dataset.wiReject),
      "data-wi-block": (el) => blockForCopy(el.dataset.wiBlock),
      "data-wi-resolve-block": (el) => resolveBlock(el.dataset.wiResolveBlock),
      "data-wi-cancel-handoff": (el) => cancelHandoffWorkItem(el.dataset.wiCancelHandoff),
    };

    for (const [attr, fn] of Object.entries(actions)) {
      const el = event.target.closest(`[${attr}]`);
      if (el) {
        fn(el);
        return;
      }
    }

    const openWiDoc = event.target.closest("[data-open-wi-doc]");
    if (openWiDoc) {
      await openWorkItemDoc(openWiDoc.dataset.openWiDoc);
      return;
    }

    const dlWiDoc = event.target.closest("[data-download-wi-doc]");
    if (dlWiDoc) await downloadWorkItemDoc(dlWiDoc.dataset.downloadWiDoc);
  });

  document.body.addEventListener("input", (event) => {
    if (event.target.id === "dailyBlocker") {
      state.daily[`${getCalendar().todayStr}-blocker`] = event.target.value;
      persistState();
    }
    if (event.target.id === "dailyTomorrow") {
      state.daily[`${getCalendar().todayStr}-tomorrow`] = event.target.value;
      persistState();
    }
  });

  document.querySelector("#inquiryForm")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const entry = {
      date: document.querySelector("#inquiryDate").value,
      source: document.querySelector("#inquirySource").value,
      product: document.querySelector("#inquiryProduct").value.trim(),
      price: document.querySelector("#inquiryPrice").value.trim(),
      status: document.querySelector("#inquiryStatus").value,
      note: document.querySelector("#inquiryNote").value.trim(),
    };
    if (!entry.source || !entry.product) return;
    state.inquiries.push(entry);
    persistState();
    event.target.reset();
    setInquiryDateDefault();
    renderInquiries();
  });

  document.querySelector("#inquiryBody")?.addEventListener("click", (event) => {
    const idx = event.target.dataset?.deleteInquiry;
    if (idx === undefined) return;
    state.inquiries.splice(Number(idx), 1);
    persistState();
    renderInquiries();
  });

  document.querySelector("#reviewForm")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const cal = getCalendar();
    const answers = ["reviewQ1", "reviewQ2", "reviewQ3", "reviewQ4", "reviewQ5"].map(
      (id) => document.querySelector(`#${id}`).value.trim(),
    );
    const existing = state.reviews.findIndex((r) => r.date === cal.todayStr);
    const entry = { date: cal.todayStr, answers };
    if (existing >= 0) state.reviews[existing] = entry;
    else state.reviews.push(entry);
    persistState();
    renderReview();
  });

  document.body.addEventListener("click", (event) => {
    if (event.target.id === "exportDataButton") exportDataJson();
    if (event.target.id === "exportCsvButton") exportWorkItemsCsv();
  });
}

function markdownToHtml(markdown) {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const blocks = [];
  let index = 0;

  while (index < lines.length) {
    const line = lines[index];

    if (!line.trim()) {
      index += 1;
      continue;
    }

    if (/^```/.test(line.trim())) {
      const code = [];
      index += 1;
      while (index < lines.length && !/^```/.test(lines[index].trim())) {
        code.push(lines[index]);
        index += 1;
      }
      index += 1;
      blocks.push(`<pre><code>${escapeHtml(code.join("\n"))}</code></pre>`);
      continue;
    }

    if (isTableStart(lines, index)) {
      const tableLines = [];
      while (index < lines.length && lines[index].trim().startsWith("|")) {
        tableLines.push(lines[index]);
        index += 1;
      }
      blocks.push(renderTable(tableLines));
      continue;
    }

    if (/^#{1,3}\s+/.test(line)) {
      const level = line.match(/^#{1,3}/)[0].length;
      const text = line.replace(/^#{1,3}\s+/, "");
      blocks.push(`<h${level}>${inline(text)}</h${level}>`);
      index += 1;
      continue;
    }

    if (/^>\s?/.test(line)) {
      const quote = [];
      while (index < lines.length && /^>\s?/.test(lines[index])) {
        quote.push(lines[index].replace(/^>\s?/, ""));
        index += 1;
      }
      blocks.push(`<blockquote>${quote.map((item) => `<p>${inline(item)}</p>`).join("")}</blockquote>`);
      continue;
    }

    if (/^\s*[-*]\s+/.test(line)) {
      const items = [];
      while (index < lines.length && /^\s*[-*]\s+/.test(lines[index])) {
        items.push(lines[index].replace(/^\s*[-*]\s+/, ""));
        index += 1;
      }
      blocks.push(`<ul>${items.map((item) => `<li>${inline(item)}</li>`).join("")}</ul>`);
      continue;
    }

    if (/^\s*\d+\.\s+/.test(line)) {
      const items = [];
      while (index < lines.length && /^\s*\d+\.\s+/.test(lines[index])) {
        items.push(lines[index].replace(/^\s*\d+\.\s+/, ""));
        index += 1;
      }
      blocks.push(`<ol>${items.map((item) => `<li>${inline(item)}</li>`).join("")}</ol>`);
      continue;
    }

    if (/^---+$/.test(line.trim())) {
      blocks.push("<hr />");
      index += 1;
      continue;
    }

    if (line.trim().startsWith("|")) {
      blocks.push(`<p>${inline(line.trim())}</p>`);
      index += 1;
      continue;
    }

    const paragraph = [];
    while (
      index < lines.length &&
      lines[index].trim() &&
      !/^#{1,3}\s+/.test(lines[index]) &&
      !/^>\s?/.test(lines[index]) &&
      !/^\s*[-*]\s+/.test(lines[index]) &&
      !/^\s*\d+\.\s+/.test(lines[index]) &&
      !lines[index].trim().startsWith("|") &&
      !/^```/.test(lines[index].trim()) &&
      !/^---+$/.test(lines[index].trim())
    ) {
      paragraph.push(lines[index]);
      index += 1;
    }
    blocks.push(`<p>${inline(paragraph.join(" "))}</p>`);
  }

  return blocks.join("\n");
}

function isTableStart(lines, index) {
  return (
    lines[index] &&
    lines[index].trim().startsWith("|") &&
    lines[index + 1] &&
    /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(lines[index + 1])
  );
}

function renderTable(tableLines) {
  const rows = tableLines
    .filter((_, index) => index !== 1)
    .map((line) =>
      line
        .trim()
        .replace(/^\|/, "")
        .replace(/\|$/, "")
        .split("|")
        .map((cell) => cell.trim()),
    );
  const head = rows[0] || [];
  const body = rows.slice(1);
  return `
    <table>
      <thead><tr>${head.map((cell) => `<th>${inline(cell)}</th>`).join("")}</tr></thead>
      <tbody>
        ${body.map((row) => `<tr>${row.map((cell) => `<td>${inline(cell)}</td>`).join("")}</tr>`).join("")}
      </tbody>
    </table>
  `;
}

function resolveDocLink(url) {
  const clean = decodeURIComponent(String(url).replace(/^\.\//, "").split("#")[0].split("?")[0]);
  return docFileToId[clean] || null;
}

function inline(value) {
  return escapeHtml(value)
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/`([^`]+?)`/g, "<code>$1</code>")
    .replace(/\[([^\]]+?)\]\((.+?)\)/g, (_, text, url) => {
      const docId = resolveDocLink(url);
      if (docId) {
        return `<a href="#" class="doc-inline-link" data-doc-link="${docId}">${text}</a>`;
      }
      if (/^https?:\/\//i.test(url)) {
        return `<a href="${url}" target="_blank" rel="noreferrer">${text}</a>`;
      }
      const safe = escapeHtml(url);
      return `<a href="${safe}" class="doc-inline-link" data-md-href="${safe}">${text}</a>`;
    });
}

function highlight(html, search) {
  const escaped = escapeRegExp(escapeHtml(search));
  if (!escaped) return html;
  return html.replace(new RegExp(`(${escaped})`, "gi"), '<mark class="search-hit">$1</mark>');
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function setLoadState(_message) {
  /* split-pane mode: no global load state element */
}

function refreshIcons() {
  if (window.lucide) window.lucide.createIcons();
}

init();
