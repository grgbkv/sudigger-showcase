"""The signal gate — the design decision the whole system rests on.

Only companies with a FRESH signal reach the expensive step (in production:
the LLM). Everyone else keeps yesterday's score. The cost meter tracks what
the naive design would have spent: re-scoring every tracked company every day.

One mechanism, two outcomes: ~95% cost reduction, and events surface weeks
before press coverage — because the system watches changes, not snapshots.
"""


class CostMeter:
    def __init__(self):
        self.scoring_calls = 0          # what the signal-driven design spends
        self.counterfactual_calls = 0   # what re-score-everything-daily would spend

    def charge(self, n=1):
        self.scoring_calls += n

    def accrue_counterfactual(self, universe_size):
        self.counterfactual_calls += universe_size

    @property
    def ratio(self):
        if not self.counterfactual_calls:
            return 0.0
        return self.scoring_calls / self.counterfactual_calls


def select_fresh(signals):
    """Group today's signals by company — each company is processed once per
    day no matter how many signals it emitted."""
    by_company = {}
    for sig in signals:
        by_company.setdefault(sig["company_raw"], []).append(sig)
    return by_company
