# 已退役的本机协同工作台

> 归档日期：2026-08-04  
> 原因：GitHub Pages 无法提供双人共享状态；日常协作已迁移至**飞书多维表格**。

## 文件说明

| 文件 | 原用途 |
| --- | --- |
| `app.js` | 浏览器端任务、交接、询盘与复盘 UI（依赖 `/api/data`） |
| `server.py` | 本机 JSON 文件存储 API |

## 请勿用于日常流程

- 不要同时维护飞书与本机工作台两套状态  
- 不要在本机 `server.py` 上继续扩展协同功能  
- 业务 SOP 与资料请使用 GitHub Pages 入口 + 飞书

当前权威说明见 [`opc-doc/storage-and-pages-boundary.md`](../opc-doc/storage-and-pages-boundary.md)。

## 本地运行（仅考古/参考）

```bash
python3 archive/server.py
# 在浏览器打开曾加载 app.js 的 HTML（已无官方入口）
```
