# Activity snapshot

Window: **2026-04-16 through 2026-10-14**, complete UTC days.
Collected: 2026-10-15T16:25:24.601039+00:00.

**1,143** unique non-merge commits · **127** active days · **288** commits in selected studio repositories.

| Repository | Authored commits | Default branch |
|---|---:|---|
| [Takomi suite](https://github.com/J-StaR-Films-Studios/VibeCode-Protocol-Suite) | 270 | `main` |
| [Takomi Code](https://github.com/JStaRFilms/Takomi-Code) | 116 | `Takomi-Code` |
| [Melo](https://github.com/JStaRFilms/Melo_School_Management_System) | 657 | `master` |
| [JStar Study](https://github.com/JStaRFilms/adaptive-study-game) | 13 | `main` |
| [Koe](https://github.com/JStaRFilms/Koe) | 46 | `master` |
| [CreativeOS](https://github.com/J-StaR-Films-Studios/CreativeOS) | 18 | `main` |
| [Cube Trainer](https://github.com/JStaRFilms/rubiks-cube-trainer) | 23 | `main` |
| [NamiStack](https://github.com/JStaRFilms/namistack) | 0 | `master` |

## What this counts

GitHub REST commits API, filtered by `author=JStaRFilms`, then checked again against the returned `author.login`. Only non-merge commits reachable from each repository’s default-branch head are included. Each head is pinned before pagination. The calendar uses the commit’s **committer timestamp in UTC**, not the push date or original author timestamp. A column is seven consecutive days from the printed start date; rows are not fixed Monday–Sunday labels. Color buckets: 0, 1–3, 4–9, 10–24, 25+.

The total and daily calendar deduplicate commit SHAs across repositories. Repository bars count unique SHAs within each repository, so shared history could make the bars sum to more than the overall total. Studio count is the union of counted SHAs in the two studio-owned repositories. An active day means at least one counted commit. Zero means no qualifying commit in this window, not an abandoned project.

This is **not** GitHub’s contribution calendar or a productivity score. It excludes private repositories, other public repositories, non-default branches, merges, issues, reviews, PR events and co-authored commits not primarily attributed to this login. Fork history is included only where GitHub identifies JStaRFilms as author; upstream authors are never assigned to John. Squash/rebase history and linked-account attribution affect counts.

## Source and refresh

Source: [GitHub REST commits API](https://docs.github.com/en/rest/commits/commits#list-commits). Audit input: [data/activity.json](data/activity.json), containing public SHAs, dates, repo names and captured heads. No emails, commit messages, tokens or private data are exported.

Run `python scripts/activity.py` to fetch the last 182 complete UTC days and rebuild the SVGs and this table. Run `python scripts/activity.py --offline` to reproduce the visual assets from the saved snapshot. `.github/workflows/activity.yml` supports manual refresh through GitHub Actions. No weekly schedule is enabled. See MAINTENANCE.md for permissions, failures and publishing.
