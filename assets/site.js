/* SUDigger showcase — no frameworks, no build step. */
"use strict";

const FLAGS = { CZ: "🇨🇿", EE: "🇪🇪", KZ: "🇰🇿", LV: "🇱🇻", LT: "🇱🇹", PL: "🇵🇱",
  RO: "🇷🇴", SK: "🇸🇰", HU: "🇭🇺", MD: "🇲🇩", UA: "🇺🇦", UZ: "🇺🇿" };
const stars = n => "★".repeat(+n) + "☆".repeat(5 - +n);

/* ---------------------------------------------------------------- hero counters */
function animateCounters() {
  document.querySelectorAll(".stat-n").forEach(el => {
    const target = +el.dataset.count;
    const dur = 1100, t0 = performance.now();
    const tick = t => {
      const p = Math.min(1, (t - t0) / dur);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))).toLocaleString("en-US");
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });
}

/* ---------------------------------------------------------------- receipts */
function renderReceipts() {
  const maxLead = Math.max(...CATCHES.map(c => c.lead));
  const chart = document.getElementById("lead-chart");
  chart.innerHTML = CATCHES.map(c => `
    <div class="lead-row">
      <span class="lead-name">${c.flag} ${c.company}</span>
      <div class="lead-track"><div class="lead-bar" data-w="${(c.lead / maxLead) * 100}">−${c.lead}d</div></div>
      <span class="lead-days">before news</span>
    </div>`).join("");

  document.getElementById("catch-cards").innerHTML = CATCHES.map(c => `
    <div class="catch">
      <div class="catch-head">${c.flag} <strong>${c.company}</strong>
        <span class="badge ${c.unattended ? "unattended" : ""}">
          ${c.unattended ? "unattended · " : ""}−${c.lead} days</span></div>
      <div class="catch-dates">in the pipeline ${c.inPipeline} → public ${c.public} · ${c.round}</div>
      <div class="catch-how">${c.how}</div>
      ${c.links.length ? `<div class="catch-links">${
        c.links.map(l => `<a href="${l[1]}" target="_blank" rel="noopener">${l[0]} ↗</a>`).join("")
      }</div>` : ""}
    </div>`).join("");

  // animate bars when scrolled into view
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.querySelectorAll(".lead-bar, .bar").forEach(b => {
        b.style.width = b.dataset.w + "%";
      });
      io.unobserve(e.target);
    });
  }, { threshold: 0.3 });
  io.observe(chart);
  document.querySelectorAll(".econ-card").forEach(el => io.observe(el));
}

/* ---------------------------------------------------------------- the loop */
const LOOP = [
  ["Collect", "Daily collectors watch ~30 curated sources per region.",
   "news_watcher (5–11 RSS feeds per country), job_monitor (boards + APIs), vc_scraper " +
   "(4–15 portfolios per country), national registries — including Uzbekistan's IT Park API " +
   "(3,406 residents) — EU CORDIS, curated ecosystem reports."],
  ["Signal gate", "Only companies with a fresh signal reach the expensive step.",
   "The core economic decision. A signal queue (funding · hiring · news · partnership) decides " +
   "who gets processed today. Everyone else keeps yesterday's score. Result: ~5% of the naive " +
   "cost — and the latency edge, because the system watches changes, not snapshots."],
  ["Geo-verify", "Is this company actually from this country?",
   "Deterministic ccTLD/blocklist checks plus an evidence-rich LLM pass with relocation " +
   "handling. Foreign branches registered locally for tax reasons get rejected with logged " +
   "reasoning — 4,266 verified / 139 relocated / 186 dropped in the v2 rollout."],
  ["Score + enrich", "5-indicator partnership fit; the LLM runs on a short leash.",
   "B2B · SaaS · global scaling · ecosystem fit · performance — ternary Yes/No/Unclear, and " +
   "Unclear counts as No: a company only scores on what can be evidenced. Enrichment fills " +
   "sector, one-liner, founder, funding stage."],
  ["Verify facts", "Nothing unverified reaches the dashboard.",
   "Every LinkedIn URL HTTP-verified with content matching (guessed slugs were ~90% broken); " +
   "conservative name cleaning — only when a legal suffix is detected; cross-script dedup " +
   "collapses Cyrillic/Latin duplicates."],
  ["Publish", "The product meets users where they already work.",
   "Google Sheets + Excel-on-OneDrive rebuilt daily from CSV; Top-Targets brief, daily digest, " +
   "weekly industry pulse. Human annotation columns are read before every rebuild and written " +
   "back — in months of operation, no annotation was ever lost."],
];

