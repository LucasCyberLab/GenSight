#!/usr/bin/env python3
"""Fetch Hacker News stories and write a Chinese AI-focused daily digest.

The script deliberately uses only Python's standard library so it can run from
cron on a clean machine. It uses the official Hacker News Firebase API and
keeps the original URL for every selected story.
"""

from __future__ import annotations

import argparse
import gzip
import html
import json
import math
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


API_ROOT = "https://hacker-news.firebaseio.com/v0"
HN_ITEM_URL = "https://news.ycombinator.com/item?id={id}"
USER_AGENT = "Gensight-HN-AI-Digest/1.0 (+https://news.ycombinator.com/)"
LOCAL_TZ = ZoneInfo("Asia/Shanghai")
TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"
MAX_PAGE_BYTES = 1_500_000
MAX_SUMMARY_SOURCE_CHARS = 1_200

AI_TERMS: tuple[tuple[str, float, str], ...] = (
    ("artificial intelligence", 6.0, "人工智能"),
    ("machine learning", 5.0, "机器学习"),
    ("deep learning", 5.0, "深度学习"),
    ("large language model", 6.0, "大语言模型"),
    ("language model", 5.0, "语言模型"),
    ("generative ai", 6.0, "生成式 AI"),
    ("computer vision", 4.0, "计算机视觉"),
    ("reinforcement learning", 4.0, "强化学习"),
    ("openai", 5.0, "OpenAI"),
    ("anthropic", 5.0, "Anthropic"),
    ("claude", 4.0, "Claude"),
    ("chatgpt", 5.0, "ChatGPT"),
    ("gemini", 4.0, "Gemini"),
    ("llama", 4.0, "Llama"),
    ("mistral", 4.0, "Mistral"),
    ("transformer", 4.0, "Transformer"),
    ("neural network", 4.0, "神经网络"),
    ("prompt engineering", 4.0, "提示词工程"),
    ("retrieval augmented generation", 5.0, "检索增强生成"),
    (r"\brag\b", 4.0, "RAG"),
    (r"\bllm\b", 5.0, "LLM"),
    (r"\bai\b", 4.0, "AI"),
    (r"\bml\b", 3.0, "ML"),
    ("agentic", 4.0, "智能体"),
    (r"\bagents?\b", 3.0, "智能体"),
    ("inference", 3.0, "推理"),
    ("fine[- ]?tuning", 4.0, "微调"),
    ("embedding", 3.0, "嵌入"),
    ("diffusion", 3.0, "扩散模型"),
    ("stable diffusion", 5.0, "Stable Diffusion"),
    ("gpu", 2.0, "GPU"),
    ("tensor", 2.0, "Tensor"),
)

TITLE_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ("large language model", "大语言模型"),
    ("language model", "语言模型"),
    ("artificial intelligence", "人工智能"),
    ("machine learning", "机器学习"),
    ("deep learning", "深度学习"),
    ("computer vision", "计算机视觉"),
    ("reinforcement learning", "强化学习"),
    ("retrieval augmented generation", "检索增强生成"),
    ("prompt engineering", "提示词工程"),
    ("fine-tuning", "微调"),
    ("fine tuning", "微调"),
    ("open source", "开源"),
    ("open-source", "开源"),
    ("benchmark", "基准测试"),
    ("benchmarks", "基准测试"),
    ("inference", "推理"),
    ("embedding", "嵌入"),
    ("agents", "智能体"),
    ("agent", "智能体"),
    ("model", "模型"),
    ("models", "模型"),
    ("training", "训练"),
    ("developer tool", "开发者工具"),
    ("developer tools", "开发者工具"),
    ("framework", "框架"),
    ("frameworks", "框架"),
    ("database", "数据库"),
    ("databases", "数据库"),
    ("research", "研究"),
    ("paper", "论文"),
    ("papers", "论文"),
    ("how to", "如何"),
    ("why", "为什么"),
    ("new", "新"),
    ("build", "构建"),
    ("building", "构建"),
)


