# GenSight 跨境视觉外包运营资料库

GenSight 当前的唯一业务主线是跨境电商与独立站视觉素材代制作，覆盖 Amazon、美客多、Shopee、TikTok、SHEIN 与 Shopify。

## 系统职责

| 系统 | 唯一职责 |
| --- | --- |
| 飞书多维表格 | 日常协作与业务数据源：任务、交接、线索、报价、成交、交付、复盘 |
| GitHub Pages | 只读运营入口：当前判断、SOP、产品与报价、案例与战略参考 |
| 本地 Markdown | 内容源文件与版本管理 |

GitHub Pages 不保存任务、客户或复盘数据。请勿将本机 `app.js` 工作台或浏览器 `localStorage` 当作协作状态来源。

## 开始使用

1. 在飞书查看今日任务、待接手项与晚间复盘。
2. 打开 [当前运营基线](./opc-doc/00-current-operating-baseline.md)，确认本周主线和优先级。
3. 需要业务上下文时，从 GitHub Pages 打开产品报价、案例、交付与转化 SOP。

## 主要资料

- [当前运营基线](./opc-doc/00-current-operating-baseline.md)
- [每日执行 SOP](./opc-doc/daily-action-and-review-guide.md)
- [产品与报价](./opc-doc/product-spec-and-pricing.md)
- [Demo 与案例](./opc-doc/visual-portfolio-showcase.md)
- [获客到复购 SOP](./opc-doc/07-conversion-loop.md)
- [飞书多维表格工作台规划](./16-feishu-bitable-workbench-plan.md)

## 文档状态

- `opc-doc/`：当前跨境业务资料库。
- root `00–18`：国内设计业务的历史规划与机会型现金流参考，不进入跨境日计划。
- `app.js`、`server.py`：退役的本机协同方案，不再作为日常数据源。

## 发布

更新 `opc-doc/` 中被站点引用的内容后，运行：

```bash
python3 build_opc_html.py
```

再提交并推送 `index.html`、`build_opc_html.py` 与对应 Markdown 文件。GitHub Pages 会从仓库根目录发布站点。
