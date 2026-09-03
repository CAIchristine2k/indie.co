/* ============================================================
   INDIE.CO — Deck slide-by-slide
   Animations · reveals · count-ups · charts
   ============================================================ */

/* ---------- Slide entrance animation (fallback si pas de animation-timeline) ---------- */
(function () {
  const supportsViewTimeline = CSS.supports && CSS.supports('animation-timeline: view()');
  if (supportsViewTimeline) return;
  const slides = document.querySelectorAll('.slide');
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('slide-in');
      }
    });
  }, { threshold: 0.15 });
  slides.forEach((s) => io.observe(s));
})();

/* ---------- Reveal on scroll (fade-up + stagger) ---------- */
(function () {
  // Targets pour reveal simple
  const singleTargets = [
    '.slide-head',
    '.pullquote',
    '.vision-block',
    '.problem-quote',
    '.solution-pillars',
    '.softpower-strip',
    '.softpower-bar',
    '.stat-strip',
    '.techno-layout',
    '.iptv-schema',
    '.ai-illustration',
    '.ott-illustration',
    '.infra-strip',
    '.journey',
    '.structure-grid',
    '.humans-duo',
    '.budget-table',
    '.fin-compensation',
    '.fin-note',
    '.cover-quote',
    '.cover-problem',
    '.cover-contact',
    '.problematique',
    '.merci-contact',
    '.merci-body',
    '.merci-title',
    '.merci-signature',
    '.revenues-duo',
    '.bm-audience-note',
    '.geo',
    '.grid-tv',
    '.legal__timeline',
    '.legal__grid',
    '.gradient-model',
    '.revenue-streams',
    '.bm-duo',
    '.bm-streams',
    '.partners-open',
    '.fin-hero',
    '.fin-mid',
    '.fin-charts',
    '.fin-marketing',
    '.prev-hero',
    '.prev-sources',
    '.fin-empty',
    '.outro-contact',
    '.tv-frame',
    '.cover-hook',
  ];

  // Targets pour stagger sur enfants
  const staggerTargets = [
    '.split-cards',
    '.problem-stats',
    '.problem-grid',
    '.convictions',
    '.duo',
    '.timeline',
    '.levels',
    '.themes',
    '.themes-grid',
    '.catalog-flow',
    '.programs',
    '.shorts',
    '.apps',
    '.prev-timeline',
    '.ecosystem',
    '.partners',
    '.team-cards',
    '.team-editorial',
    '.forecast-grid',
    '.forecast-kpis',
    '.budget__lines',
    '.pipeline',
    '.pipeline-v2',
    '.ai-features',
  ];

  singleTargets.forEach(sel => {
    document.querySelectorAll(sel).forEach(el => el.setAttribute('data-reveal', ''));
  });
  staggerTargets.forEach(sel => {
    document.querySelectorAll(sel).forEach(el => el.setAttribute('data-reveal-stagger', ''));
  });

  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('is-visible');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('[data-reveal], [data-reveal-stagger]').forEach(el => io.observe(el));
})();

/* ---------- Count-up animation on [data-count] elements ---------- */
(function () {
  const formatters = {
    int: (v) => Math.round(v).toString(),
    intFr: (v) => Math.round(v).toLocaleString('fr-FR'),
    decimal: (v) => v.toFixed(1).replace('.', ','),
  };

  function animate(el) {
    const target = parseFloat(el.dataset.count);
    const format = formatters[el.dataset.format] || formatters.int;
    const duration = 1800;
    const start = performance.now();
    el.classList.add('is-counting');

    function frame(now) {
      const p = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = format(target * eased);
      if (p < 1) {
        requestAnimationFrame(frame);
      } else {
        el.textContent = format(target);
        el.classList.remove('is-counting');
      }
    }
    requestAnimationFrame(frame);
  }

  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        animate(e.target);
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('[data-count]').forEach(el => io.observe(el));
})();



const PALETTE = {
  blueKlein: '#0033a0',
  blueKleinDark: '#001f66',
  blueKleinSoft: '#4a6fd8',
  blueDeep: '#0d1220',
  blueRoyal: '#1a2440',
  blueBrand: '#0033a0',
  blueElectric: '#4a6fd8',
  orange: '#e85d2f',
  red: '#b8351a',
  yellow: '#f5a623',
  crimson: '#8f1e13',
  pink: '#d94a6b',
  purple: '#6b2d5c',
  gold: '#d4a441',
};

