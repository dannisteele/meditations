(function () {
  "use strict";
  var KEY = "meditations.version";
  var dayData = null;

  function todayLondon() {
    var q = new URLSearchParams(location.search).get("date");
    if (q && /^\d{4}-\d{2}-\d{2}$/.test(q)) return q;
    var parts = {};
    new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/London", year: "numeric", month: "2-digit", day: "2-digit" })
      .formatToParts(new Date())
      .forEach(function (p) { parts[p.type] = p.value; });
    return parts.year + "-" + parts.month + "-" + parts.day;
  }

  function getVersion() {
    try {
      var v = localStorage.getItem(KEY);
      return v === "original" || v === "explained" ? v : "modern";
    }
    catch (e) { return "modern"; }
  }

  function setVersion(v) {
    try { localStorage.setItem(KEY, v); } catch (e) { /* private mode: fine */ }
  }

  function prettyDate(iso) {
    var p = iso.split("-");
    var d = new Date(Date.UTC(+p[0], +p[1] - 1, +p[2], 12));
    return d.toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long", year: "numeric", timeZone: "UTC" });
  }

  function addParas(el, text) {
    text.split("\n\n").forEach(function (para) {
      var p = document.createElement("p");
      p.textContent = para;
      el.appendChild(p);
    });
  }

  function renderText(text, isMessage) {
    var el = document.getElementById("text");
    el.className = isMessage ? "text message" : "text";
    el.textContent = "";
    addParas(el, text);
  }

  function renderExplained(x) {
    var el = document.getElementById("text");
    el.className = "text explained";
    el.textContent = "";
    addParas(el, x.summary);
    if (x.today) {
      var h = document.createElement("p");
      h.className = "label";
      h.textContent = "In everyday life";
      el.appendChild(h);
      addParas(el, x.today);
    }
  }

  function render() {
    var v = getVersion();
    document.querySelectorAll(".toggle button").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.version === v));
    });
    if (!dayData) return;
    if (v === "explained" && dayData.explained) renderExplained(dayData.explained);
    else renderText(dayData[v === "explained" ? "modern" : v], false);
  }

  function showMissing() {
    renderText("Today's passage isn't available — check back soon.", true);
    document.querySelector(".toggle").hidden = true;
  }

  document.querySelectorAll(".toggle button").forEach(function (b) {
    b.addEventListener("click", function () { setVersion(b.dataset.version); render(); });
  });

  var shownDate = null;

  function load() {
    var date = todayLondon();
    if (date === shownDate) return;
    shownDate = date;
    dayData = null;
    document.getElementById("date").textContent = prettyDate(date);
    document.getElementById("ref").textContent = "";
    document.querySelector(".toggle").hidden = false;
    fetch("days/" + date + ".json", { cache: "no-cache" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) {
        if (date !== shownDate) return;
        dayData = d;
        document.getElementById("ref").textContent = d.ref;
        render();
      })
      .catch(function () { if (date === shownDate) showMissing(); });
  }

  // iOS keeps home-screen apps and tabs suspended: re-check the date on return.
  document.addEventListener("visibilitychange", function () { if (!document.hidden) load(); });
  window.addEventListener("pageshow", load);
  load();
})();