SKIP_HTML_TAGS = {"script", "style", "noscript", "svg", "template", "iframe", "nav", "footer"}
CONTENT_BLOCK_TAGS = {"p", "blockquote", "h1", "h2", "h3", "li"}
GENERIC_PAGE_TEXT = {
    "subscribe",
    "sign in",
    "log in",
    "advertisement",
    "cookie policy",
    "privacy policy",
    "terms of use",
}


def fetch_json(url: str, retries: int = 3, timeout: int = 15) -> Any:
    """Fetch JSON with a small retry budget suitable for a daily job."""
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            last_error = error
            if attempt < retries - 1:
                time.sleep(0.6 * (attempt + 1))
    raise RuntimeError(f"无法获取 {url}: {last_error}")


def fetch_page(url: str, retries: int = 2, timeout: int = 12) -> str:
    """Fetch a page as text; article access is best-effort for a daily digest."""
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            request = Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "text/html,application/xhtml+xml,text/plain;q=0.8,*/*;q=0.5",
                    "Accept-Language": "en-US,en;q=0.8",
                },
            )
            with urlopen(request, timeout=timeout) as response:
                payload = response.read(MAX_PAGE_BYTES)
                if response.headers.get("Content-Encoding", "").lower() == "gzip":
                    payload = gzip.decompress(payload)
                charset = response.headers.get_content_charset() or "utf-8"
                return payload.decode(charset, errors="replace")
        except (HTTPError, URLError, TimeoutError, UnicodeError, OSError) as error:
            last_error = error
            if attempt < retries - 1:
                time.sleep(0.5 * (attempt + 1))
    raise RuntimeError(f"无法获取原文页面 {url}: {last_error}")