function renderLoop() {
  const steps = document.getElementById("loop-steps");
  steps.innerHTML = LOOP.map((s, i) =>
    `<div class="loop-step" data-i="${i}"><span class="n">${i + 1}</span><span>${s[0]}</span></div>`
  ).join("");

  let current = 0, timer = null;
  const select = i => {
    current = i;
    steps.querySelectorAll(".loop-step").forEach((el, j) =>
      el.classList.toggle("active", j === i));
    document.getElementById("loop-detail").innerHTML =
      `<h3>${i + 1} · ${LOOP[i][0]}</h3><p>${LOOP[i][1]}</p>
       <div class="prod"><strong>In production:</strong> ${LOOP[i][2]}</div>`;
  };
  const advance = () => select((current + 1) % LOOP.length);
  const restart = () => { clearInterval(timer); timer = setInterval(advance, 4000); };

  steps.addEventListener("click", e => {
    const step = e.target.closest(".loop-step");
    if (!step) return;
    select(+step.dataset.i);
    restart();
  });
  select(0);
  restart();
}

/* ---------------------------------------------------------------- demo table */
const REAL_COLS = [
  ["company_name", "Company"], ["country", ""], ["score_total", "Score"],
  ["sector", "Sector"], ["one_liner", "What they do"],
  ["funding_stage", "Stage"], ["website", "Website"],
];
const SYNTH_COLS = [
  ["company_name", "Company"], ["country", ""], ["score_total", "Score"],
  ["score_b2b", "B2B"], ["score_saas", "SaaS"], ["score_global", "Global"],
  ["score_ecosystem_fit", "Fit"], ["score_performance", "Perf"],
  ["sector", "Sector"], ["one_liner", "What they do"], ["funding_stage", "Stage"],
  ["funding_info", "Funding"], ["employee_count", "Employees"],
  ["founder_ceo_name", "Founder/CEO"], ["last_90d_signals", "Last-90d signals"],
  ["discovered_date", "Discovered"],
];

let demoTab = "real", demoCountry = "ALL";

function renderChips() {
  const rows = demoTab === "real" ? REAL_SAMPLE : SYNTH_SAMPLE;
  const countries = [...new Set(rows.map(r => r.country))].sort();
  document.getElementById("country-chips").innerHTML =
    [`<button class="chip ${demoCountry === "ALL" ? "active" : ""}" data-c="ALL">All</button>`]
      .concat(countries.map(c =>
        `<button class="chip ${demoCountry === c ? "active" : ""}" data-c="${c}">${FLAGS[c] || ""} ${c}</button>`))
      .join("");
}

