// 从 app.js 提取清单数据，生成飞书多维表格可导入的 CSV
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const appJs = readFileSync(join(here, "..", "app.js"), "utf8");

// 截取 app.js 中的纯数据段（foundationCategories ~ phases 之前）
const start = appJs.indexOf("const foundationCategories");
const end = appJs.indexOf("const phases");
const dataCode = appJs.slice(start, end);
const ctx = {};
new Function("ctx", dataCode + "\nctx.foundationCategories = foundationCategories;\nctx.prepCategories = prepCategories;\nctx.weeklyPlans = weeklyPlans;")(ctx);

const esc = (v) => {
  const s = String(v ?? "");
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
};
const csv = (rows) => rows.map((r) => r.map(esc).join(",")).join("\n") + "\n";
const write = (name, rows) => {
  writeFileSync(join(here, name), "\uFEFF" + csv(rows), "utf8");
  console.log(`${name}: ${rows.length - 1} 行`);
};

// 1. 基础校验清单
write("03-基础校验清单.csv", [
  ["编号", "校验项", "分类", "负责人", "状态"],
  ...ctx.foundationCategories.flatMap((cat) =>
    cat.items.map((it) => [it.id, it.text, cat.title, cat.owner, "未完成"])
  ),
]);

// 2. 启动准备清单
write("02-启动准备清单.csv", [
  ["编号", "任务", "分类", "负责人", "状态"],
  ...ctx.prepCategories.flatMap((cat) =>
    cat.items.map((it) => [it.id, it.text, cat.title, cat.owner, "未完成"])
  ),
]);

// 3. 每日任务（四周计划展开）
const dailyRows = [["日期", "周次", "当日重点", "执行人", "任务", "当日交付物", "状态"]];
for (const week of ctx.weeklyPlans) {
  for (const day of week.days) {
    for (const t of day.huang) dailyRows.push([day.date, `第${week.week}周`, day.focus, "Howard", t, day.deliverable, "未开始"]);
    for (const t of day.li) dailyRows.push([day.date, `第${week.week}周`, day.focus, "Brian", t, day.deliverable, "未开始"]);
  }
}
write("04-每日任务表.csv", dailyRows);

// 4. 任务交接表（空表结构 + 示例）
write("01-任务交接表.csv", [
  ["任务标题", "类型", "状态", "发起人", "接手人", "关联文档", "制作说明", "截止日期"],
  ["示例：企业介绍私聊转发图", "文案定稿 → 视觉制作", "待接手", "Howard", "Brian", "12-company-profile-delivery-standards.md", "按 §1.3 私聊转发版做图，尺寸 1080x1440", "2026-07-08"],
]);

// 5. 询盘记录（空表结构 + 示例）
write("05-询盘记录.csv", [
  ["日期", "来源", "产品", "报价金额", "状态", "备注", "跟进人"],
  ["2026-07-07", "闲鱼", "Logo 体验款", "99", "询盘中", "示例行，导入后删除", "Howard"],
]);

// 6. 晚间复盘（空表结构）
write("06-晚间复盘.csv", [
  ["日期", "填写人", "1-今天有没有形成可发/可转发/可报价的成果", "2-有没有新增案例素材", "3-有没有新增客户反馈或询盘", "4-有没有任务卡在对方手里超过24小时", "5-明天上午第一件必须完成的事"],
]);

console.log("完成");