class PageParser(HTMLParser):
    """Extract metadata and readable blocks without requiring third-party packages."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.metadata: dict[str, str] = {}
        self.title_parts: list[str] = []
        self.headings: list[str] = []
        self.blocks: list[str] = []
        self._skip_depth = 0
        self._content_depth = 0
        self._block_stack: list[list[str]] = []
        self._heading_stack: list[list[str]] = []
        self._in_title = False
        self._content_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag == "meta":
            key = attrs_map.get("property") or attrs_map.get("name")
            value = attrs_map.get("content", "")
            if key and value:
                self.metadata[key.lower()] = clean_text(value)
        if tag in SKIP_HTML_TAGS:
            self._skip_depth += 1
            return
        if tag == "title":
            self._in_title = True
        if tag in {"article", "main"}:
            self._content_depth += 1
        if tag in CONTENT_BLOCK_TAGS:
            self._block_stack.append([])
        if tag in {"h1", "h2", "h3"}:
            self._heading_stack.append([])

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self._skip_depth:
            if tag in SKIP_HTML_TAGS:
                self._skip_depth -= 1
            return
        if tag == "title":
            self._in_title = False
        if tag in {"article", "main"} and self._content_depth:
            self._content_depth -= 1
        if tag in CONTENT_BLOCK_TAGS and self._block_stack:
            block = clean_text(" ".join(self._block_stack.pop()))
            if block:
                self.blocks.append(block)
        if tag in {"h1", "h2", "h3"} and self._heading_stack:
            heading = clean_text(" ".join(self._heading_stack.pop()))
            if heading:
                self.headings.append(heading)

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = clean_text(data)
        if not text:
            return
        if self._in_title:
            self.title_parts.append(text)
        if self._block_stack:
            self._block_stack[-1].append(text)
        if self._heading_stack:
            self._heading_stack[-1].append(text)
        elif self._content_depth:
            self._content_parts.append(text)

    @property
    def content(self) -> list[str]:
        return self.blocks + [clean_text(" ".join(self._content_parts))]


def jsonld_fields(page: str) -> tuple[str, str]:
    """Read description/articleBody from common JSON-LD blocks when present."""
    descriptions: list[str] = []
    bodies: list[str] = []
    pattern = re.compile(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        flags=re.IGNORECASE | re.DOTALL,
    )
    for raw in pattern.findall(page):
        try:
            value = json.loads(html.unescape(raw.strip()))
        except (TypeError, ValueError, json.JSONDecodeError):
            continue
        nodes = value if isinstance(value, list) else [value]
        for node in nodes:
            if not isinstance(node, dict):
                continue
            description = clean_text(str(node.get("description", "")))
            body = clean_text(str(node.get("articleBody", "")))
            if description:
                descriptions.append(description)
            if body:
                bodies.append(body)
    return " ".join(descriptions), " ".join(bodies)


def extract_page_content(page: str) -> tuple[str, str, str]:
    """Return (title, readable content, source type) from an HTML page."""
    parser = PageParser()
    try:
        parser.feed(page)
        parser.close()
    except Exception:
        return "", "", "页面解析失败"
    jsonld_description, jsonld_body = jsonld_fields(page)
    metadata = parser.metadata
    title = (
        parser.title_parts
        and clean_text(" ".join(parser.title_parts))
        or metadata.get("og:title", "")
        or (parser.headings[0] if parser.headings else "")
    )
    candidates = [
        jsonld_body,
        *parser.content,
        jsonld_description,
        metadata.get("og:description", ""),
        metadata.get("twitter:description", ""),
        metadata.get("description", ""),
    ]
    unique: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        candidate = clean_text(candidate)
        if len(candidate) < 40:
            continue
        normalized = re.sub(r"\W+", "", candidate).lower()
        if not normalized or normalized in seen:
            continue
        if normalized in {re.sub(r"\W+", "", text).lower() for text in GENERIC_PAGE_TEXT}:
            continue
        seen.add(normalized)
        unique.append(candidate)
    if not unique:
        return title, "", "未获取正文"
    content = "\n".join(unique[:8])
    if len(content) > 7_000:
        content = content[:7_000].rsplit(" ", 1)[0]
    source_type = "原文正文" if jsonld_body or parser.blocks else "原文页面摘要"
    return title, content, source_type


def translate_to_chinese(text: str, max_chars: int = MAX_SUMMARY_SOURCE_CHARS) -> str:
    """Translate a short excerpt; return an empty string when the service is unavailable."""
    text = clean_text(text)
    if not text:
        return ""
    if re.search(r"[\u4e00-\u9fff]", text) and not re.search(r"[A-Za-z]{4,}", text):
        return text
    text = text[:max_chars]
    query = urlencode(
        {"client": "gtx", "sl": "auto", "tl": "zh-CN", "dt": "t", "q": text}
    )
    try:
        payload = fetch_json(f"{TRANSLATE_URL}?{query}", retries=2, timeout=12)
        parts = [str(part[0]) for part in payload[0] if isinstance(part, list) and part]
        return clean_text("".join(parts))
    except (RuntimeError, IndexError, KeyError, TypeError, ValueError):
        return ""


def fetch_story_ids(limit: int) -> list[int]:
    """Combine new, top, and best story streams while keeping their order."""
    ids: list[int] = []
    seen: set[int] = set()
    endpoints = ("newstories", "topstories", "beststories")
    errors: list[str] = []
    for endpoint in endpoints:
        try:
            values = fetch_json(f"{API_ROOT}/{endpoint}.json")
        except RuntimeError as error:
            errors.append(str(error))
            continue
        for story_id in values[:limit]:
            if isinstance(story_id, int) and story_id not in seen:
                seen.add(story_id)
                ids.append(story_id)
    if not ids:
        detail = "; ".join(errors) if errors else "API 没有返回故事 ID"
        raise RuntimeError(f"没有拿到 Hacker News 故事列表：{detail}")
    return ids[:limit]


def fetch_story(story_id: int) -> dict[str, Any] | None:
    """Return one story item, ignoring deleted/dead/non-story items."""
    try:
        item = fetch_json(f"{API_ROOT}/item/{story_id}.json")
    except RuntimeError:
        return None
    if not item or item.get("type") != "story" or item.get("dead") or item.get("deleted"):
        return None
    if not item.get("title"):
        return None
    return item


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = html.unescape(value)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def ai_signal(story: dict[str, Any]) -> tuple[float, list[str]]:
    searchable = " ".join(
        (clean_text(str(story.get(field, ""))) for field in ("title", "text", "url"))
    ).lower()
    score = 0.0
    topics: list[str] = []
    for pattern, weight, label in AI_TERMS:
        if re.search(pattern, searchable, flags=re.IGNORECASE):
            score += weight
            if label not in topics:
                topics.append(label)
    return score, topics


def localized_title(title: str, topics: Iterable[str], translated: str = "") -> str:
    """Create a Chinese-readable title, using a translated title when available."""
    source = clean_text(title)
    prefix = ""
    if source.lower().startswith("show hn:"):
        prefix, source = "项目分享：", source[8:].strip()
    elif source.lower().startswith("ask hn:"):
        prefix, source = "社区讨论：", source[7:].strip()
    else:
        prefix = "AI 技术动态："
    localized = clean_text(translated) if translated else ""
    if prefix:
        localized = re.sub(r"^(?:show|ask)\s+hn\s*[:：]\s*", "", localized, flags=re.IGNORECASE)
    if not localized:
        localized = source
        for english, chinese in TITLE_REPLACEMENTS:
            localized = re.sub(rf"\b{re.escape(english)}\b", chinese, localized, flags=re.IGNORECASE)
        localized = re.sub(r"\s+", " ", localized).strip(" -:")
    if not re.search(r"[\u4e00-\u9fff]", localized):
        topic = "、".join(list(topics)[:2]) or "人工智能"
        localized = f"围绕{topic}的 Hacker News 内容"
    return f"{prefix}{localized}"


def domain_for(url: str | None) -> str:
    if not url:
        return "Hacker News 社区"
    return urlparse(url).netloc or "原文网站"


def score_story(story: dict[str, Any], signal: float) -> float:
    age_hours = max((time.time() - int(story.get("time", time.time()))) / 3600, 0.0)
    recency = max(0.0, 48.0 - age_hours) / 8.0
    points = math.log1p(max(int(story.get("score", 0)), 0))
    comments = math.log1p(max(int(story.get("descendants", 0)), 0))
    # AI relevance is a gate and a tie-breaker; HN engagement remains the
    # main signal so a highly discussed story does not lose to a low-signal
    # item that merely contains several AI keywords.
    return points * 5 + comments * 3 + min(signal, 12.0) * 1.5 + recency


def source_content(story: dict[str, Any], original_url: str) -> tuple[str, str, str]:
    """Get usable source text from HN first, then the linked article."""
    hn_text = clean_text(story.get("text"))
    if len(hn_text) >= 80:
        return clean_text(str(story.get("title", ""))), hn_text, "Hacker News 正文"
    if original_url.startswith("https://news.ycombinator.com/"):
        return clean_text(str(story.get("title", ""))), hn_text, "Hacker News 正文" if hn_text else "未获取正文"
    try:
        page = fetch_page(original_url)
        title, content, source_type = extract_page_content(page)
        if content:
            return title or clean_text(str(story.get("title", ""))), content, source_type
    except RuntimeError:
        pass
    if hn_text:
        return clean_text(str(story.get("title", ""))), hn_text, "Hacker News 正文"
    discussion_parts: list[str] = []
    for comment_id in (story.get("kids") or [])[:3]:
        try:
            comment = fetch_json(f"{API_ROOT}/item/{comment_id}.json", retries=1, timeout=8)
        except RuntimeError:
            continue
        if isinstance(comment, dict) and comment.get("type") == "comment" and not comment.get("dead"):
            text = clean_text(comment.get("text"))
            if len(text) >= 60:
                discussion_parts.append(text)
    if discussion_parts:
        return clean_text(str(story.get("title", ""))), " ".join(discussion_parts), "HN 讨论背景"
    return clean_text(str(story.get("title", ""))), "", "未获取正文"


def summary_source_excerpt(content: str) -> str:
    """Select the first useful paragraphs/sentences instead of translating the whole page."""
    blocks = [clean_text(block) for block in content.splitlines() if len(clean_text(block)) >= 45]
    if not blocks:
        blocks = [clean_text(part) for part in re.split(r"(?<=[.!?。！？])\s+", content) if len(clean_text(part)) >= 45]
    excerpt = " ".join(blocks[:3])
    excerpt = re.sub(r"https?://\S+", "", excerpt)
    return clean_text(excerpt)[:MAX_SUMMARY_SOURCE_CHARS]


def concise_summary(text: str, max_chars: int = 360, max_sentences: int = 3) -> str:
    """Keep the translated result short enough for a public daily brief."""
    text = re.sub(r"\s+([，。！？：；,.!?])", r"\1", text)
    text = re.sub(r"(?:\.\s*){2,}", "…", text)
    sentences = [clean_text(part) for part in re.split(r"(?<=[。！？.!?])\s*", text) if clean_text(part)]
    selected = " ".join(sentences[:max_sentences])
    if len(selected) <= max_chars:
        return selected
    clipped = selected[:max_chars].rsplit("。", 1)[0].strip()
    return f"{clipped}。" if clipped else f"{selected[:max_chars].rstrip()}…"


def summary_label(item: dict[str, Any]) -> str:
    quality = item.get("summary_quality", "正文摘要")
    if quality in {"正文摘要", "页面摘要"}:
        return "正文摘要"
    if quality == "讨论摘要":
        return "HN 讨论背景摘要"
    return "摘要情况"


def summary_from_content(title_zh: str, content: str, source_type: str) -> tuple[str, str]:
    """Produce a publishable Chinese summary and a quality label."""
    if not content:
        return (
            f"原文暂未提供可提取的正文内容。本文围绕“{title_zh}”展开，建议发布前打开原文补充核对。",
            "标题摘要",
        )
    source_excerpt = summary_source_excerpt(content)
    translated = translate_to_chinese(source_excerpt)
    if translated:
        translated = concise_summary(translated)
        quality = "正文摘要" if source_type in {"原文正文", "Hacker News 正文"} else "页面摘要"
        if source_type == "HN 讨论背景":
            quality = "讨论摘要"
        return translated, quality
    return (
        f"原文围绕“{title_zh}”展开，已抓取到正文或页面摘要，但本次中文翻译服务不可用；"
        "建议发布前打开原文核对并补充中文摘要。",
        "待翻译",
    )


def build_item(story: dict[str, Any], enrich_content: bool = True) -> dict[str, Any]:
    signal, topics = ai_signal(story)
    original_url = story.get("url") or HN_ITEM_URL.format(id=story["id"])
    original_title = clean_text(str(story["title"]))
    translated_title = translate_to_chinese(original_title, max_chars=500) if enrich_content else ""
    title_zh = localized_title(original_title, topics, translated=translated_title)
    score = int(story.get("score", 0) or 0)
    comments = int(story.get("descendants", 0) or 0)
    topic_text = "、".join(topics[:4]) or "人工智能"
    if enrich_content:
        _, content, source_type = source_content(story, original_url)
        summary, summary_quality = summary_from_content(title_zh, content, source_type)
    else:
        content, source_type, summary_quality = "", "未获取正文", "测试"
        summary = f"这条内容聚焦于“{title_zh}”，主要涉及{topic_text}。"
    engagement = f"{score} 分、{comments} 条讨论"
    reason = (
        f"内容直接涉及{topic_text}，Hacker News 当前有 {engagement}；"
        "它适合作为今天 AI 行业观察、产品判断或技术讨论的一个切入口。"
    )
    published = datetime.fromtimestamp(int(story.get("time", 0)), timezone.utc).astimezone(LOCAL_TZ)
    return {
        "rank": 0,
        "title_zh": title_zh,
        "title_original": original_title,
        "summary": summary,
        "summary_quality": summary_quality,
        "summary_source": source_type,
        "reason": reason,
        "original_url": original_url,
        "hacker_news_url": HN_ITEM_URL.format(id=story["id"]),
        "source_domain": domain_for(original_url),
        "score": score,
        "comments": comments,
        "author": story.get("by"),
        "published_at": published.isoformat(),
        "ai_topics": topics,
        "ai_signal": round(signal, 2),
    }


def collect_digest(fetch_limit: int = 180, count: int = 10) -> dict[str, Any]:
    ids = fetch_story_ids(fetch_limit)
    stories: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = [pool.submit(fetch_story, story_id) for story_id in ids]
        for future in as_completed(futures):
            story = future.result()
            if story:
                signal, _ = ai_signal(story)
                if signal > 0:
                    story["_ranking"] = score_story(story, signal)
                    stories.append(story)
    stories.sort(key=lambda item: item["_ranking"], reverse=True)
    selected_stories = stories[:count]
    with ThreadPoolExecutor(max_workers=8) as pool:
        selected = list(pool.map(build_item, selected_stories))
    for index, item in enumerate(selected, start=1):
        item["rank"] = index
    return {
        "generated_at": datetime.now(LOCAL_TZ).isoformat(),
        "source": "Hacker News official Firebase API",
        "source_api": API_ROOT,
        "timezone": "Asia/Shanghai",
        "filter": "AI 关键词信号 + Hacker News 热度、讨论度、时效性综合排序",
        "count": len(selected),
        "items": selected,
    }


def markdown_digest(data: dict[str, Any]) -> str:
    generated_at = data["generated_at"].replace("T", " ")
    generated_date = datetime.fromisoformat(data["generated_at"]).strftime("%Y年%m月%d日")
    lines = [
        f"# Hacker News AI 日报｜{generated_date}",
        "",
        f"> 每日精选 Hacker News 前 10 条 AI 动态。生成时间：{generated_at}（Asia/Shanghai）",
        "> 排序依据：AI 相关度、热度、讨论度与时效性综合评估。",
        "",
    ]
    if not data["items"]:
        lines.extend(["今天暂未筛选到可用的 AI 相关内容。", ""])
        return "\n".join(lines)
    lines.extend(
        [
            "## 今日导读",
            "",
            "以下内容按综合关注度排序，摘要基于原文正文、页面摘要或 Hacker News 条目正文整理；发布前可按需删去链接和数据说明。",
            "",
        ]
    )
    for item in data["items"]:
        lines.extend(
            [
                f"## {item['rank']:02d}｜{item['title_zh']}",
                "",
                f"**一句话导读**：{item['title_zh']}",
                "",
                f"**{summary_label(item)}**：{item['summary']}",
                "",
                f"**为什么值得关注**：{item['reason']}",
                "",
                f"**原文链接**：[阅读原文]({item['original_url']})",
                f"**HN 讨论**：[查看讨论]({item['hacker_news_url']})（{item['score']} 分，{item['comments']} 条评论）",
                "",
                "---",
                "",
            ]
        )
    return "\n".join(lines)


def write_outputs(data: dict[str, Any], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "data.json"
    markdown_path = output_dir / "hacker-news-ai.md"
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(markdown_digest(data), encoding="utf-8")
    return markdown_path, json_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 Hacker News AI 中文每日简报")
    default_output = Path(__file__).resolve().parent / "output"
    parser.add_argument("--output-dir", type=Path, default=default_output)
    parser.add_argument("--fetch-limit", type=int, default=180, help="最多抓取多少个故事 ID")
    parser.add_argument("--count", type=int, default=10, help="输出多少条，默认 10")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.fetch_limit < args.count or args.count < 1:
        print("--fetch-limit 必须不小于 --count，且 --count 至少为 1", file=sys.stderr)
        return 2
    try:
        data = collect_digest(fetch_limit=args.fetch_limit, count=args.count)
        markdown_path, json_path = write_outputs(data, args.output_dir)
    except Exception as error:  # cron needs a useful non-zero exit and message
        print(f"生成简报失败：{error}", file=sys.stderr)
        return 1
    print(f"已生成 {len(data['items'])} 条：{markdown_path}")
    print(f"JSON 数据：{json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
