
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

/* Normalized DO2 illustration for perfusing scenarios at default settings. */
(function () {
"use strict";
function do2(blood,saline=0,plasma=0,hr=75,sat=97,ppv=false,peep=5,dilution=saline){
 const total=Math.max(.1,blood+saline+plasma),v=Math.min(1.1,total/6);
 let sv=Math.pow(v,1.6);
 if(ppv){const empty=1-Math.min(1,v/1.1),pen=Math.max(0,Math.min(1,(empty-.12)/.88))*.35*(1+Math.max(0,Math.min(1,(peep-5)/10))*.5);sv*=Math.max(.25,1-pen);}
 let rate=Math.max(.3,Math.min(1.35,1+(hr/75-1)*.4));
 if(hr>150){const raw=1-Math.max(0,Math.min(1,(hr-150)/70))*.55;rate*=1-(1-raw)*(1-Math.min(1,v));}
 return {sv,co:sv*rate,hb:Math.min(1,blood/Math.max(.1,blood+dilution+plasma)),do2:Math.min(1,blood/Math.max(.1,blood+dilution+plasma))*(sat/100)*sv*rate/.97};
}
window.ACMEWiki.calculateDO2 = function(v) {
 if (!v || !["blood","saline","plasma","heartRate","saturation","peep"].every(k => Number.isFinite(v[k])) || v.blood < .1 || v.blood > 6.6 || v.saline < 0 || v.saline > 6 || v.plasma < 0 || v.plasma > 6 || v.heartRate < 20 || v.heartRate > 220 || v.saturation < 1 || v.saturation > 100 || v.peep < 0 || v.peep > 20 || !["none","bvm","vent"].includes(v.support)) return null;
 return do2(v.blood,v.saline,v.plasma,v.heartRate,v.saturation,v.support!=="none",v.support==="vent"?v.peep:5);
};
const form=document.querySelector("[data-do2-calculator]");
if (!form) return;
const keys=["blood","saline","plasma","heartRate","saturation","peep"], labels={sv:"sv",co:"co",hb:"hb",delivery:"do2"};
function update(){
 const values={support:form.elements.namedItem("support").value};
 let empty=false;
 for(const key of keys){const field=form.elements.namedItem(key);if(field.value.trim()==="")empty=true;values[key]=Number(field.value);}
 const result=empty || !form.checkValidity()?null:window.ACMEWiki.calculateDO2(values);
 const error=form.querySelector('[data-do2-result="error"]');error.hidden=!!result;error.textContent=result?"":"Enter a valid value in each field to calculate delivery.";
 for(const [label,key] of Object.entries(labels))form.querySelector('[data-do2-result="'+label+'"]').textContent=result?new Intl.NumberFormat(undefined,{maximumFractionDigits:1}).format(result[key]*100)+"%":"Unavailable";
}
form.addEventListener("input",update);form.addEventListener("change",update);form.addEventListener("submit",e=>{e.preventDefault();update();});update();
})();
