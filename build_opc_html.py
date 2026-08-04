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
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>元晟传媒 · OPC 一人企业工作台与出海独立站规划中心</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {{
      --bg-dark: #090d16;
      --bg-card: rgba(21, 30, 47, 0.75);
      --bg-sidebar: #0f1624;
      --border-color: rgba(255, 255, 255, 0.08);
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --accent-cyan: #00f2fe;
      --accent-purple: #8b5cf6;
      --accent-green: #10b981;
      --accent-gold: #f59e0b;
      --sidebar-width: 320px;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background-color: var(--bg-dark);
      color: var(--text-main);
      display: flex;
      height: 100vh;
      overflow: hidden;
      line-height: 1.6;
    }}

    /* Header */
    .top-header {{
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 64px;
      background: rgba(15, 22, 36, 0.85);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      z-index: 100;
    }}

    .logo-group {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .logo-badge {{
      background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
      color: #fff;
      font-weight: 800;
      font-size: 14px;
      padding: 6px 12px;
      border-radius: 8px;
      letter-spacing: 0.5px;
      box-shadow: 0 0 12px rgba(0, 242, 254, 0.3);
    }}

    .title-text {{
      font-size: 17px;
      font-weight: 700;
      background: linear-gradient(90deg, #ffffff, #94a3b8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .search-box {{
      position: relative;
      width: 320px;
    }}

    .search-input {{
      width: 100%;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      border-radius: 20px;
      padding: 8px 16px 8px 36px;
      color: #fff;
      font-size: 13px;
      outline: none;
      transition: all 0.2s;
    }}

    .search-input:focus {{
      border-color: var(--accent-cyan);
      background: rgba(255, 255, 255, 0.08);
      box-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
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
      gap: 12px;
    }}

    .btn-action {{
      background: rgba(255, 255, 255, 0.06);
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
      background: rgba(255, 255, 255, 0.12);
      border-color: var(--accent-cyan);
    }}

    .btn-primary {{
      background: linear-gradient(135deg, #00f2fe, #4facfe);
      border: none;
      color: #000;
      font-weight: 700;
    }}

    .btn-primary:hover {{
      opacity: 0.9;
      box-shadow: 0 0 14px rgba(0, 242, 254, 0.4);
    }}

    /* Main Container */
    .app-container {{
      display: flex;
      width: 100%;
      height: calc(100vh - 64px);
      margin-top: 64px;
    }}

    /* Sidebar */
    .sidebar {{
      width: var(--sidebar-width);
      background: var(--bg-sidebar);
      border-right: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      padding: 16px 12px;
    }}

    .nav-section-title {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--text-muted);
      margin: 16px 8px 8px;
    }}

    .nav-item {{
      display: flex;
      align-items: center;
      padding: 10px 12px;
      border-radius: 10px;
      color: #94a3b8;
      text-decoration: none;
      font-size: 13.5px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
      margin-bottom: 4px;
    }}

    .nav-item:hover {{
      background: rgba(255, 255, 255, 0.05);
      color: #fff;
    }}

    .nav-item.active {{
      background: linear-gradient(135deg, rgba(0, 242, 254, 0.15), rgba(139, 92, 246, 0.15));
      border: 1px solid rgba(0, 242, 254, 0.3);
      color: #ffffff;
      font-weight: 600;
    }}

    .nav-item .icon {{
      margin-right: 10px;
      font-size: 16px;
    }}

    /* Content Area */
    .content-area {{
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      background: var(--bg-dark);
      padding: 24px 36px 60px;
    }}

    /* KPI Summary Cards */
    .kpi-row {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}

    .kpi-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 16px 20px;
      backdrop-filter: blur(10px);
      transition: transform 0.2s, border-color 0.2s;
    }}

    .kpi-card:hover {{
      transform: translateY(-2px);
      border-color: rgba(0, 242, 254, 0.3);
    }}

    .kpi-label {{
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .kpi-value {{
      font-size: 18px;
      font-weight: 700;
      color: #fff;
      margin-top: 4px;
    }}

    .kpi-sub {{
      font-size: 11.5px;
      color: var(--accent-cyan);
      margin-top: 2px;
    }}

    /* Article Card / Markdown Container */
    .doc-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 36px 44px;
      backdrop-filter: blur(12px);
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }}

    /* Markdown Styling */
    .markdown-body {{
      color: #e2e8f0;
      font-size: 15px;
      line-height: 1.75;
    }}

    .markdown-body h1 {{
      font-size: 26px;
      font-weight: 800;
      margin-bottom: 20px;
      padding-bottom: 12px;
      border-bottom: 2px solid rgba(0, 242, 254, 0.2);
      color: #ffffff;
      background: linear-gradient(90deg, #ffffff, #38bdf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .markdown-body h2 {{
      font-size: 20px;
      font-weight: 700;
      margin-top: 32px;
      margin-bottom: 14px;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .markdown-body h3 {{
      font-size: 16px;
      font-weight: 600;
      margin-top: 24px;
      margin-bottom: 10px;
      color: #f1f5f9;
    }}

    .markdown-body p {{
      margin-bottom: 16px;
      color: #cbd5e1;
    }}

    .markdown-body blockquote {{
      border-left: 4px solid var(--accent-cyan);
      background: rgba(0, 242, 254, 0.05);
      padding: 14px 20px;
      border-radius: 0 10px 10px 0;
      margin: 20px 0;
      color: #e0f2fe;
      font-style: normal;
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
      background: rgba(30, 41, 59, 0.9);
      color: var(--accent-cyan);
      font-weight: 700;
      text-align: left;
      padding: 12px 16px;
      border-bottom: 1px solid var(--border-color);
    }}

    .markdown-body td {{
      padding: 12px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      background: rgba(15, 23, 42, 0.4);
      color: #cbd5e1;
    }}

    .markdown-body tr:hover td {{
      background: rgba(255, 255, 255, 0.03);
    }}

    .markdown-body ul, .markdown-body ol {{
      padding-left: 24px;
      margin-bottom: 16px;
    }}

    .markdown-body li {{
      margin-bottom: 6px;
      color: #cbd5e1;
    }}

    .markdown-body code {{
      background: rgba(255, 255, 255, 0.1);
      color: #38bdf8;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: monospace;
      font-size: 13.5px;
    }}

    .markdown-body pre {{
      background: #0f172a;
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 16px;
      overflow-x: auto;
      margin: 20px 0;
    }}

    .markdown-body pre code {{
      background: none;
      padding: 0;
      color: #e2e8f0;
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
        left: -320px;
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
        width: 180px;
      }}
    }}
  </style>
</head>
<body>

  <!-- Top Header -->
  <header class="top-header">
    <div class="logo-group">
      <div class="logo-badge">OPC WORKBENCH</div>
      <div class="title-text">元晟传媒 · OPC 一人企业工作台与出海独立站规划中心</div>
    </div>

    <div class="search-box">
      <span class="search-icon">🔍</span>
      <input type="text" id="searchInput" class="search-input" placeholder="搜索 OPC 文档、SOP、报价或逻辑...">
    </div>

    <div class="header-actions">
      <button class="btn-action" onclick="copyMarkdown()">📋 复制 MD</button>
      <button class="btn-action btn-primary" onclick="window.print()">🖨️ 打印 / 导出 PDF</button>
    </div>
  </header>

  <!-- App Body -->
  <div class="app-container">

    <!-- Sidebar Navigation -->
    <nav class="sidebar" id="sidebar">
      <div class="nav-section-title">🚀 战略总纲 (Master Plan)</div>
      <div class="nav-item active" data-file="05-crossborder-opc-master-plan.md" onclick="loadDoc('05-crossborder-opc-master-plan.md')">
        <span class="icon">🎯</span> 05. OPC 运营方案总纲
      </div>

      <div class="nav-section-title">📋 战略建盘 (OPC Foundation)</div>
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
      <!-- Top KPI Row -->
      <div class="kpi-row">
        <div class="kpi-card">
          <div class="kpi-label">项目阶段</div>
          <div class="kpi-value" style="color: var(--accent-cyan);">出海独立站全案</div>
          <div class="kpi-sub">建盘期完成 ➔ 运营执行阶段</div>
        </div>

        <div class="kpi-card">
          <div class="kpi-label">主力产品定价</div>
          <div class="kpi-value" style="color: var(--accent-gold);">¥19.8K ~ ¥39.8K</div>
          <div class="kpi-sub">Shopify / WP 独立站起飞全案</div>
        </div>

        <div class="kpi-card">
          <div class="kpi-label">长期 LTV 续费</div>
          <div class="kpi-value" style="color: var(--accent-green);">¥5,680 / 月</div>
          <div class="kpi-sub">海外广告视觉与素材代制作包</div>
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

    // Initialize
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

print("Generated index.html, opc-dashboard.html and opc-doc/index.html successfully!")
