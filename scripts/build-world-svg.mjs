// Build data/world.svg — one <path> per country from world-atlas 110m TopoJSON.
// Source: https://unpkg.com/world-atlas@2/countries-110m.json (save as data/countries-110m.json)
// Needs: npm i topojson-client d3-geo
// Run: node scripts/build-world-svg.mjs
// Output: data/world.svg (viewBox 0 0 1000 500, NaturalEarth1, Antarctica excluded)
import { readFileSync, writeFileSync } from 'node:fs';
import { feature } from 'topojson-client';
import { geoNaturalEarth1, geoPath } from 'd3-geo';

const topo = JSON.parse(readFileSync(new URL('../data/countries-110m.json', import.meta.url)));
const projection = geoNaturalEarth1().fitExtent([[10, 10], [990, 490]], { type: 'Sphere' });
const path = geoPath(projection);

const round = (d) => d.replace(/-?\d+\.\d+/g, (m) => {
  const n = Number(m);
  return Number.isFinite(n) ? n.toFixed(1) : m;
});

let paths = '';
let count = 0;
for (const geom of topo.objects.countries.geometries) {
  if (geom.id === '010') continue; // skip Antarctica for a tighter map
  const gj = feature(topo, geom);
  const d = path(gj);
  if (!d) continue;
  const name = (geom.properties && geom.properties.name || '').replace(/"/g, '');
  // A few 110m features (N. Cyprus, Somaliland, Kosovo) carry no ISO id —
  // give them a stable slug instead of a duplicate id.
  const slug = geom.id
    ? `c-${geom.id}`
    : 'c-x-' + name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  paths += `  <path id="${slug}" data-name="${name}" d="${round(d)}"/>\n`;
  count++;
}

// Micro-territories too small to appear at 110m get a dot marker instead.
const MICRO = [
  { iso: '533', name: 'Aruba', lng: -70.0349, lat: 12.5237 },
  { iso: '060', name: 'Bermuda', lng: -64.7841, lat: 32.2936 },
];
let micros = '';
for (const m of MICRO) {
  const [x, y] = projection([m.lng, m.lat]);
  micros += `  <circle id="c-${m.iso}" data-name="${m.name}" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="3"/>\n`;
}

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500" role="img" aria-label="World map">\n${paths}${micros}</svg>\n`;
writeFileSync(new URL('../data/world.svg', import.meta.url), svg);
console.log(`wrote data/world.svg with ${count} country paths + ${micros.split('<circle').length - 1} micro markers, ${svg.length} bytes`);
