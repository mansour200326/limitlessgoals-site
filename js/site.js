/* Limitless Goals: motion + small behaviours. Adapted from the Websmith kit (18 reveal, 19 micro, 11 preview, 07 marquee).
   All content is visible without JS; motion is off under prefers-reduced-motion. */
(() => {
  const d = document, root = d.documentElement;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // header border on scroll
  const top = d.querySelector(".top");
  const onScroll = () => top && top.classList.toggle("is-scrolled", scrollY > 8);
  addEventListener("scroll", onScroll, { passive: true }); onScroll();

  // mobile menu
  const btn = d.querySelector(".menu-btn"), nav = d.getElementById("nav");
  if (btn && nav) {
    btn.addEventListener("click", () => {
      const open = btn.getAttribute("aria-expanded") !== "true";
      btn.setAttribute("aria-expanded", open); nav.classList.toggle("is-open", open);
    });
    d.addEventListener("keydown", (e) => { if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") { btn.click(); btn.focus(); } });
  }

  // split headings into masked lines (re-split on resize)
  const splitLines = (el) => {
    if (!el.dataset.src) el.dataset.src = el.innerHTML;
    el.innerHTML = el.dataset.src;
    const words = [];
    const walk = (node) => {
      [...node.childNodes].forEach((n) => {
        if (n.nodeType === 3) {
          const parts = n.textContent.split(/(\s+)/);
          const frag = d.createDocumentFragment();
          parts.forEach((p) => { if (/^\s+$/.test(p) || !p) frag.append(p); else { const s = d.createElement("span"); s.className = "w"; s.style.display = "inline-block"; s.textContent = p; frag.append(s); words.push(s); } });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && n.tagName !== "BR") walk(n);
      });
    };
    walk(el);
    // group by offsetTop
    const lines = []; let last = null;
    words.forEach((w) => { const t = w.offsetTop; if (last === null || Math.abs(t - last) > 4) { lines.push([]); last = t; } lines[lines.length - 1].push(w); });
    if (lines.length < 1) return;
    // rebuild: keep inline markup simple by wrapping each line's words (wrapping ancestors are cloned per word)
    const out = d.createDocumentFragment();
    lines.forEach((ws, i) => {
      const ln = d.createElement("span"); ln.className = "ln"; const inner = d.createElement("span"); inner.style.setProperty("--i", i); ln.append(inner);
      ws.forEach((w, j) => {
        let node = d.createTextNode(w.textContent), p = w.parentNode;
        while (p && p !== el) { const c = p.cloneNode(false); c.append(node); node = c; p = p.parentNode; }
        inner.append(node); if (j < ws.length - 1) inner.append(" ");
      });
      out.append(ln);
    });
    el.innerHTML = ""; el.append(out);
  };
  const lineEls = [...d.querySelectorAll('[data-reveal="lines"]')];
  const doSplit = () => lineEls.forEach(splitLines);
  if (!reduce) {
    (d.fonts && d.fonts.ready ? d.fonts.ready : Promise.resolve()).then(doSplit);
    let w = innerWidth; addEventListener("resize", () => { if (Math.abs(innerWidth - w) > 40) { w = innerWidth; doSplit(); } });
  }

  // reveal on scroll
  d.querySelectorAll("[data-reveal-stagger]").forEach((p) => [...p.querySelectorAll("[data-reveal]")].forEach((c, i) => c.style.setProperty("--d", i * 90 + "ms")));
  d.querySelectorAll("[data-reveal-delay]").forEach((e) => e.style.setProperty("--d", e.dataset.revealDelay + "ms"));
  const els = d.querySelectorAll("[data-reveal]");
  if (reduce || !("IntersectionObserver" in window)) els.forEach((e) => e.classList.add("in"));
  else {
    // clip-path hides the element from IntersectionObserver, so clip reveals watch their parent instead
    const owner = new Map();
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { (owner.get(e.target) || [e.target]).forEach((t) => t.classList.add("in")); io.unobserve(e.target); } }), { rootMargin: "0px 0px -8% 0px", threshold: 0.01 });
    els.forEach((e) => { const t = e.dataset.reveal === "clip" ? e.parentElement : e; owner.set(t, [...(owner.get(t) || []), e]); io.observe(t); });
  }
  // hero L draws in
  requestAnimationFrame(() => d.querySelectorAll(".hero").forEach((h) => h.classList.add("is-drawn")));

  // floating preview on the commodity index (desktop, fine pointer only)
  const idx = d.querySelector("[data-peek]");
  if (idx && !reduce && matchMedia("(hover:hover) and (pointer:fine)").matches) {
    const peek = d.createElement("div"); peek.className = "peek chamfer"; peek.setAttribute("aria-hidden", "true");
    const imgs = {};
    idx.querySelectorAll("a[data-img]").forEach((a) => { const i = new Image(); i.src = a.dataset.img; i.alt = ""; i.decoding = "async"; peek.append(i); imgs[a.dataset.img] = i; });
    d.body.append(peek);
    let x = 0, y = 0, cx = 0, cy = 0, raf = 0, on = false;
    const loop = () => { cx += (x - cx) * 0.14; cy += (y - cy) * 0.14; peek.style.transform = `translate(${cx + 28}px, ${cy - 180}px) scale(${on ? 1 : 0.9})`; raf = on || Math.abs(x - cx) > 0.5 ? requestAnimationFrame(loop) : 0; };
    idx.querySelectorAll("a").forEach((a) => {
      a.addEventListener("mouseenter", (e) => {
        Object.values(imgs).forEach((i) => i.classList.remove("is-on"));
        if (!a.dataset.img) { on = false; peek.classList.remove("is-on"); return; }
        imgs[a.dataset.img].classList.add("is-on"); on = true; peek.classList.add("is-on");
        if (!cx) { cx = e.clientX; cy = e.clientY; }
        if (!raf) raf = requestAnimationFrame(loop);
      });
      a.addEventListener("mouseleave", () => { on = false; peek.classList.remove("is-on"); });
    });
    addEventListener("mousemove", (e) => { x = e.clientX; y = e.clientY; }, { passive: true });
  }

  // marquee: clone the track once for a seamless loop (clone is hidden from AT and inert)
  d.querySelectorAll(".mq__track").forEach((t) => {
    [...t.children].forEach((c) => { const k = c.cloneNode(true); k.setAttribute("aria-hidden", "true"); t.append(k); });
  });

  // magnetic main buttons (kit 19)
  if (!reduce && matchMedia("(hover:hover) and (pointer:fine)").matches) {
    d.querySelectorAll("[data-magnetic]").forEach((b) => {
      b.addEventListener("mousemove", (e) => { const r = b.getBoundingClientRect(); b.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * 0.22}px, ${(e.clientY - r.top - r.height / 2) * 0.3}px)`; });
      b.addEventListener("mouseleave", () => { b.style.transform = ""; });
    });
  }

  // products sub-nav: mark the section in view
  const sub = d.querySelectorAll(".subnav a");
  if (sub.length && "IntersectionObserver" in window) {
    const map = new Map([...sub].map((a) => [a.hash.slice(1), a]));
    const so = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { sub.forEach((a) => a.classList.remove("is-active")); map.get(e.target.id)?.classList.add("is-active"); } }), { rootMargin: "-40% 0px -55% 0px" });
    map.forEach((_, id) => { const s = d.getElementById(id); s && so.observe(s); });
  }

  // form: stamp consent time
  d.querySelectorAll("form[data-enquiry]").forEach((f) => f.addEventListener("submit", () => { const t = f.querySelector('[name="consent_time"]'); if (t) t.value = new Date().toISOString(); }));
})();
