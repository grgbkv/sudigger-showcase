"""The synthetic world: 28 companies, 4 countries, 60 days of events.

Everything is deterministic. Names, storylines and dates are invented; the
*shapes* mirror what the production sources emit (registries, news RSS, job
boards, VC portfolios).
"""
import random
from datetime import date, timedelta

DAY_ZERO = date(2026, 4, 1)
DAYS = 60
COUNTRIES = ["CZ", "EE", "PL", "KZ"]


def day_to_date(day):
    return (DAY_ZERO + timedelta(days=day)).isoformat()


# --------------------------------------------------------------------------
# Companies. `attrs` are the ground-truth partnership indicators the scorer
# can see once context is rich enough; `hq_actual` is what geo-verification
# discovers (feed country vs. real HQ).
# name / country / hq_actual / website / sector / attrs(b2b, saas, global, fit, perf)
# --------------------------------------------------------------------------

def _c(name, country, hq, website, sector, b2b, saas, glob, fit, perf, linkedin=None):
    return {
        "name_raw": name, "country": country, "hq_actual": hq,
        "website": website, "sector": sector,
        "attrs": {"b2b": b2b, "saas": saas, "global": glob, "fit": fit, "perf": perf},
        "linkedin_real": linkedin,
    }


COMPANIES = [
    # -- the 18-day catch storyline ------------------------------------------------
    _c("Aurora Robotics s.r.o.", "CZ", "CZ", "aurora-robotics.example", "Robotics / AI",
       "Yes", "Yes", "Yes", "Yes", "Unclear", linkedin="linkedin.example/company/aurora-robotics"),
    # -- the 9-day investor-portfolio catch ----------------------------------------
    _c("Baltic Ledger OÜ", "EE", "EE", "balticledger.example", "Fintech",
       "Yes", "Yes", "Unclear", "Yes", "Unclear", linkedin="linkedin.example/company/baltic-ledger"),
    # -- cross-script duplicate pair (collapses to one row) ------------------------
    _c("Nordik Data OÜ", "EE", "EE", "nordikdata.example", "Data / Analytics",
       "Yes", "Yes", "No", "Unclear", "No"),
    _c("Нордик Дата", "EE", "EE", "nordikdata.example", "Data / Analytics",
       "Yes", "Yes", "No", "Unclear", "No"),
    # -- geo-gate rejection: local branch of a foreign multinational ---------------
    _c("Global Corp Prague s.r.o.", "CZ", "US", "globalcorp.example", "IT Services",
       "Yes", "No", "Yes", "No", "Yes"),
    # -- LinkedIn honesty case: plausible slug, page doesn't exist ------------------
    _c("Vector Analytics Sp. z o.o.", "PL", "PL", "vectoranalytics.example", "SaaS",
       "Yes", "Yes", "Unclear", "Yes", "No"),
    # -- conservative-cleaning cases ------------------------------------------------
    _c("QUANTA.IO", "PL", "PL", "quanta-io.example", "DevTools",
       "Yes", "Yes", "Yes", "Unclear", "No"),
    _c("Datovka a.s.", "CZ", "CZ", "datovka.example", "Govtech",
       "Yes", "Unclear", "No", "No", "No"),
    # -- solid mid-field ------------------------------------------------------------
    _c("Helios Grid s.r.o.", "CZ", "CZ", "heliosgrid.example", "Energy / Climate",
       "Yes", "Unclear", "Yes", "Yes", "Yes", linkedin="linkedin.example/company/helios-grid"),
    _c("Praga Bio s.r.o.", "CZ", "CZ", "pragabio.example", "Biotech",
       "No", "No", "Unclear", "No", "Unclear"),
    _c("Karlin Pay s.r.o.", "CZ", "CZ", "karlinpay.example", "Fintech",
       "Yes", "Yes", "Unclear", "Yes", "Unclear", linkedin="linkedin.example/company/karlin-pay"),
    _c("Moravia Sense s.r.o.", "CZ", "CZ", "moraviasense.example", "IoT",
       "Yes", "No", "No", "Unclear", "No"),
    _c("Bohemia Lex s.r.o.", "CZ", "CZ", "bohemialex.example", "Legaltech",
       "Yes", "Yes", "No", "No", "No"),
    _c("Tallinn Shield OÜ", "EE", "EE", "tallinnshield.example", "Cybersecurity",
       "Yes", "Yes", "Yes", "Yes", "Yes", linkedin="linkedin.example/company/tallinn-shield"),
    _c("Saaremaa Health OÜ", "EE", "EE", "saaremaahealth.example", "Healthtech",
       "No", "Yes", "No", "Unclear", "No"),
    _c("Tartu Vision OÜ", "EE", "EE", "tartuvision.example", "Computer Vision",
       "Yes", "Unclear", "Yes", "Unclear", "No"),
    _c("Narva Logistics OÜ", "EE", "EE", "narvalogistics.example", "Logistics",
       "Yes", "No", "No", "No", "No"),
    _c("Wisla Cloud Sp. z o.o.", "PL", "PL", "wislacloud.example", "Cloud / SaaS",
       "Yes", "Yes", "Yes", "Yes", "Unclear", linkedin="linkedin.example/company/wisla-cloud"),
    _c("Gdansk Marine Sp. z o.o.", "PL", "PL", "gdanskmarine.example", "Maritime",
       "Yes", "No", "Unclear", "No", "No"),
    _c("Krakow Quantum Sp. z o.o.", "PL", "PL", "krakowquantum.example", "Deeptech",
       "No", "No", "Yes", "Unclear", "No"),
    _c("Silesia Steelworks AI Sp. z o.o.", "PL", "PL", "silesiaai.example", "Industrial AI",
       "Yes", "Unclear", "No", "Yes", "No"),
    _c("Warsaw Ledger Sp. z o.o.", "PL", "PL", "warsawledger.example", "Fintech",
       "Yes", "Yes", "No", "Unclear", "No"),
    _c("Almaty FinServe ТОО", "KZ", "KZ", "almatyfinserve.example", "Fintech",
       "Yes", "Yes", "Unclear", "Yes", "No"),
    _c("Astana AgriTech ЖШС", "KZ", "KZ", "astanaagritech.example", "Agritech",
       "Yes", "No", "No", "Unclear", "No"),
    _c("Steppe Mobility ТОО", "KZ", "KZ", "steppemobility.example", "Mobility",
       "No", "No", "Unclear", "No", "No"),
    _c("Caspian Cloud ТОО", "KZ", "KZ", "caspiancloud.example", "Cloud / SaaS",
       "Yes", "Yes", "No", "Yes", "Unclear", linkedin="linkedin.example/company/caspian-cloud"),
    _c("Oskemen Robotics ТОО", "KZ", "KZ", "oskemenrobotics.example", "Robotics",
       "Yes", "No", "No", "No", "No"),
    _c("Balkhash Analytics ТОО", "KZ", "KZ", "balkhash.example", "Data / Analytics",
       "Yes", "Unclear", "No", "Unclear", "No"),
]

