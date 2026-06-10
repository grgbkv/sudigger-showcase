# Design decisions & operational war stories

> The engineering substance behind the README claims — written for a technical reader.
> Everything here was learned by *operating* the system in production, not just building it.

## 1. Signal-driven rescoring (the core economic decision)

**Problem:** 4,751 companies × daily LLM re-evaluation = unaffordable and pointless (most
companies change nothing in a given week).

**Decision:** an append-only changelog + signal queue. Daily collectors (news watcher, job
monitor) emit events — funding, hiring, news, partnership. A weekly signal processor re-scores
*only* companies with fresh events, logging every score change with its trigger.

**Result:** ~5% the cost of full-refresh — and the latency record is the same mechanism: a
hiring-surge signal re-scored BirdyChat 22 days before its round was announced. Watching deltas
is simultaneously the cheap design and the early-warning design.

## 2. Verification as a hard gate (anti-hallucination)

- LLM-suggested LinkedIn URLs were ~90% broken (models construct plausible slugs). Fix: a
  verification cascade — (1) HTTP GET + page-content match on the LLM's URL (HEAD is useless;
  LinkedIn returns 200 for any slug), (2) website-domain-derived slug, (3) site-restricted
  search, (4) honest "Not found". Never guess.
- Geo-verification before insert: every candidate's HQ country is verified before it enters a
  country file; rejections are logged with reasoning.
- Score-change explanations ("Why Δ") are LLM-generated with an explicit instruction: if the
  delta is just thinner context at re-evaluation, *say so* — never invent a reason.

## 3. Conservative auto-cleaning (a lesson in restraint)

First version of company-name normalization made 969 automatic changes — and broke real names
("Labs of Latvia" → "Labs of"; "ZEN.COM" → "Zen.Com"). Rewrite: only clean when a legal suffix
is positively detected (s.r.o., Sp. z o.o., ТОО, MChJ…), transliterate only pure-Cyrillic names,
leave everything else untouched. 513 changes, zero false positives. **Aggressive cleaning
optimizes the metric; conservative cleaning preserves trust.**

Cross-script dedup: the dedup key transliterates Cyrillic *before* the alphanumeric strip, so
«Иннотех» and "Innotech" collapse to one company.

## 4. Human data is sacred

The team annotates rows (account owner, comments) directly in the dashboards. Sync scripts read
those columns before every rebuild and write them back after. Any new automated column lands to
the right of the human ones. In months of daily rebuilds, no annotation was ever lost — which is
the difference between "a tool the team tolerates" and "a tool the team trusts."

## 5. Failure modes hit in production (and fixes)

| Failure | Root cause | Fix |
|---|---|---|
| Countries silently vanishing from the daily digest | Dead RSS feeds produce no file → structurally absent, not "0 items" | Health checks + always render every country, quiet days marked explicitly |
| Dashboard tab wiped empty | clear-then-write pattern + API rate-limit (429) between the two calls | Safe-replace: write first, trim tail only on success, retry with backoff — old content survives failures |
| Stale columns beyond column Z | Tail-clear range hardcoded to `A:Z`; the tab had grown to 32 columns | Compute clear-range from actual column count |
| Enrichment overwriting a parallel backfill | Both scripts load CSV at start, write at end — last writer wins | Sequence, never parallelize writers: enrich → dedup → backfill → publish |
| Cron jobs silently doing nothing | System Python lacked third-party deps; scripts "ran" and failed quietly | Pin the interpreter path; pipeline self-reports per-stage status to a daily status file |
| Registry pollution (Uzbekistan) | Foreign companies register in the local IT park purely for tax benefits | LLM-batch foreign-origin classifier with conservative defaults + backup-before-delete |

## 6. Things deliberately NOT built

- **Copilot-agent-as-pipeline** — prototyped, measured, rejected: a chat agent answers from one
  live web pass and won't execute a multi-step pipeline reliably. It's a front door. (Full
  reasoning in [PRD.md](PRD.md).)
- **Aggressive global dedup/cleaning passes** — see §3.
- **Duplicate "shadow rows"** for companies that relocated across tracked countries — one row,
  one owner country, relocation captured as fields. Schema simplicity beat completeness theater.
- **A new UI** — the team already lived in Sheets/Excel; adoption beat elegance.
