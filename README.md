# GenSight 跨境视觉外包运营资料库

GenSight 当前的唯一业务主线是跨境电商与独立站视觉素材代制作，覆盖 Amazon、美客多、Shopee、TikTok、SHEIN 与 Shopify。

## 系统职责

| 系统 | 唯一职责 |
| --- | --- |
| 飞书多维表格 | 日常协作与业务数据源：任务、交接、线索、报价、成交、交付、复盘 |
| GitHub Pages | **今日作战台** + 只读 SOP、产品与报价、案例与战略参考 |
| GitHub 仓库 Markdown | 内容源文件与版本管理 |

GitHub Pages **不保存**任务、客户或复盘数据。请勿将 `archive/app.js` 或浏览器 `localStorage` 当作协作状态来源。

## 开始使用（Howard + Brian）

1. 打开 GitHub Pages **今日作战台**（首页），确认本周唯一目标与飞书入口。
2. 在飞书 **T04 / T01** 确认今日 Top 3 与阻塞项。
3. 需要报价、平台规范、案例或 SOP 时，从左侧导航按需打开。
4. 晚间在飞书 **T06** 完成四问复盘，次日 Top 3 写回 T04。

## 主要资料

- [当前运营基线](./opc-doc/00-current-operating-baseline.md)
- [飞书日常协同 SOP](./opc-doc/feishu-daily-workflow.md)
- [存储与发布边界](./opc-doc/storage-and-pages-boundary.md)
- [每日执行 SOP](./opc-doc/daily-action-and-review-guide.md)
- [产品与报价](./opc-doc/product-spec-and-pricing.md)
- [一日工作流演练清单](./opc-doc/daily-warroom-validation.md)
- [飞书多维表格工作台规划](./16-feishu-bitable-workbench-plan.md)

## 文档状态

- `opc-doc/`：当前跨境业务资料库。
- root `00–18`：国内设计历史规划 → 见 [archive-domestic-plans.md](./opc-doc/archive-domestic-plans.md)。
- `archive/app.js`、`archive/server.py`：已退役本机协同方案。

## 配置飞书入口

编辑 [`portal/site-config.json`](./portal/site-config.json) 填入 `feishu.baseUrl`，然后：

```bash
python3 build_opc_html.py
```

## 发布

```bash
python3 build_opc_html.py
git add index.html build_opc_html.py opc-doc/ portal/
git commit -m "docs: update operations portal"
git push
```

GitHub Pages 从仓库根目录 **`index.html`** 发布。  
Vite 品牌展示页入口：**`deck/index.html`**（与 Pages 分离）。
