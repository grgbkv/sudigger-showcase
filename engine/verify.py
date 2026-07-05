"""Verification gates: geo, URLs, and conservative name handling.

Production lesson these encode: verification is not a post-processing step,
it is the product. Nothing unverified reaches the dashboard.
"""
import re

from . import fixtures

# ---------------------------------------------------------------- names

# Legal suffixes across the region (subset of the production list).
_LEGAL_SUFFIXES = [
    "s.r.o.", "s. r. o.", "sro", "a.s.", "a. s.",
    "sp. z o.o.", "sp. z o. o.", "sp z oo",
    "oü", "ou", "uab", "sia", "srl",
    "тоо", "жшс", "ао", "ип",
]

_CYRILLIC_MAP = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
    "ж": "zh", "з": "z", "и": "i", "й": "i", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch",
    "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}


def _is_pure_cyrillic(text):
    letters = [ch for ch in text if ch.isalpha()]
    return bool(letters) and all("Ѐ" <= ch <= "ӿ" for ch in letters)


def transliterate(text):
    return "".join(_CYRILLIC_MAP.get(ch.lower(), ch) for ch in text)


def clean_display_name(raw):
    """Conservative by design: only touch a name when a legal suffix is
    positively detected; transliterate only pure-Cyrillic names.

    The aggressive version of this function was the production project's
    most instructive failure (969 changes, broke "Labs of Latvia").
    The conservative rewrite made 513 changes with zero false positives.
    """
    name = raw.strip()
    lowered = name.lower()
    for suffix in _LEGAL_SUFFIXES:
        if lowered.endswith(" " + suffix) or lowered.endswith("," + suffix):
            name = name[: -(len(suffix) + 1)].rstrip(" ,")
            break
    if _is_pure_cyrillic(name):
        name = transliterate(name).title()
    return name


def dedup_key(raw):
    """Aggressive comparable form — transliterate BEFORE stripping, so
    «Нордик Дата» and "Nordik Data OÜ" collapse to the same key."""
    name = clean_display_name(raw)
    name = transliterate(name)
    return re.sub(r"[^a-z0-9]", "", name.lower())


# ---------------------------------------------------------------- geo gate

def geo_verify(company):
    """Reject companies whose real HQ is outside the feed's country.

    In production this is geo_verifier_v2: deterministic ccTLD/blocklist
    checks plus an evidence-rich LLM pass with relocation handling. The
    fixture world just knows the truth directly.
    """
    if company["hq_actual"] == company["country"]:
        return True, "HQ matches feed country"
    return False, "registered locally, HQ in %s — foreign branch" % company["hq_actual"]


# ---------------------------------------------------------------- URL gate

def verify_url(url):
    """Stand-in for the production HTTP GET + content-match check."""
    return url in fixtures.URL_ALLOWLIST or url in fixtures.LINKEDIN_ALLOWLIST


def resolve_linkedin(company):
    """The production cascade, miniaturized:
    1. verify the model's guessed URL (GET + content match — HEAD lies),
    2. try the website-domain-derived slug,
    3. site-restricted search,
    4. honest "Not found" — never publish a guess.
    """
    guess = fixtures.LINKEDIN_GUESSES.get(company["name_raw"])
    if guess and verify_url(guess):
        return guess, "verified model suggestion"
    real = company.get("linkedin_real")
    if real:
        slug = company["website"].split(".")[0]
        derived = "linkedin.example/company/" + slug
        if verify_url(derived):
            return derived, "derived from website domain"
        if verify_url(real):
            return real, "found via site-restricted search"
    return "Not found", "no verifiable page — guess rejected" if guess else "no verifiable page"
