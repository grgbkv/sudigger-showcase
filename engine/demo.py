"""The 60-day replay: cron, miniaturized.

Each simulated day runs the production loop:
collect → signal gate → geo-verify → score → verify facts → state.
At the end: the catch report and the cost meter — the two numbers the whole
architecture exists to produce.
"""
from . import collect, fixtures, gate, publish, score, verify
from .state import Engine_State


def process_company(state, meter, day, company_raw, sigs, verbose):
    company = collect.company_record(company_raw)
    if company is None:
        return
    key = verify.dedup_key(company_raw)
    display = verify.clean_display_name(company_raw)
    existing = state.companies.get(key)
    trigger = ", ".join(sorted({s["signal_type"] for s in sigs}))

    # ---- new discovery ----------------------------------------------------
    if existing is None:
        ok, reason = verify.geo_verify(company)
        if not ok:
            state.log(day, "geo_reject", display, reason)
            if verbose:
                print("  day %02d  ✗ geo-reject   %-28s %s" % (day, display, reason))
            return
        attrs = score.initial_attrs(company, sigs[0]["source"])
        for s in sigs:
            attrs, _ = score.apply_signal(attrs, s["signal_type"])
        meter.charge()
        linkedin, note = verify.resolve_linkedin(company)
        total = score.total(attrs)
        state.companies[key] = {
            "company_name": display, "country": company["country"],
            "sector": company["sector"], "website": company["website"],
            "linkedin_company": linkedin, "linkedin_note": note,
            "score_total": str(total),
            "score_b2b": attrs["b2b"], "score_saas": attrs["saas"],
            "score_global": attrs["global"], "score_fit": attrs["fit"],
            "score_perf": attrs["perf"],
            "discovered_day": str(day), "last_signal_day": str(day),
            "geo_verified": "True", "source": sigs[0]["source"],
            "_attrs": attrs,
        }
        state.log(day, "new_discovery", display, "%s via %s → scored %d★"
                  % (trigger, sigs[0]["source"], total))
        state.record_score(day, display, "", total, trigger)
        if verbose:
            mark = " ← TOP TARGET" if total >= 4 else ""
            extra = "" if linkedin != "Not found" else "  [linkedin: %s]" % note
            print("  day %02d  + discovered   %-28s %d★ (%s)%s%s"
                  % (day, display, total, sigs[0]["source"], mark, extra))
        return

    # ---- known company, fresh signal → re-score ----------------------------
    attrs = dict(existing["_attrs"])
    changed = False
    for s in sigs:
        attrs, ch = score.apply_signal(attrs, s["signal_type"])
        changed = changed or ch
    old_total = int(existing["score_total"])
    if not changed:
        state.log(day, "signal_noop", display, trigger + " — no indicator change")
        return
    meter.charge()
    new_total = score.total(attrs)
    existing["_attrs"] = attrs
    existing.update({
        "score_total": str(new_total), "last_signal_day": str(day),
        "score_b2b": attrs["b2b"], "score_saas": attrs["saas"],
        "score_global": attrs["global"], "score_fit": attrs["fit"],
        "score_perf": attrs["perf"],
    })
    state.record_score(day, display, old_total, new_total, trigger)
    state.log(day, "rescore", display, "%s: %d★ → %d★" % (trigger, old_total, new_total))
    if verbose and new_total != old_total:
        mark = " ← ENTERS TOP TARGETS" if new_total >= 4 > old_total else ""
        print("  day %02d  ▲ re-scored    %-28s %d★ → %d★ on %s%s"
              % (day, display, old_total, new_total, trigger, mark))


def run(days=fixtures.DAYS, verbose=True):
    state = Engine_State()
    meter = gate.CostMeter()

    for day in range(days):
        signals = collect.signals_for_day(day)
        for company_raw, sigs in gate.select_fresh(signals).items():
            process_company(state, meter, day, company_raw, sigs, verbose)
        # what the naive design would have spent today
        meter.accrue_counterfactual(len(state.companies))

    # ---- catch report -------------------------------------------------------
    catches = []
    for display, truth in fixtures.CATCH_TRUTH.items():
        flagged = state.first_top_target_day(display)
        if flagged is not None and flagged < truth["announced_day"]:
            catches.append({"company": display, "flagged_day": flagged,
                            "announced_day": truth["announced_day"],
                            "lead": truth["announced_day"] - flagged})
    return state, meter, catches


def main():
    print("SUDigger mini engine — replaying %d synthetic days" % fixtures.DAYS)
    print("=" * 74)
    state, meter, catches = run()
    state.save()
    n_targets = publish.publish_top_targets(state)
    publish.publish_digest(state, fixtures.DAYS - 1)
    dash = publish.publish_dashboard(state, meter, catches)

    print("=" * 74)
    print("CATCH REPORT")
    for c in catches:
        print("  %-16s entered top targets day %02d · round announced day %02d"
              "  →  %d DAYS BEFORE THE NEWS"
              % (c["company"], c["flagged_day"], c["announced_day"], c["lead"]))
    print()
    print("COST METER")
    print("  scoring calls made:            %4d" % meter.scoring_calls)
    print("  re-score-daily counterfactual: %4d" % meter.counterfactual_calls)
    print("  signal-driven cost ratio:      %5.1f%%" % (meter.ratio * 100))
    print()
    print("STATE  %d companies tracked · %d top targets · %d changelog events"
          % (len(state.companies), n_targets, len(state.changelog)))
    print("OUT    %s" % dash)
    print()
    print("The production system ran this loop daily over 12 countries and 4,751")
    print("companies — six real funding rounds surfaced 4-22 days before public")
    print("news. Receipts: docs/CATCHES.md")


if __name__ == "__main__":
    main()
