(() => {
  const sectionMeta = {
    warroom: { label: "作战台", groups: [] },
    playbooks: { label: "执行手册", groups: ["start", "do"] },
    tools: { label: "工具", groups: ["tools"] },
    reference: { label: "战略参考", groups: ["reference"] },
    archive: { label: "归档", groups: ["archive"] },
  };

  const groupLabels = {
    start: "必读",
    do: "执行",
    tools: "工具",
    reference: "战略",
    archive: "归档",
  };

  const quickLinks = [
    { file: "product-spec-and-pricing.md", label: "产品与报价" },
    { file: "visual-portfolio-showcase.md", label: "Demo 与案例" },
    { file: "__calculator__", label: "报价计算器", view: "calculator" },
    { file: "daily-action-and-review-guide.md", label: "每日 SOP" },
    { file: "07-conversion-loop.md", label: "获客 SOP" },
    { file: "00-current-operating-baseline.md", label: "运营基线" },
  ];

  let activeSection = "warroom";
  let activeFile = null;

  function sectionForItem(item) {
    for (const [key, meta] of Object.entries(sectionMeta)) {
      if (meta.groups.includes(item.group)) return key;
    }
    return "playbooks";
  }

  function feishuUrl(tableKey) {
    const base = siteConfig.feishu?.baseUrl || "";
    const table = siteConfig.feishu?.tables?.[tableKey];
    if (!base) return "";
    if (table?.path) return base.replace(/\/$/, "") + "/" + table.path.replace(/^\//, "");
    return base;
  }

  function renderWarroom() {
    const el = document.getElementById("warroom");
    if (!el) return;
    const goal = siteConfig.weeklyGoal || "";
    const owner = siteConfig.weeklyGoalOwner || "";
    const due = siteConfig.weeklyGoalDue || "";
    const baseUrl = siteConfig.feishu?.baseUrl || "";

    const metricsHtml = (siteConfig.metrics || [])
      .map((m) => {
        const url = feishuUrl(m.table);
        const link = url
          ? `<a href="${url}" target="_blank" rel="noreferrer">在飞书填写 →</a>`
          : `<span class="muted-link">链接未配置</span>`;
        return `<article class="metric-card"><div class="label">${m.label}</div><h3>—</h3><p>${m.hint}</p>${link}</article>`;
      })
      .join("");

    const tableButtons = ["dailyTasks", "handoff", "leads", "eveningReview"]
      .map((key) => {
        const t = siteConfig.feishu?.tables?.[key];
        if (!t) return "";
        const url = feishuUrl(key);
        if (!url) return "";
        return `<a class="feishu-btn" href="${url}" target="_blank" rel="noreferrer">${t.code} ${t.label}</a>`;
      })
      .join("");

    const quickHtml = quickLinks
      .map((link) => {
        if (link.view === "calculator") {
          return `<button type="button" class="chip-btn" data-action="calculator">${link.label}</button>`;
        }
        return `<button type="button" class="chip-btn" data-file="${link.file}">${link.label}</button>`;
      })
      .join("");

    el.innerHTML = `
      <section class="warroom">
        <div class="warroom-head">
          <div>
            <p class="eyebrow">今日作战台 · Howard & Brian</p>
            <h1>打开这里，开始今天的工作。</h1>
            <p class="warroom-lead">任务、线索、成交与复盘以飞书为准。需要 SOP 或报价时，用下方按钮或顶部导航打开。</p>
          </div>
          <aside class="goal-card">
            <strong>本周唯一目标</strong>
            <p>${goal}</p>
            <div class="goal-meta">${owner ? `负责人 ${owner}` : ""}${due ? ` · 截止 ${due}` : ""}</div>
          </aside>
        </div>
        <p class="section-label">关键数字 · 在飞书维护</p>
        <div class="metrics-row">${metricsHtml}</div>
        <div class="panels-row">
          <article class="panel">
            <h3>今日 Top 3（飞书 T04）</h3>
            <p>晨会各确认 1–3 项可验收输出。</p>
            <button type="button" class="copy-template-btn" id="copyTop3">复制 Top 3 模板</button>
          </article>
          <article class="panel">
            <h3>当前阻塞（飞书 T01）</h3>
            <p>被阻塞任务必须在晨会读出。</p>
            <button type="button" class="copy-template-btn" id="copyBlocker">复制阻塞项模板</button>
          </article>
        </div>
        <section class="feishu-bar">
          <div>
            <h2>飞书 · 唯一协作数据源</h2>
            <p>本站不保存任务或客户数据。</p>
          </div>
          <div class="feishu-actions">
            ${baseUrl ? `<a class="feishu-btn primary" href="${baseUrl}" target="_blank" rel="noreferrer">打开 Base</a>` : ""}
            ${tableButtons}
          </div>
        </section>
        <section class="playbook-quick">
          <p class="section-label">按需打开 · 常用资料</p>
          <div class="chip-row">${quickHtml}</div>
        </section>
      </section>`;

    document.getElementById("copyTop3")?.addEventListener("click", () => {
      const d = new Date().toISOString().slice(0, 10);
      const text = `【${d} 今日 Top 3 — 写入飞书 T04】\nHoward:\n1.\n2.\n3.\nBrian:\n1.\n2.\n3.\n本周目标：${goal}`;
      navigator.clipboard.writeText(text).then(() => alert("Top 3 模板已复制，请粘贴到飞书。"));
    });
    document.getElementById("copyBlocker")?.addEventListener("click", () => {
      const text = `【阻塞项 — 写入飞书 T01】\n任务：\n阻塞原因：\n解除条件：\n负责人：\n期望解除日：`;
      navigator.clipboard.writeText(text).then(() => alert("阻塞项模板已复制，请粘贴到飞书。"));
    });
    el.querySelectorAll(".chip-btn[data-file]").forEach((btn) =>
      btn.addEventListener("click", () => openDocument(btn.dataset.file))
    );
    el.querySelectorAll('.chip-btn[data-action="calculator"]').forEach((btn) =>
      btn.addEventListener("click", showCalculator)
    );
  }

  function buildTopNav() {
    const topNav = document.getElementById("topNav");
    topNav.innerHTML = "";
    for (const [key, meta] of Object.entries(sectionMeta)) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "top-tab";
      btn.dataset.section = key;
      btn.textContent = meta.label;
      btn.addEventListener("click", () => {
        if (key === "warroom") showWarroom();
        else showSection(key);
      });
      topNav.appendChild(btn);
    }
  }

  function buildSubNav(section) {
    const subNav = document.getElementById("subNav");
    subNav.innerHTML = "";
    if (section === "warroom") {
      subNav.hidden = true;
      return;
    }
    subNav.hidden = false;
    const groups = sectionMeta[section].groups;
    for (const group of groups) {
      manifest
        .filter((item) => item.group === group)
        .forEach((item) => {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "sub-tab";
          btn.dataset.file = item.file;
          btn.textContent = item.title;
          btn.title = item.description;
          if (item.view === "calculator") {
            btn.addEventListener("click", showCalculator);
          } else {
            btn.addEventListener("click", () => openDocument(item.file));
          }
          subNav.appendChild(btn);
        });
    }
  }

  function renderSectionHub(section) {
    const hub = document.getElementById("sectionHub");
    const groups = sectionMeta[section].groups;
    const cards = manifest.filter((item) => groups.includes(item.group));
    hub.innerHTML = `
      <section class="section-hub">
        <h2>${sectionMeta[section].label}</h2>
        <p class="hub-lead">选择要打开的资料，或使用上方标签快速切换。</p>
        <div class="hub-grid">
          ${cards
            .map(
              (item) => `
            <button type="button" class="hub-card" data-file="${item.file}" data-view="${item.view || ""}">
              <span class="hub-card-tag">${groupLabels[item.group] || item.group}</span>
              <strong>${item.title}</strong>
              <span>${item.description}</span>
            </button>`
            )
            .join("")}
        </div>
      </section>`;
    hub.querySelectorAll(".hub-card").forEach((card) => {
      card.addEventListener("click", () => {
        if (card.dataset.view === "calculator") showCalculator();
        else openDocument(card.dataset.file);
      });
    });
  }

  function setActiveNav() {
    document.querySelectorAll(".top-tab").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.section === activeSection);
    });
    document.querySelectorAll(".sub-tab").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.file === activeFile);
    });
  }

  function hideAllViews() {
    document.getElementById("warroom").style.display = "none";
    document.getElementById("sectionHub").hidden = true;
    document.getElementById("docView").style.display = "none";
    document.getElementById("calcView").style.display = "none";
  }

  function showWarroom() {
    activeSection = "warroom";
    activeFile = null;
    hideAllViews();
    document.getElementById("warroom").style.display = "block";
    buildSubNav("warroom");
    setActiveNav();
    window.location.hash = "";
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function showSection(section) {
    activeSection = section;
    activeFile = null;
    hideAllViews();
    buildSubNav(section);
    const hub = document.getElementById("sectionHub");
    hub.hidden = false;
    renderSectionHub(section);
    setActiveNav();
    window.location.hash = section;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function showCalculator() {
    activeSection = "tools";
    activeFile = "__calculator__";
    hideAllViews();
    buildSubNav("tools");
    const calc = document.getElementById("calcView");
    calc.style.display = "block";
    if (window.GensightCalculator) window.GensightCalculator.mount(calc);
    setActiveNav();
    window.location.hash = "calculator";
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function openDocument(file) {
    const item = manifest.find((doc) => doc.file === file);
    if (!item || !docs[file]) return;
    activeSection = sectionForItem(item);
    activeFile = file;
    hideAllViews();
    buildSubNav(activeSection);
    document.getElementById("docView").style.display = "block";
    document.querySelector("#docMeta").textContent = `${item.title} · ${item.description}`;
    document.querySelector("#docBody").innerHTML = marked.parse(docs[file]);
    document.querySelectorAll("[data-doc-link]").forEach((link) =>
      link.addEventListener("click", (event) => {
        event.preventDefault();
        openDocument(link.dataset.docLink);
      })
    );
    setActiveNav();
    window.location.hash = file;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  const renderer = new marked.Renderer();
  renderer.link = (href, title, text) => {
    const filename = decodeURIComponent(String(href || ""))
      .replace(/^\.\//, "")
      .split("#")[0]
      .split("/")
      .pop();
    if (docs[filename]) {
      return `<a href="#${filename}" data-doc-link="${filename}"${title ? ` title="${title}"` : ""}>${text}</a>`;
    }
    return `<a href="${href}" target="_blank" rel="noreferrer"${title ? ` title="${title}"` : ""}>${text}</a>`;
  };
  marked.setOptions({ renderer });

  buildTopNav();
  renderWarroom();

  const hash = decodeURIComponent(window.location.hash.slice(1));
  if (hash === "calculator") showCalculator();
  else if (sectionMeta[hash]) showSection(hash);
  else if (docs[hash]) openDocument(hash);
  else showWarroom();
})();
