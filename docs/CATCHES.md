# The receipts — funding rounds surfaced before the news

> The core claim of this project is latency: the pipeline surfaces companies *before* the press
> does. This page is the evidence. Every internal timestamp below is from the pipeline's
> append-only changelog; every announcement date links to public coverage. Anyone can check the math.

## Verified catches

| Company | In the pipeline | Round went public | Lead time | How it was caught |
|---|---|---|---|---|
| **BirdyChat** 🇱🇻 | 2026-04-15 | 2026-05-07 — €1.7M round ([Mam Startup](https://mamstartup.pl), [Arctic Startup](https://arcticstartup.com)) | **22 days** | hiring + news signals, rescored before announcement |
| **Kodesage** 🇭🇺 | 2026-05-14, scored 4★ at entry | 2026-06-04 — $6.6M seed led by VentureFriends, angels incl. xAI co-founder Christian Szegedy ([Tech.eu](https://tech.eu/2026/06/04/kodesage-raises-66m-for-ai-powered-legacy-software-modernisation/), [BBJ](https://bbj.hu/business/tech/innovation/hungarian-founded-kodesage-raises-usd-6-6-mln-to-modernize-legacy-enterprise-software/)) | **21 days** | curated-report ingestion flagged it as a top target on prior-round + sector signals |
| **TAPAYA** 🇨🇿 | 2026-04-13 | 2026-04-29 — funding event | **16 days** | discovery + momentum signals pre-announcement |
| **DesignVerse** 🇷🇴 | 2026-05-04, via Underline Ventures portfolio scrape | 2026-05-13 — $5.5M seed; **Underline Ventures participated in the round** ([Tech.eu](https://tech.eu/2026/05/13/romanian-designverse-raises-55m-to-modernise-legacy-enterprise-software/), [Romania Insider](https://www.romania-insider.com/design-verse-seed-round-may-2026)) | **9 days** | the investor-portfolio watcher saw the investor's interest before the press did |
| **Webout** 🇨🇿 | 2026-05-26 — "closed a second round, amount undisclosed" (CzechCrunch); rescored 2★→5★ on 05-28 | 2026-06-03 — €1.65M figure published ([Startitup.sk](https://startitup.sk)) | **8 days** | round detected from local-language press before the amount/details went wide |
| **Edmund** 🇨🇿 | 2026-04-09 | 2026-04-13 — funding event | **4 days** | discovery signal days before announcement |

## In progress (as of 2026-06-10)

- **NCSpeech** 🇰🇿 — tracked since 2026-05-28 as *raising $3M* (GenAI training-data startup,
  source: DigitalBusiness.kz). The round has not been publicly closed. If/when the close is
  announced, the lead time gets measured the same way.

## Why this keeps happening (the mechanism, not luck)

The pipeline watches **leading indicators** — hiring surges, investor-portfolio additions,
local-language press, registry changes — and re-scores a company the day a signal lands.
Funding announcements are *lagging* indicators: by the time a round is press-released, the
hiring, the portfolio listing, or the local coverage usually happened weeks earlier. Global
databases index the announcement; this pipeline indexes what precedes it.

Three of the six catches above (Kodesage, DesignVerse, Webout) happened in the last 30 days —
**during a period when the system ran fully unattended**, with no operator intervention. The
mechanism, not the operator, produces the latency.
