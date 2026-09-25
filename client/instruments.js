/* instruments.js: the readouts. Each one is a snapshot field, converted for display. */
(function (root) {
  "use strict";
  var U = root.Units;

  function set(id, text) {
    var e = document.getElementById(id);
    if (e) e.textContent = text;
  }

  function render(snap) {
    var s = snap.ship;
    var w = snap.wind;
    set("i-time", snap.stamp);
    set("i-bell", snap.bell ? U.formatBells(snap.bell.bells) + " of the " + snap.bell.watch.toLowerCase() : "");
    set("i-heading", U.formatHeading(s.heading));
    set("i-speed", U.formatKnots(s.speed_through_water));
    set("i-leeway", U.formatSigned(s.leeway, "to starboard", "to larboard"));
    set("i-heel", U.formatSigned(s.heel, "to starboard", "to larboard"));
    set("i-true-wind", U.pointName(w.true_from) + ", " + U.formatKnots(w.true_speed, 0));
    set("i-wind-words", U.windStrength(w.true_speed) + (w.gust_factor > 1.05 ? ", gusting" : ""));
    var awa = w.apparent_angle;
    set("i-apparent", Math.round(Math.abs(U.deg(awa))) + "° on the " + (awa >= 0 ? "starboard" : "larboard") + " bow, " + U.formatKnots(w.apparent_speed, 0));
    set("i-tack", s.tack + " tack");
    set("i-helm", U.formatSigned(s.rudder, "a-starboard", "a-larboard"));
    var wh = s.weather_helm;
    set("i-balance", Math.abs(U.deg(wh)) < 1 ? "balanced" : Math.abs(Math.round(U.deg(wh))) + "° " + (wh > 0 ? "weather helm" : "lee helm"));
    var mode = s.helm_mode === "heading" ? "steering " + U.formatHeading(s.target_heading) : s.helm_mode === "full_and_by" ? "full and by" : "helm held";
    set("i-course", mode);
    var d = snap.driver || {};
    set("i-clock", (d.running ? "running" : "held") + " at " + (d.compression || 1) + "x");
    set("i-tick", "tick " + snap.tick);

    var setSails = snap.sails.filter(function (x) {
      return x.state === "set";
    });
    set("i-sails", setSails.length ? setSails.map(function (x) { return U.partName(x.id) + (x.reefs ? " (" + x.reefs + (x.reefs > 1 ? " reefs)" : " reef)") : ""); }).join(", ") : "none");
    var strain = snap.sails.concat(snap.spars).filter(function (x) {
      return x.strain_ratio > 1.0;
    });
    set("i-strain", strain.length ? strain.map(function (x) { return U.partName(x.id) + " " + x.strain_ratio.toFixed(2); }).join(", ") : "none above rating");

    var evoList = document.getElementById("i-evolutions");
    if (evoList) {
      evoList.innerHTML = "";
      var evos = snap.evolutions_in_progress || [];
      if (!evos.length) {
        var li = document.createElement("li");
        li.className = "none";
        li.textContent = "nothing in hand";
        evoList.appendChild(li);
      }
      evos.forEach(function (e) {
        var li2 = document.createElement("li");
        var subject = e.subject ? U.partName(e.subject) : "";
        li2.textContent = e.id.replace(/_/g, " ") + (subject ? ": " + subject : "") + " · " + e.step.replace(/_/g, " ") + (e.waiting ? " (waiting)" : ", " + Math.round(e.remaining_s) + " s to go");
        evoList.appendChild(li2);
      });
    }
  }

  root.Instruments = { render: render };
})(window);
