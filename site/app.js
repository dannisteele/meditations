(function () {
  "use strict";
  var KEY = "meditations.version";
  var dayData = null;

  function todayLondon() {
    var q = new URLSearchParams(location.search).get("date");
    if (q && /^\d{4}-\d{2}-\d{2}$/.test(q)) return q;
    return new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/London" }).format(new Date());
  }

  function getVersion() {
    try { return localStorage.getItem(KEY) === "original" ? "original" : "modern"; }
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

  function renderText(text, isMessage) {
    var el = document.getElementById("text");
    el.className = isMessage ? "text message" : "text";
    el.textContent = "";
    text.split("\n\n").forEach(function (para) {
      var p = document.createElement("p");
      p.textContent = para;
      el.appendChild(p);
    });
  }

  function render() {
    var v = getVersion();
    document.querySelectorAll(".toggle button").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.version === v));
    });
    if (dayData) renderText(dayData[v], false);
  }

  function showMissing() {
    renderText("Today's passage isn't available — check back soon.", true);
    document.querySelector(".toggle").hidden = true;
  }

  var date = todayLondon();
  document.getElementById("date").textContent = prettyDate(date);
  document.querySelectorAll(".toggle button").forEach(function (b) {
    b.addEventListener("click", function () { setVersion(b.dataset.version); render(); });
  });

  fetch("days/" + date + ".json", { cache: "no-cache" })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (d) {
      dayData = d;
      document.getElementById("ref").textContent = d.ref;
      render();
    })
    .catch(showMissing);
})();
