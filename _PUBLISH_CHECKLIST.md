# Pre-publish checklist (delete this file before pushing public)

Run through this top to bottom the day you publish. Nothing goes public until every box is checked.

## Legal / employment
- [ ] Read the internship agreement: who owns work created during the internship? Does it cover
      personal-time work on personal hardware? (This repo contains no source code or company
      data, which keeps risk low — but check anyway.)
- [ ] Nothing in the repo names colleagues, managers, internal org structures, or internal
      tool names beyond what's on your LinkedIn already.

## Data
- [ ] `grep -ri "docs.google.com\|onedrive\|sharepoint" .` → zero hits
- [ ] Real-data files are bounded: `real_top_targets_sample.csv` (21 rows, trimmed columns:
      no founder/LinkedIn/MSFT-fit/account/comments) and `docs/CATCHES.md` (only facts that are
      already public + our timestamps). Publishing these is gated on the IP skim below —
      a small sample is a demonstration; the full CSV would be the deliverable. Keep it small.
- [ ] Synthetic file stays clearly marked (every row says "synthetic")
- [ ] Screenshots redacted with SOLID FILL (not blur/pixelation) per assets/README.md
- [ ] No 🟡 ACCOUNT / 🟢 COMMENTS content visible in any screenshot (that's colleagues' text)

## Secrets
- [ ] `grep -riE "api[_-]?key|client_id|secret|token|sk-" . --include="*.md" --include="*.csv"` → zero hits
- [ ] No .env, .json credential files, or token files present
- [ ] `git log --all --oneline` reviewed — no commit ever contained sensitive content
      (history is forever on GitHub; if in doubt, re-init the repo fresh before first push)

## Quality
- [ ] README renders correctly on GitHub (check the tables + ASCII diagram in preview)
- [ ] All relative links work (docs/, sample_data/)
- [ ] Screenshots added to assets/ and embedded in README
- [ ] assets/README.md instructions file removed (it's a note-to-self, not portfolio content)
- [ ] This checklist file deleted
- [ ] Repo name + description set: e.g. `sudigger-showcase` — "Signal-driven startup
      intelligence pipeline — architecture & results (12 countries, 22-day latency edge)"
- [ ] Pin the repo on your GitHub profile; add the link to LinkedIn/CV

## Publish commands (when ready)
```bash
cd ~/Desktop/sudigger-showcase
git add -A && git commit -m "Final pre-publish pass"
gh repo create sudigger-showcase --public --source=. --push
```
