# 元晟传媒双人工作台 · 功能开发文档（v2）

> 状态：**已确认开发**  
> 本文替代「仅Howard推送 → Brian被动接手」的窄模型，并解决文档区混乱、导航重复、工作仅限当日等问题。

---

## 1. 问题诊断

| 问题 | 说明 |
| --- | --- |
| 文档区混乱 | 18 个 MD 平铺 + 与内容页重复，找不到「现在该看哪份」 |
| Brian被动 | 协同区以「Howard推送」为主，不符合Brian自有节奏 |
| 确认流不完整 | Brian有大量视觉稿待Howard确认，不只是缺文案回传 |
| 工作不止当天 | 需要积压、跨天、本周持续项 |
| 整站 IA 失控 | 协同 / 今日推进 / 总览 / 校验 / 周计划功能重叠 |

## 2. 产品定位

- **工作台**：谁今天做什么、卡在哪、待谁确认、是否完成（状态机）
- **飞书**：评论与评审，不替代状态跟踪
- **MD 文件**：唯一正文源；Brian制作成果仍存本地文件夹，工作台记路径/备注

## 3. 信息架构（极简导航）

| 导航 | 作用 |
| --- | --- |
| **协同工作台** | 默认首页，双栏统一工作板 |
| **文档速查** | 搜索 + 最近打开 + 与工作项关联的 MD |
| **询盘与复盘** | 询盘表 + 晚间五问 + 交接/确认汇总 |
| **设置** | 协同服务器状态、阶段说明、数据导出 |

## 4. 核心数据模型：工作项 `workItems`

### 4.1 字段

```json
{
  "id": "wi-20260708-001",
  "title": "对外报价图 v1",
  "owner": "li",
  "category": "own",
  "status": "in_progress",
  "priority": "p0",
  "dueDate": "2026-07-08",
  "source": "weekly_plan",
  "linkedTaskKey": "2026-07-08-li-0",
  "docFile": "03-public-pricing.md",
  "docSection": "",
  "brief": "按定稿口径做报价图，渠道价不出现",
  "expectedOutputs": ["对外报价图 v1"],
  "outputNote": "",
  "reviewTarget": null,
  "direction": null,
  "parentId": null,
  "createdAt": "...",
  "updatedAt": "...",
  "completedAt": null
}
```

### 4.2 三类 category

| category | 含义 |
| --- | --- |
| `own` | 自有任务（可独立推进） |
| `handoff` | 来自对方交接 |
| `review` | 待对方确认（视觉稿等） |

### 4.3 方向 direction（handoff / review）

| direction | 场景 |
| --- | --- |
| `huang_to_li` | Howard文案定稿 → Brian视觉制作 |
| `li_to_huang` | Brian视觉稿 → Howard确认 |
| `li_blocked_huang` | Brian需Howard补充文案/口径 |

### 4.4 状态机

| status | 用户可见文案 |
| --- | --- |
| `backlog` | 待开始 |
| `in_progress` | 进行中 |
| `waiting_handoff` | 待接手 |
| `waiting_review` | 待确认 |
| `blocked` | 待补充 |
| `done` | 已完成 |

## 5. 协同工作台 UI

双栏：Howard / Brian，每人四类区块——自有、交接/待确认、待补充、我发起的交接。

## 6. 文档与工作项联动

工作项卡片 → 右侧 split pane 打开 MD；记录 `recentDocs` 到 data.json。

## 7. 验收标准

1. Brian自有任务区有本周/积压项，不依赖Howard推送
2. Brian提交视觉稿后，Howard「待我确认」可确认或打回
3. Howard推送交接后，Brian「来自Howard的交接」可打开关联 MD
4. 文档从工作项打开是主路径
5. 导航仅 4 项
6. 工作项可跨天保留
7. 两人电脑 data.json 同步正常
