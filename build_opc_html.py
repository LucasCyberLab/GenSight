import os
import json

doc_dir = 'opc-doc'
docs = {}

doc_titles = {
    "05-crossborder-opc-master-plan.md": "05. OPC 运营方案总纲 (Master Plan)",
    "01-resource-audit.md": "01. 资源盘点 (Resource Audit)",
    "02-niche-positioning.md": "02. 利基定位重塑 (Niche Positioning)",
    "03-value-proposition.md": "03. 价值主张设计 (Value Proposition)",
    "04-business-model.md": "04. 精益商业模式 (Business Model)",
    "06-mvp-design.md": "06. MVP 验证设计 (MVP Design)",
    "07-conversion-loop.md": "07. 转化闭环 SOP (Conversion Loop)",
    "product-spec-and-pricing.md": "💎 产品手册与报价单 (Product & Pricing)",
    "learning-and-sop-roadmap.md": "🛠️ 7天学习计划与协同SOP (Learning & SOP)",
    "demo-case-blueprint.md": "💡 首个 Demo 样板案例思考 (Demo Strategy)",
    "README.md": "📚 OPC 文档库说明 (Overview)"
}

doc_categories = {
    "05-crossborder-opc-master-plan.md": "master",
    "01-resource-audit.md": "foundation",
    "02-niche-positioning.md": "foundation",
    "03-value-proposition.md": "foundation",
    "04-business-model.md": "foundation",
    "06-mvp-design.md": "foundation",
    "07-conversion-loop.md": "foundation",
    "product-spec-and-pricing.md": "product",
    "learning-and-sop-roadmap.md": "execution",
    "demo-case-blueprint.md": "execution",
    "README.md": "meta"
}

