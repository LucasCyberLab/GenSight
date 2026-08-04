const menuToggle = document.querySelector(".menu-toggle");
const siteNav = document.querySelector("#siteNav");

if (menuToggle && siteNav) {
  menuToggle.addEventListener("click", () => {
    const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
    menuToggle.setAttribute("aria-expanded", String(!isOpen));
    siteNav.classList.toggle("is-open", !isOpen);
  });

  siteNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      menuToggle.setAttribute("aria-expanded", "false");
      siteNav.classList.remove("is-open");
    });
  });
}

const revealItems = document.querySelectorAll("[data-reveal]");
if ("IntersectionObserver" in window) {
  const revealObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.14 },
  );
  revealItems.forEach((item) => revealObserver.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}

const copyBriefButton = document.querySelector("#copyBrief");
const copyStatus = document.querySelector("#copyStatus");
const briefTemplate = "项目类型：\n希望解决的问题：\n已有素材：\n期望时间：\n预算范围：\n";

if (copyBriefButton && copyStatus) {
  copyBriefButton.addEventListener("click", async () => {
    try {
      if (navigator.clipboard?.writeText) {
        await Promise.race([
          navigator.clipboard.writeText(briefTemplate),
          new Promise((resolve) => setTimeout(resolve, 500)),
        ]);
      }
      copyStatus.textContent = "需求模板已复制，可以直接补充后发送。";
    } catch {
      copyStatus.textContent = "复制未完成，请手动记录需求类型、问题、素材、时间和预算。";
    }
  });
}
