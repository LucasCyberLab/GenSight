import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from fetch_digest import (
    ai_signal,
    build_item,
    extract_page_content,
    localized_title,
    markdown_digest,
    write_outputs,
)


class DigestTests(unittest.TestCase):
    def test_ai_signal_detects_multiple_topics(self):
        signal, topics = ai_signal(
            {"title": "Show HN: An open-source LLM agent", "text": "Built with RAG."}
        )
        self.assertGreater(signal, 0)
        self.assertIn("LLM", topics)
        self.assertIn("智能体", topics)
        self.assertIn("RAG", topics)

    def test_localized_title_has_chinese_label(self):
        title = localized_title("Show HN: Open-source AI developer tools", ["AI"])
        self.assertTrue(title.startswith("项目分享："))
        self.assertIn("开源", title)
        self.assertIn("AI", title)

    def test_localized_title_does_not_mangle_english(self):
        title = localized_title("OpenAI did not notice the hack for a week", ["AI"])
        self.assertNotIn("一个 week", title)

    def test_extract_page_content_reads_article_body(self):
        page = """
        <html><head><meta property="og:description" content="A page summary." /></head>
        <body><nav>Subscribe</nav><article><h1>AI security</h1>
        <p>The agent ran for seven days and accessed internal repositories.</p>
        <p>Researchers described the incident and its implications for security teams.</p>
        </article></body></html>
        """
        title, content, source_type = extract_page_content(page)
        self.assertEqual(title, "AI security")
        self.assertIn("accessed internal repositories", content)
        self.assertEqual(source_type, "原文正文")

    def test_build_item_preserves_original_links(self):
        item = build_item(
            {
                "id": 123,
                "title": "OpenAI releases a new model",
                "url": "https://example.com/story",
                "score": 42,
                "descendants": 8,
                "time": 1_700_000_000,
                "by": "tester",
            },
            enrich_content=False,
        )
        self.assertEqual(item["original_url"], "https://example.com/story")
        self.assertEqual(item["hacker_news_url"], "https://news.ycombinator.com/item?id=123")
        self.assertTrue(item["summary"].startswith("这条内容聚焦于"))

    @patch("fetch_digest.translate_to_chinese", side_effect=["OpenAI 发布了新模型", "原文介绍了模型的能力、限制以及开发者使用方式。"])
    @patch("fetch_digest.fetch_page")
    def test_build_item_uses_translated_body_summary(self, fetch_page, _translate):
        fetch_page.return_value = """
        <article><p>The new model improves reasoning and tool use for developers.</p>
        <p>The article also explains its limitations and evaluation results.</p></article>
        """
        item = build_item(
            {
                "id": 123,
                "title": "OpenAI releases a new model",
                "url": "https://example.com/story",
                "score": 42,
                "descendants": 8,
                "time": 1_700_000_000,
                "by": "tester",
            }
        )
        self.assertEqual(item["title_zh"], "AI 技术动态：OpenAI 发布了新模型")
        self.assertEqual(item["summary"], "原文介绍了模型的能力、限制以及开发者使用方式。")
        self.assertEqual(item["summary_quality"], "正文摘要")
        self.assertEqual(item["summary_source"], "原文正文")

    def test_markdown_is_publication_ready(self):
        output = markdown_digest(
            {
                "generated_at": "2026-01-01T08:00:00+08:00",
                "items": [
                    {
                        "rank": 1,
                        "title_zh": "AI 技术动态：新模型",
                        "summary": "正文介绍了模型能力与限制。",
                        "reason": "内容直接涉及大语言模型，适合关注。",
                        "original_url": "https://example.com/story",
                        "hacker_news_url": "https://news.ycombinator.com/item?id=1",
                        "score": 10,
                        "comments": 2,
                    }
                ],
            }
        )
        self.assertIn("# Hacker News AI 日报｜2026年01月01日", output)
        self.assertIn("**正文摘要**：正文介绍了模型能力与限制。", output)
        self.assertIn("**为什么值得关注**", output)

    def test_write_outputs_creates_markdown_and_json(self):
        data = {"generated_at": "2026-01-01T08:00:00+08:00", "items": []}
        with tempfile.TemporaryDirectory() as temp_dir:
            markdown_path, json_path = write_outputs(data, Path(temp_dir))
            self.assertTrue(markdown_path.exists())
            self.assertTrue(json_path.exists())
            self.assertEqual(json.loads(json_path.read_text(encoding="utf-8"))["items"], [])


if __name__ == "__main__":
    unittest.main()
