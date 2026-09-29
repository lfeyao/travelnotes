# Travel Notes

A personal travel journal — everywhere we've been, on one interactive map.
A complete rebuild of the original 2015 Django/SQLite app as a modern
**static site**: no backend, no database, no build step. Deploys free on
GitHub Pages.

## Stack

- **No framework** — vanilla HTML, CSS, and JavaScript (no build step, runs in any modern browser)
- **Data** — `data/trips.json` (destinations, years visited, notes, saved
  sights/restaurants/hotels, photo-album links, map coordinates)
- **Map** — [Leaflet](https://leafletjs.com/) with CARTO dark tiles
  (no API key required)
- **Hosting** — GitHub Pages (serves straight from this repo)

The old Django project (Django 1.8, SQLite, gunicorn, Picasa-era photo
feeds) is fully retired; its travel data was migrated into
`data/trips.json`. Git history preserves the original for reference.

## Run locally

Any static server works, e.g.:

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

(Open `index.html` directly also works for layout, but `fetch()` of
`data/trips.json` needs http(s) — hence the local server.)

## Deploy

1. Push this repo to GitHub.
2. Repo Settings → Pages → Deploy from branch → `main` / root.
3. The site goes live at `https://<user>.github.io/travelnotes/`.

## Add a new trip

Edit `data/trips.json` and append an entry:

```json
{
  "name": "Kyoto",
  "pin": "Kyoto, Japan",
  "country": "Japan",
  "region": "Asia",
  "years": ["2026"],
  "notes": "Cherry blossom season.",
  "album": "https://photos.google.com/...",
  "lat": 35.0116,
  "lng": 135.7681,
  "places": [
    { "name": "Fushimi Inari", "type": "See", "address": "", "notes": "Go early." }
  ]
}
```

Regions: `Europe`, `Asia`, `North America`, `South America`, `Africa`
(the map colors key off these names). Place types: `See`, `Eat`, `Sleep`.
