# Travel Notes · The Yu Family Atlas

A personal travel atlas — every country we've visited, mapped, counted,
and journaled. A complete rebuild of the original 2015 Django/SQLite app
as a modern **static site**: no backend, no database, no build step, no
API keys. Deploys free on GitHub Pages.

## What it shows

- **World map** — custom SVG (built from world-atlas 110m shapes):
  visited countries are colored by visit count (darker teal = more
  visits), unvisited countries are gray. Tap/hover for details.
- **Continents** — per-continent progress bars (% of the world's
  countries visited) plus the target next country per continent.
- **Countries visited** — visit counts per country, filterable by
  continent, with the destinations visited in each.
- **Travel journal** — the original trip entries: years, notes, saved
  sights/restaurants/hotels, and photo-album links, with search and
  region filters.

## Stack

- **No framework** — vanilla HTML, CSS, and JavaScript (no build step,
  runs in any modern browser)
- **Data** — `data/trips.json` (source of truth: destinations, years,
  notes, places, albums), `data/countries.json` (generated per-country
  visit stats + continent targets), `data/world.svg` (generated country
  shapes)
- **Map** — dependency-free inline SVG, no tile server, no API key
- **Hosting** — GitHub Pages (serves straight from this repo)

The old Django project (Django 1.8, SQLite, gunicorn, Picasa-era photo
feeds) is fully retired; its travel data was migrated into
`data/trips.json`. Git history preserves the original for reference.

## Data definitions

- **Visit count** = number of unique recorded trip years per country. A
  single trip covering several destinations in one country counts once.
  Entries with no recorded years (currently Brazil, Vietnam) show
  "at least 1 visit" and the hero total carries a "+" suffix.
- **Countries** = entries from the trip journal, which include
  territories (Aruba, Bermuda, Puerto Rico). Continent progress bars
  count these entries against standard sovereign-country totals
  (Africa 54, Asia 48, Europe 44, North America 23, South America 12,
  Oceania 14).

## Run locally

Any static server works, e.g.:

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

(`fetch()` of the data files needs http(s) — opening `index.html`
directly won't load them.)

## Deploy

1. Push this repo to GitHub.
2. Repo Settings → Pages → Deploy from branch → `master` / root.
3. The site goes live at `https://<user>.github.io/travelnotes/`.

## Add a new trip

1. Edit `data/trips.json` and append an entry (same shape as the
   others; `country` must match an existing country name or be added
   to the ISO table in `scripts/build-countries.mjs`).
2. Regenerate the derived data:

```bash
cd scripts && npm i topojson-client d3-geo   # first time only
node build-countries.mjs
# (world.svg only needs rebuilding if the map shapes change)
```

Regions: `Europe`, `Asia`, `North America`, `South America`, `Africa`
(the continent stats key off these names). Place types: `See`, `Eat`,
`Sleep`.

To set a continent's next-country target, edit the `targets` object in
`scripts/build-countries.mjs` and re-run it.
