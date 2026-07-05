"""Collectors: turn the day's raw source events into typed signals.

Production equivalents: news_watcher.py (RSS + LLM extraction), job_monitor.py
(job-board APIs/HTML), vc_scraper.py (portfolio diffs), registry adapters.
Here the sources are fixture streams; the signal shape is the same.
"""
from . import fixtures


def signals_for_day(day):
    out = []
    for (d, source, sig_type, company_raw, detail) in fixtures.events_for_day(day):
        out.append({
            "day": d,
            "date": fixtures.day_to_date(d),
            "source": source,
            "signal_type": sig_type,
            "company_raw": company_raw,
            "detail": detail,
        })
    return out


def company_record(company_raw):
    for c in fixtures.COMPANIES:
        if c["name_raw"] == company_raw:
            return c
    return None