/* ---------- Progress bar + counter + nav dots ---------- */
(function () {
  const slides = Array.from(document.querySelectorAll('.slide'));
  const total = slides.length;
  const bar = document.getElementById('progressBar');
  const current = document.getElementById('counterCurrent');
  const totalEl = document.getElementById('counterTotal');
  totalEl.textContent = String(total).padStart(2, '0');

  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        const i = slides.indexOf(e.target);
        current.textContent = String(i + 1).padStart(2, '0');
        bar.style.width = `${((i + 1) / total) * 100}%`;
      }
    });
  }, { threshold: 0.55 });

  slides.forEach((s) => io.observe(s));

  // Keyboard navigation
  let cur = 0;
  window.addEventListener('keydown', (e) => {
    const active = slides.findIndex((s) => {
      const r = s.getBoundingClientRect();
      return r.top >= -50 && r.top < window.innerHeight * 0.5;
    });
    if (active >= 0) cur = active;
    if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === ' ') {
      e.preventDefault();
      slides[Math.min(cur + 1, total - 1)].scrollIntoView({ behavior: 'smooth' });
    } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
      e.preventDefault();
      slides[Math.max(cur - 1, 0)].scrollIntoView({ behavior: 'smooth' });
    } else if (e.key === 'Home') {
      e.preventDefault();
      slides[0].scrollIntoView({ behavior: 'smooth' });
    } else if (e.key === 'End') {
      e.preventDefault();
      slides[total - 1].scrollIntoView({ behavior: 'smooth' });
    }
  });
})();

/* ---------- Chart.js defaults ---------- */
if (window.Chart) {
  Chart.defaults.font.family = "'Inter', system-ui, sans-serif";
  Chart.defaults.font.size = 11;
  Chart.defaults.color = 'rgba(10, 8, 16, 0.6)';
  Chart.defaults.borderColor = 'rgba(10, 8, 16, 0.06)';
}

function gradient(ctx, chartArea, from, to) {
  if (!chartArea) return from;
  const g = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
  g.addColorStop(0, from);
  g.addColorStop(1, to);
  return g;
}

/* ---------- BUDGET DONUT (SLIDE 19) — vrais chiffres ---------- */
(function () {
  const el = document.getElementById('chartBudget');
  if (!el) return;
  new Chart(el, {
    type: 'doughnut',
    data: {
      labels: [
        'Droits artistiques',
        'Achat matériel',
        'Location & prestataires',
        'Frais généraux',
        'Frais financiers',
        'Imprévus',
        'Charges sociales & fiscales',
        'Salaires techniciens',
        'Assurances',
        'Salaires société',
        'Transports & régie',
        'Conseils & divers',
      ],
      datasets: [{
        data: [
          32932800,
          21235000,
          12837000,
          7254158,
          3627079,
          3627079,
          1955501,
          1680803,
          1450832,
          1111188,
          490488,
          298800,
        ],
        backgroundColor: [
          '#0a1a3a',
          '#163a7a',
          '#2b7fd9',
          '#f5a623',
          '#e85d2f',
          '#b8351a',
          '#8f1e13',
          '#4a1810',
          '#6b4a1a',
          '#8a6d3a',
          '#a89168',
          '#c9b898',
        ],
        borderWidth: 2,
        borderColor: '#fff',
        hoverOffset: 15,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '62%',
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (c) => `${c.label}: ${(c.parsed / 1e6).toFixed(2)} M€`,
          },
        },
      },
    },
  });
})();

/* ---------- FORECAST CHARTS (SLIDE 20) ---------- */
(function () {
  const el = document.getElementById('chartRampUp');
  if (!el) return;
  new Chart(el, {
    type: 'bar',
    data: {
      labels: ['A1', 'A2', 'A3', 'A4'],
      datasets: [
        {
          label: 'Investissement (M€)',
          data: [88.5, 45, 25, 15],
          backgroundColor: (ctx) => {
            const { chart } = ctx;
            return gradient(chart.ctx, chart.chartArea, PALETTE.blueBrand, PALETTE.blueDeep);
          },
          borderRadius: 6,
          borderSkipped: false,
          barPercentage: 0.55,
        },
        {
          label: 'Compléments (M€)',
          data: [25, 15, 8, 5],
          backgroundColor: (ctx) => {
            const { chart } = ctx;
            return gradient(chart.ctx, chart.chartArea, PALETTE.yellow, PALETTE.red);
          },
          borderRadius: 6,
          borderSkipped: false,
          barPercentage: 0.55,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 10, boxHeight: 10, padding: 10, font: { size: 10 } } },
        tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${c.parsed.y} M€` } },
      },
      scales: {
        x: { grid: { display: false } },
        y: { ticks: { callback: (v) => v + ' M€' }, grid: { color: 'rgba(10,8,16,0.05)' } },
      },
    },
  });
})();

(function () {
  const el = document.getElementById('chartSubs');
  if (!el) return;
  new Chart(el, {
    type: 'line',
    data: {
      labels: ['A1', 'A2', 'A3', 'A4'],
      datasets: [
        {
          label: 'Payants',
          data: [10000, 45000, 120000, 250000],
          borderColor: PALETTE.blueBrand,
          backgroundColor: (ctx) => {
            const { chart } = ctx;
            if (!chart.chartArea) return 'rgba(43,127,217,0.1)';
            const g = chart.ctx.createLinearGradient(0, chart.chartArea.top, 0, chart.chartArea.bottom);
            g.addColorStop(0, 'rgba(43,127,217,0.4)');
            g.addColorStop(1, 'rgba(43,127,217,0)');
            return g;
          },
          fill: true, tension: 0.4, borderWidth: 3,
          pointBackgroundColor: PALETTE.blueDeep, pointBorderColor: '#fff', pointBorderWidth: 2, pointRadius: 4,
        },
        {
          label: 'Gratuits',
          data: [25000, 90000, 220000, 500000],
          borderColor: PALETTE.orange,
          backgroundColor: 'transparent',
          borderDash: [5, 4], tension: 0.4, borderWidth: 2,
          pointBackgroundColor: PALETTE.orange, pointBorderColor: '#fff', pointBorderWidth: 2, pointRadius: 3,
        },
      ],
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 10, boxHeight: 10, padding: 10, font: { size: 10 } } },
        tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${c.parsed.y.toLocaleString('fr-FR')}` } },
      },
      scales: {
        x: { grid: { display: false } },
        y: { ticks: { callback: (v) => (v >= 1000 ? (v / 1000) + 'K' : v) }, grid: { color: 'rgba(10,8,16,0.05)' } },
      },
    },
  });
})();

