"""5-indicator partnership-fit scoring.

Production runs this as an LLM call (Azure OpenAI) over enriched context.
Here it is a deterministic stand-in reading fixture ground truth, because the
demo must run identically everywhere with zero keys. The *rules around* the
call are the point:

- ternary indicators (Yes / No / Unclear);
- Unclear counts as No in the total — bias toward known data, a company only
  scores on what can actually be evidenced;
- signals upgrade specific indicators, which is how a fresh signal can move a
  company into the top targets.
"""

INDICATORS = ["b2b", "saas", "global", "fit", "perf"]

# Which signal types can resolve which indicators to Yes. A signal only
# lifts an indicator that is Unclear — evidence resolves uncertainty, it
# never contradicts a known No.
_SIGNAL_UPGRADES = {
    "hiring_surge": ["perf", "global"],   # sustained hiring = execution + scaling evidence
    "vc_portfolio_add": ["perf"],         # investor conviction = performance evidence
    "funding_event": ["global", "perf"],  # fresh capital = scaling evidence
    "partnership": ["fit"],               # ecosystem activity = partnership evidence
}


def apply_signal(attrs, signal_type):
    """Return (new_attrs, changed) after a signal lands."""
    upgraded = dict(attrs)
    changed = False
    for key in _SIGNAL_UPGRADES.get(signal_type, []):
        if upgraded.get(key) == "Unclear":
            upgraded[key] = "Yes"
            changed = True
    return upgraded, changed


def total(attrs):
    """Yes-count. Unclear collapses to No — the production bias-known-data rule."""
    return sum(1 for k in INDICATORS if attrs.get(k) == "Yes")


def initial_attrs(company, source):
    """Discovery context is thin: registry rows carry less evidence than a
    news profile or a VC portfolio listing. Model that by degrading Unclear-
    prone indicators when the source is a bare registry row."""
    attrs = dict(company["attrs"])
    if source.startswith("registry"):
        for k in ("global", "fit"):
            if attrs[k] == "Yes":
                attrs[k] = "Unclear"
    return attrs
