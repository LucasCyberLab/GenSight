(() => {
  const groupLabels = {
    start: "今日必读",
    do: "执行时打开",
    tools: "工具",
    reference: "战略参考",
    archive: "历史归档",
  };

  let activeView = "warroom";
  let activeFile = null;

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
    const setupNote = siteConfig.feishu?.setupNote || "配置 portal/site-config.json 后重建站点";

    const metricsHtml = (siteConfig.metrics || [])
      .map((m) => {
        const url = feishuUrl(m.table);
        const link = url
          ? `<a href="${url}" target="_blank" rel="noreferrer">在飞书填写 →</a>`
          : `<button type="button" class="linkish" disabled title="${setupNote}">先配置飞书链接</button>`;
        return `<article class="metric-card"><div class="label">${m.label}</div><h3>—</h3><p>${m.hint}</p>${link}</article>`;
      })
      .join("");

    const tables = siteConfig.feishu?.tables || {};
    const tableButtons = Object.entries(tables)
      .map(([key, t]) => {
        const url = feishuUrl(key);
        const cls = url ? "feishu-btn" : "feishu-btn disabled";
        const href = url || "#";
        return `<a class="${cls}" href="${href}" target="_blank" rel="noreferrer">${t.code} ${t.label}</a>`;
      })
      .join("");

    el.innerHTML = `
      <section class="warroom">
        <div class="warroom-head">
          <div>
            <p class="eyebrow">今日作战台 · Howard & Brian</p>
            <h1>打开这里，开始今天的工作。</h1>
            <p class="warroom-lead">任务、线索、成交与复盘以飞书为准。本站只回答：本周目标是什么、今天优先做什么、需要时去哪查 SOP 与报价。</p>
          </div>
          <aside class="goal-card">
            <strong>本周唯一目标</strong>
            <p>${goal}</p>
            <div class="goal-meta">${owner ? `负责人 ${owner}` : ""}${due ? ` · 截止 ${due}` : ""}</div>
          </aside>
        </div>
        <p class="section-label">关键数字 · 在飞书维护权威状态</p>
        <div class="metrics-row">${metricsHtml}</div>
        <div class="panels-row">
          <article class="panel">
            <h3>今日 Top 3（写在飞书 T04）</h3>
            <p>晨会各确认 1–3 项，必须可验收。复制模板到飞书填写，本站不保存。</p>
            <ol>
              <li>Howard：有效触达 / 询盘跟进 / Brief</li>
              <li>Brian：对比卡 / Listing 交付 / Prompt 沉淀</li>
              <li>共同：阻塞项解除或升级</li>
            </ol>
            <button type="button" class="copy-template-btn" id="copyTop3">复制 Top 3 模板</button>
          </article>
          <article class="panel">
            <h3>当前阻塞（写在飞书 T01）</h3>
            <p>状态 = 被阻塞 的任务必须在晨会读出。复制模板记录原因与解除条件。</p>
            <ol>
              <li>阻塞任务：</li>
              <li>原因：</li>
              <li>解除条件 / 负责人：</li>
            </ol>
            <button type="button" class="copy-template-btn" id="copyBlocker">复制阻塞项模板</button>
          </article>
        </div>
        <section class="feishu-bar">
          <div>
            <h2>飞书多维表格 · 唯一协作数据源</h2>
            <p>GitHub Pages 不保存任务或客户数据。${baseUrl ? "点击下方进入对应表。" : setupNote}</p>
            ${baseUrl ? "" : `<div class="feishu-note">编辑 portal/site-config.json → python3 build_opc_html.py</div>`}
          </div>
          <div class="feishu-actions">
            ${baseUrl ? `<a class="feishu-btn primary" href="${baseUrl}" target="_blank" rel="noreferrer">打开飞书 Base</a>` : ""}
            ${tableButtons}
          </div>
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
  }

  function buildNav() {
    const nav = document.getElementById("nav");
    nav.innerHTML = "";

    const homeBtn = document.createElement("button");
    homeBtn.className = "nav-item nav-home";
    homeBtn.innerHTML = `今日作战台<small>本周目标 · Top 3 · 飞书入口</small>`;
    homeBtn.addEventListener("click", showWarroom);
    nav.appendChild(homeBtn);

    for (const group of ["start", "do", "tools", "reference", "archive"]) {
      nav.insertAdjacentHTML("beforeend", `<div class="nav-group">${groupLabels[group]}</div>`);
      manifest
        .filter((item) => item.group === group)
        .forEach((item) => {
          const button = document.createElement("button");
          button.className = "nav-item";
          button.dataset.file = item.file;
          button.innerHTML = `${item.title}<small>${item.description}</small>`;
          if (item.view === "calculator") {
            button.addEventListener("click", showCalculator);
          } else {
            button.addEventListener("click", () => openDocument(item.file));
          }
          nav.append(button);
        });
    }
  }

  function setActiveNav(fileOrView) {
    document.querySelectorAll(".nav-item").forEach((btn) => {
      const match = fileOrView === "warroom" ? btn.classList.contains("nav-home") : btn.dataset.file === fileOrView;
      btn.classList.toggle("active", match);
    });
  }

  function showWarroom() {
    activeView = "warroom";
    activeFile = null;
    document.getElementById("warroom").style.display = "block";
    document.getElementById("docView").style.display = "none";
    document.getElementById("calcView").style.display = "none";
    setActiveNav("warroom");
    window.location.hash = "";
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function showCalculator() {
    activeView = "calculator";
    activeFile = "__calculator__";
    document.getElementById("warroom").style.display = "none";
    document.getElementById("docView").style.display = "none";
    const calc = document.getElementById("calcView");
    calc.style.display = "block";
    setActiveNav("__calculator__");
    if (window.GensightCalculator) {
      window.GensightCalculator.mount(calc);
    }
    window.location.hash = "calculator";
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function openDocument(file) {
    const item = manifest.find((doc) => doc.file === file);
    if (!item || !docs[file]) return;
    activeView = "doc";
    activeFile = file;
    document.getElementById("warroom").style.display = "none";
    document.getElementById("calcView").style.display = "none";
    document.getElementById("docView").style.display = "block";
    document.querySelector("#docMeta").textContent = `${item.title} · ${item.description}`;
    document.querySelector("#docBody").innerHTML = marked.parse(docs[file]);
    document.querySelectorAll("[data-doc-link]").forEach((link) =>
      link.addEventListener("click", (event) => {
        event.preventDefault();
        openDocument(link.dataset.docLink);
      })
    );
    setActiveNav(file);
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

  buildNav();
  renderWarroom();

  const hash = decodeURIComponent(window.location.hash.slice(1));
  if (hash === "calculator") showCalculator();
  else if (docs[hash]) openDocument(hash);
  else showWarroom();
})();
