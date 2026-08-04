import { StrictMode, useCallback, useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import { motion } from "motion/react";
import Hls from "hls.js";
import "./index.css";

const MUX_PLAYBACK_URL = import.meta.env.VITE_MUX_PLAYBACK_URL || "";

const slides = [
  { id: "intro", image: "/assets/ppt/cover.png", alt: "洞察本源，晟见未来。元晟传媒品牌视觉与广告设计。" },
  { id: "positioning", image: "/assets/ppt/positioning.png", alt: "公司定位：策略引领、专业交付、AI 深度应用。" },
  { id: "services", image: "/assets/ppt/services.png", alt: "全域业务矩阵：品牌识别、广告创意、商业方案、空间效果图、品牌全案。" },
  { id: "process", image: "/assets/ppt/process.png", alt: "合作流程：从需求沟通到方案交付与案例授权。" },
  { id: "close", image: "/assets/ppt/closing.png", alt: "期待与您，共创品牌价值。" },
];

function Arrow() {
  return <span aria-hidden="true" className="arrow" />;
}

function HlsVideo({ poster, label, isActive }) {
  const videoRef = useRef(null);
  const hlsRef = useRef(null);
  const [status, setStatus] = useState(MUX_PLAYBACK_URL ? "loading" : "poster");

  useEffect(() => {
    const video = videoRef.current;
    if (!video || !MUX_PLAYBACK_URL) return undefined;

    if (Hls.isSupported()) {
      const hls = new Hls({ autoStartLoad: true, enableWorker: true, capLevelToPlayerSize: true, maxBufferLength: 30 });
      hlsRef.current = hls;
      hls.loadSource(MUX_PLAYBACK_URL);
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, () => setStatus("ready"));
      hls.on(Hls.Events.ERROR, (_, data) => data?.fatal && setStatus("error"));
    } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
      video.src = MUX_PLAYBACK_URL;
      video.addEventListener("loadedmetadata", () => setStatus("ready"), { once: true });
    } else {
      setStatus("unsupported");
    }

    return () => {
      hlsRef.current?.destroy();
      hlsRef.current = null;
    };
  }, []);

  useEffect(() => {
    const video = videoRef.current;
    if (!video || !MUX_PLAYBACK_URL) return;
    if (isActive) video.play().catch(() => {});
    else video.pause();
  }, [isActive]);

  return (
    <div className="video-lens">
      <video ref={videoRef} className={`video-lens-media ${status === "ready" ? "is-ready" : ""}`} poster={poster} muted playsInline loop preload="auto" aria-label={label} />
      <img className={`video-lens-poster ${status === "ready" ? "is-hidden" : ""}`} src={poster} alt="" />
      <div className="video-lens-shade" />
      <div className="video-lens-meta"><span>{label}</span><span className="video-status"><i className={status === "ready" ? "is-live" : ""} />{status === "ready" ? "LIVE" : "MUX / HLS"}</span></div>
    </div>
  );
}

function SlideShell({ slide, index, activeIndex, children }) {
  const isActive = index === activeIndex;
  return (
    <motion.section
      id={slide.id}
      aria-hidden={!isActive}
      className="absolute inset-0 overflow-hidden bg-[#f5f1e8]"
      animate={{ opacity: isActive ? 1 : 0 }}
      transition={{ duration: 0.35, ease: "easeInOut" }}
      style={{ zIndex: isActive ? 10 : 0, pointerEvents: isActive ? "auto" : "none" }}
    >
      <img className="ppt-canvas" src={slide.image} alt={slide.alt} draggable="false" />
      {children}
    </motion.section>
  );
}

function SlideAction({ children, onClick }) {
  return <button className="slide-action" onClick={onClick}>{children}<Arrow /></button>;
}

function IntroSlide({ activeIndex }) {
  return (
    <SlideShell slide={slides[0]} index={0} activeIndex={activeIndex}>
      <div className="slide-hotspot slide-hotspot-intro">
        <span className="hotspot-kicker">GENSIGHT / 元晟</span>
        <SlideAction onClick={() => window.dispatchEvent(new CustomEvent("deck:next"))}>进入介绍</SlideAction>
      </div>
    </SlideShell>
  );
}

