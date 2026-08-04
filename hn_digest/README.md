# Hacker News AI 每日简报

这个小工具每天从 Hacker News 获取最新、热门和最佳故事，自动筛选 AI 相关内容，按 AI 相关度、点赞数、评论数和时效性综合排序，输出前 10 条，并尽量抓取原文正文生成中文摘要。

## 输出内容

- `output/hacker-news-ai.md`：公众号可直接复制再编辑的 Markdown 日报，按“今日导读—正文摘要—为什么值得关注—链接”排版。
- `output/data.json`：同一批结果的结构化 JSON，包含 `summary_quality`、`summary_source` 等摘要质量字段，方便网页、脚本或其他自动化继续使用。

工具使用 Hacker News 官方 Firebase API，不需要 API Key，也不需要安装第三方 Python 包。脚本会先使用 Hacker News 条目正文，再尝试抓取原文页面中的正文、JSON-LD 或页面摘要；中文标题和正文摘要通过 Google Translate 的公开接口增强，翻译服务不可用时会保留明确的待翻译提示，不会伪造正文摘要。原始标题、原始链接和 HN 讨论链接始终保留。

摘要质量字段：

- `正文摘要`：抓取到原文正文或 HN 条目正文，并完成中文翻译。
- `页面摘要`：只抓取到页面描述、Open Graph 描述或其他页面摘要。
- `标题摘要`：未能取得正文，只能保留人工补充提示。
- `待翻译`：取得了原文内容，但翻译服务暂时不可用。

## 手动运行

在项目根目录执行：

```bash
cd /Users/apple/Desktop/Gensight
python3 hn_digest/fetch_digest.py
```

自定义抓取规模或输出位置：

```bash
python3 hn_digest/fetch_digest.py --fetch-limit 240 --count 10 \
  --output-dir /Users/apple/Desktop/Gensight/hn_digest/output
```

## 测试

测试不访问网络：

```bash
cd /Users/apple/Desktop/Gensight
python3 -m unittest discover -s hn_digest -p 'test_*.py'
```

## 每天早上 8:00 的 cron 示例

下面的时间使用运行机器的本地时区；在当前 Asia/Shanghai 环境中就是每天早上 8:00：

```cron
0 8 * * * cd /Users/apple/Desktop/Gensight && /usr/bin/python3 hn_digest/fetch_digest.py >> hn_digest/cron.log 2>&1
```

编辑当前用户的 crontab：

```bash
crontab -e
```

如果 `/usr/bin/python3` 不是机器上的 Python 路径，请先运行 `command -v python3`，再替换 cron 示例中的路径。建议保留日志，便于检查网络或 API 暂时不可用的情况。

## 任务调度说明

ChatGPT 的已安排任务适合保存“每天几点执行什么工作”的重复指令，并在运行后发送结果或失败通知；它和本地 cron 是两种不同的调度方式。当前项目同时提供本地 Python 脚本与 cron 示例，适合完全由本机生成文件。若使用 Codex 的项目自动化，应让自动化运行本脚本并检查两个输出文件，而不是把现有官网的 `data.json` 当作简报数据文件。
