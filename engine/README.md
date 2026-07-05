# The engine, demonstrated

A clean-room, zero-dependency replay of SUDigger's core mechanism — **signal-driven
rescoring** — on a synthetic 60-day world. The production system is private; this is the
architecture, runnable.

```bash
python3 -m engine            # replay 60 days, watch the catches happen
python3 -m unittest discover engine/tests -v
```

No API keys, no network, no third-party packages. Python 3.9+.

## What the demo shows

A synthetic world of 28 companies across 4 countries emits news, job posts and VC-portfolio
changes over 60 simulated days. The engine runs the same loop as production:

```
collect → signal gate → geo-verify → score → verify facts → state → publish
```

Three things happen that mirror the real system's results:

1. **The catch.** A company shows a hiring surge on day 12 and gets re-scored into the top
   targets — 18 days before its funding round is "announced" in the fixture news feed. A second
   company is caught 9 days early via an investor-portfolio addition. This is the mechanism that
   produced the production system's 4–22-day leads on six real funding rounds
   ([receipts](../docs/CATCHES.md)).
2. **The economics.** The cost meter counts scoring calls actually made vs. the
   re-score-everything-daily counterfactual. Signal-driven processing runs at a few percent of
   the naive cost — same code path that makes it cheap makes it early.
3. **The gates.** A foreign company registered locally is rejected by geo-verification, a
   guessed LinkedIn URL fails verification and is recorded as "Not found" (never guessed), a
   Cyrillic duplicate («Иннотех» vs "Innotech OÜ") collapses via cross-script dedup, and human
   annotation columns survive every dashboard rebuild.

Output lands in `engine/out/`: a mini dashboard (`dashboard.html`), the top-targets CSV, and a
daily digest.

## Module map (mini → production)

| Module | What it does here | Production counterpart |
|---|---|---|
| `fixtures.py` | deterministic synthetic world | 30+ real sources: registries, RSS, job boards, VC portfolios, CORDIS |
| `collect.py` | per-day collectors emit signals | `news_watcher.py`, `job_monitor.py`, `vc_scraper.py`, registry adapters |
| `gate.py` | only fresh-signal companies pass to scoring; cost meter | `signal_processor.py` — the ~5%-of-full-refresh economy |
| `verify.py` | geo gate, URL verification, conservative name cleaning, cross-script dedup | `geo_verifier_v2.py`, `enricher.py` cascade, `name_normalizer.py` |
| `score.py` | 5-indicator partnership-fit scoring (deterministic stand-in for the LLM) | `scorer.py` on Azure OpenAI |
| `state.py` | companies table, append-only changelog, score history | the per-country CSVs + `changelog.csv` + `score_history.csv` |
| `publish.py` | dashboard + top-targets + digest; human columns preserved | `sheets_sync.py`, `excel_sync.py`, `executive_brief.py`, `daily_digest.py` |
| `demo.py` | the 60-day replay loop | cron |

The scoring stub is deliberately deterministic so the demo runs identically everywhere. In
production that box is an LLM call — the harness around it is what this repo demonstrates
([why that's the design](../docs/HARNESS.md)).
