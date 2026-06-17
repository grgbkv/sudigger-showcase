# SUDigger as an agent harness

> A harness is the scaffolding around an LLM that turns a text-in/text-out model into a system
> that acts: a loop, tools, context management, state, and control gates. SUDigger was built as
> one before the vocabulary was common. This page redraws it in those terms.
>
> Honest framing up front: SUDigger is **workflow-dominant** — the *code* controls the flow and
> the LLM runs bounded sub-tasks on a short leash. That is a deliberate design choice, and for a
> system whose output must be trusted and cheap, it is the correct one. It is not a fully
> autonomous agent, and does not try to be.

## The diagram

```
  TRIGGER ────────────────────────────────────────────────────────────────────
     cron: daily collectors · weekly re-score / brief / pulse
     │
     ▼
  ┌───────────────────────────────  THE LOOP  ──────────────────────────────┐
  │                                                                          │
  │  1  COLLECT            news_watcher · job_monitor · registry adapters    │
  │     [tools]           ─► RSS · job boards · VC portfolios · EU CORDIS ·  │
  │                          national registries · curated reports          │
  │                                    │                                     │
  │  2  CONTEXT / COST     signal_processor — only companies with a FRESH    │
  │     [gate]             signal enter the expensive step                   │
  │                          └─► this is the ~5%-of-full-refresh economy     │
  │                                    │                                     │
  │  3  GUARDRAIL          geo_verify HQ country ─► reject foreign + log why │
  │     [interception]                 │                                     │
  │                                    ▼                                     │
  │  4  MODEL CALL         LLM: score (5 indicators) · enrich · normalize    │
  │     [swappable]        gpt-5.5 today — the model is ONE box in the loop  │
  │                                    │                                     │
  │  5  GUARDRAIL          HTTP-verify every URL · conservative name-clean   │
  │     [interception]     never emit an unverified fact                     │
  │                                    ▼                                     │
  │  6  STATE / MEMORY     changelog.csv · score_history · {cc}_final.csv    │
  │                        the system's memory across runs                   │
  │                                                                          │
  └────────────────────────────────────┬─────────────────────────────────┘
                                        ▼
  OUTPUT / SURFACES ──────────────────────────────────────────────────────────
     Google Sheets · Excel-on-OneDrive · Top Targets brief · daily digest
     human columns (account owner / comments) preserved across every rebuild
                                        │
  OBSERVABILITY ──────────────────────────────────────────────────────────────
     pipeline_status.txt · pipeline_health.py  (wraps the whole loop)
```

## Mapping to the generic harness vocabulary

| Harness concept | What it's called in the wider ecosystem | SUDigger's implementation |
|---|---|---|
| Trigger | event / schedule / webhook | cron (daily + weekly) |
| Tools | function calling, MCP servers | source adapters: RSS, job boards, registry APIs, VC scrapers, CORDIS |
| Context management | context engineering, retrieval | signal-driven gate — decide what reaches the model, not "send everything" |
| Control / guardrails | interception points (e.g. ACS), policy | geo-verify + HTTP-verify gates: allow / reject / log |
| Model call | the LLM | scoring + enrichment + normalization (swappable model) |
| State / memory | persistence, scratchpad | changelog + score history + per-country CSVs |
| Error / health | observability, evals | pipeline_health + status file + macOS alerts |
| Output | surfaces, sinks | Sheets, Excel, briefs, digests |

## Why "workflow-dominant" is the right call here

Two ways to build this:

- **Agent-dominant** — hand the LLM the goal ("find partnership-ready startups in Poland") and let
  it decide every step. Flexible, impressive in a demo, expensive, and you cannot explain why any
  given row is in the output.
- **Workflow-dominant** (what SUDigger is) — code owns the sequence; the LLM does narrow,
  checkable jobs (score *this* company, extract *this* field, verify *this* URL). Predictable,
  cheap, debuggable, and every row is traceable to a source.

For an output that a non-technical team acts on commercially, trust and cost win. The verification
gates are not training wheels — they are the product.

## Where a managed runtime would slot in

If this engine were hosted on a managed agent runtime (e.g. Azure Foundry Hosted Agents), the
boxes don't change — they get adopted by the platform: the platform's scheduled **triggers**
replace cron, its **per-agent identity + policy layer** formalizes the guardrail gates, and its
**hosted loop** runs the pipeline. Porting SUDigger to the cloud is moving a hand-built harness
onto a managed one, not learning a new paradigm.
