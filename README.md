# 元晟传媒 · 业务与自媒体运营包

本目录用于承接元晟传媒未来 90 天的现金流业务规划与自媒体执行。

## 飞书协同工作台（当前推荐）

当前协同方向已从本机服务器工作台切换为飞书多维表格。原因是：飞书能直接解决双人同步、手机查看、权限控制、文档评论、自动提醒和长期资料沉淀，不需要Howard Mac 常开。

核心文件：

| 文件 | 用途 |
| --- | --- |
| [16-feishu-bitable-workbench-plan.md](./16-feishu-bitable-workbench-plan.md) | 飞书工作台总体规划：功能分层、表结构、文档库、视图、自动化 |
| [feishu-import/飞书协同工作台搭建手册.md](./feishu-import/飞书协同工作台搭建手册.md) | 飞书多维表格逐步配置手册 |
| [feishu-import/01-任务交接表.csv](./feishu-import/01-任务交接表.csv) 至 [feishu-import/10-产品与报价表.csv](./feishu-import/10-产品与报价表.csv) | 可直接导入飞书的 10 张基础表 |

飞书方案的工作方式：

- 飞书文档承载正文：业务规划、报价、企业介绍、案例拆解、SOP。
- 多维表格承载协同：任务、负责人、状态、截止日期、案例进度、内容发布、询盘。
- 文档库作为索引：每份本地文件导入飞书后，把链接填回「文档库」，再关联到任务、案例、内容和报价。

## 网页工作台（备用 / 本地阅读器）

当前 `index.html` 是元晟传媒两人内部运营工作台，每天打开即可推进任务。功能模块：

- **协同工作台（默认首页）**：Howard / Brian双栏对照；Howard推送文案与 MD 交接，Brian接手、打开/下载文档、确认完成；支持Brian回传「需Howard补充」。
- **总览**：自动显示当前周次、今日重点、启动准备完成率；**已定稿资产**清单（对外可直接使用的成果）。
- **基础校验**：企业介绍、业务范围、报价合理性逐项勾选（**当前第一步**）。
- **启动准备**：34 项清单（校验定稿 v1 后再推进）。
- **本周计划**：根据日期自动定位第 N 周，显示 7 天日计划和验收标准。
- **今日推进**：Howard / Brian当日任务勾选 + 卡点记录（两人实时同步）。
- **询盘记录**：来源、产品、报价、状态表格（共享）。
- **晚间复盘**：每日五问表单，保存历史（共享）。
- **业务与定价 / 案例资产 / 内容计划 / 多淼协作**：参考信息。
- **文档库**：Markdown 阅读、搜索、对照、草稿复制和下载。

### 本地启动（单人 / 仅查看）

```bash
cd /Users/apple/Desktop/Gensight && python3 -m http.server 8080
```

浏览器访问 `http://localhost:8080`。不要直接双击 `index.html`（Markdown 无法加载）。此方式**不能双人协同**。

### 双人协同启动（已不作为推荐方案）

在Howard Mac 上运行协同服务器：

```bash
cd /Users/apple/Desktop/Gensight && python3 server.py --port 8025 --bind 0.0.0.0
```

| 访问方式 | 地址 |
| --- | --- |
| Howard本机 | `http://localhost:8025` |
| Brian电脑（同一 WiFi） | `http://192.168.1.4:8025`（IP 以你 Mac 实际地址为准） |

两人勾选、询盘、复盘、**交接推送**都会写入同一文件：`data.json`。侧边栏显示「双人协同已开启」即表示同步正常。

查本机 IP：

```bash
ipconfig getifaddr en0
```

**注意**：服务器运行时不要关闭终端窗口；Howard Mac 休眠后Brian将无法访问。

### 协同工作台日流程

1. **09:30** 两人打开「协同工作台」，查看双栏今日任务与待接手项。
2. **Howard** 在文档库定稿 → 点「推送给Brian」或任务旁「推送」→ 填写关联 MD 与制作说明。
3. **Brian** 在右侧「待接手」点 **打开 MD** / **下载 MD** → **已接手** → 本地制作 → **确认完成**。
4. 若缺文案，Brian点 **需Howard补充** → 出现在Howard「Brian回传待处理」→ Howard补充后点 **已补充，重新推送**。
5. **18:00** 晚间复盘区会汇总今日交接完成数。

### 协同规则

> 工作台看状态，飞书做评论，你统一改正文

品牌资产位于：

- `assets/brand/gensight-logo-source.png`：原始 LOGO。
- `assets/brand/gensight-logo.png`：裁切后的网页 LOGO。
- `assets/reference/`：门头、海报、官网风格、品牌影片、导视参考图。

## 核心结论

