/* main.js – Futuristic Dashboard client-side logic */
"use strict";

// ── Starfield ──────────────────────────────────────────────────────────────
(function initStarfield() {
  const canvas = document.getElementById("starfield");
  const ctx = canvas.getContext("2d");
  let stars = [];
  const STAR_COUNT = 220;

  function resize() {
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  function createStars() {
    stars = Array.from({ length: STAR_COUNT }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 1.4 + 0.2,
      speed: Math.random() * 0.25 + 0.05,
      opacity: Math.random() * 0.7 + 0.3,
    }));
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    stars.forEach((s) => {
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(200, 230, 255, ${s.opacity})`;
      ctx.fill();
      s.y += s.speed;
      if (s.y > canvas.height) {
        s.y = 0;
        s.x = Math.random() * canvas.width;
      }
    });
    requestAnimationFrame(draw);
  }

  window.addEventListener("resize", () => { resize(); createStars(); });
  resize();
  createStars();
  draw();
})();

// ── Clock ──────────────────────────────────────────────────────────────────
(function initClock() {
  const el = document.getElementById("clock");
  function tick() {
    const now = new Date();
    const pad = (n) => String(n).padStart(2, "0");
    el.textContent =
      `${pad(now.getUTCHours())}:${pad(now.getUTCMinutes())}:${pad(now.getUTCSeconds())} UTC`;
  }
  tick();
  setInterval(tick, 1000);
})();

// ── Fetch charts & build grid ──────────────────────────────────────────────
const grid     = document.getElementById("chartGrid");
const lightbox = document.getElementById("lightbox");
const lbClose  = document.getElementById("lbClose");

let allCharts = [];

function buildCard(chart) {
  const card = document.createElement("article");
  card.className = "card";
  card.dataset.cat = chart.category;
  card.innerHTML = `
    <div class="card-header">
      <span class="card-category">${escHtml(chart.category)}</span>
      <div class="card-dots">
        <span class="dot-red"></span>
        <span class="dot-yellow"></span>
        <span class="dot-green"></span>
      </div>
    </div>
    <div class="card-img-wrap">
      <img class="card-img" src="${escHtml(chart.image)}" alt="${escHtml(chart.title)}" loading="lazy" />
    </div>
    <div class="card-footer">
      <p class="card-title">${escHtml(chart.title)}</p>
      <p class="card-subtitle">${escHtml(chart.subtitle)}</p>
      <p class="card-cta">▶ EXPAND CHART</p>
    </div>
  `;
  card.addEventListener("click", () => openLightbox(chart));
  return card;
}

function renderGrid(charts) {
  grid.innerHTML = "";
  charts.forEach((c) => grid.appendChild(buildCard(c)));
}

// ── Filter ─────────────────────────────────────────────────────────────────
document.getElementById("filterBar").addEventListener("click", (e) => {
  const btn = e.target.closest(".filter-btn");
  if (!btn) return;
  document.querySelectorAll(".filter-btn").forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
  const cat = btn.dataset.cat;
  renderGrid(cat === "all" ? allCharts : allCharts.filter((c) => c.category === cat));
});

// ── Lightbox ───────────────────────────────────────────────────────────────
function openLightbox(chart) {
  document.getElementById("lbCategory").textContent = chart.category.toUpperCase();
  document.getElementById("lbTitle").textContent    = chart.title;
  document.getElementById("lbSubtitle").textContent = chart.subtitle;
  const img = document.getElementById("lbImg");
  img.src = chart.image;
  img.alt = chart.title;
  lightbox.classList.add("open");
  document.body.style.overflow = "hidden";
}

function closeLightbox() {
  lightbox.classList.remove("open");
  document.body.style.overflow = "";
}

lbClose.addEventListener("click", closeLightbox);
lightbox.addEventListener("click", (e) => { if (e.target === lightbox) closeLightbox(); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeLightbox(); });

// ── Helper: escape HTML ────────────────────────────────────────────────────
function escHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ── Bootstrap ─────────────────────────────────────────────────────────────
fetch("/api/charts")
  .then((r) => r.json())
  .then((data) => {
    allCharts = data;
    renderGrid(allCharts);
  })
  .catch((err) => {
    console.error("Failed to load chart data:", err);
    grid.innerHTML = `<p style="color:#ff4455;padding:2rem;">Error loading charts. Please refresh.</p>`;
  });
