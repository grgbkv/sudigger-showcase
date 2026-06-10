# PRD — Partnership Intelligence for Overlooked Markets

> Product requirements for the productized pipeline ("engine") + agent front-end ("window").
> Design artifact: this is the product the production system points at.

## 1. The job to be done

> "As someone whose job is to *partner with* startups — not invest in them — show me which
> companies in my territory are partnership-ready **right now**, before my competitors and
> before the news cycle, without paying €15k/year or babysitting a research tool."

Incumbents (PitchBook, Dealroom, Crunchbase, Tracxn) score companies through an **investor
lens** — valuations, rounds, cap tables. Partnership/BD teams ask different questions: is this
company a fit for *our* ecosystem? Is it actively scaling? Who do I contact? What changed since
last week? No incumbent answers these natively.

## 2. Users

| Persona | Need | Today's workaround |
|---|---|---|
| **P1 — Corporate BD / partnership manager** (primary — the persona this was built inside) | A ranked, current, *verified* list of partnership-ready startups in their territory + what changed | Manual scouting, intern labor, repurposed investor tools |
| P2 — Ecosystem orgs (accelerators, agencies, startup programs) | Coverage of their own ecosystem that global tools don't have | Self-maintained spreadsheets, annual reports |
| P3 — Investors entering an overlooked region | Earlier signal than global databases provide there | Cross-referencing 3+ databases |

## 3. Positioning

**Signal-native partnership intelligence for the markets global databases skim.**

- vs PitchBook/Dealroom: ~100× cheaper, partnership lens, deeper in CEE/Central Asia
  (e.g. 1,652 verified Uzbek companies — a dataset no commercial tool has).
- vs Harmonic/Specter (signal-native leaders): same method, opposite geography — they are
  global/US-first; this is curated-region-first with honest depth labels.
- vs regional directories: a *pipeline with daily signals and scoring*, not a static list.

The moat is not the code — it's accumulated per-country curation (a 16-file source playbook ×
12 countries × months of signal history) plus a latency record to prove it works.

## 4. Product shape — window + engine

Validated by a Copilot Studio prototype (and, importantly, by its failure mode: a chat agent
cannot *be* the pipeline — it must be a window onto one).

```
   WINDOW — chat agent (Copilot/Teams today; any chat surface later)
   "What's moving in Kazakhstan?" / "Deep-dive on company X"
                 │ tool call
   ENGINE — hosted pipeline (cloud runtime + managed store)
   scrape → verify → enrich → score → store → publish
                 │
   SURFACES — Sheets / Excel / chat answers / weekly brief
```

- **Tier 1 — curated countries:** full depth — verified rows, partnership scores, signal
  history, daily refresh.
- **Tier 2 — any other country:** live web scan, shallower, **explicitly labelled** as such.
  The shallow tier must never impersonate the curated tier — the honesty is the brand.

## 5. Requirements

### Core (proven in production)
- R1. Per-country ingestion with pluggable sources; new country onboarded from a playbook in <1 day.
- R2. Verification gates: geo-verify before insert; HTTP-verify every URL; no unverified fact reaches a surface.
- R3. Signal-driven rescoring only (funding/hiring/news/partnership events) — preserves ~5%-of-refresh economics.
- R4. Partnership-fit scoring as a **pluggable rubric** — any ecosystem loads its own definition of "fit."
- R5. Human annotations survive every automated rebuild. Non-negotiable.
- R6. Daily unattended operation with health self-reporting.

### Productization
- R7. Engine hosted as a service (off the operator's machine) so surfaces are shareable and always-fresh.
- R8. Window agent queries the engine via API/tool call — never via static data uploads.
- R9. Coverage/confidence labels on every answer (tier, freshness, verification status).
- R10. Multi-tenant key on every artifact from day one.
- R11. Usage analytics: queried countries/companies = the demand signal for what to curate next.

### Out of scope (deliberately)
- Investor-grade financials (cap tables, valuations) — different job, ceded to incumbents.
- Faked global depth — the two-tier honesty *is* the product.
- CRM replacement — integrate with surfaces people already use.

## 6. Success metrics

| Metric | Why |
|---|---|
| Latency: days-before-public-news on funding/partnership events | The headline differentiator (record: 22 days) |
| Verified-fact rate on surfaces (target: 100%) | Trust is the product |
| Weekly active use by the team | Adoption, not vanity row counts |
| Cost per tracked company per month | Keeps the economics claim honest |
| New-country onboarding time | Keeps the playbook claim honest |

## 7. Phasing

- **Phase 0 — Package:** docs, demo, this PRD.
- **Phase 1 — Host:** engine to a cloud runtime, files → managed store, API in front (1–2 weeks).
- **Phase 2 — Window:** agent wired to the API with tier labels (1 week; prototype already proved the pattern).
- **Phase 3 — Second tenant:** another team loads its own rubric and territory — the first true
  test of the product hypothesis.

Rule for every phase after 0: **build on pull, not on push** — no phase starts without a named
consumer waiting for its output.
