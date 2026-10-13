# Tough Old Men

Static site for tougholdmen.com (Option B, "Field Guide"), deployed to GitHub Pages by `.github/workflows/pages.yml`.

- `site/` — the published site: plain HTML and one stylesheet (`assets/css/site.css`), no build step
- `site/assets/` — `css/`, `js/` (menu toggle, join-form mailto), `fonts/`, `img/`, `logo/`
- `source/raw/` — archived Wayback Machine HTML of the original 2014 site (reference only; the old build script was removed because it would overwrite the redesigned pages)
- `prototypes/` — the three design concepts (A Summit, B Field Guide, C Poster) used to choose the direction
- Preview: `python3 -m http.server 8765 -d site`

Pages keep their original URLs (`/adventure-story/`, `/join/`, `/contact/`, `/privacy-policy/`, `/terms-of-use/`) and add `/adventures/`, `/events/`, `/salute/`. There is no store at launch.

## Before launch

- Fonts are free stand-ins: League Gothic (for Trade Gothic) and Figtree (for Gotham). License web versions of the real fonts.
- `/events/` and `/salute/` contain sample placeholder slots.
- The Join form posts to Buttondown (list: tougholdmen) with name and postal code saved as subscriber metadata. Confirm in Buttondown that open and click tracking are off.
