/* Travel Notes — renders the trip journal from data/trips.json */
(function () {
  "use strict";

  var REGION_COLORS = {
    "Europe": "#5b8def",
    "Asia": "#f2707a",
    "North America": "#43c783",
    "South America": "#e8a33d",
    "Africa": "#9a6ee8"
  };
  var REGION_ORDER = ["Europe", "Asia", "North America", "South America", "Africa"];

  var state = { trips: [], region: "All", query: "" };
  var markers = {}; // trip name -> leaflet marker

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function esc(s) { return String(s); }

  /* ---------- stats ---------- */
  function renderStats(trips) {
    var countries = {};
    var years = [];
    trips.forEach(function (t) {
      countries[t.country] = 1;
      t.years.forEach(function (y) { if (/^\d{4}$/.test(y)) years.push(+y); });
    });
    var span = years.length ? Math.min.apply(null, years) + "–" + Math.max.apply(null, years) : "–";
    var stats = [
      [trips.length, "destinations"],
      [Object.keys(countries).length, "countries"],
      [REGION_ORDER.length, "regions"],
      [span, "traveled"]
    ];
    var wrap = document.getElementById("stats");
    wrap.innerHTML = "";
    stats.forEach(function (s) {
      var d = el("div", "stat");
      d.appendChild(el("b", null, esc(s[0])));
      d.appendChild(el("span", null, s[1]));
      wrap.appendChild(d);
    });
  }

  /* ---------- map ---------- */
  var map;
  function initMap(trips) {
    map = L.map("map", { scrollWheelZoom: false }).setView([28, 8], 2);
    L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
      maxZoom: 18
    }).addTo(map);
    map.on("focus", function () { map.scrollWheelZoom.enable(); });
    map.on("blur", function () { map.scrollWheelZoom.disable(); });

    trips.forEach(function (t) {
      var color = REGION_COLORS[t.region] || "#6ea8fe";
      var icon = L.divIcon({
        className: "",
        html: '<div class="pin" style="background:' + color + '"></div>',
        iconSize: [14, 14],
        iconAnchor: [7, 7]
      });
      var m = L.marker([t.lat, t.lng], { icon: icon, title: t.name })
        .addTo(map)
        .bindTooltip(esc(t.pin), { className: "pin-tip", direction: "top", offset: [0, -8] })
        .on("click", function () { focusCard(t.name); });
      markers[t.name] = m;
    });
  }

  function focusCard(name) {
    var card = document.querySelector('[data-trip="' + CSS.escape(name) + '"]');
    if (!card) return;
    card.scrollIntoView({ behavior: "smooth", block: "center" });
    card.classList.add("flash");
    setTimeout(function () { card.classList.remove("flash"); }, 1600);
  }

  /* ---------- cards ---------- */
  function bannerStyle(region) {
    var c = REGION_COLORS[region] || "#6ea8fe";
    return "background: linear-gradient(135deg, " + c + "cc, " + c + "55 60%, #161b26);";
  }

  function renderCards() {
    var wrap = document.getElementById("cards");
    wrap.innerHTML = "";
    var q = state.query.trim().toLowerCase();
    var shown = 0;

    state.trips.forEach(function (t) {
      if (state.region !== "All" && t.region !== state.region) return;
      if (q) {
        var hay = (t.name + " " + t.pin + " " + t.country + " " + t.region + " " +
          t.years.join(" ") + " " + t.notes + " " +
          t.places.map(function (p) { return p.name + " " + p.address + " " + p.notes; }).join(" ")
        ).toLowerCase();
        if (hay.indexOf(q) === -1) return;
      }
      shown++;
      var card = el("article", "card");
      card.setAttribute("data-trip", t.name);

      var banner = el("div", "card-banner");
      banner.setAttribute("style", bannerStyle(t.region));
      banner.appendChild(el("span", "card-region", t.region));
      banner.appendChild(el("h2", null, t.pin));
      banner.appendChild(el("div", "country", t.country));
      card.appendChild(banner);

      var body = el("div", "card-body");

      if (t.years.length) {
        var years = el("div", "years");
        t.years.forEach(function (y) { years.appendChild(el("span", "year", y)); });
        body.appendChild(years);
      }
      if (t.notes) body.appendChild(el("p", "notes", t.notes));

      if (t.places.length) {
        var groups = {};
        t.places.forEach(function (p) { (groups[p.type] = groups[p.type] || []).push(p); });
        Object.keys(groups).sort().forEach(function (type) {
          var sec = el("div", "places");
          sec.appendChild(el("h3", null, type === "See" ? "Sights" : type === "Eat" ? "Food & Drink" : type === "Sleep" ? "Stay" : type));
          groups[type].forEach(function (p) {
            var d = el("div", "place");
            var head = el("div", null);
            head.appendChild(el("span", "p-name", p.name));
            head.appendChild(el("span", "p-type", p.type));
            d.appendChild(head);
            if (p.address) d.appendChild(el("div", "p-addr", p.address));
            if (p.notes) d.appendChild(el("div", "p-note", p.notes));
            sec.appendChild(d);
          });
          body.appendChild(sec);
        });
      }

      if (t.album) {
        var a = el("a", "album-link", "View photo album \u2197");
        a.href = t.album;
        a.target = "_blank";
        a.rel = "noopener";
        body.appendChild(a);
      }

      card.appendChild(body);
      wrap.appendChild(card);
    });

    document.getElementById("empty").classList.toggle("hidden", shown > 0);
    // dim markers that are filtered out
    Object.keys(markers).forEach(function (name) {
      var t = state.trips.find(function (x) { return x.name === name; });
      var visible = t && (state.region === "All" || t.region === state.region);
      var mEl = markers[name].getElement();
      if (mEl) mEl.style.opacity = visible ? "1" : "0.18";
    });
  }

  /* ---------- controls ---------- */
  function initControls() {
    var chips = document.getElementById("regionChips");
    ["All"].concat(REGION_ORDER).forEach(function (r) {
      var b = el("button", "chip" + (r === "All" ? " active" : ""), r);
      b.setAttribute("role", "tab");
      b.addEventListener("click", function () {
        state.region = r;
        chips.querySelectorAll(".chip").forEach(function (c) {
          c.classList.toggle("active", c.textContent === r);
        });
        renderCards();
      });
      chips.appendChild(b);
    });
    document.getElementById("search").addEventListener("input", function (e) {
      state.query = e.target.value;
      renderCards();
    });
  }

  /* ---------- boot ---------- */
  fetch("data/trips.json")
    .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
    .then(function (trips) {
      state.trips = trips;
      renderStats(trips);
      initMap(trips);
      initControls();
      renderCards();
    })
    .catch(function (err) {
      document.getElementById("cards").innerHTML =
        '<p class="empty">Could not load trip data.</p>';
      console.error(err);
    });
})();
