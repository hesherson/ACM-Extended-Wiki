
/* Offline reference controls. No requests, analytics or stored patient data. */
(function () {
  "use strict";
  function drip(values) {
    var p = values.position, d = values.dropSet, max = values.maximum;
    var curve = values.curve, volume = values.volume, concentration = values.concentration;
    if (![p,d,max,curve,volume,concentration].every(Number.isFinite) ||
        p < 0 || p > 100 || [10,15,20,60].indexOf(d) < 0 ||
        max < 60 || max > 300 || curve < 1 || curve > 4 ||
        volume < 0 || volume > 10000 || concentration < 0 || concentration > 10000) return null;
    var drops = p <= 1 ? 0 : Math.round(max * Math.pow(p / 100, curve) / 5) * 5;
    var rate = drops / d;
    return { drops: drops, rate: rate, hourly: rate * 60, dose: rate * concentration,
      duration: volume === 0 ? 0 : rate > 0 ? volume / rate : null };
  }
  window.ACMEWiki = { calculateDrip: drip };
  var form = document.querySelector("[data-drip-calculator]");
  if (form) {
    var keys = ["position","dropSet","maximum","curve","volume","concentration"], out = {};
    ["drops","rate","hourly","dose","duration","error"].forEach(function (key) {
      out[key] = form.querySelector('[data-result="' + key + '"]');
    });
    function number(value) { return new Intl.NumberFormat(undefined, { maximumFractionDigits: 2 }).format(value); }
    function update() {
      var values = {}, empty = false;
      keys.forEach(function (key) {
        var field = form.elements.namedItem(key);
        if (field.value.trim() === "") empty = true;
        values[key] = Number(field.value);
      });
      var result = empty || !form.checkValidity() ? null : drip(values);
      out.error.hidden = !!result;
      if (!result) {
        out.error.textContent = "Enter a valid value in every field. Clamp: 0 to 100%; maximum: 60 to 300 gtt/min; exponent: 1 to 4.";
        ["drops","rate","hourly","dose","duration"].forEach(function (key) { out[key].textContent = "Unavailable"; });
        return;
      }
      out.drops.textContent = number(result.drops) + " gtt/min";
      out.rate.textContent = number(result.rate) + " mL/min";
      out.hourly.textContent = number(result.hourly) + " mL/h";
      out.dose.textContent = number(result.dose) + " mg/min";
      out.duration.textContent = result.duration === null ? "Stopped" : number(result.duration) + " min";
    }
    form.addEventListener("input", update);
    form.addEventListener("change", update);
    form.addEventListener("submit", function (event) { event.preventDefault(); update(); });
    update();
  }
  function revealAnchor() {
    var id;
    try { id = decodeURIComponent(window.location.hash.slice(1)); } catch (_) { return; }
    if (!id) return;
    var target = document.getElementById(id);
    if (!target) return;
    for (var parent = target.parentElement; parent; parent = parent.parentElement) {
      if (parent.tagName === "DETAILS") parent.open = true;
    }
    requestAnimationFrame(function () { target.scrollIntoView({ block: "start" }); });
  }
  window.addEventListener("hashchange", revealAnchor);
  revealAnchor();
  var printDetails = [];
  window.addEventListener("beforeprint", function () {
    printDetails = Array.from(document.querySelectorAll("details")).filter(function (d) { return !d.open; });
    printDetails.forEach(function (d) { d.open = true; });
  });
  window.addEventListener("afterprint", function () {
    printDetails.forEach(function (d) { d.open = false; });
    printDetails = [];
  });
  document.addEventListener("keydown", function (event) {
    var el = event.target;
    if (event.key !== "/" || event.ctrlKey || event.metaKey || event.altKey ||
        el.isContentEditable || /^(INPUT|SELECT|TEXTAREA)$/.test(el.tagName)) return;
    var q = document.getElementById("q"), button = document.getElementById("mSearch");
    if (!q) return;
    event.preventDefault();
    if (window.innerWidth < 820 && button) button.click(); else q.focus();
  });
})();
