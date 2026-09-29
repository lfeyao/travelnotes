/* Travel Notes · The Yu Family Atlas — SVG world map + stats from data/*.json */
(function () {
  "use strict";

  var CONTINENTS = [
    { name: "Africa", total: 54 },
    { name: "Asia", total: 48 },
    { name: "Europe", total: 44 },
    { name: "North America", total: 23 },
    { name: "South America", total: 12 },
    { name: "Oceania", total: 14 }
  ];

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function bucket(v) { return v >= 4 ? "v3" : v >= 2 ? "v2" : "v1"; }
  function visitLabel(c) {
    if (c.yearsUnknown) return "at least 1 visit";
    return c.visits + (c.visits === 1 ? " visit" : " visits");
  }
  function $(id) { return document.getElementById(id); }

  function load() {
    return Promise.all([
      fetch("data/trips.json").then(function (r) { return r.json(); }),
      fetch("data/countries.json").then(function (r) { return r.json(); }),
      fetch("data/world.svg").then(function (r) { return r.text(); })
    ]);
  }

  function renderHero(trips, countries) {
    var visits = countries.reduce(function (s, c) { return s + c.visits; }, 0);
    var unknown = countries.some(function (c) { return c.yearsUnknown; });
    var visitStr = visits + (unknown ? "+" : "");
    var conts = {};
    countries.forEach(function (c) { conts[c.continent] = true; });
    $("stat-countries").textContent = countries.length;
    $("stat-visits").textContent = visitStr;
    $("stat-continents").textContent = Object.keys(conts).length;
    $("stat-trips").textContent = trips.length;
    $("foot-count").textContent = countries.length + " countries · " + visitStr + " visits";
  }

  function renderMap(countries) {
    var wrap = $("map-wrap"), tip = $("map-tip");
    var loading = $("map-loading");
    if (loading) loading.remove();

    var byIso = {};
    countries.forEach(function (c) { byIso[c.iso] = c; });

    var svg = wrap.querySelector("svg");
    var shapes = svg.querySelectorAll("path, circle");
    shapes.forEach(function (p) {
      var iso = p.id.replace(/^c-/, "");
      var c = byIso[iso];
      if (c) {
        p.classList.add("visited", bucket(c.visits));
        p.dataset.iso = iso;
      } else {
        p.classList.add("unvisited");
      }
    });

    function showTip(c, x, y) {
      var dests = c.destinations.map(function (d) { return d.name; }).join(" · ");
      tip.innerHTML = "<strong>" + esc(c.country) + "</strong>" +
        '<span class="tip-visits">' + visitLabel(c) + "</span>" +
        (dests ? '<div class="tip-dests">' + esc(dests) + "</div>" : "");
      tip.hidden = false;
      moveTip(x, y);
    }
    function moveTip(x, y) {
      var pad = 12;
      var r = tip.getBoundingClientRect();
      var left = Math.min(Math.max(x, r.width / 2 + pad), window.innerWidth - r.width / 2 - pad);
      tip.style.left = left + "px";
      tip.style.top = Math.max(y, r.height + pad + 8) + "px";
    }
    function hideTip() { tip.hidden = true; }

    svg.addEventListener("mousemove", function (e) {
      var t = e.target.closest("path.visited, circle.visited");
      if (t) { showTip(byIso[t.dataset.iso], e.clientX, e.clientY); }
      else hideTip();
    });
    svg.addEventListener("mouseleave", hideTip);
    // touch: tap toggles the tooltip
    var openIso = null;
    svg.addEventListener("click", function (e) {
      var t = e.target.closest("path.visited, circle.visited");
      if (t && t.dataset.iso !== openIso) {
        openIso = t.dataset.iso;
        showTip(byIso[openIso], e.clientX, e.clientY);
      } else {
        openIso = null;
        hideTip();
      }
    });
  }

  function renderContinents(data) {
    var grid = $("continent-grid");
    var countries = data.countries, targets = data.targets || {}, notes = data.targetNotes || {};
    grid.innerHTML = CONTINENTS.map(function (cont, i) {
      var visited = countries.filter(function (c) { return c.continent === cont.name; });
      var n = visited.length;
      var pct = Math.round((n / cont.total) * 1000) / 10;
      var target = targets[cont.name];
      var targetHtml = target
        ? "<b>" + esc(target) + "</b>" + (notes[cont.name] ? '<span class="target-note">' + esc(notes[cont.name]) + "</span>" : "")
        : "<b>Not set yet</b>";
      return '<div class="continent-card" style="animation-delay:' + (i * 60) + 'ms">' +
        '<div class="continent-row"><div><p class="continent-name">' + esc(cont.name) + "</p>" +
        '<p class="continent-sub"><b>' + n + "</b> of " + cont.total + " countries</p></div>" +
        '<span class="continent-pct">' + pct + "%</span></div>" +
        '<div class="bar"><i data-w="' + pct + '"></i></div>' +
        '<p class="next-target' + (target ? "" : " unset") + '">Next target: ' + targetHtml + "</p>" +
        "</div>";
    }).join("");
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        grid.querySelectorAll(".bar > i").forEach(function (el) {
          el.style.width = el.getAttribute("data-w") + "%";
        });
      });
    });
  }

  function renderCountries(countries, active) {
    var groups = $("country-groups");
    var list = active === "All" ? countries.slice() : countries.filter(function (c) { return c.continent === active; });
    var order = CONTINENTS.map(function (c) { return c.name; });
    list.sort(function (a, b) {
      var d = order.indexOf(a.continent) - order.indexOf(b.continent);
      return d !== 0 ? d : (b.visits - a.visits || a.country.localeCompare(b.country));
    });
    var html = "", current = null;
    list.forEach(function (c, i) {
      if (c.continent !== current) {
        if (current !== null) html += "</div></div>";
        current = c.continent;
        var n = list.filter(function (x) { return x.continent === current; }).length;
        html += '<div class="country-group"><h3>' + esc(current) + ' <span class="g-count">' + n + "</span></h3>" + '<div class="country-grid">';
      }
      var dests = c.destinations.map(function (d) { return d.name; }).join(" · ");
      html += '<div class="country-card" style="animation-delay:' + Math.min(i * 30, 300) + 'ms">' +
        "<div><p class=\"country-name\">" + esc(c.country) + "</p>" +
        (dests ? '<p class="country-dests">' + esc(dests) + "</p>" : "") + "</div>" +
        '<span class="visit-pill">' + visitLabel(c) + "</span></div>";
    });
    if (current !== null) html += "</div></div>";
    groups.innerHTML = html || '<p class="empty">No countries here yet.</p>';
  }

  function renderCountryFilters(countries, onChange) {
    var box = $("country-filters");
    var present = [];
    CONTINENTS.forEach(function (c) {
      if (countries.some(function (x) { return x.continent === c.name; })) present.push(c.name);
    });
    var opts = ["All"].concat(present);
    box.innerHTML = opts.map(function (o, i) {
      return '<button class="chip' + (i === 0 ? " active" : "") + '" role="tab" data-f="' + esc(o) + '">' + esc(o) + "</button>";
    }).join("");
    box.addEventListener("click", function (e) {
      var b = e.target.closest(".chip");
      if (!b) return;
      box.querySelectorAll(".chip").forEach(function (x) { x.classList.remove("active"); });
      b.classList.add("active");
      onChange(b.getAttribute("data-f"));
    });
  }

  function latestYear(t) {
    if (!t.years || !t.years.length) return 0;
    return Math.max.apply(null, t.years.map(Number));
  }

  function renderJournal(trips) {
    var cards = $("journal-cards"), empty = $("journal-empty");
    var search = $("journal-search"), regions = $("region-filters");
    var regionList = [];
    trips.forEach(function (t) { if (regionList.indexOf(t.region) === -1) regionList.push(t.region); });
    var activeRegion = "All", query = "";

    regions.innerHTML = ["All"].concat(regionList).map(function (r, i) {
      return '<button class="chip' + (i === 0 ? " active" : "") + '" role="tab" data-r="' + esc(r) + '">' + esc(r) + "</button>";
    }).join("");
    regions.addEventListener("click", function (e) {
      var b = e.target.closest(".chip");
      if (!b) return;
      regions.querySelectorAll(".chip").forEach(function (x) { x.classList.remove("active"); });
      b.classList.add("active");
      activeRegion = b.getAttribute("data-r");
      draw();
    });
    search.addEventListener("input", function () { query = search.value.trim().toLowerCase(); draw(); });

    function matches(t) {
      if (activeRegion !== "All" && t.region !== activeRegion) return false;
      if (!query) return true;
      var hay = [t.name, t.country, t.notes, (t.years || []).join(" ")]
        .concat((t.places || []).map(function (p) { return p.name + " " + p.address + " " + p.notes; }))
        .join(" ").toLowerCase();
      return hay.indexOf(query) !== -1;
    }

    function draw() {
      var list = trips.filter(matches).sort(function (a, b) { return latestYear(b) - latestYear(a); });
      empty.hidden = list.length > 0;
      cards.innerHTML = list.map(function (t, i) {
        var years = (t.years || []).map(function (y) { return '<span class="year-tag">' + esc(y) + "</span>"; }).join("");
        var notes = t.notes ? '<p class="trip-notes">' + esc(t.notes) + "</p>" : "";
        var places = (t.places && t.places.length) ? '<ul class="trip-places">' + t.places.map(function (p) {
          return "<li><span class=\"p-type\">" + esc(p.type) + "</span>" + esc(p.name) +
            (p.address ? '<span class="p-addr">' + esc(p.address) + "</span>" : "") +
            (p.notes ? '<span class="p-note">' + esc(p.notes) + "</span>" : "") + "</li>";
        }).join("") + "</ul>" : "";
        var album = t.album ? '<div class="trip-foot"><a class="album-link" href="' + esc(t.album) + '" target="_blank" rel="noopener">📷 Photo album</a></div>' : "";
        return '<article class="trip-card" style="animation-delay:' + Math.min(i * 30, 300) + 'ms">' +
          '<div class="trip-top"><div><h3 class="trip-name">' + esc(t.name) + "</h3>" +
          '<p class="trip-country">' + esc(t.country) + "</p></div></div>" +
          (years ? '<div class="year-tags">' + years + "</div>" : "") +
          notes + places + album + "</article>";
      }).join("");
    }
    draw();
  }

  load().then(function (res) {
    var trips = res[0], data = res[1], svgText = res[2];
    var countries = data.countries;
    renderHero(trips, countries);
    $("map-wrap").insertAdjacentHTML("afterbegin", svgText);
    renderMap(countries);
    renderContinents(data);
    renderCountryFilters(countries, function (f) { renderCountries(countries, f); });
    renderCountries(countries, "All");
    renderJournal(trips);
  }).catch(function (err) {
    var loading = $("map-loading");
    if (loading) loading.textContent = "Couldn't load the map data. Please refresh.";
    // eslint-disable-next-line no-console
    console.error(err);
  });
})();
