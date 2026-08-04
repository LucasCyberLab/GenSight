# GenSight 数据存储与系统边界

> 版本：2026-08-04  
> 读者：Howard、Brian — 避免 GitHub Pages、本机工具与飞书三套状态分叉

---

## 1. 三系统职责（唯一权威）

| 系统 | 职责 | 是否权威状态 |
| --- | --- | --- |
| **飞书多维表格** | 任务、交接、线索、报价成交、交付进度、晚间复盘 | **是** |
| **GitHub Pages（本站）** | 今日作战台入口、SOP、报价标准、案例、战略上下文、报价计算器 | **否**（只读） |
| **GitHub 仓库 Markdown** | 内容源文件、版本历史、构建输入 | **否**（源文件，非运行时状态） |

---

## 2. 已退役系统

| 组件 | 原用途 | 现状 |
| --- | --- | --- |
| `archive/app.js` + `archive/server.py` | 本机 `/api/data` 双人协同 | **已归档**，不参与日常流程 |
| 浏览器 `localStorage` 日记录 | 每日复盘持久化 | **已移除**；复盘仅写飞书 T06 |
| 首页「自动同步 / 双人共享」文案 | 误导性承诺 | **已改为**飞书入口与配置说明 |

如需查看旧工作台实现，见 [`archive/README.md`](../archive/README.md)。

---

## 3. 飞书表与 CSV 导入

| 编号 | 表 | CSV |
| --- | --- | --- |
| T01 | 任务交接 | `feishu-import/01-任务交接表.csv` |
| T04 | 每日任务 | `feishu-import/04-每日任务表.csv` |
| T05 | 询盘记录 | `feishu-import/05-询盘记录.csv` |
| T06 | 晚间复盘 | `feishu-import/06-晚间复盘.csv` |
| T08 | 案例库 | `feishu-import/08-案例库.csv` |
| T10 | 产品与报价 | `feishu-import/10-产品与报价表.csv` |

规划全文：[`16-feishu-bitable-workbench-plan.md`](../16-feishu-bitable-workbench-plan.md)  
日常用法：[`feishu-daily-workflow.md`](./feishu-daily-workflow.md)

---

## 4. 配置 GitHub Pages 上的飞书入口

1. 在飞书创建多维表格 base，导入上述 CSV。  
2. 编辑 `portal/site-config.json`：  
   - `feishu.baseUrl`：表格 base 链接  
   - `feishu.tables.*.path`：各子表路径（可选，留空则只跳 base）  
3. 运行 `python3 build_opc_html.py`，提交 `index.html`。  
4. 首页「打开飞书」与各指标卡将指向已配置链接。

**未配置时**：首页显示配置说明，不假装已连接。

---

## 5. 发布流程

```bash
# 1. 改 Markdown 或 portal/site-config.json
# 2. 重新生成静态站
python3 build_opc_html.py
# 3. 提交 index.html 与源文件
git add index.html build_opc_html.py opc-doc/ portal/
git commit -m "docs: update operations portal"
git push
```

GitHub Pages 从仓库 **root `index.html`** 发布。  
Vite 品牌展示页在 **`deck/index.html`**，与 Pages 入口分离。

---

## 6. 禁止事项

- 不要在 Pages 上新增「保存任务/线索」表单并声称双人同步  
- 不要恢复 `localStorage` 作为复盘权威存储  
- 不要并行维护第四套 Notion/Excel 状态表（除非明确迁移并废弃飞书）
