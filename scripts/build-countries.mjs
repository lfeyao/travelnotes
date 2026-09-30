// Build data/countries.json — aggregate trips.json into per-country visit stats.
// Run: node scripts/build-countries.mjs
// visits = number of UNIQUE recorded years across destinations (a single trip
// covering several destinations in one country counts once). Destinations with
// no recorded years set yearsUnknown: true (visits excludes them).
import { readFileSync, writeFileSync } from 'node:fs';

const trips = JSON.parse(readFileSync(new URL('../data/trips.json', import.meta.url)));

// ISO 3166-1 numeric ids as they appear in world-atlas (zero-padded strings).
const ISO = {
  'Netherlands': '528', 'Spain': '724', 'Croatia': '191', 'Italy': '380',
  'USA': '840', 'China': '156', 'Japan': '392', 'France': '250',
  'Argentina': '032', 'Ecuador': '218', 'Peru': '604', 'Puerto Rico': '630',
  'South Africa': '710', 'United Kingdom': '826', 'Germany': '276',
  'Zimbabwe': '716', 'Aruba': '533', 'Czech Republic': '203', 'Iceland': '352',
  'Bermuda': '060', 'Mexico': '484', 'Brazil': '076', 'Vietnam': '704',
  'Indonesia': '360', 'Singapore': '702', 'Türkiye': '792',
  'Greece': '300', 'Montenegro': '499', 'Thailand': '764',
};

// "USA" displays better as "United States".
const DISPLAY = { 'USA': 'United States' };

const byCountry = new Map();
for (const t of trips) {
  const c = t.country;
  if (!byCountry.has(c)) {
    byCountry.set(c, {
      country: DISPLAY[c] || c,
      iso: ISO[c] || null,
      continent: t.region,
      visits: 0,
      _years: new Set(),
      destinations: [],
    });
  }
  const e = byCountry.get(c);
  for (const y of (t.years || [])) e._years.add(String(y));
  e.visits = e._years.size;
  e.destinations.push({ name: t.name, years: t.years || [] });
}

const countries = [...byCountry.values()].map((e) => {
  const { _years, ...rest } = e;
  if (_years.size === 0) rest.yearsUnknown = true;
  return rest;
}).sort((a, b) => b.visits - a.visits || a.country.localeCompare(b.country));

const missing = countries.filter((c) => !c.iso).map((c) => c.country);
if (missing.length) {
  console.error('missing ISO ids for:', missing.join(', '));
  process.exit(1);
}

const out = {
  generated: new Date().toISOString().slice(0, 10),
  // Next-country targets per continent (null = not set yet).
  targets: {
    'Africa': null,
    'Asia': 'Japan',
    'Europe': null,
    'North America': null,
    'South America': null,
    'Oceania': null,
  },
  targetNotes: { 'Asia': 'Family trip planned Apr 2027' },
  countries,
};

writeFileSync(new URL('../data/countries.json', import.meta.url), JSON.stringify(out, null, 2) + '\n');
const totalVisits = countries.reduce((s, c) => s + c.visits, 0);
console.log(`wrote data/countries.json: ${countries.length} countries, ${totalVisits} total visits`);