# URL / LinkedIn ground truth for the verification gate: only these resolve.
URL_ALLOWLIST = {c["website"] for c in COMPANIES}
LINKEDIN_ALLOWLIST = {c["linkedin_real"] for c in COMPANIES if c["linkedin_real"]}

# A plausible-but-wrong guess the "LLM" makes for Vector Analytics (production
# finding: ~90% of guessed LinkedIn slugs were broken).
LINKEDIN_GUESSES = {"Vector Analytics Sp. z o.o.": "linkedin.example/company/vector-analytics"}


# --------------------------------------------------------------------------
# Scripted events. (day, source, signal_type, company_raw, detail)
# Discovery events bring companies in; signal events trigger re-scoring.
# --------------------------------------------------------------------------

SCRIPTED_EVENTS = [
    # discoveries, days 1-10, mixed sources
    (1, "registry:CZ", "new_discovery", "Datovka a.s.", "new registration, software"),
    (2, "news:cz-tech-daily", "new_discovery", "Karlin Pay s.r.o.", "profile piece on Prague fintech"),
    (3, "registry:CZ", "new_discovery", "Aurora Robotics s.r.o.", "new registration, robotics"),
    (3, "news:ee-startup-wire", "new_discovery", "Tallinn Shield OÜ", "cyber startup expands SOC team"),
    (4, "vc:sudeten-ventures", "new_discovery", "Helios Grid s.r.o.", "listed in portfolio refresh"),
    (4, "news:pl-founders", "new_discovery", "Wisla Cloud Sp. z o.o.", "cloud migration tooling roundup"),
    (5, "news:ee-startup-wire", "new_discovery", "Baltic Ledger OÜ", "SME payments reconciliation launch"),
    (5, "registry:PL", "new_discovery", "QUANTA.IO", "new registration"),
    (6, "registry:KZ", "new_discovery", "Нордик Дата", "ИТ-компания, аналитика данных"),
    (6, "news:kz-digital", "new_discovery", "Almaty FinServe ТОО", "digital banking rails feature"),
    (7, "news:cz-tech-daily", "new_discovery", "Global Corp Prague s.r.o.", "opens Prague office"),
    (7, "jobs:pl-board", "new_discovery", "Vector Analytics Sp. z o.o.", "3 data roles posted"),
    (8, "vc:nordic-seed-fund", "vc_portfolio_add", "Baltic Ledger OÜ", "appeared in Nordic Seed Fund portfolio"),
    (8, "registry:EE", "new_discovery", "Tartu Vision OÜ", "new registration, CV"),
    (9, "cordis:EU", "new_discovery", "Nordik Data OÜ", "Horizon Europe SME participant"),
    (9, "registry:EE", "new_discovery", "Saaremaa Health OÜ", "new registration"),
    (10, "registry:PL", "new_discovery", "Krakow Quantum Sp. z o.o.", "new registration"),
    (10, "news:kz-digital", "new_discovery", "Caspian Cloud ТОО", "regional cloud provider feature"),

    # the Aurora storyline: hiring surge → rescore into top targets (day 12),
    # partnership (day 20), funding announced day 30 → 18-day lead
    (12, "jobs:cz-board", "hiring_surge", "Aurora Robotics s.r.o.", "5 engineering roles in one week"),
    (20, "news:cz-tech-daily", "partnership", "Aurora Robotics s.r.o.", "pilot with a national logistics operator"),
    (30, "news:cz-tech-daily", "funding_event", "Aurora Robotics s.r.o.", "raises €6M Series A (announcement)"),

    # the Baltic Ledger storyline: investor interest day 8 (above) → round public day 17
    (17, "news:ee-startup-wire", "funding_event", "Baltic Ledger OÜ", "€2.1M seed round announced"),

    # background life for the rest of the world
    (14, "jobs:ee-board", "hiring_surge", "Tallinn Shield OÜ", "4 detection-engineering roles"),
    (18, "news:pl-founders", "general_news", "Wisla Cloud Sp. z o.o.", "SOC 2 certification"),
    (22, "news:kz-digital", "general_news", "Almaty FinServe ТОО", "partnership talks with regional bank"),
    (26, "jobs:pl-board", "hiring_surge", "Wisla Cloud Sp. z o.o.", "6 platform roles posted"),
    (33, "news:ee-startup-wire", "general_news", "Tartu Vision OÜ", "wins municipal CV contract"),
    (38, "vc:sudeten-ventures", "vc_portfolio_add", "Karlin Pay s.r.o.", "new portfolio entry"),
    (41, "news:cz-tech-daily", "general_news", "Helios Grid s.r.o.", "grid-balancing pilot expands"),
    (47, "news:kz-digital", "hiring_surge", "Caspian Cloud ТОО", "opens Astana engineering hub"),
    (52, "news:pl-founders", "partnership", "Vector Analytics Sp. z o.o.", "reseller agreement signed"),
]

# Truth table for the catch report at the end of the replay.
CATCH_TRUTH = {
    "Aurora Robotics": {"announced_day": 30},
    "Baltic Ledger": {"announced_day": 17},
}


def noise_events():
    """Low-value general news spread across the window — the realistic haystack.

    Deterministic (seeded). These mention companies without carrying a scoring
    signal type that changes anything material.
    """
    rng = random.Random(42)
    quiet = [c["name_raw"] for c in COMPANIES
             if c["name_raw"] not in {e[3] for e in SCRIPTED_EVENTS}]
    out = []
    for day in range(11, DAYS, 3):
        company = rng.choice(quiet)
        out.append((day, "news:regional-wire", "general_news", company,
                    "brief mention in a market roundup"))
    return out


def events_for_day(day):
    evs = [e for e in SCRIPTED_EVENTS if e[0] == day]
    evs += [e for e in noise_events() if e[0] == day]
    return evs