for fname in sorted(os.listdir(doc_dir)):
    if fname.endswith('.md'):
        path = os.path.join(doc_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            docs[fname] = f.read()

docs_json = json.dumps(docs, ensure_ascii=False)
titles_json = json.dumps(doc_titles, ensure_ascii=False)
cats_json = json.dumps(doc_categories, ensure_ascii=False)

html_template = f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GenSight · 通往出海独立站与 AI 品牌之路 (OPC 知识库)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    /* CSS Variables for Light Mode (Default) & Dark Mode */
    :root {{
      --bg-main: #f8fafc;
      --bg-sidebar: #ffffff;
      --bg-card: #ffffff;
      --border-color: #e2e8f0;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --accent-blue: #2563eb;
      --accent-cyan: #0284c7;
      --accent-purple: #7c3aed;
      --accent-green: #10b981;
      --accent-gold: #d97706;
      --callout-bg: #fff7ed;
      --callout-border: #f97316;
      --callout-text: #9a3412;
      --table-header-bg: #f1f5f9;
      --table-row-hover: #f8fafc;
      --code-bg: #f1f5f9;
      --code-text: #0284c7;
      --sidebar-width: 300px;
      --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.05);
    }}

    [data-theme="dark"] {{
      --bg-main: #090d16;
      --bg-sidebar: #0f1624;
      --bg-card: rgba(21, 30, 47, 0.85);
      --border-color: rgba(255, 255, 255, 0.08);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent-blue: #3b82f6;
      --accent-cyan: #00f2fe;
      --accent-purple: #8b5cf6;
      --accent-green: #10b981;
      --accent-gold: #f59e0b;
      --callout-bg: rgba(249, 115, 22, 0.1);
      --callout-border: #f97316;
      --callout-text: #ffedd5;
      --table-header-bg: rgba(30, 41, 59, 0.9);
      --table-row-hover: rgba(255, 255, 255, 0.03);
      --code-bg: #0f172a;
      --code-text: #38bdf8;
      --shadow-card: 0 10px 30px rgba(0, 0, 0, 0.3);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background-color: var(--bg-main);
      color: var(--text-main);
      display: flex;
      height: 100vh;
      overflow: hidden;
      line-height: 1.6;
      transition: background-color 0.3s, color 0.3s;
    }}

    /* Top Header */
    .top-header {{
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 64px;
      background: var(--bg-sidebar);
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      z-index: 100;
      transition: background-color 0.3s, border-color 0.3s;
    }}

    .logo-group {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .logo-icon {{
      font-size: 22px;
    }}

    .title-text {{
      font-size: 17px;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .title-tag {{
      background: linear-gradient(135deg, #0284c7, #7c3aed);
      color: #ffffff;
      font-size: 11px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 6px;
      text-transform: uppercase;
    }}

    .search-box {{
      position: relative;
      width: 320px;
    }}

    .search-input {{
      width: 100%;
      background: var(--bg-main);
      border: 1px solid var(--border-color);
      border-radius: 20px;
      padding: 8px 16px 8px 36px;
      color: var(--text-main);
      font-size: 13px;
      outline: none;
      transition: all 0.2s;
    }}

    .search-input:focus {{
      border-color: var(--accent-blue);
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
    }}

    .search-icon {{
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 14px;
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .theme-toggle {{
      background: var(--bg-main);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 7px 14px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}

    .theme-toggle:hover {{
      border-color: var(--accent-blue);
      color: var(--accent-blue);
    }}

    .btn-action {{
      background: var(--bg-main);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 7px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}

    .btn-action:hover {{
      border-color: var(--accent-blue);
    }}

    .btn-primary {{
      background: linear-gradient(135deg, #2563eb, #0284c7);
      border: none;
      color: #ffffff;
      font-weight: 700;
    }}

    .btn-primary:hover {{
      opacity: 0.95;
      box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }}

    /* Main Layout */
    .app-container {{
      display: flex;
      width: 100%;
      height: calc(100vh - 64px);
      margin-top: 64px;
    }}

    /* Sidebar Navigation (Feishu Wiki Style) */
    .sidebar {{
      width: var(--sidebar-width);
      background: var(--bg-sidebar);
      border-right: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      padding: 16px 12px;
      transition: background-color 0.3s, border-color 0.3s;
    }}

    .sidebar-header-title {{
      font-size: 14px;
      font-weight: 800;
      color: var(--text-main);
      padding: 8px 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .nav-section-title {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-muted);
      margin: 16px 8px 6px;
    }}

    .nav-item {{
      display: flex;
      align-items: center;
      padding: 9px 12px;
      border-radius: 8px;
      color: var(--text-muted);
      text-decoration: none;
      font-size: 13.5px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
      margin-bottom: 2px;
    }}

    .nav-item:hover {{
      background: var(--bg-main);
      color: var(--text-main);
    }}

    .nav-item.active {{
      background: rgba(37, 99, 235, 0.1);
      color: var(--accent-blue);
      font-weight: 700;
    }}

    [data-theme="dark"] .nav-item.active {{
      background: rgba(0, 242, 254, 0.15);
      color: #ffffff;
      border: 1px solid rgba(0, 242, 254, 0.3);
    }}

    .nav-item .icon {{
      margin-right: 8px;
      font-size: 15px;
    }}

    /* Main Content Area */
    .content-area {{
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      background: var(--bg-main);
      padding: 24px 40px 60px;
      transition: background-color 0.3s;
    }}

    /* Panoramic Header Banner (WaytoAGI Style) */
    .banner-container {{
      width: 100%;
      border-radius: 16px;
      overflow: hidden;
      margin-bottom: 24px;
      box-shadow: var(--shadow-card);
      border: 1px solid var(--border-color);
      background: var(--bg-card);
      position: relative;
    }}

    .banner-img {{
      width: 100%;
      height: 240px;
      object-fit: cover;
      display: block;
    }}

    .banner-overlay {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: linear-gradient(0deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0) 100%);
      padding: 20px 24px 16px;
      color: #ffffff;
    }}

    .banner-title {{
      font-size: 24px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 10px;
      text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }}

    .banner-subtitle {{
      font-size: 13px;
      opacity: 0.9;
      margin-top: 4px;
      font-weight: 500;
    }}

    /* KPI Summary Row */
    .kpi-row {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}

    .kpi-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 16px 18px;
      box-shadow: var(--shadow-card);
      transition: transform 0.2s, border-color 0.2s, background-color 0.3s;
    }}

    .kpi-card:hover {{
      transform: translateY(-2px);
      border-color: var(--accent-blue);
    }}

    .kpi-label {{
      font-size: 11.5px;
      color: var(--text-muted);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .kpi-value {{
      font-size: 17px;
      font-weight: 800;
      color: var(--text-main);
      margin-top: 4px;
    }}

    .kpi-sub {{
      font-size: 11.5px;
      color: var(--accent-blue);
      margin-top: 2px;
      font-weight: 600;
    }}

    /* Document Card */
    .doc-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 40px 48px;
      box-shadow: var(--shadow-card);
      transition: background-color 0.3s, border-color 0.3s;
    }}

    /* WaytoAGI / Feishu Callout Box */
    .waytoagi-callout {{
      background: var(--callout-bg);
      border-left: 4px solid var(--callout-border);
      color: var(--callout-text);
      padding: 16px 20px;
      border-radius: 0 12px 12px 0;
      margin: 20px 0;
      font-size: 14.5px;
      font-weight: 500;
      line-height: 1.7;
    }}

    /* Markdown Styling */
    .markdown-body {{
      color: var(--text-main);
      font-size: 15px;
      line-height: 1.75;
    }}

    .markdown-body h1 {{
      font-size: 26px;
      font-weight: 800;
      margin-bottom: 20px;
      padding-bottom: 12px;
      border-bottom: 2px solid var(--border-color);
      color: var(--text-main);
    }}

    .markdown-body h2 {{
      font-size: 20px;
      font-weight: 700;
      margin-top: 32px;
      margin-bottom: 14px;
      color: var(--accent-blue);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .markdown-body h3 {{
      font-size: 16px;
      font-weight: 700;
      margin-top: 24px;
      margin-bottom: 10px;
      color: var(--text-main);
    }}

    .markdown-body p {{
      margin-bottom: 16px;
      color: var(--text-main);
    }}

    .markdown-body blockquote {{
      border-left: 4px solid var(--accent-blue);
      background: rgba(37, 99, 235, 0.05);
      padding: 14px 20px;
      border-radius: 0 10px 10px 0;
      margin: 20px 0;
      color: var(--text-main);
    }}

    .markdown-body table {{
      width: 100%;
      border-collapse: collapse;
      margin: 24px 0;
      font-size: 14px;
      border-radius: 10px;
      overflow: hidden;
      border: 1px solid var(--border-color);
    }}

    .markdown-body th {{
      background: var(--table-header-bg);
      color: var(--text-main);
      font-weight: 700;
      text-align: left;
      padding: 12px 16px;
      border-bottom: 1px solid var(--border-color);
    }}

    .markdown-body td {{
      padding: 12px 16px;
      border-bottom: 1px solid var(--border-color);
      background: var(--bg-card);
      color: var(--text-main);
    }}

    .markdown-body tr:hover td {{
      background: var(--table-row-hover);
    }}

    .markdown-body ul, .markdown-body ol {{
      padding-left: 24px;
      margin-bottom: 16px;
    }}

    .markdown-body li {{
      margin-bottom: 6px;
      color: var(--text-main);
    }}

    .markdown-body code {{
      background: var(--code-bg);
      color: var(--code-text);
      padding: 2px 6px;
      border-radius: 4px;
      font-family: monospace;
      font-size: 13.5px;
    }}

    .markdown-body pre {{
      background: var(--code-bg);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 16px;
      overflow-x: auto;
      margin: 20px 0;
    }}

    .markdown-body pre code {{
      background: none;
      padding: 0;
      color: var(--text-main);
    }}

    /* Nav Buttons at bottom of doc */
    .doc-footer-nav {{
      display: flex;
      justify-content: space-between;
      margin-top: 40px;
      padding-top: 24px;
      border-top: 1px solid var(--border-color);
    }}

    /* Responsive */
    @media (max-width: 900px) {{
      .sidebar {{
        position: fixed;
        left: -300px;
        top: 64px;
        bottom: 0;
        z-index: 90;
        transition: left 0.3s;
      }}
      .sidebar.open {{
        left: 0;
      }}
      .content-area {{
        padding: 16px;
      }}
      .search-box {{
        width: 160px;
      }}
    }}
  </style>
</head>
<body>

  <!-- Top Header -->
  <header class="top-header">
    <div class="logo-group">
      <span class="logo-icon">🌈</span>
      <div class="title-text">
        GenSight · 通往出海独立站与 AI 品牌之路
        <span class="title-tag">OPC 知识库</span>
      </div>
    </div>

    <div class="search-box">
      <span class="search-icon">🔍</span>
      <input type="text" id="searchInput" class="search-input" placeholder="搜索知识库、SOP、报价或策略...">
    </div>

    <div class="header-actions">
      <!-- Theme Switcher Button -->
      <button class="theme-toggle" id="themeToggleBtn" onclick="toggleTheme()">
        <span id="themeIcon">☀️</span>
        <span id="themeLabel">浅色</span>
      </button>

      <button class="btn-action" onclick="copyMarkdown()">📋 复制 MD</button>
      <button class="btn-action btn-primary" onclick="window.print()">🖨️ 打印 / 导出 PDF</button>
    </div>
  </header>

  <!-- App Body -->
  <div class="app-container">

    <!-- Sidebar Navigation (Feishu Wiki Style) -->
    <nav class="sidebar" id="sidebar">
      <div class="sidebar-header-title">
        <span>📖</span> 目录导航
      </div>

      <div class="nav-section-title">🚀 战略总纲 (Master Plan)</div>
      <div class="nav-item active" data-file="05-crossborder-opc-master-plan.md" onclick="loadDoc('05-crossborder-opc-master-plan.md')">
        <span class="icon">🌈</span> 05. 通往 GenSight 出海之路
      </div>

      <div class="nav-section-title">📋 OPC 战略建盘 (01-07)</div>
      <div class="nav-item" data-file="01-resource-audit.md" onclick="loadDoc('01-resource-audit.md')">
        <span class="icon">📊</span> 01. 资源盘点
      </div>
      <div class="nav-item" data-file="02-niche-positioning.md" onclick="loadDoc('02-niche-positioning.md')">
        <span class="icon">🏹</span> 02. 利基定位重塑
      </div>
      <div class="nav-item" data-file="03-value-proposition.md" onclick="loadDoc('03-value-proposition.md')">
        <span class="icon">💡</span> 03. 价值主张设计
      </div>
      <div class="nav-item" data-file="04-business-model.md" onclick="loadDoc('04-business-model.md')">
        <span class="icon">📐</span> 04. 精益商业模式
      </div>
      <div class="nav-item" data-file="06-mvp-design.md" onclick="loadDoc('06-mvp-design.md')">
        <span class="icon">🧪</span> 06. MVP 验证设计
      </div>
      <div class="nav-item" data-file="07-conversion-loop.md" onclick="loadDoc('07-conversion-loop.md')">
        <span class="icon">🔄</span> 07. 转化闭环 SOP
      </div>

      <div class="nav-section-title">💎 产品与报价 (Product & Pricing)</div>
      <div class="nav-item" data-file="product-spec-and-pricing.md" onclick="loadDoc('product-spec-and-pricing.md')">
        <span class="icon">💰</span> 产品手册与报价单
      </div>

      <div class="nav-section-title">🛠️ 学习与 SOP (SOP & Roadmap)</div>
      <div class="nav-item" data-file="learning-and-sop-roadmap.md" onclick="loadDoc('learning-and-sop-roadmap.md')">
        <span class="icon">📚</span> 7天学习计划与协同SOP
      </div>

      <div class="nav-section-title">💡 Demo 样板策略 (Demo Strategy)</div>
      <div class="nav-item" data-file="demo-case-blueprint.md" onclick="loadDoc('demo-case-blueprint.md')">
        <span class="icon">⚡</span> 首个 Demo 样板思考
      </div>

      <div class="nav-section-title">📚 总体索引 (Overview)</div>
      <div class="nav-item" data-file="README.md" onclick="loadDoc('README.md')">
        <span class="icon">📖</span> OPC 文档库说明
      </div>
    </nav>

    <!-- Main Content Area -->
    <main class="content-area">

      <!-- Panoramic WaytoAGI Style Header Banner -->
      <div class="banner-container">
        <img class="banner-img" src="gensight_roadmap_banner.png" alt="GenSight Panoramic Roadmap Banner">
        <div class="banner-overlay">
          <div class="banner-title">
            🌈 通往 GenSight 出海独立站与 AI 品牌之路
          </div>
          <div class="banner-subtitle">
            愿景与目标：策略先于建站，视觉撬动转化 — 让中小型企业出海少走弯路，让品牌借力 AI 高效飞跃。
          </div>
        </div>
      </div>

      <!-- Top KPI Row -->
      <div class="kpi-row">
        <div class="kpi-card">
          <div class="kpi-label">项目阶段</div>
          <div class="kpi-value" style="color: var(--accent-cyan);">出海独立站全案</div>
          <div class="kpi-sub">建盘完成 ➔ 7天SOP执行</div>
        </div>

        <div class="kpi-card">
          <div class="kpi-label">主力全案定价</div>
          <div class="kpi-value" style="color: var(--accent-gold);">¥19.8K ~ ¥39.8K</div>
          <div class="kpi-sub">Shopify / WP 独立站全案</div>
        </div>

        <div class="kpi-card">
          <div class="kpi-label">长期 LTV 续费</div>
          <div class="kpi-value" style="color: var(--accent-green);">¥5,680 / 月</div>
          <div class="kpi-sub">海外广告视觉代制作包</div>
        </div>

        <div class="kpi-card">
          <div class="kpi-label">团队协同分工</div>
          <div class="kpi-value" style="color: var(--accent-purple);">Howard & Brian</div>
          <div class="kpi-sub">商业策略+英文Copy & 欧美视觉</div>
        </div>
      </div>

      <!-- Document Content Card -->
      <div class="doc-card">
        <div id="docViewer" class="markdown-body">
          <!-- Rendered Markdown will appear here -->
        </div>

        <!-- Footer Page Navigation -->
        <div class="doc-footer-nav">
          <button id="prevBtn" class="btn-action" onclick="prevDoc()">← 上一文档</button>
          <button id="nextBtn" class="btn-action btn-primary" onclick="nextDoc()">下一文档 →</button>
        </div>
      </div>
    </main>

  </div>

  <script>
    const docs = {docs_json};
    const docTitles = {titles_json};
    const docFiles = [
      "05-crossborder-opc-master-plan.md",
      "01-resource-audit.md",
      "02-niche-positioning.md",
      "03-value-proposition.md",
      "04-business-model.md",
      "06-mvp-design.md",
      "07-conversion-loop.md",
      "product-spec-and-pricing.md",
      "learning-and-sop-roadmap.md",
      "demo-case-blueprint.md",
      "README.md"
    ];

    let currentFile = "05-crossborder-opc-master-plan.md";

    // Theme Management (Light by default, toggleable to dark)
    function initTheme() {{
      const savedTheme = localStorage.getItem('gensight_theme') || 'light';
      setTheme(savedTheme);
    }}

    function setTheme(theme) {{
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('gensight_theme', theme);
      
      const themeIcon = document.getElementById('themeIcon');
      const themeLabel = document.getElementById('themeLabel');
      
      if (theme === 'dark') {{
        themeIcon.textContent = '🌙';
        themeLabel.textContent = '暗色';
      }} else {{
        themeIcon.textContent = '☀️';
        themeLabel.textContent = '浅色';
      }}
    }}

    function toggleTheme() {{
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      const nextTheme = current === 'light' ? 'dark' : 'light';
      setTheme(nextTheme);
    }}

    function loadDoc(filename) {{
      if (!docs[filename]) return;
      currentFile = filename;

      // Render Markdown
      const content = docs[filename];
      document.getElementById('docViewer').innerHTML = marked.parse(content);

      // Update Nav Class
      document.querySelectorAll('.nav-item').forEach(el => {{
        if (el.dataset.file === filename) el.classList.add('active');
        else el.classList.remove('active');
      }});

      // Update Footer Buttons
      const idx = docFiles.indexOf(filename);
      document.getElementById('prevBtn').style.visibility = idx > 0 ? 'visible' : 'hidden';
      document.getElementById('nextBtn').style.visibility = idx < docFiles.length - 1 ? 'visible' : 'hidden';

      // Scroll to top
      document.querySelector('.content-area').scrollTop = 0;
    }}

    function prevDoc() {{
      const idx = docFiles.indexOf(currentFile);
      if (idx > 0) loadDoc(docFiles[idx - 1]);
    }}

    function nextDoc() {{
      const idx = docFiles.indexOf(currentFile);
      if (idx < docFiles.length - 1) loadDoc(docFiles[idx + 1]);
    }}

    function copyMarkdown() {{
      const content = docs[currentFile];
      navigator.clipboard.writeText(content).then(() => {{
        alert("Markdown 内容已成功复制到剪贴板！");
      }});
    }}

    // Search functionality
    document.getElementById('searchInput').addEventListener('input', function(e) {{
      const query = e.target.value.toLowerCase().trim();
      if (!query) {{
        loadDoc(currentFile);
        return;
      }}

      // Find matches across all docs
      for (const file of docFiles) {{
        if (docs[file].toLowerCase().includes(query)) {{
          loadDoc(file);
          break;
        }}
      }}
    }});

    // Initialize Theme and Document
    initTheme();
    loadDoc(currentFile);
  </script>
</body>
</html>
"""

# Write to root index.html, opc-dashboard.html and opc-doc/index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

with open('opc-dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

with open('opc-doc/index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Generated index.html, opc-dashboard.html and opc-doc/index.html with Light/Dark Theme & Banner!")