元晟传媒当前主线聚焦：

- AI 广告设计
- Logo / VI
- PPT 设计
- 店面 / 装修效果图
- 品牌全案服务

**7 月前提**：公司注册延后至 8 月后；先用个人创作者账号运营小红书、抖音、视频号、闲鱼；公众号注册后再开。

企业 AI 落地暂不作为主推现金流产品，只作为 AI 提效能力与后续增值项。

## 文件入口

| 文件 | 用途 |
| --- | --- |
| [00-foundation-review.md](./00-foundation-review.md) | **第一步**：企业介绍、业务范围、报价合理性校验 |
| [00-startup-checklist.md](./00-startup-checklist.md) | Phase 0 启动准备（校验通过后）：账号、收款、素材库 |
| [01-business-plan.md](./01-business-plan.md) | 总体业务规划、90 天目标、收入线与执行节奏 |
| [02-channel-internal-pricing.md](./02-channel-internal-pricing.md) | 合作广告公司内部渠道价，禁止公开 |
| [03-public-pricing.md](./03-public-pricing.md) | 自媒体对外报价口径，可用于报价图和公开介绍 |
| [04-social-media-plan.md](./04-social-media-plan.md) | 小红书、抖音、视频号、闲鱼、朋友圈运营规划 |
| [05-90-day-execution-calendar.md](./05-90-day-execution-calendar.md) | 2026-07-06 起 90 天执行节奏 |
| [06-case-packaging-library.md](./06-case-packaging-library.md) | 已收费案例、进行中案例、测试案例包装清单 |
| [07-content-first-month.md](./07-content-first-month.md) | 首月内容选题、标题、脚本与图文拆分 |
| [08-sales-and-intake-sop.md](./08-sales-and-intake-sop.md) | 询盘、报价、个人收款、交付和复盘 SOP |
| [09-duomiao-partnership.md](./09-duomiao-partnership.md) | 多淼联合业务范围、定价协作和宣传策略 |
| [10-two-person-execution-plan.md](./10-two-person-execution-plan.md) | Howard + Brian双人分工、每日推进计划和月度复盘指标 |
| [11-xianyu-channel-pilot.md](./11-xianyu-channel-pilot.md) | 闲鱼 14 天渠道试点、体验款定价、商品话术和风控边界 |
| [12-company-profile-delivery-standards.md](./12-company-profile-delivery-standards.md) | 对外企业介绍、服务范围、全国/苏州边界和各产品交付标准 |
| [13-commercial-proposal-service.md](./13-commercial-proposal-service.md) | 商业项目方案设计服务、崇明案例包装和高阶报价建议 |
| [14-strategy-case-placement.md](./14-strategy-case-placement.md) | 小马宝莉、Teddy、华南茶养食集的案例归类、公开边界和内容用法 |
| [15-company-registration-roadmap.md](./15-company-registration-roadmap.md) | 8 月后公司注册触发条件与步骤 |
| [18-social-media-content-sprint.md](./18-social-media-content-sprint.md) | 2026-07-13 起两周自媒体内容推进计划：公众号、抖音、视频号、朋友圈 |

## 执行纪律

- 渠道内部价只给合作广告公司，不出现在自媒体、朋友圈公开报价和官网式物料中。
- 自媒体只展示对外"起"价，用来建立元晟传媒自己的价格锚点。
- 7-8 月直客用个人微信/支付宝收款，50% 预付 + 50% 尾款，暂不提供发票。
- 免费试做只允许用于破冰，原则上限 1 张 KV 或 1 个小样，不做整案免费。
- 所有项目默认写清交付物、周期、付款节点、修改轮次和不包含事项。
- 每个项目交付时同步留存案例素材，方便拆成长文、短视频和小红书图文。
- 多淼是紧密合作方，不只是渠道来源；涉及制作安装、政务公益传播、空间美陈、文创落地的线上询盘，优先评估联合承接。
- 两人推进时每天只确认 1-3 件必须完成的事，在工作台勾选，先形成可报价、可发布、可转发的成果。
- 闲鱼只作为 14 天体验款试点，站内沟通和成交，不公开渠道价，不主动导流微信。
- 元晟传媒纯设计业务可全国线上交付；多淼实施类业务以苏州本地制作、安装和现场落地为主，外地实施项目单独评估。
- 7 月自媒体主战场：小红书 + 抖音/视频号 + 朋友圈 + 闲鱼；公众号 8 月注册后启用。
- 2026-07-13 起工作重心转为公众号待发布稿、抖音/视频号短视频、朋友圈转发素材；公众号主体未完成时先产出待发布稿，不阻塞内容生产。
- 日内不讨论战略方向，方向问题只在周一和周五处理。
