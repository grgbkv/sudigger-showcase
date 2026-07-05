"""Publishing: the surfaces the humans actually use.

Two production rules are demonstrated here:
1. Human annotation columns (ACCOUNT, COMMENTS) are read before every rebuild
   and written back after. In months of daily production rebuilds no
   annotation was ever lost — that rule is why the team trusted the tool.
2. Everything rebuilds from the state CSVs; the dashboard is a projection,
   never a second source of truth.
"""
import csv
import html
import os

from . import fixtures
from .state import OUT_DIR

HUMAN_COLS = ["ACCOUNT", "COMMENTS"]
TOP_TARGETS = os.path.join(OUT_DIR, "top_targets.csv")


def _read_existing_annotations():
    if not os.path.exists(TOP_TARGETS):
        return {}
    with open(TOP_TARGETS, newline="") as f:
        return {row["company_name"]: {c: row.get(c, "") for c in HUMAN_COLS}
                for row in csv.DictReader(f)}


def publish_top_targets(state):
    """Rebuild the top-targets surface, preserving human columns."""
    os.makedirs(OUT_DIR, exist_ok=True)
    annotations = _read_existing_annotations()
    fields = ["company_name", "country", "score_total", "sector", "website",
              "linkedin_company"] + HUMAN_COLS
    rows = sorted(state.top_targets(),
                  key=lambda r: (-int(r["score_total"]), r["company_name"]))
    with open(TOP_TARGETS, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            out = {k: r.get(k, "") for k in fields}
            out.update(annotations.get(r["company_name"], {c: "" for c in HUMAN_COLS}))
            w.writerow(out)
    return len(rows)


def publish_digest(state, day):
    lines = ["SUDigger mini — daily digest, %s (day %d)" % (fixtures.day_to_date(day), day),
             "=" * 56]
    todays = [e for e in state.changelog if e["day"] == day]
    if not todays:
        lines.append("quiet day")
    for e in todays:
        lines.append("[%s] %s — %s" % (e["event"], e["company"], e["detail"]))
    path = os.path.join(OUT_DIR, "digest_day%02d.txt" % day)
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path


def publish_dashboard(state, meter, catches):
    """A single-file HTML projection of the state — the mini version of the
    production Sheets/Excel surfaces."""
    rows = sorted(state.companies.values(),
                  key=lambda r: (-int(r["score_total"]), r["company_name"]))
    stars = lambda n: "★" * int(n) + "☆" * (5 - int(n))
    tr = "".join(
        "<tr><td>%s</td><td>%s</td><td class='score s%s'>%s</td><td>%s</td>"
        "<td>%s</td><td>%s</td></tr>" % (
            html.escape(r["company_name"]), r["country"], r["score_total"],
            stars(r["score_total"]), html.escape(r["sector"]),
            html.escape(r.get("linkedin_company", "")),
            "✓" if r["geo_verified"] == "True" else "✗")
        for r in rows)
    catch_html = "".join(
        "<li><strong>%s</strong> — entered top targets day %d, round announced "
        "day %d → <span class='lead'>%d days early</span></li>"
        % (html.escape(c["company"]), c["flagged_day"], c["announced_day"], c["lead"])
        for c in catches)
    style = """
body{font-family:'Segoe UI',Inter,system-ui,sans-serif;background:#f8fafc;color:#0f172a;
     margin:0;padding:40px;max-width:960px;margin-inline:auto}
h1{font-size:22px} .sub{color:#475569;margin-bottom:24px}
.card{background:#fff;border-radius:16px;box-shadow:0 1px 3px rgba(15,23,42,.08);
      padding:20px 24px;margin-bottom:20px}
table{border-collapse:collapse;width:100%;font-size:14px}
th{text-align:left;color:#475569;font-weight:600;padding:6px 10px;border-bottom:2px solid #e2e8f0}
td{padding:6px 10px;border-bottom:1px solid #f1f5f9}
.score{white-space:nowrap;color:#6366f1}.s5,.s4{font-weight:700}
.lead{color:#4f46e5;font-weight:700}
.meter{font-size:15px}
"""
    doc = ("<!DOCTYPE html><html><head><meta charset=\"utf-8\">"
           "<title>SUDigger mini — dashboard</title><style>" + style + "</style></head><body>"
           "<h1>SUDigger mini — 60-day replay result</h1>"
           "<p class=\"sub\">Synthetic world · deterministic · the mechanism is real, "
           "the companies are not</p>"
           "<div class=\"card\"><strong>Catches</strong><ul>" + catch_html + "</ul></div>"
           "<div class=\"card meter\"><strong>Cost meter</strong><br>"
           "scoring calls made: <strong>" + str(meter.scoring_calls) + "</strong> · "
           "re-score-everything-daily counterfactual: <strong>"
           + str(meter.counterfactual_calls) + "</strong> · ratio: <strong>"
           + ("%.1f" % (meter.ratio * 100)) + "%</strong></div>"
           "<div class=\"card\"><strong>Companies (" + str(len(rows)) + " tracked, "
           + str(len(state.top_targets())) + " top targets)</strong>"
           "<table><tr><th>Company</th><th>Country</th><th>Score</th><th></th>"
           "<th>Sector</th><th>LinkedIn</th><th>Geo</th></tr>" + tr + "</table></div>"
           "</body></html>")
    path = os.path.join(OUT_DIR, "dashboard.html")
    with open(path, "w") as f:
        f.write(doc)
    return path