function renderTable() {
  const cols = demoTab === "real" ? REAL_COLS : SYNTH_COLS;
  let rows = demoTab === "real" ? REAL_SAMPLE : SYNTH_SAMPLE;
  if (demoCountry !== "ALL") rows = rows.filter(r => r.country === demoCountry);

  const head = "<tr>" + cols.map(c => `<th>${c[1]}</th>`).join("") + "</tr>";
  const body = rows.map(r => "<tr>" + cols.map(([key]) => {
    let v = r[key] || "";
    if (key === "company_name") return `<td class="name">${v}</td>`;
    if (key === "country") return `<td>${FLAGS[v] || ""} ${v}</td>`;
    if (key === "score_total") return `<td class="score">${stars(v)}</td>`;
    if (key === "website") {
      const url = v.startsWith("http") ? v : "https://" + v;
      return `<td><a href="${url}" target="_blank" rel="noopener">${v.replace(/^https?:\/\//, "")} ↗</a></td>`;
    }
    if (key === "one_liner" || key === "last_90d_signals")
      return `<td class="dim wide">${v}</td>`;
    if (key === "funding_info" || key === "sector")
      return `<td class="dim">${v}</td>`;
    return `<td>${v}</td>`;
  }).join("") + "</tr>").join("");

  document.getElementById("demo-table").innerHTML = head + body;
  document.getElementById("demo-foot").textContent = demoTab === "real"
    ? `${rows.length} of 21 rows shown — real 5★ targets, trimmed columns. The full database ` +
      `(4,751 companies, 30+ columns) was delivered to the team it was built for.`
    : `${rows.length} synthetic rows — invented companies showing the full production schema, ` +
      `including the five scoring indicators and the signal trail.`;
}

function wireDemo() {
  document.querySelectorAll(".tab").forEach(t => t.addEventListener("click", () => {
    demoTab = t.dataset.tab;
    demoCountry = "ALL";
    document.querySelectorAll(".tab").forEach(x => x.classList.toggle("active", x === t));
    renderChips(); renderTable();
  }));
  document.getElementById("country-chips").addEventListener("click", e => {
    const chip = e.target.closest(".chip");
    if (!chip) return;
    demoCountry = chip.dataset.c;
    renderChips(); renderTable();
  });
  renderChips(); renderTable();
}

/* ---------------------------------------------------------------- terminal replay */
const TERM_LINES = [
  ["", "SUDigger mini engine — replaying 60 synthetic days"],
  ["dim", "=========================================================================="],
  ["", "  day 03  + discovered   Aurora Robotics              2★ (registry:CZ)"],
  ["", "  day 05  + discovered   Baltic Ledger                3★ (news:ee-startup-wire)"],
  ["", "  day 07  ✗ geo-reject   Global Corp Prague           registered locally, HQ in US — foreign branch"],
  ["hl", "  day 08  ▲ re-scored    Baltic Ledger                3★ → 4★ on vc_portfolio_add ← ENTERS TOP TARGETS"],
  ["hl", "  day 12  ▲ re-scored    Aurora Robotics              2★ → 4★ on hiring_surge ← ENTERS TOP TARGETS"],
  ["", "  day 17  ▲ re-scored    Baltic Ledger                4★ → 5★ on funding_event"],
  ["", "  day 20  ▲ re-scored    Aurora Robotics              4★ → 5★ on partnership"],
  ["dim", "  …"],
  ["dim", "=========================================================================="],
  ["", "CATCH REPORT"],
  ["ok", "  Aurora Robotics  entered top targets day 12 · round announced day 30  →  18 DAYS BEFORE THE NEWS"],
  ["ok", "  Baltic Ledger    entered top targets day 08 · round announced day 17  →  9 DAYS BEFORE THE NEWS"],
  ["", ""],
  ["", "COST METER"],
  ["", "  scoring calls made:              31"],
  ["", "  re-score-daily counterfactual: 1114"],
  ["ok", "  signal-driven cost ratio:        2.8%"],
];

function renderTerminal() {
  const body = document.getElementById("term-body");
  let started = false;
  const io = new IntersectionObserver(entries => {
    if (!entries.some(e => e.isIntersecting) || started) return;
    started = true;
    io.disconnect();
    body.textContent = "$ python3 -m engine\n";
    let i = 0;
    const push = () => {
      if (i >= TERM_LINES.length) return;
      const [cls, text] = TERM_LINES[i++];
      const span = document.createElement("span");
      if (cls) span.className = cls;
      span.textContent = text + "\n";
      body.appendChild(span);
      setTimeout(push, i < 3 ? 350 : 140);
    };
    setTimeout(push, 400);
  }, { threshold: 0.35 });
  io.observe(body);
}

/* ---------------------------------------------------------------- boot */
animateCounters();
renderReceipts();
renderLoop();
wireDemo();
renderTerminal();
