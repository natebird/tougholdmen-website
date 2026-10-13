# Tough Old Men

Static recreation of tougholdmen.com from Wayback Machine captures (Sept 2014 where available).

- `site/` — the published site (deployed to GitHub Pages by `.github/workflows/pages.yml`)
- `source/raw/` — unmodified archived HTML; `source/build.py` regenerates the pages in `site/` from it
- Rebuild: `python3 -I source/build.py`
- Preview: `python3 -m http.server 8765 -d site`

Fonts are free stand-ins for the original Typekit fonts: Figtree (Proxima Nova) and League Gothic (Alternate Gothic No. 2).
