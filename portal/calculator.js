/** GenSight pricing calculator — on-demand tool, no persistence */
(() => {
  let mountEl = null;
  let selectedCurr = "RMB";
  let state = {
    trial: false,
    singleSkuQty: 0,
    monthlyTerm: "none",
    addonAplus: false,
    addonMultiLang: false,
    addonTiktokMotionQty: 0,
    addonVi: false,
  };

function renderCalculatorUI() {
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

      if (state.trial) {
        total += pTrial;
        billList.push({
          name: "3套高CTR素材体验包",
          specs: "• 确切数量：3套KV (含1:1与9:16双尺寸，共6张图)\n• 标准：含Howard文案+现有素材点击率诊断",
          price: `${symbol}${pTrial.toLocaleString()}`
        });
      }

      if (state.singleSkuQty > 0) {
        const skuSub = state.singleSkuQty * pSku;
        total += skuSub;
        billList.push({
          name: `单平台 Listing 全套开款包 x${state.singleSkuQty} SKU`,
          specs: `• 确切数量：${state.singleSkuQty}主图 + ${state.singleSkuQty*6}附图 + ${state.singleSkuQty}套Banner/A+ (共${state.singleSkuQty*8}件物料)\n• 标准：100%纯白底合规+多语种卖点+欧美Lifestyle模特`,
          price: `${symbol}${skuSub.toLocaleString()}`
        });
      }

      if (state.monthlyTerm === 'month') {
        total += pMonth;
        billList.push({
          name: "跨平台素材代制作包 (月付方案)",
          specs: "• 确切数量：24件核心素材 (12套跨尺寸广告KV共36张图 + 4套Listing包 + 8组TikTok卡片)\n• 标准：Howard+Brian全包+全店合规诊断",
          price: `${symbol}${pMonth.toLocaleString()}`
        });
      } else if (state.monthlyTerm === 'quarter') {
        total += pQuarter;
        billList.push({
          name: "跨平台素材代制作包 (季签 - 推荐)",
          specs: "• 确切数量：连续3个月 (每月24件核心素材/36张图/8组TikTok卡片)\n• 标准：周度按时交货+月度CTR数据复盘",
          price: `${symbol}${pQuarter.toLocaleString()}`
        });
        discountText = selectedCurr === 'RMB' ? "🎉 已享受季签折扣（立省 ¥1,600）" : "🎉 Quarter Discount Applied (Saved $450 USD)";
      } else if (state.monthlyTerm === 'halfyear') {
        total += pHalfyear;
        billList.push({
          name: "跨平台素材代制作包 (半年签 - 专享)",
          specs: "• 确切数量：连续6个月 (每月24件核心素材，衍生60+张视觉资产)\n• 标准：专享品牌策略倾斜+最高折算优惠",
          price: `${symbol}${pHalfyear.toLocaleString()}`
        });
        discountText = selectedCurr === 'RMB' ? "🎉 已享受半年签专享折扣（立省 ¥7,000）" : "🎉 Half-Year Discount Applied (Saved $1,600 USD)";
      }

      if (state.addonAplus) {
        total += pAplus;
        billList.push({
          name: "亚马逊 A+ 页面高级定制模块",
          specs: "• 确切数量：1套完整 A+ 页面 (970x600/970x300 高保真大厂排版)",
          price: `${symbol}${pAplus.toLocaleString()}`
        });
      }

      if (state.addonMultiLang) {
        total += pLang;
        billList.push({
          name: "西/葡多语种本土化文案包",
          specs: "• 确切数量：匹配美客多拉美美墨巴站点的全套西班牙语/葡萄牙语文案",
          price: `${symbol}${pLang.toLocaleString()}`
        });
      }

      if (state.addonTiktokMotionQty > 0) {
        const ttSub = state.addonTiktokMotionQty * pTtMotion;
        total += ttSub;
        billList.push({
          name: `TikTok 9:16 微动效广告卡片 x${state.addonTiktokMotionQty} 组`,
          specs: `• 确切数量：${state.addonTiktokMotionQty} 组带微动效的 9:16 沉浸式 Hook 封面卡片`,
          price: `${symbol}${ttSub.toLocaleString()}`
        });
      }

      if (state.addonVi) {
        total += pVi;
        billList.push({
          name: "品牌 Logo / VI 基础识别规范包",
          specs: "• 确切数量：1套 Logo 标志 + 标准色/标准字规范 + 基础应用物料",
          price: `${symbol}${pVi.toLocaleString()}`
        });
      }

      const html = `
        <div class="calculator-container">
          <!-- Left Options Panel -->
          <div class="calc-box">
            <div class="calc-title">
              <span>🧮</span> GenSight 智能报价计算器 (精准数量与标准)
            </div>

            <!-- Currency Switcher -->
            <div class="currency-switcher">
              <button class="curr-btn ${selectedCurr === 'RMB' ? 'active' : ''}" onclick="switchCurrency('RMB')">
                🇨🇳 国内商家报价 (RMB / ¥)
              </button>
              <button class="curr-btn ${selectedCurr === 'USD' ? 'active' : ''}" onclick="switchCurrency('USD')">
                🌎 海外客户报价 (USD / $)
              </button>
            </div>

            <!-- Section 1: Standard Packages -->
            <div class="option-group">
              <div class="group-label">一、 基础服务与 Listing 开款套餐 (包含确切数量与标准)</div>

              <!-- Trial Package -->
              <div class="item-card ${state.trial ? 'selected' : ''}" onclick="toggleState('trial')">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">🧪 3套高 CTR 广告素材体验包</div>
                    <div class="item-desc">诊断现有素材痛点 + 交付 3 套高 CTR 广告 KV (签约月包可全额抵扣)。</div>
                  </div>
                  <div class="item-price">${symbol}${pTrial.toLocaleString()}</div>
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
              <div class="item-card ${state.singleSkuQty > 0 ? 'selected' : ''}">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">📦 单平台 Listing 全套开款包 (选定 1 SKU)</div>
                    <div class="item-desc">一站式解决 Amazon / 美客多 / Shopee / SHEIN 上的新品开款或爆款打造。</div>
                    <div class="qty-control" onclick="event.stopPropagation()">
                      <span style="font-size: 13px; font-weight: 600;">SKU 数量：</span>
                      <button class="qty-btn" onclick="changeSkuQty(-1)">-</button>
                      <span class="qty-num">${state.singleSkuQty}</span>
                      <button class="qty-btn" onclick="changeSkuQty(1)">+</button>
                    </div>
                  </div>
                  <div class="item-price">${symbol}${pSku.toLocaleString()} / SKU</div>
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

              <div class="item-card ${state.monthlyTerm === 'month' ? 'selected' : ''}" onclick="setMonthlyTerm('month')">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">🚀 跨平台素材包 (月付方案)</div>
                    <div class="item-desc">满足多平台布局卖家的全套素材按月代制作。</div>
                  </div>
                  <div class="item-price">${symbol}${pMonth.toLocaleString()} / 月</div>
                </div>
                <div class="deliverables-box">
                  <div class="deliverable-title">📋 确切交付物数量与标准：</div>
                  <ul class="deliverable-list">
                    <li>🔹 <strong>每月确切交付数量</strong>：<strong>12套</strong>广告KV(免费延伸1:1/9:16/16:9三尺寸<strong>共36张图</strong>) + <strong>4套</strong>Listing升级包(<strong>折合24+张图</strong>) + <strong>8组</strong>TikTok动态/静态卡片</li>
                    <li>🔹 <strong>执行标准</strong>：每周一/周四分批交付告别拖卡；Howard策略文案+Brian美工AI排版全包；每月赠送全店视觉合规诊断</li>
                  </ul>
                </div>
              </div>

              <div class="item-card ${state.monthlyTerm === 'quarter' ? 'selected' : ''}" onclick="setMonthlyTerm('quarter')">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">🌟 跨平台素材包 (季签 - 推荐)</div>
                    <div class="item-desc">按季度签署，包含全套 24 件/月素材量，资金使用率最高。</div>
                  </div>
                  <div class="item-price">${symbol}${pQuarter.toLocaleString()} / 季</div>
                </div>
                <div class="deliverables-box">
                  <div class="deliverable-title">📋 确切交付物数量与标准：</div>
                  <ul class="deliverable-list">
                    <li>🔹 <strong>确切交付数量</strong>：连续3个月，每月包含24件/套核心素材 (包含108张跨尺寸KV及24组TikTok卡片)</li>
                    <li>🔹 <strong>执行标准</strong>：在月付标准基础上，额外包含每月广告点击率 (CTR) 数据复盘，指导下月素材迭代方向</li>
                  </ul>
                </div>
              </div>

              <div class="item-card ${state.monthlyTerm === 'halfyear' ? 'selected' : ''}" onclick="setMonthlyTerm('halfyear')">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">👑 跨平台素材包 (半年签 - 专享价)</div>
                    <div class="item-desc">长期品牌策略倾斜，享受最高折算优惠。</div>
                  </div>
                  <div class="item-price">${symbol}${pHalfyear.toLocaleString()} / 半年</div>
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

              <div class="item-card ${state.addonAplus ? 'selected' : ''}" onclick="toggleState('addonAplus')">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">✨ 亚马逊 A+ 页面高级定制模块</div>
                    <div class="item-desc">970x600 / 970x300 高保真大厂风格 A+ 模块设计。</div>
                  </div>
                  <div class="item-price">+${symbol}${pAplus.toLocaleString()}</div>
                </div>
              </div>

              <div class="item-card ${state.addonMultiLang ? 'selected' : ''}" onclick="toggleState('addonMultiLang')">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">🌮 西班牙语 / 葡萄牙语多语种本土化文案包</div>
                    <div class="item-desc">专为美客多 (Mercado Libre) 拉美站点定制符合当地语境的文案。</div>
                  </div>
                  <div class="item-price">+${symbol}${pLang.toLocaleString()}</div>
                </div>
              </div>

              <div class="item-card ${state.addonTiktokMotionQty > 0 ? 'selected' : ''}">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">🎵 TikTok 9:16 微动效 / 动态广告封面卡片</div>
                    <div class="item-desc">针对 TikTok 高 CTR 广告设计的带动态微效果封面图。</div>
                    <div class="qty-control" onclick="event.stopPropagation()">
                      <span style="font-size: 13px; font-weight: 600;">组数：</span>
                      <button class="qty-btn" onclick="changeTtMotionQty(-1)">-</button>
                      <span class="qty-num">${state.addonTiktokMotionQty}</span>
                      <button class="qty-btn" onclick="changeTtMotionQty(1)">+</button>
                    </div>
                  </div>
                  <div class="item-price">+${symbol}${pTtMotion.toLocaleString()} / 组</div>
                </div>
              </div>

              <div class="item-card ${state.addonVi ? 'selected' : ''}" onclick="toggleState('addonVi')">
                <div class="item-header-row">
                  <div class="item-info">
                    <div class="item-name">🎨 品牌 Logo / VI 基础识别升级规范包</div>
                    <div class="item-desc">Logo 标志设计 + 标准色/标准字规范 + 基础应用物料。</div>
                  </div>
                  <div class="item-price">+${symbol}${pVi.toLocaleString()}</div>
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
              ${billList.length === 0 ? '<div style="color: var(--text-muted); font-size: 13.5px; padding: 20px 0; text-align: center;">请在左侧勾选您需要的服务项目</div>' : ''}
              ${billList.map(item => `
                <div class="bill-item-block">
                  <div class="bill-item-title-row">
                    <span>${item.name}</span>
                    <span style="color: var(--accent-gold);">${item.price}</span>
                  </div>
                  <div class="bill-item-specs">${item.specs.replace(/\n/g, '<br>')}</div>
                </div>
              `).join('')}
            </div>

            ${discountText ? `<div class="discount-badge">${discountText}</div>` : ''}

            <div class="bill-total-box">
              <div class="bill-total-label">预估项目总额 (Estimated Total)</div>
              <div class="bill-total-amount">${symbol}${total.toLocaleString()} <span style="font-size: 14px; font-weight: 600; color: var(--text-muted);">${unit}</span></div>
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

      mountEl.innerHTML = html;
    }
  function toggleState(key) {
    state[key] = !state[key];
    renderCalculatorUI();
  }
  function changeSkuQty(delta) {
    state.singleSkuQty = Math.max(0, state.singleSkuQty + delta);
    renderCalculatorUI();
  }
  function changeTtMotionQty(delta) {
    state.addonTiktokMotionQty = Math.max(0, state.addonTiktokMotionQty + delta);
    renderCalculatorUI();
  }
  function setMonthlyTerm(term) {
    state.monthlyTerm = state.monthlyTerm === term ? "none" : term;
    renderCalculatorUI();
  }
  function switchCurrency(curr) {
    selectedCurr = curr;
    renderCalculatorUI();
  }
  function copyBillSummary() {
    const symbol = selectedCurr === "RMB" ? "¥" : "$";
    let text = `【GenSight 官方视觉素材代制作项目报价与交付明细单】\n`;
    text += `计价币种：${selectedCurr === "RMB" ? "人民币 (RMB)" : "美金 (USD)"}\n`;
    text += `==================================\n`;
    let total = 0;
    const pTrial = selectedCurr === "RMB" ? 880 : 150;
    const pSku = selectedCurr === "RMB" ? 1680 : 280;
    const pMonth = selectedCurr === "RMB" ? 6800 : 1350;
    const pQuarter = selectedCurr === "RMB" ? 18800 : 3600;
    const pHalfyear = selectedCurr === "RMB" ? 33800 : 6500;
    const pAplus = selectedCurr === "RMB" ? 1200 : 200;
    const pLang = selectedCurr === "RMB" ? 800 : 130;
    const pTtMotion = selectedCurr === "RMB" ? 600 : 100;
    const pVi = selectedCurr === "RMB" ? 1980 : 320;
    if (state.trial) {
      total += pTrial;
      text += `• 3套高CTR素材体验包: ${symbol}${pTrial.toLocaleString()}\n  [确切数量]: 3套KV (含1:1与9:16双尺寸，共6张精修图)\n  [交付标准]: Howard文案+现存素材CTR诊断报告\n\n`;
    }
    if (state.singleSkuQty > 0) {
      const sub = state.singleSkuQty * pSku;
      total += sub;
      text += `• 单平台 Listing 开款包 (x${state.singleSkuQty} SKU): ${symbol}${sub.toLocaleString()}\n  [确切数量]: ${state.singleSkuQty}白底主图 + ${state.singleSkuQty*6}卖点附图 + ${state.singleSkuQty}套Banner/A+ (共${state.singleSkuQty*8}件物料)\n  [交付标准]: 100%白底合规+多语种卖点+欧美Lifestyle模特\n\n`;
    }
    if (state.monthlyTerm === "month") {
      total += pMonth;
      text += `• 跨平台素材代制作包 (月付): ${symbol}${pMonth.toLocaleString()}\n  [确切数量]: 24件/套核心素材 (12套KV共36张图 + 4套Listing包 + 8组TikTok卡片)\n  [交付标准]: 周度按时交货+Howard+Brian全包+全店诊断\n\n`;
    }
    if (state.monthlyTerm === "quarter") {
      total += pQuarter;
      text += `• 跨平台素材代制作包 (季签折扣): ${symbol}${pQuarter.toLocaleString()}\n  [确切数量]: 连续3个月 (每月24件/套核心素材/36张图/8组TikTok卡片)\n  [交付标准]: 周度交货+月度CTR数据复盘指导下月迭代\n\n`;
    }
    if (state.monthlyTerm === "halfyear") {
      total += pHalfyear;
      text += `• 跨平台素材代制作包 (半年签专享): ${symbol}${pHalfyear.toLocaleString()}\n  [确切数量]: 连续6个月 (累计交付144+件素材/360+张视觉资产)\n  [交付标准]: 专享品牌策略倾斜+最高折算优惠\n\n`;
    }
    if (state.addonAplus) { total += pAplus; text += `• 亚马逊 A+ 页面高级定制模块: ${symbol}${pAplus.toLocaleString()}\n`; }
    if (state.addonMultiLang) { total += pLang; text += `• 西/葡多语种本土化文案包: ${symbol}${pLang.toLocaleString()}\n`; }
    if (state.addonTiktokMotionQty > 0) { const sub = state.addonTiktokMotionQty * pTtMotion; total += sub; text += `• TikTok 9:16 微动效广告卡片 x${state.addonTiktokMotionQty} 组: ${symbol}${sub.toLocaleString()}\n`; }
    if (state.addonVi) { total += pVi; text += `• 品牌 Logo / VI 基础识别规范包: ${symbol}${pVi.toLocaleString()}\n`; }
    text += `==================================\n`;
    text += `预估项目总额: ${symbol}${total.toLocaleString()}\n`;
    text += `商务对接：Howard (GenSight 策略总监)`;
    navigator.clipboard.writeText(text).then(() => {
      alert("报价与交付明细清单已成功复制到剪贴板！可直接粘贴发送给客户或写入飞书 T05。");
    });
  }

  function bindGlobals() {
    window.toggleState = toggleState;
    window.changeSkuQty = changeSkuQty;
    window.changeTtMotionQty = changeTtMotionQty;
    window.setMonthlyTerm = setMonthlyTerm;
    window.switchCurrency = switchCurrency;
    window.copyBillSummary = copyBillSummary;
  }

  window.GensightCalculator = {
    mount(el) {
      mountEl = el;
      bindGlobals();
      renderCalculatorUI();
    },
  };
})();