/* ---------- Prévisionnel CA 5 ans ---------- */
(function () {
  const el = document.getElementById('chartCA6');
  if (!el) return;
  new Chart(el, {
    type: 'line',
    data: {
      labels: ['An 1', 'An 2', 'An 3', 'An 4', 'An 5'],
      datasets: [{
        label: 'Chiffre d\'affaires (M€)',
        data: [0.834, 13.344, 95.91, 500.4, 1251],
        borderColor: PALETTE.orange,
        backgroundColor: (ctx) => {
          const { chart } = ctx;
          if (!chart.chartArea) return 'rgba(232,93,47,0.15)';
          const g = chart.ctx.createLinearGradient(0, chart.chartArea.top, 0, chart.chartArea.bottom);
          g.addColorStop(0, 'rgba(232,93,47,0.45)');
          g.addColorStop(1, 'rgba(232,93,47,0)');
          return g;
        },
        fill: true,
        tension: 0.35,
        borderWidth: 3,
        pointBackgroundColor: PALETTE.crimson,
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (c) => {
              const v = c.parsed.y;
              return v < 1
                ? `${(v * 1000).toFixed(0)} K€`
                : `${v.toFixed(v < 10 ? 2 : 0)} M€`;
            },
          },
        },
      },
      scales: {
        x: { grid: { display: false } },
        y: {
          ticks: {
            callback: (v) => v >= 1 ? v + ' M€' : (v * 1000) + ' K€',
          },
          grid: { color: 'rgba(10,8,16,0.05)' },
        },
      },
    },
  });
})();

(function () {
  const el = document.getElementById('chartRevenue');
  if (!el) return;
  new Chart(el, {
    type: 'doughnut',
    data: {
      labels: ['Abonnements', 'Œuvres d\'art', 'Publicité audiovisuelle', 'Publicité display', 'VOD / SVOD'],
      datasets: [{
        data: [89.9, 7.2, 1.8, 0.6, 0.5],
        backgroundColor: [PALETTE.blueDeep, PALETTE.orange, PALETTE.yellow, PALETTE.blueBrand, PALETTE.crimson],
        borderWidth: 2, borderColor: '#fff', hoverOffset: 10,
      }],
    },
    options: {
      responsive: true, maintainAspectRatio: false, cutout: '58%',
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 10, boxHeight: 10, padding: 8, font: { size: 10 } } },
        tooltip: { callbacks: { label: (c) => `${c.label}: ${c.parsed}%` } },
      },
    },
  });
})();

(function () {
  const el = document.getElementById('chartCac');
  if (!el) return;
  new Chart(el, {
    type: 'bar',
    data: {
      labels: ['CAC', 'ARPU annuel', 'LTV (3 ans)'],
      datasets: [{
        data: [60, 180, 480],
        backgroundColor: [PALETTE.orange, PALETTE.blueBrand, PALETTE.blueDeep],
        borderRadius: 6, borderSkipped: false, barPercentage: 0.55,
      }],
    },
    options: {
      indexAxis: 'y',
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (c) => `${c.parsed.x} €` } },
      },
      scales: {
        x: { ticks: { callback: (v) => v + ' €' }, grid: { color: 'rgba(10,8,16,0.05)' } },
        y: { grid: { display: false } },
      },
    },
  });
})();