function PositioningSlide({ activeIndex }) {
  return (
    <SlideShell slide={slides[1]} index={1} activeIndex={activeIndex}>
      <div className="slide-hotspot slide-hotspot-positioning">
        <span className="hotspot-kicker">01 / POSITIONING</span>
        <SlideAction onClick={() => window.dispatchEvent(new CustomEvent("deck:next"))}>看服务矩阵</SlideAction>
      </div>
      <HlsVideo poster="/assets/reference/brand-film.png" label="Brand film / 15 sec" isActive={activeIndex === 1} />
    </SlideShell>
  );
}

function ServicesSlide({ activeIndex }) {
  return (
    <SlideShell slide={slides[2]} index={2} activeIndex={activeIndex}>
      <div className="slide-hotspot slide-hotspot-services">
        <span className="hotspot-kicker">02 / BUSINESS SPECTRUM</span>
        <SlideAction onClick={() => window.dispatchEvent(new CustomEvent("deck:next"))}>查看合作流程</SlideAction>
      </div>
    </SlideShell>
  );
}

function ProcessSlide({ activeIndex }) {
  return (
    <SlideShell slide={slides[3]} index={3} activeIndex={activeIndex}>
      <div className="slide-hotspot slide-hotspot-process">
        <span className="hotspot-kicker">03 / HOW WE WORK</span>
        <SlideAction onClick={() => window.dispatchEvent(new CustomEvent("deck:next"))}>联系元晟</SlideAction>
      </div>
    </SlideShell>
  );
}

function CloseSlide({ activeIndex }) {
  return (
    <SlideShell slide={slides[4]} index={4} activeIndex={activeIndex}>
      <div className="slide-hotspot slide-hotspot-close">
        <span className="hotspot-kicker">04 / NEXT MOVE</span>
        <a className="slide-action" href="https://www.gensight.cn" target="_blank" rel="noreferrer">开始沟通<Arrow /></a>
      </div>
    </SlideShell>
  );
}

function DeckNavigation({ activeIndex, setActiveIndex }) {
  return (
    <nav className="ppt-dots-tray" aria-label="幻灯片导航">
      {slides.map((slide, index) => (
        <button
          className={`h-2 transition-all duration-300 ${index === activeIndex ? "w-6 rounded-full bg-white" : "w-2 rounded-full bg-white/40 hover:bg-white/70"}`}
          key={slide.id}
          aria-label={`前往第 ${index + 1} 页`}
          aria-current={index === activeIndex ? "step" : undefined}
          onClick={() => setActiveIndex(index)}
        />
      ))}
    </nav>
  );
}

function App() {
  const [activeIndex, setActiveIndex] = useState(0);
  const next = useCallback(() => setActiveIndex((current) => (current + 1) % slides.length), []);
  const previous = useCallback(() => setActiveIndex((current) => (current - 1 + slides.length) % slides.length), []);

  useEffect(() => {
    const onKeyDown = (event) => {
      if (["ArrowRight", "ArrowDown", " "].includes(event.key)) { event.preventDefault(); next(); }
      if (["ArrowLeft", "ArrowUp"].includes(event.key)) { event.preventDefault(); previous(); }
    };
    const onNext = () => next();
    window.addEventListener("keydown", onKeyDown);
    window.addEventListener("deck:next", onNext);
    return () => { window.removeEventListener("keydown", onKeyDown); window.removeEventListener("deck:next", onNext); };
  }, [next, previous]);

  return (
    <main className="relative min-h-[100dvh] w-full overflow-hidden bg-black font-['Aeonik',sans-serif] text-[#0d2b4d] selection:bg-[#c49a4a] selection:text-white">
      <IntroSlide activeIndex={activeIndex} />
      <PositioningSlide activeIndex={activeIndex} />
      <ServicesSlide activeIndex={activeIndex} />
      <ProcessSlide activeIndex={activeIndex} />
      <CloseSlide activeIndex={activeIndex} />
      <DeckNavigation activeIndex={activeIndex} setActiveIndex={setActiveIndex} />
      <div className="deck-help">ARROWS / SPACE</div>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<StrictMode><App /></StrictMode>);
