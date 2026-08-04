import os
import json

doc_dir = 'opc-doc'
docs = {}

doc_titles = {
    "visual-portfolio-showcase.md": "🖼️ 视觉作品与 Demo 样板库 (Portfolio Showcase)",
    "product-spec-and-pricing.md": "💎 交付物数量与标准报价单 (Product & Pricing)",
    "05-crossborder-opc-master-plan.md": "05. OPC 运营方案总纲 (Master Plan)",
    "01-resource-audit.md": "01. 资源盘点 (Resource Audit)",
    "02-niche-positioning.md": "02. 利基定位重塑 (Niche Positioning)",
    "03-value-proposition.md": "03. 价值主张设计 (Value Proposition)",
    "04-business-model.md": "04. 精益商业模式 (Business Model)",
    "06-mvp-design.md": "06. MVP 验证设计 (MVP Design)",
    "07-conversion-loop.md": "07. 转化闭环 SOP (Conversion Loop)",
    "learning-and-sop-roadmap.md": "🛠️ 7天学习计划与协同SOP (Learning & SOP)",
    "demo-case-blueprint.md": "💡 首个 Demo 样板案例思考 (Demo Strategy)",
    "README.md": "📚 OPC 文档库说明 (Overview)"
}

doc_categories = {
    "visual-portfolio-showcase.md": "product",
    "product-spec-and-pricing.md": "product",
    "05-crossborder-opc-master-plan.md": "master",
    "01-resource-audit.md": "foundation",
    "02-niche-positioning.md": "foundation",
    "03-value-proposition.md": "foundation",
    "04-business-model.md": "foundation",
    "06-mvp-design.md": "foundation",
    "07-conversion-loop.md": "foundation",
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
  <title>GenSight · 5大跨境平台与独立站视觉素材代制作实验室 (OPC 知识库)</title>
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
      min-height: 240px;
    }}

    .banner-img {{
      width: 100%;
      height: 320px;
      object-fit: cover;
      object-position: center;
      display: block;
    }}

    .banner-overlay {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: linear-gradient(0deg, rgba(15, 23, 42, 0.85) 0%, rgba(15, 23, 42, 0) 100%);
      padding: 24px 28px 20px;
      color: #ffffff;
    }}

    .banner-title {{
      font-size: 24px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 10px;
      text-shadow: 0 2px 6px rgba(0,0,0,0.6);
    }}

    .banner-subtitle {{
      font-size: 13.5px;
      opacity: 0.95;
      margin-top: 6px;
      font-weight: 500;
      text-shadow: 0 1px 3px rgba(0,0,0,0.6);
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

    /* Markdown Styling & Image Display */
    .markdown-body {{
      color: var(--text-main);
      font-size: 15px;
      line-height: 1.75;
    }}

    .markdown-body img {{
      max-width: 100%;
      height: auto;
      border-radius: 14px;
      margin: 20px 0;
      box-shadow: var(--shadow-card);
      border: 1px solid var(--border-color);
      display: block;
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

    /* Calculator Styles */
    .calculator-container {{
      display: grid;
      grid-template-columns: 1fr 400px;
      gap: 28px;
    }}

    @media (max-width: 1050px) {{
      .calculator-container {{
        grid-template-columns: 1fr;
      }}
    }}

    .calc-box {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 28px;
      box-shadow: var(--shadow-card);
    }}

    .calc-title {{
      font-size: 20px;
      font-weight: 800;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .currency-switcher {{
      display: flex;
      background: var(--bg-main);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 4px;
      margin-bottom: 24px;
    }}

    .curr-btn {{
      flex: 1;
      padding: 10px;
      border: none;
      border-radius: 8px;
      background: transparent;
      color: var(--text-muted);
      font-weight: 700;
      font-size: 14px;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .curr-btn.active {{
      background: var(--accent-blue);
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
    }}

    .option-group {{
      margin-bottom: 28px;
    }}

    .group-label {{
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 12px;
    }}

    .item-card {{
      border: 1.5px solid var(--border-color);
      border-radius: 14px;
      padding: 18px 20px;
      margin-bottom: 14px;
      display: flex;
      flex-direction: column;
      cursor: pointer;
      transition: all 0.2s;
      background: var(--bg-card);
    }}

    .item-card:hover {{
      border-color: var(--accent-blue);
    }}

    .item-card.selected {{
      border-color: var(--accent-blue);
      background: rgba(37, 99, 235, 0.04);
    }}

    .item-header-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
    }}

    .item-info {{
      flex: 1;
      padding-right: 16px;
    }}

    .item-name {{
      font-size: 15.5px;
      font-weight: 700;
      color: var(--text-main);
    }}

    .item-desc {{
      font-size: 12.5px;
      color: var(--text-muted);
      margin-top: 4px;
    }}

    .item-price {{
      font-size: 17px;
      font-weight: 800;
      color: var(--accent-gold);
    }}

    /* Granular Deliverables Box inside Item Card */
    .deliverables-box {{
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px dashed var(--border-color);
      font-size: 12.5px;
      color: var(--text-main);
      background: var(--bg-main);
      border-radius: 8px;
      padding: 10px 14px;
    }}

    .deliverable-title {{
      font-weight: 700;
      color: var(--accent-blue);
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .deliverable-list {{
      list-style: none;
      padding-left: 0;
      margin-bottom: 0;
    }}

    .deliverable-list li {{
      margin-bottom: 3px;
      color: var(--text-main);
      display: flex;
      align-items: flex-start;
      gap: 6px;
    }}

    .qty-control {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-top: 8px;
    }}

    .qty-btn {{
      width: 28px;
      height: 28px;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      background: var(--bg-main);
      color: var(--text-main);
      font-weight: 700;
      cursor: pointer;
    }}

    .qty-num {{
      font-size: 14px;
      font-weight: 700;
      width: 24px;
      text-align: center;
    }}

    /* Right Bill Summary */
    .summary-card {{
      background: var(--bg-card);
      border: 2px solid var(--accent-blue);
      border-radius: 16px;
      padding: 24px;
      position: sticky;
      top: 88px;
      box-shadow: var(--shadow-card);
    }}

    .bill-header {{
      font-size: 18px;
      font-weight: 800;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border-color);
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .bill-item-block {{
      margin-bottom: 14px;
      padding-bottom: 12px;
      border-bottom: 1px dashed var(--border-color);
    }}

    .bill-item-title-row {{
      display: flex;
      justify-content: space-between;
      font-size: 14px;
      font-weight: 700;
      color: var(--text-main);
    }}

    .bill-item-specs {{
      font-size: 11.5px;
      color: var(--text-muted);
      margin-top: 4px;
      line-height: 1.4;
    }}

    .bill-total-box {{
      margin-top: 20px;
      padding-top: 16px;
      border-top: 2px dashed var(--border-color);
    }}

    .bill-total-label {{
      font-size: 13px;
      color: var(--text-muted);
      font-weight: 700;
    }}

    .bill-total-amount {{
      font-size: 32px;
      font-weight: 900;
      color: var(--accent-blue);
      margin-top: 4px;
    }}

    .discount-badge {{
      background: rgba(16, 185, 129, 0.12);
      color: var(--accent-green);
      font-size: 12px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      margin-top: 8px;
      display: inline-block;
    }}

    .action-btn-group {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 24px;
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
        GenSight · 5大跨境平台与独立站视觉素材代制作实验室
        <span class="title-tag">作品与报价系统</span>
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

      <div class="nav-section-title">🖼️ 视觉作品与 Demo 库</div>
      <div class="nav-item" data-file="visual-portfolio-showcase.md" onclick="loadDoc('visual-portfolio-showcase.md')">
        <span class="icon">🖼️</span> 5大平台与独立站 Demo 样板
      </div>

      <div class="nav-section-title">⚡ 智能报价工具 (Price Calculator)</div>
      <div class="nav-item active" data-file="calculator" onclick="loadCalculator()">
        <span class="icon">🧮</span> 智能报价计算器
      </div>

      <div class="nav-section-title">💎 交付物明细与报价单</div>
      <div class="nav-item" data-file="product-spec-and-pricing.md" onclick="loadDoc('product-spec-and-pricing.md')">
        <span class="icon">💰</span> 交付物数量与标准报价单
      </div>

      <div class="nav-section-title">🚀 战略总纲 (Master Plan)</div>
      <div class="nav-item" data-file="05-crossborder-opc-master-plan.md" onclick="loadDoc('05-crossborder-opc-master-plan.md')">
        <span class="icon">🌈</span> 05. 通往 GenSight 视觉外包之路
      </div>

      <div class="nav-section-title">📋 OPC 战略建盘 (01-07)</div>
      <div class="nav-item" data-file="01-resource-audit.md" onclick="loadDoc('01-resource-audit.md')">
        <span class="icon">📊</span> 01. 资源盘点
      </div>
      <div class="nav-item" data-file="02-niche-positioning.md" onclick="loadDoc('02-niche-positioning.md')">
        <span class="icon">🏹</span> 02. 利基定位重塑 (5大平台)
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

      <!-- Panoramic WaytoAGI Style Header Banner (With Multi-fallback src) -->
      <div class="banner-container">
        <img id="bannerImg" class="banner-img" 
             src="gensight_wide_banner.png" 
             alt="GenSight Panoramic Roadmap Banner"
             onerror="if(this.src.indexOf('gensight_wide_banner.png')!==-1){{this.src='gensight_roadmap_banner.png';}}else{{this.src='assets/gensight_roadmap_banner.png';}}">
        <div class="banner-overlay">
          <div class="banner-title">
            🌈 GenSight 5大跨境平台与独立站智能报价及作品案例库
          </div>
          <div class="banner-subtitle">
            一键勾选项目 ➔ 自动计算确切交付数量与标准 ➔ 实时生成官方 PDF 报价单与微信发单文本
          </div>
        </div>
      </div>

      <!-- Document Content Card -->
      <div class="doc-card">
        <div id="docViewer">
          <!-- Calculator UI or Markdown Content -->
        </div>

        <!-- Footer Page Navigation -->
        <div class="doc-footer-nav" id="footerNav">
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
      "visual-portfolio-showcase.md",
      "product-spec-and-pricing.md",
      "05-crossborder-opc-master-plan.md",
      "01-resource-audit.md",
      "02-niche-positioning.md",
      "03-value-proposition.md",
      "04-business-model.md",
      "06-mvp-design.md",
      "07-conversion-loop.md",
      "learning-and-sop-roadmap.md",
      "demo-case-blueprint.md",
      "README.md"
    ];

    let currentFile = "calculator";
    let selectedCurr = "RMB"; // 'RMB' or 'USD'

    // Pricing items state
    let state = {{
      trial: false,
      singleSkuQty: 0,
      monthlyTerm: 'none', // 'none', 'month', 'quarter', 'halfyear'
      addonAplus: false,
      addonMultiLang: false,
      addonTiktokMotionQty: 0,
      addonVi: false
    }};

    // Theme Management
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

    // Calculator Render Logic
    function loadCalculator() {{
      currentFile = "calculator";
      document.getElementById('footerNav').style.display = 'none';

      // Update Nav Class
      document.querySelectorAll('.nav-item').forEach(el => {{
        if (el.dataset.file === 'calculator') el.classList.add('active');
        else el.classList.remove('active');
      }});

      renderCalculatorUI();
    }}

    function switchCurrency(curr) {{
      selectedCurr = curr;
      renderCalculatorUI();
    }}

    function renderCalculatorUI() {{
      const symbol = selectedCurr === 'RMB' ? '¥' : '$';
      const unit = selectedCurr === 'RMB' ? '元' : 'USD';

      // Item Prices
      const pTrial = selectedCurr === 'RMB' ? 880 : 150;
      const pSku = selectedCurr === 'RMB' ? 1680 : 280;
      const pMonth = selectedCurr === 'RMB' ? 6800 : 1350;
      const pQuarter = selectedCurr === 'RMB' ? 18800 : 3600;
      const pHalfyear = selectedCurr === 'RMB' ? 33800 : 6500;

      const pAplus = selectedCurr === 'RMB' ? 1200 : 200;
      const pLang = selectedCurr === 'RMB' ? 800 : 130;
      const pTtMotion = selectedCurr === 'RMB' ? 600 : 100;
      const pVi = selectedCurr === 'RMB' ? 1980 : 320;

      // Calculate Total
      let total = 0;
      let billList = [];
      let discountText = "";

      if (state.trial) {{
        total += pTrial;
        billList.push({{
          name: "3套高CTR素材体验包",
          specs: "• 确切数量：3套KV (含1:1与9:16双尺寸，共6张图)\\n• 标准：含Howard文案+现有素材点击率诊断",
          price: `${{symbol}}${{pTrial.toLocaleString()}}`
        }});
      }}

      if (state.singleSkuQty > 0) {{
        const skuSub = state.singleSkuQty * pSku;
        total += skuSub;
        billList.push({{
          name: `单平台 Listing 全套开款包 x${{state.singleSkuQty}} SKU`,
          specs: `• 确切数量：${{state.singleSkuQty}}主图 + ${{state.singleSkuQty*6}}附图 + ${{state.singleSkuQty}}套Banner/A+ (共${{state.singleSkuQty*8}}件物料)\\n• 标准：100%纯白底合规+多语种卖点+欧美Lifestyle模特`,
          price: `${{symbol}}${{skuSub.toLocaleString()}}`
        }});
      }}

      if (state.monthlyTerm === 'month') {{
        total += pMonth;
        billList.push({{
          name: "跨平台素材代制作包 (月付方案)",
          specs: "• 确切数量：24件核心素材 (12套跨尺寸广告KV共36张图 + 4套Listing包 + 8组TikTok卡片)\\n• 标准：Howard+Brian全包+全店合规诊断",
          price: `${{symbol}}${{pMonth.toLocaleString()}}`
        }});
      }} else if (state.monthlyTerm === 'quarter') {{
        total += pQuarter;
        billList.push({{
          name: "跨平台素材代制作包 (季签 - 推荐)",
          specs: "• 确切数量：连续3个月 (每月24件核心素材/36张图/8组TikTok卡片)\\n• 标准：周度按时交货+月度CTR数据复盘",
          price: `${{symbol}}${{pQuarter.toLocaleString()}}`
        }});
        discountText = selectedCurr === 'RMB' ? "🎉 已享受季签折扣（立省 ¥1,600）" : "🎉 Quarter Discount Applied (Saved $450 USD)";
      }} else if (state.monthlyTerm === 'halfyear') {{
        total += pHalfyear;
        billList.push({{
          name: "跨平台素材代制作包 (半年签 - 专享)",
          specs: "• 确切数量：连续6个月 (每月24件核心素材，衍生60+张视觉资产)\\n• 标准：专享品牌策略倾斜+最高折算优惠",
          price: `${{symbol}}${{pHalfyear.toLocaleString()}}`
        }});
        discountText = selectedCurr === 'RMB' ? "🎉 已享受半年签专享折扣（立省 ¥7,000）" : "🎉 Half-Year Discount Applied (Saved $1,600 USD)";
      }}

      if (state.addonAplus) {{
        total += pAplus;
        billList.push({{
          name: "亚马逊 A+ 页面高级定制模块",
          specs: "• 确切数量：1套完整 A+ 页面 (970x600/970x300 高保真大厂排版)",
          price: `${{symbol}}${{pAplus.toLocaleString()}}`
        }});
      }}

      if (state.addonMultiLang) {{
        total += pLang;
        billList.push({{
          name: "西/葡多语种本土化文案包",
          specs: "• 确切数量：匹配美客多拉美美墨巴站点的全套西班牙语/葡萄牙语文案",
          price: `${{symbol}}${{pLang.toLocaleString()}}`
        }});
      }}

      if (state.addonTiktokMotionQty > 0) {{
        const ttSub = state.addonTiktokMotionQty * pTtMotion;
        total += ttSub;
        billList.push({{
          name: `TikTok 9:16 微动效广告卡片 x${{state.addonTiktokMotionQty}} 组`,
          specs: `• 确切数量：${{state.addonTiktokMotionQty}} 组带微动效的 9:16 沉浸式 Hook 封面卡片`,
          price: `${{symbol}}${{ttSub.toLocaleString()}}`
        }});
      }}

      if (state.addonVi) {{
        total += pVi;
        billList.push({{
          name: "品牌 Logo / VI 基础识别规范包",
          specs: "• 确切数量：1套 Logo 标志 + 标准色/标准字规范 + 基础应用物料",
          price: `${{symbol}}${{pVi.toLocaleString()}}`
        }});
      }}

      const html = `
        <div class="calculator-container">
          <!-- Left Options Panel -->
          <div class="calc-box">
            <div class="calc-title">
              <span>🧮</span> GenSight 智能报价计算器 (精准数量与标准)
            </div>

            <!-- Currency Switcher -->
            <div class="currency-switcher">
              <button class="curr-btn ${{selectedCurr === 'RMB' ? 'active' : ''}}" onclick="switchCurrency('RMB')">
                🇨🇳 国内商家报价 (RMB / ¥)
              </button>
              <button class="curr-btn ${{selectedCurr === 'USD' ? 'active' : ''}}" onclick="switchCurrency('USD')">
                🌎 海外客户报价 (USD / $)
              </button>
            </div>

            <!-- Section 1: Standard Packages -->
            <div class="option-group">
              <div class="group-label">一、 基础服务与 Listing 开款套餐 (包含确切数量与标准)</div>

              <!-- Trial Package -->
              <div class="item-card ${{state.trial ? 'selected' : ''}}" onclick="toggleState('trial')">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">🧪 3套高 CTR 广告素材体验包</div>
                    <div class="item-desc">诊断现有素材痛点 + 交付 3 套高 CTR 广告 KV (签约月包可全额抵扣)。</div>
                  </div>
                  <div class="item-price">${{symbol}}${{pTrial.toLocaleString()}}</div>
                </div>
                <div class="deliverables-box">
                  <div class="deliverable-title">📋 确切交付物数量与标准：</div>
                  <ul class="deliverable-list">
                    <li>🔹 <strong>确切交付数量</strong>：3 套广告 KV (每套免费赠送 1:1 + 9:16 双尺寸，<strong>共 6 张精修图</strong>)</li>
                    <li>🔹 <strong>执行标准</strong>：Howard 撰写 3 套英文/西语 Headline 与 CTA 文案；美工+AI 排版大厂质感；含现有点击率诊断报告</li>
                  </ul>
                </div>
              </div>

              <!-- Single SKU Package -->
              <div class="item-card ${{state.singleSkuQty > 0 ? 'selected' : ''}}">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">📦 单平台 Listing 全套开款包 (选定 1 SKU)</div>
                    <div class="item-desc">一站式解决 Amazon / 美客多 / Shopee / SHEIN 上的新品开款或爆款打造。</div>
                    <div class="qty-control" onclick="event.stopPropagation()">
                      <span style="font-size: 13px; font-weight: 600;">SKU 数量：</span>
                      <button class="qty-btn" onclick="changeSkuQty(-1)">-</button>
                      <span class="qty-num">${{state.singleSkuQty}}</span>
                      <button class="qty-btn" onclick="changeSkuQty(1)">+</button>
                    </div>
                  </div>
                  <div class="item-price">${{symbol}}${{pSku.toLocaleString()}} / SKU</div>
                </div>
                <div class="deliverables-box">
                  <div class="deliverable-title">📋 确切交付物数量与标准：</div>
                  <ul class="deliverable-list">
                    <li>🔹 <strong>确切交付数量</strong>：<strong>1张</strong>100%纯白底主图(2000x2000px) + <strong>6张</strong>卖点/对比/尺寸附图 + <strong>1套</strong>响应式Banner/A+ (<strong>单SKU共计8件物料</strong>)</li>
                    <li>🔹 <strong>执行标准</strong>：主图合规率100%；多语种卖点文案；欧美真实Lifestyle模特生成；交付后包含2次免费细节微调</li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- Section 2: Retainer Packages -->
            <div class="option-group">
              <div class="group-label">二、 跨平台广告与素材代制作月包 (全包 Retainer)</div>

              <div class="item-card ${{state.monthlyTerm === 'month' ? 'selected' : ''}}" onclick="setMonthlyTerm('month')">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">🚀 跨平台素材包 (月付方案)</div>
                    <div class="item-desc">满足多平台布局卖家的全套素材按月代制作。</div>
                  </div>
                  <div class="item-price">${{symbol}}${{pMonth.toLocaleString()}} / 月</div>
                </div>
                <div class="deliverables-box">
                  <div class="deliverable-title">📋 确切交付物数量与标准：</div>
                  <ul class="deliverable-list">
                    <li>🔹 <strong>每月确切交付数量</strong>：<strong>12套</strong>广告KV(免费延伸1:1/9:16/16:9三尺寸<strong>共36张图</strong>) + <strong>4套</strong>Listing升级包(<strong>折合24+张图</strong>) + <strong>8组</strong>TikTok动态/静态卡片</li>
                    <li>🔹 <strong>执行标准</strong>：每周一/周四分批交付告别拖卡；Howard策略文案+Brian美工AI排版全包；每月赠送全店视觉合规诊断</li>
                  </ul>
                </div>
              </div>

              <div class="item-card ${{state.monthlyTerm === 'quarter' ? 'selected' : ''}}" onclick="setMonthlyTerm('quarter')">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">🌟 跨平台素材包 (季签 - 推荐)</div>
                    <div class="item-desc">按季度签署，包含全套 24 件/月素材量，资金使用率最高。</div>
                  </div>
                  <div class="item-price">${{symbol}}${{pQuarter.toLocaleString()}} / 季</div>
                </div>
                <div class="deliverables-box">
                  <div class="deliverable-title">📋 确切交付物数量与标准：</div>
                  <ul class="deliverable-list">
                    <li>🔹 <strong>确切交付数量</strong>：连续3个月，每月包含24件/套核心素材 (包含108张跨尺寸KV及24组TikTok卡片)</li>
                    <li>🔹 <strong>执行标准</strong>：在月付标准基础上，额外包含每月广告点击率 (CTR) 数据复盘，指导下月素材迭代方向</li>
                  </ul>
                </div>
              </div>

              <div class="item-card ${{state.monthlyTerm === 'halfyear' ? 'selected' : ''}}" onclick="setMonthlyTerm('halfyear')">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">👑 跨平台素材包 (半年签 - 专享价)</div>
                    <div class="item-desc">长期品牌策略倾斜，享受最高折算优惠。</div>
                  </div>
                  <div class="item-price">${{symbol}}${{pHalfyear.toLocaleString()}} / 半年</div>
                </div>
                <div class="deliverables-box">
                  <div class="deliverable-title">📋 确切交付物数量与标准：</div>
                  <ul class="deliverable-list">
                    <li>🔹 <strong>确切交付数量</strong>：连续6个月，累计交付超过 144 套/件 核心视觉资产 (衍生 360+ 张图片)</li>
                    <li>🔹 <strong>执行标准</strong>：Howard 策略总监全程一对一品牌调性把控，优先加急排期</li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- Section 3: Add-ons -->
            <div class="option-group">
              <div class="group-label">三、 高级增值选配服务 (Add-ons)</div>

              <div class="item-card ${{state.addonAplus ? 'selected' : ''}}" onclick="toggleState('addonAplus')">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">✨ 亚马逊 A+ 页面高级定制模块</div>
                    <div class="item-desc">970x600 / 970x300 高保真大厂风格 A+ 模块设计。</div>
                  </div>
                  <div class="item-price">+${{symbol}}${{pAplus.toLocaleString()}}</div>
                </div>
              </div>

              <div class="item-card ${{state.addonMultiLang ? 'selected' : ''}}" onclick="toggleState('addonMultiLang')">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">🌮 西班牙语 / 葡萄牙语多语种本土化文案包</div>
                    <div class="item-desc">专为美客多 (Mercado Libre) 拉美站点定制符合当地语境的文案。</div>
                  </div>
                  <div class="item-price">+${{symbol}}${{pLang.toLocaleString()}}</div>
                </div>
              </div>

              <div class="item-card ${{state.addonTiktokMotionQty > 0 ? 'selected' : ''}}">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">🎵 TikTok 9:16 微动效 / 动态广告封面卡片</div>
                    <div class="item-desc">针对 TikTok 高 CTR 广告设计的带动态微效果封面图。</div>
                    <div class="qty-control" onclick="event.stopPropagation()">
                      <span style="font-size: 13px; font-weight: 600;">组数：</span>
                      <button class="qty-btn" onclick="changeTtMotionQty(-1)">-</button>
                      <span class="qty-num">${{state.addonTiktokMotionQty}}</span>
                      <button class="qty-btn" onclick="changeTtMotionQty(1)">+</button>
                    </div>
                  </div>
                  <div class="item-price">+${{symbol}}${{pTtMotion.toLocaleString()}} / 组</div>
                </div>
              </div>

              <div class="item-card ${{state.addonVi ? 'selected' : ''}}" onclick="toggleState('addonVi')">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">🎨 品牌 Logo / VI 基础识别升级规范包</div>
                    <div class="item-desc">Logo 标志设计 + 标准色/标准字规范 + 基础应用物料。</div>
                  </div>
                  <div class="item-price">+${{symbol}}${{pVi.toLocaleString()}}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Bill Summary Sticky Box -->
          <div class="summary-card">
            <div class="bill-header">
              <span>🧾 项目报价与交付明细</span>
              <span style="font-size: 12px; color: var(--accent-blue); font-weight: 700;">GenSight 官方</span>
            </div>

            <div id="billItemsContainer">
              ${{billList.length === 0 ? '<div style="color: var(--text-muted); font-size: 13.5px; padding: 20px 0; text-align: center;">请在左侧勾选您需要的服务项目</div>' : ''}}
              ${{billList.map(item => `
                <div class="bill-item-block">
                  <div class="bill-item-title-row">
                    <span>${{item.name}}</span>
                    <span style="color: var(--accent-gold);">${{item.price}}</span>
                  </div>
                  <div class="bill-item-specs">${{item.specs.replace(/\\n/g, '<br>')}}</div>
                </div>
              `).join('')}}
            </div>

            ${{discountText ? `<div class="discount-badge">${{discountText}}</div>` : ''}}

            <div class="bill-total-box">
              <div class="bill-total-label">预估项目总额 (Estimated Total)</div>
              <div class="bill-total-amount">${{symbol}}${{total.toLocaleString()}} <span style="font-size: 14px; font-weight: 600; color: var(--text-muted);">${{unit}}</span></div>
            </div>

            <div class="action-btn-group">
              <button class="btn-action btn-primary" style="justify-content: center; padding: 12px; font-size: 14.5px;" onclick="copyBillSummary()">
                📋 复制项目交付清单与报价给客户
              </button>
              <button class="btn-action" style="justify-content: center; padding: 10px; font-size: 13.5px;" onclick="window.print()">
                🖨️ 导出官方 PDF 报价单
              </button>
            </div>
          </div>
        </div>
      `;

      document.getElementById('docViewer').innerHTML = html;
    }}

    function toggleState(key) {{
      state[key] = !state[key];
      renderCalculatorUI();
    }}

    function changeSkuQty(delta) {{
      state.singleSkuQty = Math.max(0, state.singleSkuQty + delta);
      renderCalculatorUI();
    }}

    function changeTtMotionQty(delta) {{
      state.addonTiktokMotionQty = Math.max(0, state.addonTiktokMotionQty + delta);
      renderCalculatorUI();
    }}

    function setMonthlyTerm(term) {{
      state.monthlyTerm = state.monthlyTerm === term ? 'none' : term;
      renderCalculatorUI();
    }}

    function copyBillSummary() {{
      const symbol = selectedCurr === 'RMB' ? '¥' : '$';
      let text = `【GenSight 官方视觉素材代制作项目报价与交付明细单】\\n`;
      text += `计价币种：${{selectedCurr === 'RMB' ? '人民币 (RMB)' : '美金 (USD)'}}\\n`;
      text += `==================================\\n`;
      
      let total = 0;
      const pTrial = selectedCurr === 'RMB' ? 880 : 150;
      const pSku = selectedCurr === 'RMB' ? 1680 : 280;
      const pMonth = selectedCurr === 'RMB' ? 6800 : 1350;
      const pQuarter = selectedCurr === 'RMB' ? 18800 : 3600;
      const pHalfyear = selectedCurr === 'RMB' ? 33800 : 6500;

      const pAplus = selectedCurr === 'RMB' ? 1200 : 200;
      const pLang = selectedCurr === 'RMB' ? 800 : 130;
      const pTtMotion = selectedCurr === 'RMB' ? 600 : 100;
      const pVi = selectedCurr === 'RMB' ? 1980 : 320;

      if (state.trial) {{
        total += pTrial;
        text += `• 3套高CTR素材体验包: ${{symbol}}${{pTrial.toLocaleString()}}\\n  [确切数量]: 3套KV (含1:1与9:16双尺寸，共6张精修图)\\n  [交付标准]: Howard文案+现存素材CTR诊断报告\\n\\n`;
      }}
      if (state.singleSkuQty > 0) {{
        const sub = state.singleSkuQty * pSku;
        total += sub;
        text += `• 单平台 Listing 开款包 (x${{state.singleSkuQty}} SKU): ${{symbol}}${{sub.toLocaleString()}}\\n  [确切数量]: ${{state.singleSkuQty}}白底主图 + ${{state.singleSkuQty*6}}卖点附图 + ${{state.singleSkuQty}}套Banner/A+ (共${{state.singleSkuQty*8}}件物料)\\n  [交付标准]: 100%白底合规+多语种卖点+欧美Lifestyle模特\\n\\n`;
      }}
      if (state.monthlyTerm === 'month') {{
        total += pMonth;
        text += `• 跨平台素材代制作包 (月付): ${{symbol}}${{pMonth.toLocaleString()}}\\n  [确切数量]: 24件/套核心素材 (12套KV共36张图 + 4套Listing包 + 8组TikTok卡片)\\n  [交付标准]: 周度按时交货+Howard+Brian全包+全店诊断\\n\\n`;
      }}
      if (state.monthlyTerm === 'quarter') {{
        total += pQuarter;
        text += `• 跨平台素材代制作包 (季签折扣): ${{symbol}}${{pQuarter.toLocaleString()}}\\n  [确切数量]: 连续3个月 (每月24件/套核心素材/36张图/8组TikTok卡片)\\n  [交付标准]: 周度交货+月度CTR数据复盘指导下月迭代\\n\\n`;
      }}
      if (state.monthlyTerm === 'halfyear') {{
        total += pHalfyear;
        text += `• 跨平台素材代制作包 (半年签专享): ${{symbol}}${{pHalfyear.toLocaleString()}}\\n  [确切数量]: 连续6个月 (累计交付144+件素材/360+张视觉资产)\\n  [交付标准]: 专享品牌策略倾斜+最高折算优惠\\n\\n`;
      }}

      if (state.addonAplus) {{ total += pAplus; text += `• 亚马逊 A+ 页面高级定制模块: ${{symbol}}${{pAplus.toLocaleString()}}\\n`; }}
      if (state.addonMultiLang) {{ total += pLang; text += `• 西/葡多语种本土化文案包: ${{symbol}}${{pLang.toLocaleString()}}\\n`; }}
      if (state.addonTiktokMotionQty > 0) {{ const sub = state.addonTiktokMotionQty * pTtMotion; total += sub; text += `• TikTok 9:16 微动效广告卡片 x${{state.addonTiktokMotionQty}} 组: ${{symbol}}${{sub.toLocaleString()}}\\n`; }}
      if (state.addonVi) {{ total += pVi; text += `• 品牌 Logo / VI 基础识别规范包: ${{symbol}}${{pVi.toLocaleString()}}\\n`; }}

      text += `==================================\\n`;
      text += `预估项目总额: ${{symbol}}${{total.toLocaleString()}}\\n`;
      text += `商务对接：Howard (GenSight 策略总监)`;

      navigator.clipboard.writeText(text).then(() => {{
        alert("报价与交付明细清单已成功复制到剪贴板！可直接粘贴发送给客户。");
      }});
    }}

    function loadDoc(filename) {{
      if (!docs[filename]) return;
      currentFile = filename;

      document.getElementById('footerNav').style.display = 'flex';

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
      if (currentFile === 'calculator') {{
        copyBillSummary();
        return;
      }}
      const content = docs[currentFile];
      navigator.clipboard.writeText(content).then(() => {{
        alert("Markdown 内容已成功复制到剪贴板！");
      }});
    }}

    // Search functionality
    document.getElementById('searchInput').addEventListener('input', function(e) {{
      const query = e.target.value.toLowerCase().trim();
      if (!query) {{
        if (currentFile === 'calculator') loadCalculator();
        else loadDoc(currentFile);
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

    // Initialize Theme and Default View (Calculator)
    initTheme();
    loadCalculator();
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

print("Generated index.html, opc-dashboard.html and opc-doc/index.html with Visual Portfolio Showcase!")
