# SUDigger — startup intelligence that beat PitchBook on latency

> A signal-driven startup-intelligence pipeline I built and operated solo during my internship
> with Microsoft's Enterprise Partner Solutions team in Central and Eastern Europe and Central
> Asia. It discovered, verified, and
> scored partnership-ready startups across 12 countries and published daily dashboards the team
> worked in — flagging funding events up to **22 days before public news**, in a region where
> commercial databases openly acknowledge a coverage gap.
>
> **This is a showcase repository.** The production source and dataset are private (company
> data + credentials); this repo documents the architecture, the design decisions, and the
> results, with synthetic sample data.

**▶ [Interactive walkthrough](https://grgbkv.github.io/sudigger-showcase/)** — the receipts,
the loop, the economics, and a browsable slice of the real dataset, on one page.
**▶ Run the mechanism:** `python3 -m engine` — a clean-room [mini-engine](engine/README.md)
replays the signal-driven loop on a synthetic 60-day world (zero dependencies, zero keys) and
catches a "funding round" 18 days early at 2.8% of the naive scoring cost.

## Results

| Metric | Value |
|---|---|
| Countries in production | 12 — CZ · EE · KZ · LV · LT · PL · RO · SK · HU · MD · UA · UZ |
| Startups tracked | 4,985 active (a further 1,216 low-signal registry rows tiered to a searchable archive, 2026-07-12) |
| Partnership-ready top targets (4–5★) | 1,507 under the universal criteria (2026-07); 982 under the original Microsoft-lens criteria |
| Signal events logged | 9,519 over three months of largely unattended operation |
| Funding rounds caught before public news | **8 verified**: grid.online **−69d** · Oxylabs **−26d** ($130M first-ever round at $3.6B) · BirdyChat **−22d** · Kodesage **−21d** · TAPAYA **−16d** · DesignVerse **−9d** · Webout **−8d** · Edmund **−4d** — [receipts with public links](docs/CATCHES.md) |
| Catches while running fully unattended | 5 of the 8 (Kodesage, DesignVerse, Webout, grid.online, Oxylabs) landed with zero operator intervention |
| Operating cost | tens of $/month — ~5% of a naive full-refresh design |
| Team adoption | daily use by the partner-solutions team; final leads database delivered to the org |

> **July 2026 — the universal pivot.** After the internship the cloud edition dropped the
> single-vendor lens: scoring and briefs now serve **cloud-provider partnership teams (any
> hyperscaler), venture investors, and startup-ecosystem programs**. The live dashboard grew
> daily-digest, weekly-pulse and country-brief views plus 100 evidence-bound partnership
> dossiers; a weekly VC-portfolio monitor watches 95 funds across 10 countries; and the
> full history (news, jobs, digests) is retained instead of rotated.

## Architecture

```
 LAYER 1 — curated ingestion (per country)
   national registries · 5–11 RSS feeds · job boards · 4–15 VC portfolios
   EU CORDIS · curated ecosystem reports
        │
 LAYER 2 — universal processing
   geo-verification → name normalization (Latin+Cyrillic, cross-script dedup)
   → LLM enrichment (every URL HTTP-verified — never guessed)
   → 5-indicator partnership-fit scoring
        │
 LAYER 3 — signal loop                       ◄── the core idea
   daily collectors watch for funding / hiring / news / partnership signals;
   ONLY companies with a fresh signal get re-scored (~5% the cost of refresh,
   and the reason events surface weeks before press coverage)
        │
 LAYER 4 — delivery (daily cron, unattended, self-reporting health)
   Google Sheets + Excel-on-OneDrive dashboards · Top Targets brief
   daily digest · weekly industry pulse
   (human annotation columns survive every automated rebuild)
```

A 16-file playbook makes new-country onboarding a <1-day task — country #12 (Uzbekistan,
1,652 verified companies via a public registry API) took one day.

## The three design decisions that mattered

1. **Signal-driven economics.** Watch *changes*, not snapshots. Re-score a company only when a
   real-world signal lands. This single decision produced both the ~95% cost reduction and the
   latency record — they're the same mechanism.
2. **Verification as a hard gate.** LLM-guessed LinkedIn slugs are ~90% broken, so every URL is
   HTTP-verified with content matching; every company is geo-verified before entering a country
   file; name auto-cleaning runs conservative-only after an aggressive version produced false
   positives. The dashboards earned trust because nothing in them is hallucinated.
3. **Meet users where they live.** The team works in Sheets and Excel — so the product *is*
   Sheets and Excel, rebuilt daily around their manual annotations, not a new tool to adopt.

More depth in [docs/DESIGN_DECISIONS.md](docs/DESIGN_DECISIONS.md), including the failure modes
I hit operating it (dead feeds, API rate limits, race conditions) and how each was fixed.

## The scaling finding: window + engine

To scale beyond 12 countries I prototyped a Microsoft Copilot Studio agent front-end and proved
a non-obvious ceiling: **a chat agent cannot be the pipeline** — it answers from a single live
web pass and degrades to one source under orchestration. The correct architecture is the agent
as a *window* onto a hosted pipeline *engine*, with two honestly-labelled tiers: curated depth
for supported countries, live web scan for the rest. The full product design is in
[docs/PRD.md](docs/PRD.md).

## What's in this repo

- **[index.html](https://grgbkv.github.io/sudigger-showcase/)** — the interactive showcase site (static, no build step)
- **[engine/](engine/README.md)** — the runnable mini-engine: the signal-driven loop, clean-room, on synthetic fixtures, with tests (`python3 -m unittest discover engine/tests`)
- [docs/CATCHES.md](docs/CATCHES.md) — **the receipts**: every early catch with internal timestamps + public news links, independently checkable
- [docs/PRD.md](docs/PRD.md) — the product requirements doc for the productized version
- [docs/DESIGN_DECISIONS.md](docs/DESIGN_DECISIONS.md) — engineering decisions + operational war stories
- [docs/HARNESS.md](docs/HARNESS.md) — SUDigger redrawn as an agent harness (loop / tools / context / control gates)
- [sample_data/real_top_targets_sample.csv](sample_data/real_top_targets_sample.csv) — 21 real 5★ targets across 11 countries (trimmed columns)
- [sample_data/sample_targets.csv](sample_data/sample_targets.csv) — synthetic rows showing the **full** output schema

## What's deliberately NOT here

- The dataset (4,751 companies) — delivered to the team it was built for; not mine to publish
- Production source code and credentials
- Internal dashboard links

*Built with Python · LLM enrichment via Azure OpenAI · gspread / openpyxl / Microsoft Graph ·
cron. Designed, built, and operated by one person — with real credit due to the AI tooling that
shared the work: Claude (Anthropic), Antigravity (Google), and Azure AI Foundry (Microsoft).*
