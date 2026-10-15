# Maintain the profile

This repository supplies the README and artwork for https://github.com/JStaRFilms.

## Edit the profile

- Name and project copy: `README.md`.
- Header: the four `assets/hero-*.svg` files. Update light/dark and wide/mobile variants together.
- Graph styling: `scripts/render_assets.py`.
- Graph scope: `REPOS` in `scripts/activity.py`. Keep the README's repository count and scope accurate if this changes.
- Exact counts and exclusions: generated `ACTIVITY.md`.

The header uses the supplied J StaR Films logo in white for the dark theme and black for the light theme. The source PNG was cropped to the main logo, excluding the isolated export mark below the transparent gap, and traced into inline vector paths. No external image reference is required. Header SVGs are maintained directly; graph refreshes do not overwrite them.

## Refresh the activity snapshot

The graph is a dated snapshot. Weekly automation is not enabled.

For a manual refresh, open this repository's **Actions** tab, select **Refresh public activity**, then choose **Run workflow**. The workflow fetches public data and commits updated activity assets, data, and ACTIVITY.md to the default branch.

The included workflow uses GitHub's temporary token with `contents: write`. It reads only the eight explicit public repositories and refuses a private repository before fetching commit data. It does not need a personal access token or external statistics service. Branch protection, disabled Actions, or API limits can prevent a refresh. A failed fetch leaves the existing snapshot in place; inspect the failed run rather than replacing missing results with zeros.

To refresh locally with Python 3.10 or later:

```sh
python scripts/activity.py
```

Optionally supply an authorized GitHub token through `GH_TOKEN` to avoid the lower unauthenticated API limit. Never put token values in files or commits.

To reproduce the current graph without network access:

```sh
python scripts/activity.py --offline
```

The scripts use Python's standard library. SVG and Markdown output is written as UTF-8, including on Windows. The saved input is `data/activity.json`; the full counting method is in `ACTIVITY.md`.

Run the focused tests with:

```sh
python -m unittest discover -s tests -v
```

## Rendering

The profile uses GitHub Markdown, supported HTML, and local SVG assets. It contains no arbitrary CSS, JavaScript, remote fonts, tracking, or animation. The `picture` elements select light/dark and compact/wide artwork; each SVG has a fixed background so the fallback remains legible. Essential project information remains in text.

Before changing artwork or layout, check both GitHub themes and phone widths. Keep the Takomi suite separate from Takomi Code, preserve T3 Code attribution, and avoid implying that Koe's cloud transcription works offline.
