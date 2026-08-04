"""Build the read-only GenSight GitHub Pages internal war room portal."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent
DOC_DIR = ROOT / "opc-doc"
PORTAL_DIR = ROOT / "portal"
OUTPUT = ROOT / "index.html"
CONFIG_PATH = PORTAL_DIR / "site-config.json"

DOCUMENTS = [
    {
        "file": "00-current-operating-baseline.md",
        "title": "当前运营基线",
        "group": "start",
        "description": "唯一主线、边界与本周行动规则",
    },
    {
        "file": "feishu-daily-workflow.md",
        "title": "飞书协同 SOP",
        "group": "start",
        "description": "任务字段、表映射与闭环规则",
    },
    {
        "file": "storage-and-pages-boundary.md",
        "title": "存储与发布边界",
        "group": "start",
        "description": "飞书 vs Pages vs 已归档工具",
    },
    {
        "file": "daily-action-and-review-guide.md",
        "title": "每日执行 SOP",
        "group": "do",
        "description": "晨会、触达、交付与晚间四问",
    },
    {
        "file": "product-spec-and-pricing.md",
        "title": "产品与报价",
        "group": "do",
        "description": "跨境视觉标准交付与报价表",
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
        "description": "跨境触达、成交、交付与沉淀",
    },
    {
        "file": "learning-and-sop-roadmap.md",
        "title": "交付协同 SOP",
        "group": "do",
        "description": "两人协作与交付流程",
    },
    {
        "file": "08-asset-ops.md",
        "title": "资产沉淀",
        "group": "do",
        "description": "Prompt/模板/案例库（按需）",
    },
    {
        "file": "09-dashboard-review.md",
        "title": "经营复盘",
        "group": "do",
        "description": "日复盘、周主线与 Stop-loss",
    },
    {
        "file": "__calculator__",
        "title": "智能报价计算器",
        "group": "tools",
        "description": "体验包、Listing、月包与增配项",
        "view": "calculator",
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
    {
        "file": "archive-domestic-plans.md",
        "title": "国内规划归档",
        "group": "archive",
        "description": "00–18 历史文档状态索引",
    },
    {
        "file": "daily-warroom-validation.md",
        "title": "一日工作流演练",
        "group": "archive",
        "description": "晨会→交接→线索→复盘验收清单",
    },
]


def load_documents() -> dict[str, str]:
    docs: dict[str, str] = {}
    for item in DOCUMENTS:
        if item.get("view") == "calculator":
            continue
        path = DOC_DIR / item["file"]
        if not path.exists():
            raise FileNotFoundError(f"Missing required document: {path}")
        docs[item["file"]] = path.read_text(encoding="utf-8")
    return docs


def load_portal_asset(name: str) -> str:
    path = PORTAL_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing portal asset: {path}")
    return path.read_text(encoding="utf-8")


def load_site_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def build_html(docs: dict[str, str], site_config: dict) -> str:
    manifest = json.dumps(DOCUMENTS, ensure_ascii=False)
    contents = json.dumps(docs, ensure_ascii=False)
    config_json = json.dumps(site_config, ensure_ascii=False)
    portal_css = load_portal_asset("portal.css")
    calculator_js = load_portal_asset("calculator.js")
    portal_app_js = load_portal_asset("portal-app.js")

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="GenSight 跨境视觉外包内部作战台">
  <title>GenSight · 今日作战台</title>
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
    .eyebrow {{ margin: 0 0 10px; color: var(--blue); font: 500 12px "DM Mono", monospace; letter-spacing: .08em; text-transform: uppercase; }}
    .section-label {{ margin: 8px 0 14px; color: var(--muted); font: 500 12px "DM Mono", monospace; letter-spacing: .08em; text-transform: uppercase; }}
    .layout {{ display: grid; grid-template-columns: 280px minmax(0, 1fr); align-items: start; gap: 28px; margin-top: 8px; }}
    nav {{ position: sticky; top: 18px; padding: 8px; border: 1px solid var(--line); border-radius: var(--radius); background: var(--surface); max-height: calc(100vh - 36px); overflow: auto; }}
    .nav-group {{ padding: 10px 6px 3px; color: var(--muted); font: 500 11px "DM Mono", monospace; letter-spacing: .08em; text-transform: uppercase; }}
    .nav-item {{ display: block; width: 100%; padding: 10px; border: 0; border-radius: 9px; color: var(--ink); background: transparent; cursor: pointer; text-align: left; }}
    .nav-item:hover, .nav-item.active {{ background: var(--soft-blue); color: var(--blue); }}
    .nav-item small {{ display: block; color: var(--muted); font-size: 11px; }}
    .view {{ min-height: 520px; }}
    #docView {{ display: none; padding: clamp(22px, 4vw, 46px); border: 1px solid var(--line); border-radius: var(--radius); background: var(--surface); box-shadow: var(--shadow); }}
    #calcView {{ display: none; }}
    .doc-meta {{ margin-bottom: 24px; color: var(--muted); font-size: 13px; }}
    .doc-body h1 {{ font-size: 30px; }} .doc-body h2 {{ margin-top: 38px; font-size: 21px; }} .doc-body h3 {{ margin-top: 26px; font-size: 17px; }}
    .doc-body p, .doc-body li {{ color: #374858; }} .doc-body img {{ max-width: 100%; height: auto; border-radius: 12px; }}
    .doc-body table {{ width: 100%; border-collapse: collapse; margin: 22px 0; font-size: 14px; }}
    .doc-body th, .doc-body td {{ padding: 12px; border: 1px solid var(--line); text-align: left; vertical-align: top; }}
    .doc-body th {{ background: #eef3f7; }}
    .doc-body blockquote {{ margin: 20px 0; padding: 12px 18px; border-left: 4px solid var(--blue); background: var(--soft-blue); }}
    .doc-body code {{ padding: 2px 5px; border-radius: 4px; background: #eef3f7; }}
    footer {{ margin-top: 48px; color: var(--muted); font-size: 12px; text-align: center; }}
    @media (max-width: 780px) {{
      .shell {{ padding: 0 16px 42px; }}
      .layout {{ grid-template-columns: 1fr; }}
      nav {{ position: static; max-height: none; }}
      header .status {{ display: none; }}
    }}
{portal_css}
  </style>
</head>
<body>
  <div class="shell">
    <header>
      <div class="brand"><span class="brand-mark">G</span><span>GenSight · 今日作战台</span></div>
      <span class="status">CROSS-BORDER VISUAL OPS · FEISHU SOURCE OF TRUTH</span>
    </header>
    <main>
      <div id="warroom"></div>
      <section class="layout">
        <nav id="nav" aria-label="资料导航"></nav>
        <div class="view">
          <div id="calcView" aria-label="智能报价计算器"></div>
          <article id="docView">
            <div id="docMeta" class="doc-meta"></div>
            <div id="docBody" class="doc-body"></div>
          </article>
        </div>
      </section>
    </main>
    <footer>GenSight 内部作战台 · 协作状态以飞书为准 · 本站只读</footer>
  </div>
  <script>
    const siteConfig = {config_json};
    const manifest = {manifest};
    const docs = {contents};
  </script>
  <script>{calculator_js}</script>
  <script>{portal_app_js}</script>
</body>
</html>
"""


if __name__ == "__main__":
    site_config = load_site_config()
    OUTPUT.write_text(build_html(load_documents(), site_config), encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)}")
