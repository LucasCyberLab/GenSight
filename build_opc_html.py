"""Build the read-only GenSight GitHub Pages operations portal."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent
DOC_DIR = ROOT / "opc-doc"
OUTPUT = ROOT / "index.html"

DOCUMENTS = [
    {
        "file": "00-current-operating-baseline.md",
        "title": "当前运营基线",
        "group": "start",
        "description": "唯一主线、边界与本周行动规则",
    },
    {
        "file": "daily-action-and-review-guide.md",
        "title": "每日执行 SOP",
        "group": "do",
        "description": "晨会、获客、交付与飞书复盘",
    },
    {
        "file": "product-spec-and-pricing.md",
        "title": "产品与报价",
        "group": "do",
        "description": "跨境视觉外包的标准交付与报价",
    },
    {
        "file": "visual-portfolio-showcase.md",
        "title": "Demo 与案例",
        "group": "do",
        "description": "五大平台与独立站视觉样板",
    },
    {
        "file": "07-conversion-loop.md",
        "title": "获客到复购 SOP",
        "group": "do",
        "description": "触达、承接、成交、交付与沉淀",
    },
    {
        "file": "learning-and-sop-roadmap.md",
        "title": "交付协同 SOP",
        "group": "do",
        "description": "两人协作与交付流程",
    },
    {
        "file": "05-crossborder-opc-master-plan.md",
        "title": "跨境战略总纲",
        "group": "reference",
        "description": "战略假设、里程碑与验证路径",
    },
    {
        "file": "01-resource-audit.md",
        "title": "资源与约束盘点",
        "group": "reference",
        "description": "团队资源、边界与可用杠杆",
    },
    {
        "file": "02-niche-positioning.md",
        "title": "平台与客户定位",
        "group": "reference",
        "description": "平台场景与目标客户",
    },
    {
        "file": "03-value-proposition.md",
        "title": "价值主张",
        "group": "reference",
        "description": "客户问题与服务价值",
    },
    {
        "file": "04-business-model.md",
        "title": "商业模式",
        "group": "reference",
        "description": "收入结构与资源分配",
    },
    {
        "file": "06-mvp-design.md",
        "title": "MVP 验证",
        "group": "reference",
        "description": "验证指标与边界",
    },
    {
        "file": "demo-case-blueprint.md",
        "title": "Demo 样板策略",
        "group": "reference",
        "description": "首个样板站的选型与包装",
    },
    {
        "file": "README.md",
        "title": "OPC 资料索引",
        "group": "reference",
        "description": "方法论阶段与资料关系",
    },
]


def load_documents() -> dict[str, str]:
    docs: dict[str, str] = {}
    for item in DOCUMENTS:
        path = DOC_DIR / item["file"]
        if not path.exists():
            raise FileNotFoundError(f"Missing required document: {path}")
        docs[item["file"]] = path.read_text(encoding="utf-8")
    return docs


def build_html(docs: dict[str, str]) -> str:
    manifest = json.dumps(DOCUMENTS, ensure_ascii=False)
    contents = json.dumps(docs, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="GenSight 跨境视觉外包内部运营入口">
  <title>GenSight · 跨境视觉外包运营入口</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Noto+Sans+SC:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {{
      --ink: #17212b; --muted: #62707f; --line: #d8e0e8; --paper: #f5f7f8;
      --surface: #ffffff; --navy: #102a43; --blue: #1565c0; --mint: #1f8a70;
      --orange: #c65d07; --soft-blue: #e9f2fc; --soft-mint: #e7f5f0;
      --shadow: 0 10px 30px rgba(16,42,67,.08); --radius: 16px;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--paper); color: var(--ink); font-family: "Noto Sans SC", system-ui, sans-serif; line-height: 1.65; }}
    button {{ font: inherit; }}
    .shell {{ max-width: 1280px; margin: auto; padding: 0 24px 64px; }}
    header {{ display: flex; justify-content: space-between; align-items: center; padding: 22px 0; border-bottom: 1px solid var(--line); }}
    .brand {{ display: flex; align-items: center; gap: 12px; font-weight: 800; letter-spacing: -.02em; }}
    .brand-mark {{ display: grid; place-items: center; width: 34px; height: 34px; border-radius: 10px; background: var(--navy); color: white; }}
    .status {{ color: var(--mint); font: 500 12px "DM Mono", monospace; letter-spacing: .04em; }}
    .hero {{ display: grid; grid-template-columns: minmax(0, 1.45fr) minmax(250px, .55fr); gap: 32px; padding: 56px 0 38px; }}
    .eyebrow {{ margin: 0 0 10px; color: var(--blue); font: 500 12px "DM Mono", monospace; letter-spacing: .08em; text-transform: uppercase; }}
    h1 {{ max-width: 760px; margin: 0; font-size: clamp(30px, 4.8vw, 56px); line-height: 1.15; letter-spacing: -.055em; }}
    .hero p {{ max-width: 700px; font-size: 17px; color: var(--muted); }}
    .decision-card {{ padding: 22px; align-self: end; border: 1px solid #c6d8eb; border-radius: var(--radius); background: var(--soft-blue); }}
    .decision-card strong {{ display: block; margin-bottom: 7px; }}
    .decision-card p {{ margin: 0; color: #31516f; font-size: 14px; }}
    .section-label {{ margin: 8px 0 14px; color: var(--muted); font: 500 12px "DM Mono", monospace; letter-spacing: .08em; text-transform: uppercase; }}
    .today-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }}
    .card {{ padding: 20px; border: 1px solid var(--line); border-radius: var(--radius); background: var(--surface); box-shadow: 0 3px 12px rgba(16,42,67,.03); }}
    .card-number {{ display: inline-grid; place-items: center; width: 28px; height: 28px; border-radius: 50%; background: var(--navy); color: #fff; font: 500 12px "DM Mono", monospace; }}
    .card h2 {{ margin: 14px 0 8px; font-size: 17px; letter-spacing: -.02em; }}
    .card p {{ margin: 0; color: var(--muted); font-size: 14px; }}
    .feishu {{ display: flex; align-items: center; justify-content: space-between; gap: 18px; margin: 28px 0 40px; padding: 20px 24px; border-radius: var(--radius); background: var(--navy); color: white; }}
    .feishu h2 {{ margin: 0 0 3px; font-size: 17px; }} .feishu p {{ margin: 0; color: #b8d0e7; font-size: 14px; }}
    .feishu-badge {{ flex: none; padding: 8px 11px; border: 1px solid #52718e; border-radius: 7px; font: 500 12px "DM Mono", monospace; }}
    .layout {{ display: grid; grid-template-columns: 280px minmax(0, 1fr); align-items: start; gap: 28px; }}
    nav {{ position: sticky; top: 18px; padding: 8px; border: 1px solid var(--line); border-radius: var(--radius); background: var(--surface); }}
    .nav-group {{ padding: 10px 6px 3px; color: var(--muted); font: 500 11px "DM Mono", monospace; letter-spacing: .08em; text-transform: uppercase; }}
    .nav-item {{ display: block; width: 100%; padding: 10px; border: 0; border-radius: 9px; color: var(--ink); background: transparent; cursor: pointer; text-align: left; }}
    .nav-item:hover, .nav-item.active {{ background: var(--soft-blue); color: var(--blue); }} .nav-item small {{ display: block; color: var(--muted); font-size: 11px; }}
    .view {{ min-height: 520px; }} .start-view {{ display: block; }} .doc-view {{ display: none; }}
    .start-view .card {{ margin-bottom: 16px; }} .start-view h2 {{ margin-top: 0; }}
    .principles {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }}
    .principles li {{ list-style: none; padding: 16px; border-left: 3px solid var(--mint); background: var(--surface); color: var(--muted); }}
    .principles strong {{ display: block; color: var(--ink); }}
    .doc-view {{ padding: clamp(22px, 4vw, 46px); border: 1px solid var(--line); border-radius: var(--radius); background: var(--surface); box-shadow: var(--shadow); }}
    .doc-meta {{ margin-bottom: 24px; color: var(--muted); font-size: 13px; }} .doc-body h1 {{ font-size: 30px; }} .doc-body h2 {{ margin-top: 38px; font-size: 21px; }} .doc-body h3 {{ margin-top: 26px; font-size: 17px; }}
    .doc-body p, .doc-body li {{ color: #374858; }} .doc-body img {{ max-width: 100%; height: auto; border-radius: 12px; }} .doc-body table {{ width: 100%; border-collapse: collapse; margin: 22px 0; font-size: 14px; overflow: hidden; }} .doc-body th, .doc-body td {{ padding: 12px; border: 1px solid var(--line); text-align: left; vertical-align: top; }} .doc-body th {{ background: #eef3f7; }} .doc-body blockquote {{ margin: 20px 0; padding: 12px 18px; border-left: 4px solid var(--blue); background: var(--soft-blue); }} .doc-body code {{ padding: 2px 5px; border-radius: 4px; background: #eef3f7; }}
    footer {{ margin-top: 48px; color: var(--muted); font-size: 12px; text-align: center; }}
    @media (max-width: 780px) {{ .shell {{ padding: 0 16px 42px; }} .hero, .layout {{ grid-template-columns: 1fr; }} .today-grid, .principles {{ grid-template-columns: 1fr; }} nav {{ position: static; display: grid; grid-template-columns: repeat(2, 1fr); gap: 3px; }} .nav-group {{ grid-column: 1 / -1; }} .feishu {{ align-items: flex-start; flex-direction: column; }} header .status {{ display: none; }} }}
  </style>
</head>
<body>
  <div class="shell">
    <header><div class="brand"><span class="brand-mark">G</span><span>GenSight</span></div><span class="status">CROSS-BORDER VISUAL OPS · 2026-08</span></header>
    <main>
      <div id="home">
        <section class="hero">
          <div><p class="eyebrow">Internal operations portal</p><h1>把跨境视觉外包做成每天能推进的系统。</h1><p>这里只回答一个问题：现在该做什么。任务、线索、成交和复盘以飞书多维表格为准；本站只保留判断、SOP、案例和报价上下文。</p></div>
          <aside class="decision-card"><strong>当前唯一主线</strong><p>Amazon、美客多、Shopee、TikTok、SHEIN 与 Shopify 的视觉素材代制作。国内设计为机会型现金流，不占用主动获客资源。</p></aside>
        </section>
        <p class="section-label">Start here · 每天只走这三步</p>
        <section class="today-grid">
          <article class="card"><span class="card-number">01</span><h2>在飞书看今日任务</h2><p>只确认 Howard 与 Brian 各自 1–3 项可验收输出，任务、截止日与交接状态以飞书为准。</p></article>
          <article class="card"><span class="card-number">02</span><h2>按 SOP 推进业务</h2><p>需要报价、平台规范、交付边界或案例素材时，再从下方打开对应资料。</p></article>
          <article class="card"><span class="card-number">03</span><h2>在飞书完成复盘</h2><p>记录触达、询盘、成交、交付和一个关键瓶颈；次日 Top 3 从复盘中产生。</p></article>
        </section>
        <section class="feishu"><div><h2>飞书多维表格是唯一协作数据源</h2><p>本站不保存任务或客户数据，避免 GitHub Pages、本机工作台与飞书产生三份不同状态。</p></div><span class="feishu-badge">配置飞书入口后在此跳转</span></section>
      </div>
      <section class="layout">
        <nav id="nav" aria-label="资料导航"></nav>
        <div class="view">
          <section id="startView" class="start-view">
            <article class="card"><h2>使用边界</h2><p>这不是另一个协同系统。飞书负责状态、提醒、任务、线索和复盘；GenSight 负责让每个执行动作快速找到正确的业务上下文。</p></article>
            <p class="section-label">运行原则</p>
            <ul class="principles"><li><strong>先交付，再获客</strong>已收订金项目优先于一切主动运营。</li><li><strong>一条主线</strong>不把国内设计、跨境素材、独立站全案同时当作本周主推。</li><li><strong>行为即数据</strong>触达、报价、交付与复盘都写入飞书，而非靠记忆。</li><li><strong>资料按需打开</strong>先看今日任务，遇到问题再查 SOP，不用从知识库开始一天。</li></ul>
          </section>
          <article id="docView" class="doc-view"><div id="docMeta" class="doc-meta"></div><div id="docBody" class="doc-body"></div></article>
        </div>
      </section>
    </main>
    <footer>GenSight 内部运营入口 · 静态资料站，不保存协作数据</footer>
  </div>
  <script>
    const manifest = {manifest};
    const docs = {contents};
    const nav = document.querySelector("#nav");
    const home = document.querySelector("#home");
    const startView = document.querySelector("#startView");
    const docView = document.querySelector("#docView");
    const groupLabels = {{ start: "先看这里", do: "执行时打开", reference: "战略参考" }};
    let activeFile = null;
    for (const group of ["start", "do", "reference"]) {{
      nav.insertAdjacentHTML("beforeend", `<div class="nav-group">${{groupLabels[group]}}</div>`);
      manifest.filter(item => item.group === group).forEach(item => {{
        const button = document.createElement("button");
        button.className = "nav-item"; button.dataset.file = item.file;
        button.innerHTML = `${{item.title}}<small>${{item.description}}</small>`;
        button.addEventListener("click", () => openDocument(item.file));
        nav.append(button);
      }});
    }}
    const renderer = new marked.Renderer();
    renderer.link = (href, title, text) => {{
      const filename = decodeURIComponent(String(href || "")).replace(/^\\.\\//, "").split("#")[0].split("/").pop();
      if (docs[filename]) return `<a href="#${{filename}}" data-doc-link="${{filename}}"${{title ? ` title="${{title}}"` : ""}}>${{text}}</a>`;
      return `<a href="${{href}}" target="_blank" rel="noreferrer"${{title ? ` title="${{title}}"` : ""}}>${{text}}</a>`;
    }};
    marked.setOptions({{ renderer }});
    function openDocument(file) {{
      const item = manifest.find(doc => doc.file === file);
      if (!item || !docs[file]) return;
      activeFile = file; home.style.display = "none"; startView.style.display = "none"; docView.style.display = "block";
      document.querySelector("#docMeta").textContent = `${{item.title}} · ${{item.description}}`;
      document.querySelector("#docBody").innerHTML = marked.parse(docs[file]);
      document.querySelectorAll("[data-doc-link]").forEach(link => link.addEventListener("click", event => {{
        event.preventDefault(); openDocument(link.dataset.docLink);
      }}));
      document.querySelectorAll(".nav-item").forEach(button => button.classList.toggle("active", button.dataset.file === file));
      window.location.hash = file;
      window.scrollTo({{ top: 0, behavior: "smooth" }});
    }}
    const initial = decodeURIComponent(window.location.hash.slice(1));
    if (docs[initial]) openDocument(initial);
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    OUTPUT.write_text(build_html(load_documents()), encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)}")
