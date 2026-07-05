"""State: the engine's memory across runs.

Mirrors production: per-company table, append-only changelog, score history.
CSV-backed because CSV-as-source-of-truth is a production design decision
(both dashboards rebuild from it; when surfaces disagree, CSV wins).
"""
import csv
import os

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

COMPANY_FIELDS = [
    "company_name", "country", "sector", "website", "linkedin_company",
    "linkedin_note", "score_total", "score_b2b", "score_saas", "score_global",
    "score_fit", "score_perf", "discovered_day", "last_signal_day",
    "geo_verified", "source",
]


class Engine_State:
    def __init__(self):
        self.companies = {}       # dedup_key -> row dict
        self.changelog = []       # append-only event log
        self.score_history = []   # every scoring event

    def log(self, day, event, company, detail):
        self.changelog.append(
            {"day": day, "event": event, "company": company, "detail": detail})

    def record_score(self, day, company, old_total, new_total, trigger):
        self.score_history.append(
            {"day": day, "company": company, "old": old_total,
             "new": new_total, "trigger": trigger})

    # ------------------------------------------------------------- persist
    def save(self):
        os.makedirs(OUT_DIR, exist_ok=True)
        with open(os.path.join(OUT_DIR, "companies.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COMPANY_FIELDS)
            w.writeheader()
            for row in sorted(self.companies.values(),
                              key=lambda r: (-int(r["score_total"]), r["company_name"])):
                w.writerow({k: row.get(k, "") for k in COMPANY_FIELDS})
        for name, rows, fields in [
            ("changelog.csv", self.changelog, ["day", "event", "company", "detail"]),
            ("score_history.csv", self.score_history,
             ["day", "company", "old", "new", "trigger"]),
        ]:
            with open(os.path.join(OUT_DIR, name), "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=fields)
                w.writeheader()
                w.writerows(rows)

    # ------------------------------------------------------------- queries
    def top_targets(self):
        return [r for r in self.companies.values() if int(r["score_total"]) >= 4]

    def first_top_target_day(self, display_name):
        """Day a company first scored >=4 — the timestamp catches are measured by."""
        for ev in self.score_history:
            if ev["company"] == display_name and int(ev["new"]) >= 4:
                return ev["day"]
        return None
