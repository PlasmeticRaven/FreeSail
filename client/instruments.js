/* instruments.js: the readouts. Each one is a snapshot field, converted for display. */
(function (root) {
  "use strict";
  var U = root.Units;

  function set(id, text) {
    var e = document.getElementById(id);
    if (e) e.textContent = text;
  }

  // Where the apparent wind lies, in the primer's points of sail (freesail/units.py
  // wind_bearing_words, the same bands): the bow, the beam, the quarter, astern.
  function windBearing(awa) {
    var side = awa >= 0 ? "starboard" : "larboard";
    var points = Math.abs(U.deg(awa)) / 11.25;
    if (points < 7.5) return "on the " + side + " bow";
    if (points < 8.5) return "on the " + side + " beam";
    if (points < 14.5) return "on the " + side + " quarter, abaft the beam";
    if (points < 15.5) return "astern, a little on the " + side + " quarter";
    return "right astern";
  }

  function render(snap) {
    var s = snap.ship;
    var w = snap.wind;
    set("i-time", snap.stamp);
    set("i-bell", snap.bell ? U.formatBells(snap.bell.bells) + " of the " + snap.bell.watch.toLowerCase() : "");
    set("i-heading", U.formatHeading(s.heading));
    set("i-speed", U.formatKnots(s.speed_through_water));
    // no leeway with no way on (freesail/api/readings.py READING_SPEED_FLOOR_KN)
    set("i-leeway", s.leeway === null || s.leeway === undefined ? "no way on" : U.formatSigned(s.leeway, "to starboard", "to larboard"));
    set("i-heel", U.formatSigned(s.heel, "to starboard", "to larboard"));
    set("i-true-wind", U.pointName(w.true_from) + ", " + U.formatKnots(w.true_speed, 0));
    set("i-wind-words", U.windStrength(w.true_speed) + (w.squall ? ", a squall" : w.gust_factor > 1.05 ? ", gusting" : ""));
    renderWeather(snap.weather);
    var awa = w.apparent_angle;
    set("i-apparent", Math.round(Math.abs(U.deg(awa))) + "° " + windBearing(awa) + ", " + U.formatKnots(w.apparent_speed, 0));
    set("i-tack", s.tack + " tack");
    set("i-helm", U.formatSigned(s.rudder, "a-starboard", "a-larboard"));
    var wh = s.weather_helm;
    set("i-balance", Math.abs(U.deg(wh)) < 1 ? "balanced" : Math.abs(Math.round(U.deg(wh))) + "° " + (wh > 0 ? "weather helm" : "lee helm"));
    var mode = s.helm_mode === "heading" ? "steering " + U.formatHeading(s.target_heading) : s.helm_mode === "full_and_by" ? "full and by" : "helm held";
    set("i-course", mode);
    var d = snap.driver || {};
    var clock = (d.running ? "running" : "held") + " at " + (d.compression || 1) + "x";
    // auto-slow on an alarm (spec M4 open item 8): the speed it came down from and the
    // urgent line, until the player sets the speed again
    // (or, with the option of package 33d, when a station was sampled or spoke)
    if (d.eased) clock += "; eased from " + d.eased.from + "x" + (d.eased.why === "station" ? ": " : " on an alarm: ") + d.eased.line;
    // --lockstep: the clock waits while a model's door has the floor (spec M4 §13)
    if (d.lockstep) clock += d.waiting_for ? ", waiting for " + d.waiting_for : ", in lockstep";
    set("i-clock", clock);
    var clockEl = document.getElementById("i-clock");
    if (clockEl) clockEl.classList.toggle("eased", !!d.eased);
    set("i-tick", "tick " + snap.tick);

    var setSails = snap.sails.filter(function (x) {
      return x.state === "set" || x.state === "goose_winged";
    });
    set("i-sails", setSails.length ? setSails.map(function (x) { return U.partName(x.id) + (x.state === "goose_winged" ? " (goose-winged)" : "") + (x.reefs ? " (" + x.reefs + (x.reefs > 1 ? " reefs)" : " reef)") : ""); }).join(", ") : "none");
    var strain = snap.sails.concat(snap.spars).filter(function (x) {
      return x.strain_ratio > 1.0;
    });
    set("i-strain", strain.length ? strain.map(function (x) { return U.partName(x.id) + " " + x.strain_ratio.toFixed(2); }).join(", ") : "none above rating");

    renderCrew(snap.crew);
    renderStations(snap.agents);

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
        var how;
        if (e.waiting) how = e.waiting_for === "hands" ? " (waiting for hands)" : " (waiting)";
        else if (e.paused) how = " (belayed)";
        else how = ", " + Math.round(e.remaining_s) + " s to go";
        var men = e.hands ? " · " + e.hands + (e.hands === 1 ? " hand" : " hands") : "";
        li2.textContent = e.id.replace(/_/g, " ") + (subject ? ": " + subject : "") + " · " + e.step.replace(/_/g, " ") + how + men;
        evoList.appendChild(li2);
      });
    }
  }

  /** The glass and the sky (spec M5 §5): the registry's words, as the console says them.
   * A ship with no glass says so; a scenario with no weather systems keeps no sky. The
   * sea and the motion (spec M5 §4) likewise: the words, the sea's quarter after them. */
  function renderWeather(wx) {
    if (!wx) {
      set("i-glass", "");
      set("i-tendency", "");
      set("i-sky", "");
      set("i-sea", "");
      set("i-motion", "");
      return;
    }
    if (!wx.sea) {
      set("i-sea", wx.sea_words || "no sea kept");
      set("i-motion", "");
    } else {
      var from = wx.sea.indexOf("from") < 0 && wx.sea_from !== null && wx.sea_from !== undefined ? " from " + U.quarterWords(wx.sea_from) : "";
      set("i-sea", wx.sea + from);
      set("i-motion", wx.motion ? "; " + wx.motion : "");
    }
    if (wx.glass_in === null || wx.glass_in === undefined) {
      set("i-glass", wx.glass_words || "no glass aboard");
      set("i-tendency", "");
    } else {
      set("i-glass", wx.glass_in.toFixed(2) + " in");
      set("i-tendency", wx.tendency ? wx.tendency : (wx.tendency_words || ""));
    }
    if (!wx.sky) {
      set("i-sky", wx.sky_words || "no sky kept");
    } else {
      set("i-sky", wx.sky + (wx.signs ? ", " + wx.signs : "") + "; " + wx.weather + "; " + wx.visibility);
    }
  }

  /** The watch on deck and the hands at work (spec M3 §5.2). */
  function renderCrew(c) {
    if (!c) {
      set("i-watch", "no ship's company mustered");
      set("i-hands", "");
      return;
    }
    var watch = c.all_hands ? "all hands; the " + c.watch_on_deck + " watch has the deck" : c.watch_on_deck + " watch";
    var up = (c.turned_up || []).filter(function (w) {
      return w !== c.watch_on_deck;
    });
    if (up.length && !c.all_hands) watch += ", the " + up.join(" and ") + " turned up";
    watch += ", " + c.on_deck + " on deck";
    if (c.idlers_up !== undefined) watch += c.idlers_up ? "; idlers up" : "; idlers below";
    set("i-watch", watch);
    var work = c.at_work || [];
    var busy = work.reduce(function (n, w) {
      return n + w.hands;
    }, 0);
    var hands = work.length
      ? busy + " at work (" + work.map(function (w) { return w.hands + " " + (w.words || "at " + w.evolution.replace(/_/g, " ")); }).join(", ") + "), " + c.idle + " idle"
      : "none at work, " + c.idle + " idle";
    set("i-hands", hands + "; " + fatigueWords(c.fatigue_mean_on_deck) + " on deck, " + fatigueWords(c.fatigue_mean_below) + " below");
  }

  /** The stations (spec M4 §13 as revised): each agent's line, as the console's `state`
   * prints it (stationed, standing by until X, paused, released, its turn open), and the
   * question a pause puts to the captain, which is answered in the order box. The rows
   * are made here, after the instruments, so the page needs no row until a station is
   * manned. */
  function renderStations(stations) {
    var dl = document.querySelector("#instruments-panel .instruments");
    if (!dl) return;
    var dt = document.getElementById("i-stations-term");
    var dd = document.getElementById("i-stations");
    if (!stations || !stations.length) {
      if (dt) dt.remove();
      if (dd) dd.remove();
      return;
    }
    if (!dd) {
      dt = document.createElement("dt");
      dt.id = "i-stations-term";
      dt.textContent = "Stations";
      dd = document.createElement("dd");
      dd.id = "i-stations";
      dd.className = "wrap stations";
      dl.appendChild(dt);
      dl.appendChild(dd);
    }
    dd.innerHTML = "";
    stations.forEach(function (s) {
      var line = document.createElement("div");
      line.className = "station-line state-" + String(s.state || "").replace(/\s+/g, "-");
      line.textContent = s.line || "The " + s.station + ": " + s.words + ".";
      dd.appendChild(line);
      if (s.question) {
        var q = document.createElement("div");
        q.className = "station-question";
        q.textContent = s.question.charAt(0).toUpperCase() + s.question.slice(1) + " Say 'resume the " + s.station + "' or 'stand down the " + s.station + "'.";
        dd.appendChild(q);
      }
    });
  }

  // The muster's words for fatigue (crew/model.py FATIGUE_FRESH_BELOW, FATIGUE_TIRED_BELOW).
  function fatigueWords(f) {
    if (f < 0.2) return "fresh";
    if (f < 0.5) return "tired";
    return "worn out";
  }

  root.Instruments = { render: render };
})(window);
