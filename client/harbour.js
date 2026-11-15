/* harbour.js: the harbour (package 59; spec M7b §21d and §21e), a page of the game's own
   server (freesail/ui/harbour.py). A new game from the server's flags as controls; the
   game in play, the stations held and the doors; the desktop client's entries, one per
   station; the API door and the local runner as the server's subprocesses, each in a pane;
   the scenario maker, which reads a scenario into its form and writes back only what was
   changed (the server keeps every other line of the file as it was); the settings. */
(function () {
  "use strict";

  var $ = function (id) { return document.getElementById(id); };
  var cat = null; // the catalogue
  var paneSince = {}; // each door pane's next line
  var harbour = (window.freesailHarbour = { ready: false, cat: null, loaded: null });

  function api(method, path, body) {
    var opts = { method: method, headers: {} };
    if (body !== undefined) {
      opts.headers["Content-Type"] = "application/json";
      opts.body = JSON.stringify(body);
    }
    return fetch(path, opts).then(function (r) {
      return r.json().then(function (j) {
        if (!r.ok) throw new Error(j.detail || r.statusText);
        return j;
      });
    });
  }

  function clear(el) { while (el.firstChild) el.removeChild(el.firstChild); }
  function option(sel, value, words) {
    var o = document.createElement("option");
    o.value = value;
    o.textContent = words === undefined ? value : words;
    sel.appendChild(o);
    return o;
  }
  function li(list, words, cls) {
    var x = document.createElement("li");
    x.textContent = words;
    if (cls) x.className = cls;
    list.appendChild(x);
    return x;
  }
  function show(el, text) {
    el.textContent = text;
    el.hidden = !text;
  }
  function deep(x) { return x === undefined ? undefined : JSON.parse(JSON.stringify(x)); }

  // -- each setting explained where it is set (package 96b, step 10) --------------------
  //
  // The page's sentences are one file (harbour-words.js): one for each control, by its
  // selector. Each is put under its control, inside the control's label.
  function applyWords() {
    var words = window.freesailHarbourWords || {};
    Object.keys(words).forEach(function (sel) {
      var el = document.querySelector(sel);
      if (!el || !words[sel]) return;
      var label = el.closest("label");
      if (!label || label.querySelector(".says")) return;
      var s = document.createElement("span");
      s.className = "says";
      s.textContent = words[sel];
      label.appendChild(s);
    });
  }
  applyWords();

  // -- the tabs ------------------------------------------------------------------------

  function tab(name) {
    document.querySelectorAll("nav.tabs button").forEach(function (b) {
      b.classList.toggle("active", b.getAttribute("data-tab") === name);
    });
    document.querySelectorAll(".tab-page").forEach(function (p) {
      p.hidden = p.getAttribute("data-page") !== name;
    });
    try { sessionStorage.setItem("harbour-tab", name); } catch (e) { /* none */ }
    if (name === "maker") drawChart();
  }
  document.querySelectorAll("nav.tabs button").forEach(function (b) {
    b.addEventListener("click", function () { tab(b.getAttribute("data-tab")); });
  });

  // -- the catalogue -------------------------------------------------------------------

  // The scenarios by shelf (package 96b, step 1; docs/design/Design-Harbour.md §3.2): the
  // catalogue gives each scenario its shelf and its sentence, in the shelves' order; a
  // shelf kept for tests and gates is listed only when the tick box asks for it.
  function showTests() { return $("s-tests").checked; }
  function scenarioOptions(sel, withNone) {
    clear(sel);
    if (withNone) option(sel, "", withNone);
    (cat.shelves || []).forEach(function (shelf) {
      if (shelf.hidden && !showTests()) return;
      var group = document.createElement("optgroup");
      group.label = shelf.id === "yours" ? "Yours (" + cat.scenarios_place + ")" : shelf.title;
      group.setAttribute("data-shelf", shelf.id);
      cat.scenarios.forEach(function (s) {
        if (s.shelf !== shelf.id) return;
        var o = document.createElement("option");
        o.value = s.path;
        o.textContent = s.name;
        o.title = s.path.split(/[\\/]/).pop();
        group.appendChild(o);
      });
      if (group.children.length) sel.appendChild(group);
    });
  }
  // a scenario that begins in another year than 1805 (the design's trap 3): said wherever
  // the year is, in the words the proof uses
  function yearWords(year) {
    return "She begins in " + year + ". The ports are as they stood on that day; the wars are those of June 1805, whatever the year.";
  }
  function scenarioSays() {
    var path = $("s-scenario").value;
    var s = (cat.scenarios || []).filter(function (x) { return x.path === path; })[0];
    var shelf = s && (cat.shelves || []).filter(function (x) { return x.id === s.shelf; })[0];
    var words = "";
    if (s) words = (shelf ? shelf.title + ". " : "") + (s.says || (shelf ? shelf.says : "")) + "  (" + s.path.split(/[\\/]/).pop() + ")" + (s.year && s.year !== 1805 ? "  " + yearWords(s.year) : "");
    $("s-says").textContent = words;
    scenarioSaid(path);
  }
  // What the game is, said before it is started (package 96b, step 3): the scenario's own
  // lines as a driver prints them at the load, and the ships the player may be aboard.
  var saidFor = "";
  function scenarioSaid(path) {
    saidFor = path;
    show($("s-lines"), "");
    $("s-lines").classList.remove("refusal");
    var aboard = $("s-aboard");
    clear(aboard);
    option(aboard, "", "your own ship");
    $("s-aboard-label").hidden = true;
    if (!path) return;
    api("GET", "/api/harbour/scenario?path=" + encodeURIComponent(path)).then(function (r) {
      if (saidFor !== path) return; // another was chosen meanwhile
      show($("s-lines"), r.refusal ? "This scenario does not load: " + r.refusal : r.lines.join("\n"));
      $("s-lines").classList.toggle("refusal", !!r.refusal);
      if ($("s-from").value !== "scenario") $("s-lines").hidden = true;
      (r.aboard || []).forEach(function (name) { option(aboard, name, "the " + name); });
      $("s-aboard-label").hidden = !(r.aboard || []).length || $("s-from").value !== "scenario";
    }).catch(function () { /* the list still starts it; the start says why if it cannot */ });
  }
  function fillScenarios() {
    var keep = { s: $("s-scenario").value, m: $("m-pick").value };
    scenarioOptions($("s-scenario"));
    scenarioOptions($("m-pick"));
    if (keep.s) $("s-scenario").value = keep.s;
    if (keep.m) $("m-pick").value = keep.m;
    if ($("s-scenario").selectedIndex < 0) $("s-scenario").selectedIndex = 0;
    if ($("m-pick").selectedIndex < 0) $("m-pick").selectedIndex = 0;
    scenarioSays();
  }

  // -- begin (package 96b, step 2; docs/design/Design-Harbour.md §3.1) -------------------
  //
  // The first panel: one game named to begin with, the lessons as lessons, the newest save,
  // and the way to all the games. No seed, pace or seat is asked: each button starts its
  // game with the scenario's own choices (and the seat its shelf entry names), the clock
  // held, and goes to the game's page.

  function beginStart(body, button) {
    var words = $("b-words");
    document.querySelectorAll(".begin button").forEach(function (b) { b.disabled = true; });
    words.classList.remove("refusal");
    show(words, "Starting...");
    return api("POST", "/api/harbour/start", body).then(function () {
      window.location.href = "/";
    }).catch(function (e) {
      show(words, e.message);
      words.classList.add("refusal");
      document.querySelectorAll(".begin button").forEach(function (b) { b.disabled = false; });
    });
  }

  function fillBegin() {
    var first = cat.first_game;
    $("b-first").hidden = !first;
    if (first) {
      $("btn-b-first").textContent = "begin: " + first.name;
      $("btn-b-first").setAttribute("data-path", first.path);
      var says = $("b-first-says");
      clear(says);
      first.says.forEach(function (w) { li(says, w); });
    }
    var lessons = cat.scenarios.filter(function (s) { return s.shelf === "lessons"; });
    $("b-lessons-block").hidden = !lessons.length;
    var list = $("b-lessons");
    clear(list);
    lessons.forEach(function (s) {
      var item = document.createElement("li");
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = s.name;
      b.setAttribute("data-path", s.path);
      b.addEventListener("click", function () { beginStart({ scenario: s.path, seat: s.seat || "" }, b); });
      item.appendChild(b);
      var w = document.createElement("span");
      w.textContent = " " + s.says;
      item.appendChild(w);
      list.appendChild(item);
    });
  }
  $("btn-b-first").addEventListener("click", function () {
    beginStart({ scenario: $("btn-b-first").getAttribute("data-path"), seat: "" }, $("btn-b-first"));
  });
  $("btn-b-save").addEventListener("click", function () {
    beginStart({ load: $("btn-b-save").getAttribute("data-save") }, $("btn-b-save"));
  });
  $("btn-b-all").addEventListener("click", function () { tab("game"); });

  function beginState(s) {
    var g = s.game;
    $("b-playing").hidden = !g.started;
    if (g.started) {
      $("b-playing-says").textContent = (g.title || "A ship on open water") + (g.ship ? ": " + g.ship : "") + ", " + g.stamp + ". " + (g.running ? "The clock runs." : "The clock is held until you say go.");
    }
    var newest = s.saves && s.saves.saves.length ? s.saves.saves[0] : null;
    $("b-save").hidden = !newest;
    if (newest && $("btn-b-save").getAttribute("data-save") !== newest.name) {
      $("btn-b-save").textContent = "take up: " + newest.name;
      $("btn-b-save").setAttribute("data-save", newest.name);
      $("b-save-says").textContent = "Your newest save, written " + newest.written + ", in " + s.saves.place + ". The game tab takes up any other.";
    }
  }

  function fillCatalogue() {
    fillScenarios();
    fillBegin();
    var ship = $("s-ship");
    clear(ship);
    cat.ships.forEach(function (s) { option(ship, s); });
    var seat = $("s-seat");
    clear(seat);
    cat.seats.forEach(function (s) {
      option(seat, s, s === "" ? "as the scenario says (else the captain)" : s === "captain" ? "the captain, at the prompt" : s === "director" ? "the director, above the game" : "the " + s);
    });
    var brief = $("s-brief");
    clear(brief);
    option(brief, "", "the scenario's, if any");
    Object.keys(cat.briefs).forEach(function (b) { option(brief, b, "the starter: " + b); });
    option(brief, "*", "a file, or your words");
    var book = $("s-book");
    clear(book);
    option(book, "", "none (or the scenario's)");
    cat.books.forEach(function (b) { option(book, b); });
    // the doors' stations
    var ds = $("d-stations");
    clear(ds);
    var legend = document.createElement("legend");
    legend.textContent = "Stations";
    ds.appendChild(legend);
    cat.stations.forEach(function (s) {
      var l = document.createElement("label");
      l.className = "check";
      var c = document.createElement("input");
      c.type = "checkbox";
      c.value = s;
      c.setAttribute("data-station", s);
      l.appendChild(c);
      l.appendChild(document.createTextNode(" " + s));
      ds.appendChild(l);
    });
    // the maker's lists
    document.querySelectorAll("#maker select[data-options]").forEach(function (sel) {
      var what = sel.getAttribute("data-options");
      clear(sel);
      option(sel, "", "");
      (what === "regions" ? cat.regions.map(function (r) { return r.id; }) : cat[what]).forEach(function (v) { option(sel, v); });
    });
    var port = $("m-port");
    clear(port);
    option(port, "", "(choose to start in a port's road)");
    cat.ports.forEach(function (p) { option(port, p.id, p.name + ": " + p.road); });
    var bs = $("m-brief-starter"), bf = $("m-brief-from");
    clear(bs); clear(bf);
    Object.keys(cat.briefs).forEach(function (b) { option(bs, b); option(bf, b); });
    var books = $("m-books");
    clear(books);
    cat.books.forEach(function (b) {
      var l = document.createElement("label");
      l.className = "check";
      var c = document.createElement("input");
      c.type = "checkbox";
      c.value = b;
      c.setAttribute("data-book", b);
      l.appendChild(c);
      l.appendChild(document.createTextNode(" " + b));
      books.appendChild(l);
    });
    var st = $("m-stations");
    clear(st);
    ["captain", "officer", "master", "lookout", "director"].forEach(function (s) {
      var l = document.createElement("label");
      l.textContent = "the " + s + " ";
      var sel = document.createElement("select");
      sel.setAttribute("data-holder", s);
      option(sel, "", "");
      cat.holders.forEach(function (h) { option(sel, h); });
      l.appendChild(sel);
      st.appendChild(l);
    });
    $("m-place").textContent = "your scenarios: " + cat.scenarios_place;
    harbour.cat = cat;
  }

  function loadCatalogue() {
    return api("GET", "/api/harbour/catalogue").then(function (c) {
      cat = c;
      var keep = { s: $("s-scenario").value, m: $("m-pick").value };
      fillCatalogue();
      if (keep.s) $("s-scenario").value = keep.s;
      if (keep.m) $("m-pick").value = keep.m;
    });
  }

  // -- the game ------------------------------------------------------------------------

  var PACES = { pace: "the pace rule", lockstep: "lockstep", free: "free-running" };

  function onState(s) {
    var g = s.game;
    $("status").textContent = g.started ? "a game in play" : "no game yet";
    $("status").className = "ok";
    $("g-title").textContent = g.started ? g.title || "(a ship file)" : "none yet: start one below";
    $("g-ship").textContent = g.started ? g.ship : "";
    $("g-stamp").textContent = g.started ? g.stamp + ", tick " + g.tick : "";
    $("g-seed").textContent = g.started ? String(g.seed) : "";
    $("g-seat").textContent = g.started ? g.seat : "";
    $("g-director").textContent = g.started ? (g.director || "none") : "";
    $("g-pace").textContent = g.started ? (PACES[g.pace] || g.pace) + ", " + g.compression + "x" : "";
    $("game-clock").textContent = g.started ? (g.running ? "the clock runs" : "the clock is held until the driver says go") : "";
    $("to-game").hidden = !g.started;
    $("in-play-line").textContent = g.started
      ? (g.title || "a ship on open water") + (g.ship ? ", " + g.ship : "") + ", " + g.stamp + "; " + g.seat
      : "no game yet";
    var st = $("g-stations");
    clear(st);
    if (!s.stations.length) li(st, "none held", "muted");
    s.stations.forEach(function (x) {
      var line = x.line || "the " + x.station;
      var said = x.holder && line.indexOf(x.holder) >= 0;
      li(st, line + (x.holder && !said ? "  [" + x.holder + (x.door ? ", " + x.door : "") + "]" : ""));
    });
    fillSaves(s.saves);
    // where the saved games are, as the server has it for this run (not the settings'
    // field, which is taken only when the game is started again)
    if (s.saves) $("st-saves-says").textContent = "Your saved games are kept in " + s.saves.place + ". At the game's order line, 'save NAME' writes one there; the game tab takes one up.";
    fillStations(s);
    var gd = $("g-doors");
    clear(gd);
    if (!s.doors.length) li(gd, "none started from the harbour", "muted");
    s.doors.forEach(function (d) { li(gd, d.words, "door-" + d.state); });
    $("d-desktop-path").textContent = s.desktop.path;
    $("d-present").textContent = s.desktop.entries.length ? s.desktop.entries.join(", ") : "none";
    var cr = $("d-credential");
    clear(cr);
    s.credential.forEach(function (w) { li(cr, w); });
    s.doors.forEach(paneFor);
    beginState(s);
    harbour.state = s;
  }

  function poll() {
    api("GET", "/api/harbour/state").then(onState).catch(function () {
      $("status").textContent = "the server is not answering";
      $("status").className = "bad";
    }).then(function () { setTimeout(poll, 1500); });
    Object.keys(paneSince).forEach(readPane);
  }

  $("s-from").addEventListener("change", function () {
    var v = $("s-from").value;
    document.querySelectorAll("#start-form .from").forEach(function (l) {
      l.hidden = !l.classList.contains("from-" + v);
    });
    if (v === "scenario") {
      $("s-lines").hidden = !$("s-lines").textContent;
      $("s-aboard-label").hidden = $("s-aboard").options.length < 2;
    }
  });
  // the saved games of the saves place, newest first (package 96b, step 3): picking one
  // fills in its name; a name may still be typed (a save lying in the game's own folder)
  var savesKey = "";
  function fillSaves(saves) {
    if (!saves) return;
    var key = saves.place + "|" + saves.saves.map(function (x) { return x.name + x.written; }).join("|");
    if (key === savesKey) return;
    savesKey = key;
    var pick = $("s-load-pick"), kept = pick.value;
    clear(pick);
    option(pick, "", saves.saves.length ? "(choose a saved game)" : "(none saved yet)");
    saves.saves.forEach(function (x) { option(pick, x.name, x.name + "  (written " + x.written + ")"); });
    pick.value = kept;
    if (pick.selectedIndex < 0) pick.selectedIndex = 0;
    $("s-load-says").textContent = "Saved games are kept in " + saves.place + ". At the game's order line, 'save NAME' writes one there. A save kept elsewhere is taken up by moving it there.";
  }
  $("s-load-pick").addEventListener("change", function () {
    if ($("s-load-pick").value) $("s-load").value = $("s-load-pick").value;
  });
  $("s-scenario").addEventListener("change", scenarioSays);
  try { $("s-tests").checked = localStorage.getItem("harbour-tests") === "1"; } catch (e) { /* none */ }
  $("s-tests").addEventListener("change", function () {
    try { localStorage.setItem("harbour-tests", showTests() ? "1" : "0"); } catch (e) { /* none */ }
    if (cat) fillScenarios();
  });
  $("s-brief").addEventListener("change", function () {
    $("s-brief-file-label").hidden = $("s-brief").value !== "*";
  });

  $("start-form").addEventListener("submit", function (ev) {
    ev.preventDefault();
    var from = $("s-from").value;
    var brief = $("s-brief").value === "*" ? $("s-brief-file").value : $("s-brief").value;
    var body = {
      scenario: from === "scenario" ? $("s-scenario").value : "",
      ship: from === "ship" ? $("s-ship").value : "",
      load: from === "load" ? $("s-load").value : "",
      seed: $("s-seed").value,
      seat: $("s-seat").value,
      aboard: from === "scenario" ? $("s-aboard").value : "",
      wind: from === "ship" ? $("s-wind").value : "",
      heading: from === "ship" ? $("s-heading").value : "",
      time: $("s-time").value,
      pace: $("s-pace").value,
      crewed_cap: $("s-crewed-cap").value,
      crewed_range: $("s-crewed-range").value,
      business: $("s-business").value,
      director_brief: brief,
      standing_orders: $("s-book").value,
      ease_on_station: $("s-ease").checked,
    };
    $("btn-start").disabled = true;
    show($("start-words"), "Starting...");
    api("POST", "/api/harbour/start", body).then(function (r) {
      show($("start-words"), r.lines.join("\n"));
      $("start-words").classList.remove("refusal");
      $("btn-to-game").hidden = false;
      return api("GET", "/api/harbour/state").then(onState); // the new game's stations at once
    }).catch(function (e) {
      show($("start-words"), e.message);
      $("start-words").classList.add("refusal");
    }).then(function () { $("btn-start").disabled = false; });
  });

  // -- the doors -----------------------------------------------------------------------

  function ticked() {
    return Array.prototype.map.call(document.querySelectorAll("#d-stations input:checked"), function (c) { return c.value; });
  }

  $("btn-desktop-show").addEventListener("click", function () {
    api("POST", "/api/harbour/desktop", { stations: ticked(), ship: $("d-ship").value }).then(function (r) {
      show($("d-desktop-text"), "The client's file, " + r.path + ", would read:\n\n" + r.text + (r.named ? "" : "\nThe model's name is not in the settings yet: the entries say where it goes."));
      $("btn-desktop-write").disabled = false;
    }).catch(function (e) { show($("d-desktop-text"), e.message); });
  });
  $("btn-desktop-write").addEventListener("click", function () {
    if (!window.confirm("Write these entries into the desktop client's file? The file as it is now is kept beside it (.bak).")) return;
    api("POST", "/api/harbour/desktop", { stations: ticked(), ship: $("d-ship").value, write: true }).then(function (r) {
      show($("d-desktop-text"), "Written to " + r.path + (r.backup ? " (the old file kept as " + r.backup + ")" : "") + ". Quit the desktop client fully and start it again.\n\n" + r.text);
      $("btn-desktop-write").disabled = true;
    }).catch(function (e) { show($("d-desktop-text"), e.message); });
  });

  // -- who is where (package 96b, step 9; docs/design/Design-Harbour.md §2.6) -----------
  //
  // One table for the game in play: each station of the player's ship, the director's
  // above the game, and the captain's of every other ship with a captain of her own; who
  // holds it now, what the scenario says of it, and a door to give it to a model: the API
  // door with one of the models the settings can call, or the local runner. A door asks
  // its model for consent in its own pane, as ever: the table starts the door and no more.

  var SHIP_STATIONS = ["captain", "officer", "master", "lookout", "passenger"];
  var tableKey = "";
  function heldWords(s, station, ship) {
    var held = s.stations.filter(function (x) {
      var st = String(x.station || "").toLowerCase();
      return (st === station || st.indexOf(station) >= 0) && String(x.ship || "") === ship;
    })[0];
    if (held) return held.holder === "the player" ? "you" : (held.holder || "a model") + (held.door ? " (" + held.door + ")" : "");
    var door = s.doors.filter(function (d) { return d.state === "running" && d.station === station && String(d.ship || "") === ship; })[0];
    if (door) return "a door is asking (" + (door.door === "api" ? "the API door" : "the local runner") + ")";
    if (station === "captain" && !ship && s.game.seat.indexOf("captain's prompt") >= 0) return "you, at the prompt";
    return "the game's own";
  }
  function fillStations(s) {
    var g = s.game, plan = (g.chosen && g.chosen.plan) || {};
    var models = Object.keys(s.models || {});
    var key = JSON.stringify([g.started, g.title, g.seed, g.captains, plan, models, s.stations, s.doors.map(function (d) { return [d.id, d.state]; }), g.seat]);
    if (key === tableKey) return;
    tableKey = key;
    var body = $("t-stations").querySelector("tbody");
    var kept = {};
    body.querySelectorAll("tr").forEach(function (tr) { kept[tr.getAttribute("data-row")] = [tr.querySelector(".t-door").value, tr.querySelector(".t-model").value]; });
    clear(body);
    $("t-none").hidden = !!g.started;
    $("t-stations").hidden = !g.started;
    if (!g.started) { $("btn-t-all").disabled = true; $("t-says").textContent = ""; return; }
    var rows = SHIP_STATIONS.map(function (st) { return [g.ship || "your ship", st, ""]; });
    rows.push(["above the game", "director", ""]);
    (g.captains || []).forEach(function (name) { rows.push([name, "captain", name]); });
    var asked = 0;
    rows.forEach(function (r) {
      var station = r[1], ship = r[2], id = station + "|" + ship;
      var tr = document.createElement("tr");
      tr.setAttribute("data-row", id);
      tr.setAttribute("data-station", station);
      tr.setAttribute("data-ship", ship);
      var held = heldWords(s, station, ship);
      var says = ship ? "" : plan[station] || "";
      [r[0] + (ship ? "" : station === "director" ? "" : " (yours)"), "the " + station, held, says === "player" ? "you" : says === "model" ? "a model" : says === "rules" ? "the game's own" : ""].forEach(function (w, i) {
        var td = document.createElement("td");
        td.textContent = w;
        if (i === 2) td.className = "t-held";
        tr.appendChild(td);
      });
      var free = held === "the game's own";
      var td = document.createElement("td");
      var door = document.createElement("select");
      door.className = "t-door";
      option(door, "", "");
      option(door, "api", "the API door");
      option(door, "local", "the local runner");
      td.appendChild(door);
      tr.appendChild(td);
      td = document.createElement("td");
      var model = document.createElement("select");
      model.className = "t-model";
      option(model, "", models.length ? "the door's own (" + models[0] + ")" : "none named in the settings");
      models.forEach(function (m) { option(model, m); });
      td.appendChild(model);
      tr.appendChild(td);
      if (kept[id]) { door.value = kept[id][0]; model.value = kept[id][1]; }
      else if (says === "model" && free) door.value = "api";
      model.disabled = door.value !== "api";
      door.addEventListener("change", function () { model.disabled = door.value !== "api"; });
      td = document.createElement("td");
      var b = document.createElement("button");
      b.type = "button";
      b.className = "t-start";
      b.textContent = "start its door";
      b.disabled = !free;
      b.addEventListener("click", function () { startRow(tr); });
      td.appendChild(b);
      tr.appendChild(td);
      if (says === "model" && free) { tr.classList.add("t-asked"); asked += 1; }
      body.appendChild(tr);
    });
    $("btn-t-all").disabled = !asked;
    $("t-says").textContent = asked ? "The scenario gives " + plural(asked, "station", "stations") + " to a model, not yet held." : Object.keys(plan).length ? "" : "This game's scenario says nothing of its stations: you are where you chose, and the rest are the game's own.";
  }
  function startRow(tr) {
    var door = tr.querySelector(".t-door").value;
    if (!door) { show($("t-error"), "Choose the door for the " + tr.getAttribute("data-station") + "'s station: the API door or the local runner."); return Promise.resolve(); }
    show($("t-error"), "");
    return api("POST", "/api/harbour/doors", {
      door: door, station: tr.getAttribute("data-station"), ship: tr.getAttribute("data-ship"),
      model: door === "api" ? tr.querySelector(".t-model").value : "",
    }).then(paneFor).catch(function (e) { show($("t-error"), e.message); });
  }
  $("btn-t-all").addEventListener("click", function () {
    document.querySelectorAll("#t-stations tr.t-asked").forEach(startRow);
  });

  function startDoor(kind) {
    var stations = ticked();
    if (!stations.length) { show($("d-door-error"), "Tick the station the door is to ask for."); return; }
    show($("d-door-error"), "");
    stations.forEach(function (s) {
      api("POST", "/api/harbour/doors", { door: kind, station: s, ship: $("d-ship").value }).then(paneFor).catch(function (e) {
        show($("d-door-error"), e.message);
      });
    });
  }
  $("btn-door-api").addEventListener("click", function () { startDoor("api"); });
  $("btn-door-local").addEventListener("click", function () { startDoor("local"); });

  function paneFor(d) {
    var pane = $("pane-" + d.id);
    if (!pane) {
      pane = document.createElement("div");
      pane.id = "pane-" + d.id;
      pane.className = "door-pane";
      pane.innerHTML = '<div class="door-head"><span class="door-words"></span> <button type="button" class="door-stop">stop</button></div>' +
        '<pre class="door-out"></pre>' +
        '<div class="command-line"><span class="prompt">owner&gt;</span><input type="text" class="door-say" placeholder="a line to the door\'s terminal (your word in a consent conversation; Enter sends)"></div>';
      $("d-panes").appendChild(pane);
      pane.querySelector(".door-stop").addEventListener("click", function () {
        api("POST", "/api/harbour/doors/" + d.id + "/stop").then(paneFor);
      });
      pane.querySelector(".door-say").addEventListener("keydown", function (ev) {
        if (ev.key !== "Enter") return;
        var input = ev.target;
        api("POST", "/api/harbour/doors/" + d.id + "/say", { text: input.value }).catch(function (e) {
          pane.querySelector(".door-out").textContent += "\n" + e.message;
        });
        input.value = "";
      });
      paneSince[d.id] = 0;
      readPane(d.id);
    }
    pane.querySelector(".door-words").textContent = d.words;
    // the director's seats' doors marked as such beside the owner's own (package 67)
    pane.className = "door-pane door-" + d.state + (d.by ? " door-director" : "");
    pane.querySelector(".door-stop").disabled = d.state !== "running";
  }

  function readPane(id) {
    api("GET", "/api/harbour/doors/" + id + "?since=" + paneSince[id]).then(function (r) {
      var out = $("pane-" + id).querySelector(".door-out");
      if (r.output.length) {
        out.textContent += (out.textContent ? "\n" : "") + r.output.join("\n");
        out.scrollTop = out.scrollHeight;
      }
      paneSince[id] = r.count;
      if (r.state !== "running" && !r.output.length) delete paneSince[id];
    }).catch(function () { delete paneSince[id]; });
  }

  // -- the scenario maker --------------------------------------------------------------
  //
  // The form starts from the fields read (`loaded`), and only the fields touched since are
  // written over them (`dirty`): the server then keeps every untouched block of the file
  // as it was, byte for byte. A new scenario writes every field the form has a value for.

  var loaded = null; // {path, name, fields, position_deg}
  var dirty = {};
  var fresh = true;

  function getPath(obj, path) {
    var parts = path.split(".");
    for (var i = 0; i < parts.length; i++) {
      if (obj === null || typeof obj !== "object" || !(parts[i] in obj)) return undefined;
      obj = obj[parts[i]];
    }
    return obj;
  }
  function setPath(obj, path, value) {
    var parts = path.split(".");
    var o = obj;
    for (var i = 0; i < parts.length - 1; i++) {
      if (o[parts[i]] === null || typeof o[parts[i]] !== "object" || Array.isArray(o[parts[i]])) o[parts[i]] = {};
      o = o[parts[i]];
    }
    o[parts[parts.length - 1]] = value;
  }
  function delPath(obj, path) {
    var parts = path.split(".");
    var chain = [obj];
    for (var i = 0; i < parts.length - 1; i++) {
      var next = chain[i][parts[i]];
      if (next === null || typeof next !== "object") return;
      chain.push(next);
    }
    delete chain[chain.length - 1][parts[parts.length - 1]];
    for (var j = chain.length - 1; j > 0; j--) {
      if (Object.keys(chain[j]).length) break;
      delete chain[j - 1][parts[j - 1]];
    }
  }

  function markDirty(field) { dirty[field] = true; }

  document.querySelectorAll("#maker [data-field]").forEach(function (el) {
    var ev = el.tagName === "SELECT" || el.type === "checkbox" ? "change" : "input";
    el.addEventListener(ev, function () { markDirty(el.getAttribute("data-field")); });
  });
  $("maker").addEventListener("change", function (ev) {
    var t = ev.target;
    if (t.hasAttribute("data-holder")) markDirty("stations");
    if (t.hasAttribute("data-book")) markDirty("standing_orders");
    if (t.hasAttribute("data-brief")) markDirty("director");
    if (t.closest && t.closest("#m-ships")) markDirty("ships");
    if (t.closest && t.closest("#m-squadrons")) markDirty("squadrons");
    if (t.closest && t.closest("#m-people")) markDirty("people");
    if (t.closest && t.closest("#m-chron")) { markDirty("papers.chronometer"); chronShown(); }
    if (t.closest && t.closest("#m-wind")) markDirty("weather");
    if (t.closest && t.closest("#m-world-orders")) markDirty("world_orders");
  });
  $("maker").addEventListener("input", function (ev) {
    if (ev.target.closest && ev.target.closest("#m-people")) markDirty("people");
    if (ev.target.closest && ev.target.closest("#m-chron")) markDirty("papers.chronometer");
    if (ev.target.closest && ev.target.closest("#m-squadrons")) markDirty("squadrons");
    var t = ev.target;
    if (t.hasAttribute("data-brief")) markDirty("director");
    if (t.closest && t.closest("#m-ships")) markDirty("ships");
    if (t.closest && t.closest("#m-wind")) markDirty("weather");
    if (t.closest && t.closest("#m-world-orders")) markDirty("world_orders");
  });

  // the tables' rows
  function cell(tr, value, kind, opts) {
    var td = document.createElement("td");
    var el;
    if (kind === "select") {
      el = document.createElement("select");
      option(el, "", "");
      (opts || []).forEach(function (o) { option(el, o); });
      if (value !== undefined && value !== null && opts.indexOf(String(value)) < 0) option(el, String(value));
      el.value = value === undefined || value === null ? "" : String(value);
    } else {
      el = document.createElement("input");
      el.type = kind === "number" ? "number" : "text";
      if (kind === "number") el.step = "any";
      el.value = value === undefined || value === null ? "" : String(value);
    }
    td.appendChild(el);
    tr.appendChild(td);
    return el;
  }
  function removeButton(tr, field) {
    var td = document.createElement("td");
    var b = document.createElement("button");
    b.type = "button";
    b.textContent = "x";
    b.title = "take this row out";
    b.addEventListener("click", function () { tr.parentNode.removeChild(tr); markDirty(field); });
    td.appendChild(b);
    tr.appendChild(td);
  }

  // -- the ship's card (package 96b, step 5; docs/design/Design-Harbour.md §2.4) ---------
  //
  // One card for every ship. Another ship's is here: its head is what she is, her name,
  // her nation, her fit and what she is about; the rest is behind "more about her". The
  // card fills its blanks from her kind's own words (the catalogue's `kinds` and `fits`)
  // and invents nothing; what the game does not take for another ship is said, greyed.
  // A key of her entry the card has no field for, or whose value is not plain words, is
  // kept as the file has it.

  function kindOf(id) { return (cat.kinds || []).filter(function (k) { return k.id === id; })[0]; }
  function fitsOf(file) { return (cat.fits || {})[file] || { fits: [], "default": "" }; }
  function setOptions(sel, pairs, value) {
    clear(sel);
    pairs.forEach(function (p) { option(sel, p[0], p[1]); });
    var v = value === undefined || value === null ? "" : String(value);
    if (v !== "" && !pairs.some(function (p) { return p[0] === v; })) option(sel, v, v + "  (as written; not one of hers)");
    sel.value = v;
  }
  function fitPairs(file, own) {
    var f = fitsOf(file);
    var pairs = [["", own || (f["default"] ? "her file's own (" + f["default"] + ")" : "her file's own")]];
    f.fits.forEach(function (n) { pairs.push([n, n]); });
    if (f.fits.indexOf("unarmed") < 0) pairs.push(["unarmed", "unarmed"]);
    return pairs;
  }
  function fillShipFit(file, value) { setOptions($("m-ship-fit"), fitPairs(file), value); }
  function degMin(v, pos, neg) {
    var a = Math.abs(v), d = Math.floor(a), m = Math.round((a - d) * 600) / 10;
    if (m >= 60) { d += 1; m = 0; }
    return d + " " + m + " " + (v >= 0 ? pos : neg);
  }
  function positionWords(lat, lon) { return degMin(lat, "N", "S") + " " + degMin(lon, "E", "W"); }

  var SHIP_HEAD = [
    ["description", "What she is", "kinds"], ["name", "Her name", "text"], ["nation", "Her nation", "nations"],
    ["fit", "Her fit of guns", "fit"], ["goal", "What she is about (her goal)", "text", "trading Falmouth to Plymouth; patrolling off the Lizard; bound for Brest"],
  ];
  var SHIP_MORE = [
    ["id", "Her id (for the orders and the squadrons)", "text"],
    ["position", "Where she lies", "text", "49 50 N 5 30 W, or a place of the chart"],
    ["role", "Her role", "role"],
    ["colours", "Her colours at the start", "colours"],
    ["intent", "A captain of her own, sailing her by this intent", "text", "trade tin from Falmouth to Brest"],
    ["free_intent", "Or a goal in any words, for a model who is to command her", "text"],
    ["squadron", "Her squadron (its id)", "text"],
    ["under_the_orders_of", "Whose signals she obeys", "text", "the ship (yours), or another's name"],
    ["lights", "Her lights at night", "lights"],
    ["departing", "The port she is leaving", "ports"],
    ["sailing_factor", "How well she sails (1 is her kind's own)", "number"],
    ["letter", "A letter she carries for you", "text"],
    ["regime", "Laid up", "regime"],
    ["sortie", "When she is to come out, if laid up", "text"],
  ];
  function cardField(card, box, spec) {
    var col = spec[0], kind = spec[2], value = card._item[col];
    var l = document.createElement("label");
    l.appendChild(document.createTextNode(spec[1] + " "));
    var el;
    if (kind === "text" || kind === "number") {
      el = document.createElement("input");
      el.type = kind === "number" ? "number" : "text";
      if (kind === "number") { el.step = "any"; el.setAttribute("data-kind", "number"); }
      if (spec[3]) el.placeholder = spec[3];
      el.value = value === undefined || value === null ? "" : String(value);
    } else {
      el = document.createElement("select");
      var pairs = [["", ""]];
      if (kind === "kinds") (cat.kinds || []).forEach(function (k) { pairs.push([k.id, k.id]); });
      else if (kind === "nations") cat.nations.forEach(function (n) { pairs.push([n, nationWords(n)]); });
      else if (kind === "colours") {
        pairs = [["", "shown (her own)"], ["shown", "shown (her own)"], ["none", "none shown"]];
        cat.nations.forEach(function (n) { pairs.push([n, "false colours: " + nationWords(n)]); });
      } else if (kind === "lights") pairs = pairs.concat([["none", "none"], ["stern lantern", "a stern lantern"], ["top lights", "top lights"], ["a lantern at her nets", "a lantern at her nets"]]);
      else if (kind === "ports") cat.ports.forEach(function (x) { pairs.push([x.id, x.name]); });
      else if (kind === "regime") pairs.push(["in ordinary", "in ordinary (laid up at the port she lies off)"]);
      setOptions(el, pairs, value);
    }
    if (value !== null && typeof value === "object") {
      // a value that is not plain words (a place as latitude and longitude, a letter with
      // its origin): kept as the file has it, shown and not changed here
      el.disabled = true;
      if (el.tagName === "INPUT") { el.value = ""; el.placeholder = "written out in the file; kept as it is"; }
    }
    el.setAttribute("data-col", col);
    l.appendChild(el);
    box.appendChild(l);
    return el;
  }
  function shipCardKind(card) {
    var kind = kindOf(card.querySelector('[data-col="description"]').value);
    var fit = card.querySelector('[data-col="fit"]'), role = card.querySelector('[data-col="role"]');
    setOptions(fit, fitPairs(kind ? kind.file : "", kind && kind.fit ? "her kind's own (" + kind.fit + ")" : "her kind's own"), fit._kept !== undefined ? fit._kept : fit.value);
    var roles = [["", kind && kind.roles.length ? "by what she is about (" + kind.roles.join(", ") + ")" : "her file gives her kind no role"]];
    (kind ? kind.roles : []).forEach(function (r) { roles.push([r, r]); });
    setOptions(role, roles, role._kept !== undefined ? role._kept : role.value);
    delete fit._kept; delete role._kept;
    var says = card.querySelector(".card-says");
    says.textContent = kind ? cap(kind.what) + ", " + kind.rig + (kind.fit ? "; as that she carries " + kind.fit : "") + (kind.roles.length ? "; she may be " + kind.roles.join(", ") : "") + "." : "Choose what she is.";
  }
  function shipRow(item) {
    var card = document.createElement("div");
    card.className = "ship-card";
    card._item = item || {};
    var head = document.createElement("div");
    head.className = "card-grid";
    card.appendChild(head);
    SHIP_HEAD.forEach(function (s) {
      var el = cardField(card, head, s[2] === "fit" ? [s[0], s[1], "select"] : s);
      if (s[2] === "fit") el._kept = card._item.fit === undefined ? "" : card._item.fit;
    });
    var says = document.createElement("p");
    says.className = "card-says";
    card.appendChild(says);
    var more = document.createElement("details");
    more.className = "more";
    var sum = document.createElement("summary");
    sum.textContent = "more about her";
    more.appendChild(sum);
    var grid = document.createElement("div");
    grid.className = "card-grid";
    more.appendChild(grid);
    SHIP_MORE.forEach(function (s) {
      var el = cardField(card, grid, s[2] === "role" ? [s[0], s[1], "select"] : s);
      if (s[2] === "role") el._kept = card._item.role === undefined ? "" : card._item.role;
    });
    // where she lies: by a port's road, or by a bearing and distance from your own ship
    var place = document.createElement("div");
    place.className = "card-place";
    place.innerHTML = '<span>Put her</span> <select class="card-port"></select> <span>or</span> <input type="number" class="card-bearing" min="0" max="360" step="any" placeholder="bearing from you"> <input type="number" class="card-miles" min="0" step="any" placeholder="miles"> <button type="button" class="card-put">there</button>';
    more.appendChild(place);
    var port = place.querySelector(".card-port");
    option(port, "", "(at a port's road)");
    cat.ports.forEach(function (x) { option(port, x.id, x.name + ": " + x.road); });
    var where = grid.querySelector('[data-col="position"]');
    port.addEventListener("change", function () {
      var x = cat.ports.filter(function (y) { return y.id === port.value; })[0];
      if (!x || where.disabled) return;
      where.value = positionWords(x.lat_deg, x.lon_deg);
      markDirty("ships"); foldLines();
    });
    place.querySelector(".card-put").addEventListener("click", function () {
      var lat = parseFloat($("m-lat").value), lon = parseFloat($("m-lon").value);
      var brg = parseFloat(place.querySelector(".card-bearing").value), nm = parseFloat(place.querySelector(".card-miles").value);
      if (!isFinite(lat) || !isFinite(lon) || !isFinite(brg) || !isFinite(nm) || where.disabled) return;
      var rad = brg * Math.PI / 180;
      var lat2 = lat + nm * Math.cos(rad) / 60;
      var lon2 = lon + nm * Math.sin(rad) / (60 * Math.cos((lat + lat2) / 2 * Math.PI / 180));
      where.value = positionWords(lat2, lon2);
      markDirty("ships"); foldLines();
    });
    ["Her heading at the start: the game does not take this for another ship; she heads for the first mark of her goal.",
     "Her people, her company and her cargo: the game does not yet take these for another ship; she is mustered from her file when she comes close.",
     "Who holds a station aboard her: not written in a scenario yet; a door is started for her on the doors tab once the game is in play."].forEach(function (w) {
      var p = document.createElement("p");
      p.className = "not-yet";
      p.textContent = w;
      more.appendChild(p);
    });
    card.appendChild(more);
    var b = document.createElement("button");
    b.type = "button";
    b.className = "card-remove";
    b.textContent = "take her out";
    b.addEventListener("click", function () { card.parentNode.removeChild(card); markDirty("ships"); foldLines(); });
    card.appendChild(b);
    card.querySelector('[data-col="description"]').addEventListener("change", function () { shipCardKind(card); });
    $("m-ships").appendChild(card);
    shipCardKind(card);
  }
  function shipsOf() {
    return Array.prototype.map.call(document.querySelectorAll("#m-ships .ship-card"), function (card) {
      var item = deep(card._item) || {};
      card.querySelectorAll("[data-col]").forEach(function (el) {
        if (el.disabled) return;
        var k = el.getAttribute("data-col"), v = el.value.trim(), had = card._item[k];
        if (v === "") delete item[k];
        else if (had !== undefined && had !== null && String(had) === v) item[k] = had; // as it was, a number a number
        else item[k] = el.getAttribute("data-kind") === "number" ? Number(v) : v;
      });
      return item;
    }).filter(function (item) { return Object.keys(item).length; });
  }
  // -- a squadron's card (package 96b, step 6; docs/design/Design-Harbour.md §2.3) -------
  //
  // A squadron or a convoy is a set of the scenario's ships, the player's among them if he
  // likes: its name, its kind, its formation, its commander and its members ticked from
  // the ships; the rest behind "more". The members are written in the squadron's own entry
  // (`squadrons: members`), by each ship's id (her name where she has none) and the
  // player's ship by the game's own words for her.

  function shipChoices() {
    var me = (cat.squadrons || {}).player || "the ship";
    var out = [[me, "your own ship"]];
    document.querySelectorAll("#m-ships .ship-card").forEach(function (card) {
      var id = card.querySelector('[data-col="id"]').value.trim(), name = card.querySelector('[data-col="name"]').value.trim();
      var key = id || name;
      if (key) out.push([key, name || id]);
    });
    return out;
  }
  function squadronChoices(card) {
    var choices = shipChoices();
    var known = choices.map(function (c) { return c[0]; });
    var cmd = card.querySelector('[data-col="commander"]');
    setOptions(cmd, [["", "your own ship (when none is said)"]].concat(choices), cmd._kept !== undefined ? cmd._kept : cmd.value);
    delete cmd._kept;
    var box = card.querySelector(".card-members");
    var ticked = card._members !== undefined ? card._members : Array.prototype.map.call(box.querySelectorAll("input:checked"), function (c) { return c.value; });
    delete card._members;
    clear(box);
    ticked.forEach(function (m) { if (known.indexOf(m) < 0) choices.push([m, m + " (as written; no ship above)"]); });
    choices.forEach(function (c) {
      var l = document.createElement("label");
      l.className = "check";
      var x = document.createElement("input");
      x.type = "checkbox";
      x.value = c[0];
      x.checked = ticked.indexOf(c[0]) >= 0;
      l.appendChild(x);
      l.appendChild(document.createTextNode(" " + c[1]));
      box.appendChild(l);
    });
  }
  var SQUADRON_HEAD = [["name", "Its name", "text", "the inshore squadron"], ["kind", "A squadron or a convoy", "kinds"], ["formation", "Its formation", "formations"], ["commander", "Its commander", "commander"]];
  var SQUADRON_MORE = [
    ["id", "Its id (for the orders)", "text"], ["interval_cables", "The interval between ships (cables)", "number"],
    ["columns", "Columns (the order of sailing)", "number"], ["rendezvous", "Its rendezvous", "text", "Torbay"],
    ["goal", "What it is about, when not its commander's own intent", "text"], ["book", "The book it sails by", "books"],
    ["regime", "Its regime", "text", "in convoy"],
  ];
  function squadronField(card, box, spec) {
    var col = spec[0], kind = spec[2], value = card._item[col], el;
    var l = document.createElement("label");
    l.appendChild(document.createTextNode(spec[1] + " "));
    if (kind === "text" || kind === "number") {
      el = document.createElement("input");
      el.type = kind === "number" ? "number" : "text";
      if (kind === "number") { el.step = "any"; el.setAttribute("data-kind", "number"); }
      if (spec[3]) el.placeholder = spec[3];
      el.value = value === undefined || value === null ? "" : String(value);
    } else {
      el = document.createElement("select");
      var sq = cat.squadrons || { kinds: [], formations: [], books: [] };
      var pairs = [["", kind === "kinds" ? "a squadron, or a convoy if it has merchantmen" : kind === "formations" ? "line ahead (a convoy: the order of sailing)" : kind === "books" ? "its kind's own" : ""]];
      if (kind === "kinds") sq.kinds.forEach(function (k) { pairs.push([k, "a " + k]); });
      else if (kind === "formations") sq.formations.forEach(function (k) { pairs.push([k, k]); });
      else if (kind === "books") sq.books.forEach(function (k) { pairs.push([k, "the " + k + " book"]); });
      if (kind === "commander") el._kept = value === undefined || value === null ? "" : String(value);
      else setOptions(el, pairs, value);
    }
    el.setAttribute("data-col", col);
    l.appendChild(el);
    box.appendChild(l);
    return el;
  }
  function squadronRow(item) {
    var card = document.createElement("div");
    card.className = "ship-card squadron-card";
    card._item = item || {};
    card._members = Array.isArray(card._item.members) ? card._item.members.map(String) : [];
    var head = document.createElement("div");
    head.className = "card-grid";
    card.appendChild(head);
    SQUADRON_HEAD.forEach(function (s) { squadronField(card, head, s); });
    var mem = document.createElement("fieldset");
    mem.className = "checks card-members-box";
    var lg = document.createElement("legend");
    lg.textContent = "Its members";
    mem.appendChild(lg);
    var box = document.createElement("div");
    box.className = "card-members";
    mem.appendChild(box);
    card.appendChild(mem);
    var more = document.createElement("details");
    more.className = "more";
    var sum = document.createElement("summary");
    sum.textContent = "more about it";
    more.appendChild(sum);
    var grid = document.createElement("div");
    grid.className = "card-grid";
    more.appendChild(grid);
    SQUADRON_MORE.forEach(function (s) { squadronField(card, grid, s); });
    card.appendChild(more);
    var b = document.createElement("button");
    b.type = "button";
    b.className = "card-remove";
    b.textContent = "take it out";
    b.addEventListener("click", function () { card.parentNode.removeChild(card); markDirty("squadrons"); foldLines(); });
    card.appendChild(b);
    $("m-squadrons").appendChild(card);
    squadronChoices(card);
  }
  function refreshSquadrons() { document.querySelectorAll("#m-squadrons .squadron-card").forEach(squadronChoices); }
  function squadronsOf() {
    return Array.prototype.map.call(document.querySelectorAll("#m-squadrons .squadron-card"), function (card) {
      var item = deep(card._item) || {};
      card.querySelectorAll("[data-col]").forEach(function (el) {
        var k = el.getAttribute("data-col"), v = el.value.trim(), had = card._item[k];
        if (v === "") delete item[k];
        else if (had !== undefined && had !== null && String(had) === v) item[k] = had;
        else item[k] = el.getAttribute("data-kind") === "number" ? Number(v) : v;
      });
      var ticked = Array.prototype.map.call(card.querySelectorAll(".card-members input:checked"), function (c) { return c.value; });
      var had = Array.isArray(card._item.members) ? card._item.members.map(String) : [];
      var same = had.length === ticked.length && had.every(function (m) { return ticked.indexOf(m) >= 0; });
      if (same) { if (card._item.members !== undefined) item.members = card._item.members; } // as written, in its order
      else if (ticked.length) item.members = had.filter(function (m) { return ticked.indexOf(m) >= 0; }).concat(ticked.filter(function (m) { return had.indexOf(m) < 0; }));
      else delete item.members;
      return item;
    }).filter(function (item) { return Object.keys(item).length; });
  }
  $("btn-m-squadron-add").addEventListener("click", function () { squadronRow({}); markDirty("squadrons"); });
  // the ships named above are the squadrons' choices: a ship added, renamed or taken out
  $("m-ships").addEventListener("change", refreshSquadrons);
  $("m-ships").addEventListener("click", function (ev) { if (ev.target.tagName === "BUTTON") setTimeout(refreshSquadrons, 0); });
  $("btn-m-ship-add").addEventListener("click", function () { setTimeout(refreshSquadrons, 0); });

  // -- her papers, her purse and her people (package 96b, step 7; the design's §2.3) -----

  function goodsWords(goods) {
    return Object.keys(goods || {}).map(function (g) { return g + " " + goods[g]; }).join(", ");
  }
  function goodsOf(text) {
    // "tin 20, pilchards 4.5": each a good and its tons; undefined where none is said,
    // null where a part cannot be read (the field is then left as the file has it)
    var out = {}, parts = text.split(",").map(function (s) { return s.trim(); }).filter(Boolean), bad = false;
    parts.forEach(function (part) {
      var m = /^(.*\S)\s+(-?\d+(?:\.\d+)?)$/.exec(part);
      if (!m) { bad = true; return; }
      out[m[1].trim()] = Number(m[2]);
    });
    return bad ? null : parts.length ? out : undefined;
  }
  function chronShown() { $("m-chron-fields").hidden = !$("m-chron-on").checked; }
  function fillChron(fields) {
    var onShip = getPath(fields, "ship.chronometer") || fields.chronometer;
    var c = getPath(fields, "papers.chronometer");
    var locked = !!onShip;
    $("m-chron-on").checked = !!(c || onShip);
    $("m-chron-on").disabled = locked;
    document.querySelectorAll("#m-chron [data-chron]").forEach(function (el) {
      var v = (c || onShip || {})[el.getAttribute("data-chron")];
      el.value = v === undefined || v === null ? "" : String(v);
      el.disabled = locked;
    });
    $("m-chron")._item = c && typeof c === "object" ? c : {};
    $("m-chron-said").textContent = locked ? "Her chronometer is written on the ship's own line of the file, which wins: kept as it is." : "";
    chronShown();
  }
  function chronOf() {
    if (!$("m-chron-on").checked) return undefined;
    var item = deep($("m-chron")._item) || {};
    document.querySelectorAll("#m-chron [data-chron]").forEach(function (el) {
      var k = el.getAttribute("data-chron"), v = el.value.trim(), had = $("m-chron")._item[k];
      if (v === "") delete item[k];
      else if (had !== undefined && had !== null && String(had) === v) item[k] = had;
      else item[k] = el.hasAttribute("data-num") || (k === "drift" && v.toLowerCase() !== "seeded" && isFinite(Number(v))) ? Number(v) : v;
    });
    if (!item.maker) item.maker = "the chronometer";
    return item;
  }
  var PEOPLE_COLS = [["role", "text"], ["name", "text"], ["skill", "number"], ["place", "text"], ["ashore", "select", ["yes"]], ["port", "select", "ports"]];
  function personRow(item) {
    var tr = document.createElement("tr");
    tr._item = item || {};
    PEOPLE_COLS.forEach(function (c) {
      var opts = c[2] === "ports" ? cat.ports.map(function (x) { return x.id; }) : c[2];
      var value = tr._item[c[0]];
      if (c[0] === "ashore") value = value ? "yes" : undefined;
      var el = cell(tr, value, c[1], opts);
      el.setAttribute("data-col", c[0]);
      el.setAttribute("data-kind", c[1]);
      if (c[0] === "role") { el.setAttribute("list", "m-posts"); el.placeholder = "master, supercargo"; }
      if (c[0] === "skill") { el.min = "0"; el.max = "1"; el.placeholder = "0.7"; }
      if (c[0] === "place") el.placeholder = "cabin";
    });
    removeButton(tr, "people");
    $("m-people").querySelector("tbody").appendChild(tr);
  }
  function peopleOf() {
    return Array.prototype.map.call(document.querySelectorAll("#m-people tbody tr"), function (tr) {
      var item = deep(tr._item) || {};
      tr.querySelectorAll("[data-col]").forEach(function (el) {
        var k = el.getAttribute("data-col"), v = el.value.trim(), had = tr._item[k];
        if (k === "ashore") { if (v === "yes") item.ashore = had === undefined || !had ? true : had; else delete item.ashore; return; }
        if (v === "") delete item[k];
        else if (had !== undefined && had !== null && String(had) === v) item[k] = had;
        else item[k] = el.getAttribute("data-kind") === "number" ? Number(v) : v;
      });
      return item;
    }).filter(function (item) { return Object.keys(item).length; });
  }
  function fillPosts(file) {
    var list = $("m-posts");
    clear(list);
    ((cat.posts || {})[file] || []).forEach(function (r) { option(list, r); });
  }
  $("btn-m-person-add").addEventListener("click", function () { personRow({}); markDirty("people"); });
  function fillThings(things) {
    var el = $("m-things"), list = Array.isArray(things) ? things : [];
    var plain = list.every(function (x) { return typeof x === "string"; });
    el.disabled = !plain;
    el.value = plain ? list.join("\n") : "";
    el.placeholder = plain ? "a sealed packet, in the captain's keeping" : "written out in the file (a thing with its name, where and description apart): kept as it is";
  }

  var WIND_COLS = [["at", "text"], ["from_deg", "number"], ["knots", "number"], ["air_mass", "select", ["neutral", "warm", "unstable"]]];
  function windRow(item) {
    var tr = document.createElement("tr");
    tr._item = item || {};
    WIND_COLS.forEach(function (c) {
      var el = cell(tr, tr._item[c[0]], c[1], c[2]);
      el.setAttribute("data-col", c[0]);
      el.setAttribute("data-kind", c[1]);
    });
    removeButton(tr, "weather");
    $("m-wind").querySelector("tbody").appendChild(tr);
  }
  function orderRow(item) {
    var tr = document.createElement("tr");
    tr._item = item || {};
    cell(tr, tr._item.at, "text").setAttribute("data-col", "at");
    var o = cell(tr, tr._item.order, "text");
    o.setAttribute("data-col", "order");
    o.className = "long";
    removeButton(tr, "world_orders");
    $("m-world-orders").querySelector("tbody").appendChild(tr);
  }
  $("btn-m-ship-add").addEventListener("click", function () { shipRow({}); markDirty("ships"); });
  $("maker").querySelector('[data-field="ship.file"]').addEventListener("change", function (ev) {
    fillPosts(ev.target.value);
    fillShipFit(ev.target.value, $("m-ship-fit").value);
  });
  $("btn-m-wind-add").addEventListener("click", function () { windRow({}); markDirty("weather"); setWeatherMode("pinned"); });
  $("btn-m-order-add").addEventListener("click", function () { orderRow({}); markDirty("world_orders"); });

  function rowsOf(table, numeric) {
    return Array.prototype.map.call(document.querySelectorAll("#" + table + " tbody tr"), function (tr) {
      var item = deep(tr._item) || {};
      tr.querySelectorAll("[data-col]").forEach(function (el) {
        var k = el.getAttribute("data-col");
        var v = el.value.trim();
        if (v === "") delete item[k];
        else item[k] = (numeric && el.getAttribute("data-kind") === "number") ? Number(v) : v;
      });
      return item;
    }).filter(function (item) { return Object.keys(item).length; });
  }

  function setWeatherMode(mode) {
    $("m-weather-mode").value = mode;
    $("m-wind").hidden = mode !== "pinned";
    $("btn-m-wind-add").parentNode.hidden = mode !== "pinned";
  }
  $("m-weather-mode").addEventListener("change", function () {
    setWeatherMode($("m-weather-mode").value);
    if ($("m-weather-mode").value === "pinned" && !$("m-wind").querySelector("tbody tr")) {
      windRow({ at: ($("maker").querySelector('[data-field="start"]').value || ""), from_deg: 270, knots: 12 });
    }
  });

  function briefMode(mode) {
    $("m-brief-mode").value = mode;
    $("m-brief-starter-label").hidden = mode !== "starter";
    $("m-brief-named-label").hidden = mode !== "named";
    $("m-brief-written").hidden = mode !== "written";
  }
  $("m-brief-mode").addEventListener("change", function () { briefMode($("m-brief-mode").value); });
  function fillBrief(b) {
    document.querySelectorAll("#m-brief-written [data-brief]").forEach(function (el) {
      var v = getPath(b || {}, el.getAttribute("data-brief"));
      if (el.type === "checkbox") el.checked = !!v;
      else el.value = v === undefined || v === null ? "" : String(v).trim();
    });
  }
  $("btn-m-brief-from").addEventListener("click", function () {
    fillBrief(cat.briefs[$("m-brief-from").value]);
    briefMode("written");
    markDirty("director");
  });
  function writtenBrief() {
    var b = {};
    document.querySelectorAll("#m-brief-written [data-brief]").forEach(function (el) {
      var k = el.getAttribute("data-brief");
      if (el.type === "checkbox") { if (el.checked) setPath(b, k, true); return; }
      var v = el.value.trim();
      if (v === "") return;
      setPath(b, k, el.hasAttribute("data-num") ? Number(v) : v);
    });
    return b;
  }

  /** The form's fields from a scenario's (`fields`, as the server read them). */
  // the two blocks offered as the file's own words (package 96b, step 8): sent to the
  // proof and the save only when they were touched, so that an untouched block is the
  // scenario's own, byte for byte
  var dirtyBlocks = {};
  document.querySelectorAll("#maker [data-block]").forEach(function (el) {
    el.addEventListener("input", function () { dirtyBlocks[el.getAttribute("data-block")] = true; });
  });
  function blocksToSend() {
    var out = {}, any = false;
    document.querySelectorAll("#maker [data-block]").forEach(function (el) {
      var k = el.getAttribute("data-block");
      if (dirtyBlocks[k] || (fresh && el.value.trim())) { out[k] = el.value; any = true; }
    });
    return any ? out : undefined;
  }
  $("btn-m-ports-region").addEventListener("click", function () {
    var region = $("maker").querySelector('[data-field="region"]').value;
    var el = $("maker").querySelector('[data-field="ports"]');
    if (!region || el.disabled) return;
    el.value = cat.ports.filter(function (x) { return x.region === region; }).map(function (x) { return x.id; }).join(", ");
    markDirty("ports");
    foldLines();
  });

  function fillForm(fields, positionDeg) {
    dirty = {};
    dirtyBlocks = {};
    var blocks = (loaded && loaded.blocks) || {};
    $("m-systems").value = blocks.systems || "";
    $("m-ports-state").value = blocks.ports || "";
    fillShipFit(getPath(fields, "ship.file"), getPath(fields, "ship.fit"));
    fillPosts(getPath(fields, "ship.file"));
    // `director: observe` is a word, not a mapping: its grant has no fields to fill
    document.querySelectorAll('#maker [data-field^="director."]').forEach(function (el) { el.disabled = typeof fields.director === "string"; });
    fillChron(fields);
    fillThings(fields.things);
    clear($("m-people").querySelector("tbody"));
    (Array.isArray(fields.people) ? fields.people : []).forEach(personRow);
    document.querySelectorAll("#maker [data-field]").forEach(function (el) {
      var kind = el.getAttribute("data-kind");
      var path = el.getAttribute("data-field");
      var v = getPath(fields, path);
      if (kind === "text" || kind === "number") el.value = v === undefined || v === null ? "" : String(v);
      else if (kind === "select") {
        if (v !== undefined && v !== null && !Array.prototype.some.call(el.options, function (o) { return o.value === String(v); })) option(el, String(v));
        el.value = v === undefined || v === null ? "" : String(v);
      } else if (kind === "bool") el.checked = v === true;
      else if (kind === "business") el.value = v === true || v === "on" ? "on" : v === false || v === "off" ? "off" : v === undefined ? "" : String(v);
      else if (kind === "lines") el.value = Array.isArray(v) ? v.join("\n") : "";
      else if (kind === "csv") el.value = Array.isArray(v) ? v.join(", ") : v && typeof v === "object" ? "" : "";
      else if (kind === "tri") el.value = v === true ? "true" : v === false ? "false" : "";
      else if (kind === "goods") el.value = goodsWords(v);
    });
    var ports = fields.ports;
    $("maker").querySelector('[data-field="ports"]').disabled = !!(ports && !Array.isArray(ports));
    $("maker").querySelector('[data-field="ports"]').title = ports && !Array.isArray(ports) ? "the ports' state is written as a mapping: kept as written" : "";
    $("m-lat").value = positionDeg ? positionDeg[0] : "";
    $("m-lon").value = positionDeg ? positionDeg[1] : "";
    $("m-port").value = "";
    // the weather
    var w = fields.weather;
    clear($("m-wind").querySelector("tbody"));
    var pinned = Array.isArray(w) ? w : w && typeof w === "object" && Array.isArray(w.wind) ? w.wind : null;
    var systems = w && typeof w === "object" && !Array.isArray(w) && w.systems && w.systems.length;
    if (w && typeof w === "object" && !Array.isArray(w) && w.climatology && !pinned && !systems) setWeatherMode("climatology");
    else if (pinned && !systems) { setWeatherMode("pinned"); pinned.forEach(windRow); }
    else {
      setWeatherMode("");
      if (pinned) pinned.forEach(windRow);
    }
    $("m-weather-said").textContent = systems ? "systems written by hand (" + w.systems.length + "), kept as written" : w === undefined ? "none said" : "";
    // the other sail, the world orders
    clear($("m-ships"));
    (fields.ships || []).forEach(shipRow);
    clear($("m-squadrons"));
    (Array.isArray(fields.squadrons) ? fields.squadrons : []).forEach(squadronRow);
    clear($("m-world-orders").querySelector("tbody"));
    (fields.world_orders || []).forEach(orderRow);
    // the books, the stations, the director
    var books = fields.standing_orders || [];
    document.querySelectorAll("#m-books [data-book]").forEach(function (c) { c.checked = books.indexOf(c.value) >= 0; });
    $("m-book").value = "";
    var holders = fields.stations || {};
    document.querySelectorAll("#m-stations [data-holder]").forEach(function (s) {
      var h = holders[s.getAttribute("data-holder")];
      s.value = h === undefined ? "" : String(h);
    });
    var brief = fields.director && fields.director.brief;
    fillBrief(null);
    $("m-brief-named").value = "";
    if (brief === undefined || brief === null) briefMode("");
    else if (typeof brief === "object") { fillBrief(brief); briefMode("written"); }
    else if (cat.briefs[String(brief)]) { $("m-brief-starter").value = String(brief); briefMode("starter"); }
    else { $("m-brief-named").value = String(brief); briefMode("named"); }
    dirty = {};
    drawChart();
    foldLines();
  }

  // -- the sheet folded (package 96b, step 4; docs/design/Design-Harbour.md §2.3) --------
  //
  // Each part of the scenario is a line when closed, written from the fields as the form
  // would write them now, so that the whole scenario reads without a part opened; a part's
  // name opens and closes it.

  function plural(n, one, many) {
    var words = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"];
    return (n >= 0 && n <= 10 ? words[n] : String(n)) + " " + (n === 1 ? one : many);
  }
  function cap(s) { return s ? s.charAt(0).toUpperCase() + s.slice(1) : s; }
  function nationWords(id) { return String(id).split("-").map(cap).join(" "); }
  function stem(path) { return String(path || "").split(/[\\/]/).pop().replace(/\.(yaml|yml|orders)$/, ""); }
  function whenWords(start) {
    var m = /^(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2}))?/.exec(String(start || ""));
    if (!m) return start ? String(start) : "";
    var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    return Number(m[3]) + " " + months[Number(m[2]) - 1] + " " + m[1] + (m[4] ? ", " + m[4] + ":" + m[5] : "");
  }
  function lineOf(part, f) {
    var bits = [], ship = f.ship && typeof f.ship === "object" ? f.ship : null;
    if (part === "day") {
      bits.push(f.name ? '"' + f.name + '"' : "No name yet");
      bits.push(f.start ? whenWords(f.start) : "the game's own first day (1 June 1805, 04:00)");
      if (f.seed !== undefined) bits.push("seed " + f.seed);
      if (f.nation) bits.push("of " + nationWords(f.nation));
      if (f.follows_history === true) bits.push("the world keeps to the course of history");
      var yr = /^(\d{4})/.exec(String(f.start || ""));
      $("m-year-says").textContent = yr && Number(yr[1]) !== 1805 ? yearWords(Number(yr[1])) : "";
      if (yr && Number(yr[1]) !== 1805) bits.push("the ports as on that day, the wars those of June 1805");
      if (f.knowledge === "all") bits.push("everyone knows everything (for testing)");
    } else if (part === "ship") {
      if (!ship) bits.push(typeof f.ship === "string" || (f.director === "observe") ? "No ship of your own: the world is watched from the director's station" : "No ship file chosen: a point on the sea");
      else {
        bits.push((ship.file ? "The " + stem(ship.file) : "No ship file chosen") + (ship.name ? " " + ship.name : ""));
        bits.push(ship.fit ? "her fit " + ship.fit : "her file's own fit of guns");
        if (f.papers && f.papers.service) bits.push({ kings: "a King's ship", privateer: "a privateer", merchant: "a merchantman" }[f.papers.service] || "in service as " + f.papers.service);
        bits.push(ship.glass ? "a glass aboard" : "no glass");
        bits.push((ship.instrument || f.instrument || "octant") === "sextant" ? "a sextant" : "an octant");
      }
    } else if (part === "start") {
      var lat = $("m-lat").value, lon = $("m-lon").value;
      if (lat !== "" && lon !== "") bits.push(Math.abs(Number(lat)).toFixed(2) + "° " + (Number(lat) >= 0 ? "N" : "S") + ", " + Math.abs(Number(lon)).toFixed(2) + "° " + (Number(lon) >= 0 ? "E" : "W"));
      else bits.push("No place on a chart: the endless plane");
      if (f.chart || f.region) bits.push("on the chart of " + (f.chart || f.region));
      if (ship && ship.heading_deg !== undefined) bits.push("heading " + ship.heading_deg + "°");
      if (ship && ship.speed_kn) bits.push(ship.speed_kn + " knots on her");
    } else if (part === "papers") {
      var cargo = f.cargo || {}, papers = f.papers || {};
      bits.push("Purse £" + (cargo.purse_pounds || 0));
      var goods = Object.keys(cargo.goods || {});
      if (goods.length) bits.push("in the hold " + goods.map(function (g) { return cargo.goods[g] + " tons of " + g; }).join(", "));
      var chron = (ship && ship.chronometer) || f.chronometer || papers.chronometer;
      bits.push(chron ? "a chronometer" + (chron.maker ? " by " + chron.maker : "") : "no chronometer");
      var ep = (ship && ship.epitome) || f.epitome || papers.epitome;
      if (ep) bits.push(cap(String(ep)) + "'s epitome");
      if ((papers.price_lists || []).length) bits.push("the price lists of " + papers.price_lists.join(", "));
      if (papers.private_signals !== undefined) bits.push(papers.private_signals ? "the private signals carried" : "no private signals");
      if ((papers.signal_books || []).length) bits.push("the signal books of " + papers.signal_books.join(", "));
      var people = f.people || [];
      bits.push(people.length ? "people said: " + people.map(function (x) { return (x.name ? x.name + ", " : "") + "the " + x.role + (x.skill !== undefined ? " (skill " + x.skill + ")" : "") + (x.ashore ? ", ashore" + (x.port ? " at " + x.port : "") : ""); }).join(", ") : "her people as her wardroom has them");
      if ((f.things || []).length) bits.push(plural(f.things.length, "thing", "things") + " aboard or ashore");
    } else if (part === "weather") {
      var w = f.weather, wind = f.wind || {};
      var pinned = Array.isArray(w) ? w : w && Array.isArray(w.wind) ? w.wind : [];
      var systems = w && !Array.isArray(w) && Array.isArray(w.systems) ? w.systems : [];
      if (dirtyBlocks.systems) bits.push("the systems' words changed here (the proof reads them)");
      if (pinned.length) bits.push("The wind pinned by the hour, " + plural(pinned.length, "waypoint", "waypoints") + ", from " + pinned[0].from_deg + "° at " + pinned[0].knots + " knots");
      if (systems.length) bits.push(plural(systems.length, "weather system", "weather systems") + " written out (" + systems.map(function (x) { return x.name || x.kind || "a system"; }).join(", ") + ")");
      if (w && !Array.isArray(w) && w.climatology) bits.push("the month's own weather");
      if (!pinned.length && !systems.length && !(w && !Array.isArray(w) && w.climatology)) bits.push("One fixed wind, from " + (wind.from_deg !== undefined ? wind.from_deg : 225) + "° at " + (wind.knots !== undefined ? wind.knots : 15) + " knots");
      if (w && !Array.isArray(w) && w.sky) bits.push("the sky pinned");
      if (f.weather_bound) bits.push("held to the season's bounds");
      if (f.current && f.current.knots) bits.push("a current of " + f.current.knots + " knots");
    } else if (part === "ships") {
      var ships = f.ships || [], sets = f.squadrons || [];
      if (!ships.length) bits.push("None");
      else bits.push(cap(plural(ships.length, "ship", "ships")) + ": " + ships.map(function (x) {
        var flag = x.colours && ["shown", "none", "yes", "no", "true", "false", "hidden"].indexOf(String(x.colours)) < 0 ? " under the colours of " + nationWords(x.colours) : "";
        return (x.name || x.id || x.description) + (x.nation ? " of " + nationWords(x.nation) : "") + (x.description ? ", a " + x.description : "") + (x.fit ? " (" + x.fit + ")" : "") + flag;
      }).join("; "));
      if (sets.length) bits.push(sets.map(function (x) { return (x.name || x.id) + (x.kind === "convoy" ? ", a convoy" : ", a squadron") + (x.formation ? " in " + x.formation : "") + ((x.members || []).length ? " (" + x.members.join(", ") + ")" : ""); }).join("; "));
    } else if (part === "sea") {
      var ports = f.ports;
      if (dirtyBlocks.ports) bits.push("the ports' state changed here (the proof reads it)");
      if (ports === undefined) bits.push("Every port of the chart");
      else {
        var ids = Array.isArray(ports) ? ports : Object.keys(ports);
        bits.push(cap(plural(ids.length, "port", "ports")) + (ids.length ? ": " + ids.join(", ") : ""));
        if (!Array.isArray(ports)) {
          var said = ids.filter(function (k) { return ports[k] && Object.keys(ports[k]).length; });
          if (said.length) bits.push("their state said of " + said.join(", "));
        }
      }
      bits.push(f.business === undefined || f.business === false || f.business === "off" || f.business === 0 ? "no traffic of the sea's own" : "the sea's traffic " + (f.business === true || f.business === "on" ? "on" : "at " + f.business));
      if (f.crewed) bits.push("crewed ships: " + (f.crewed.cap !== undefined ? f.crewed.cap : "three") + " at once within " + (f.crewed.range_nm !== undefined ? f.crewed.range_nm : "four") + " miles");
      if ((f.world_orders || []).length) bits.push(plural(f.world_orders.length, "world order", "world orders") + " by the clock");
    } else if (part === "orders") {
      var books = (f.standing_orders || []).map(stem);
      bits.push(books.length ? "The " + books.join(" and the ") + " book" + (books.length > 1 ? "s" : "") : "No book of standing orders");
      if ($("m-book").value.trim()) bits.push("a book drafted here");
      var orders = f.orders || [];
      bits.push(orders.length ? (orders.length === 1 ? "first order: " + orders[0] : plural(orders.length, "first order", "first orders") + ", the first: " + orders[0]) : "no first orders");
      if (f.intent) bits.push("intent: " + f.intent);
    } else if (part === "stations") {
      var st = f.stations || {}, who = Object.keys(st);
      bits.push(who.length ? who.map(function (k) { return "the " + k + ": " + (st[k] === "player" ? "you" : st[k] === "model" ? "a model" : "the game's own"); }).join(", ") : "You are the captain; nobody else is said");
      var d = f.director, brief = d && typeof d === "object" ? d.brief : undefined;
      if (d === "observe" || (d && d.observe)) bits.push("the world observed");
      bits.push(brief === undefined || brief === null ? "no director" : "a director on the brief " + (typeof brief === "object" ? '"' + (brief.name || "written here") + '"' : brief));
      if (d && typeof d === "object" && (d.models || []).length) bits.push("the director may seat " + plural(d.models.length, "model", "models"));
    }
    return cap(bits.join("; ")) + ".";
  }
  function foldLines() {
    if (!cat) return;
    var f;
    try { f = collect(); } catch (e) { return; }
    document.querySelectorAll("#maker [data-line]").forEach(function (p) {
      p.textContent = lineOf(p.getAttribute("data-line"), f);
    });
  }
  harbour.foldLines = foldLines;
  function fold(fs, folded) {
    fs.classList.toggle("folded", folded);
    if (!folded && fs.getAttribute("data-part") === "start") drawChart();
  }
  document.querySelectorAll("#maker fieldset[data-part] > legend").forEach(function (lg) {
    lg.addEventListener("click", function () { fold(lg.parentNode, !lg.parentNode.classList.contains("folded")); });
  });
  $("btn-m-open").addEventListener("click", function () { document.querySelectorAll("#maker fieldset[data-part]").forEach(function (fs) { fold(fs, false); }); });
  $("btn-m-close").addEventListener("click", function () { document.querySelectorAll("#maker fieldset[data-part]").forEach(function (fs) { fold(fs, true); }); });
  $("maker").addEventListener("input", foldLines);
  $("maker").addEventListener("change", foldLines);
  $("maker").addEventListener("click", function (ev) { if (ev.target.tagName === "BUTTON" || ev.target.tagName === "CANVAS") setTimeout(foldLines, 0); });

  function valueOf(el) {
    var kind = el.getAttribute("data-kind");
    if (kind === "text") return el.value.trim() === "" ? undefined : el.value.trim();
    if (kind === "number") return el.value.trim() === "" ? undefined : Number(el.value);
    if (kind === "select") return el.value === "" ? undefined : el.value;
    if (kind === "bool") return el.checked;
    if (kind === "business") return el.value === "on" ? true : el.value === "off" ? false : undefined;
    if (kind === "lines") {
      var lines = el.value.split("\n").map(function (s) { return s.trim(); }).filter(Boolean);
      return lines.length ? lines : undefined;
    }
    if (kind === "csv") {
      var items = el.value.split(",").map(function (s) { return s.trim(); }).filter(Boolean);
      return items.length ? items : undefined;
    }
    if (kind === "tri") return el.value === "true" ? true : el.value === "false" ? false : undefined;
    return undefined;
  }

  /** The scenario's fields: those read, with the touched ones (or, for a new scenario,
      every one the form has a value for) written over them. */
  function collect() {
    var f = fresh ? {} : deep(loaded.fields);
    var all = fresh;
    var on = function (field) { return all || dirty[field]; };
    document.querySelectorAll("#maker [data-field]").forEach(function (el) {
      var path = el.getAttribute("data-field");
      var kind = el.getAttribute("data-kind");
      if (["text", "number", "select", "bool", "business", "lines", "csv", "tri"].indexOf(kind) < 0) return;
      if (!on(path) || el.disabled) return;
      var v = valueOf(el);
      if (kind === "bool" && all && !v) v = undefined;
      if (v === undefined) delPath(f, path);
      else setPath(f, path, v);
    });
    if (on("position")) {
      if ($("m-lat").value !== "" && $("m-lon").value !== "") f.position = { lat_deg: Number($("m-lat").value), lon_deg: Number($("m-lon").value) };
      else if (all) delete f.position;
    }
    if (on("weather")) {
      var mode = $("m-weather-mode").value;
      var base = f.weather && typeof f.weather === "object" && !Array.isArray(f.weather) ? f.weather : {};
      if (mode === "climatology") f.weather = { climatology: true };
      else if (mode === "pinned") {
        var w = deep(base);
        delete w.climatology;
        w.wind = rowsOf("m-wind", true);
        f.weather = w;
      } else if (all) delete f.weather;
    }
    if (on("ships")) {
      var ships = shipsOf();
      if (ships.length) f.ships = ships; else delete f.ships;
    }
    if (on("cargo.goods")) {
      var goods = goodsOf($("m-goods").value);
      if (goods === undefined) delPath(f, "cargo.goods");
      else if (goods !== null) setPath(f, "cargo.goods", goods);
    }
    if (on("papers.chronometer") && !$("m-chron-on").disabled) {
      var chron = chronOf();
      if (chron === undefined) delPath(f, "papers.chronometer"); else setPath(f, "papers.chronometer", chron);
    }
    if (on("people")) {
      var people = peopleOf();
      if (people.length) f.people = people; else delete f.people;
    }
    if (on("things") && !$("m-things").disabled) {
      var things = $("m-things").value.split("\n").map(function (s) { return s.trim(); }).filter(Boolean);
      if (things.length) f.things = things; else delete f.things;
    }
    if (on("squadrons")) {
      var sets = squadronsOf();
      if (sets.length) f.squadrons = sets; else delete f.squadrons;
    }
    if (on("world_orders")) {
      var orders = rowsOf("m-world-orders", false);
      if (orders.length) f.world_orders = orders; else delete f.world_orders;
    }
    if (on("standing_orders")) {
      var had = (f.standing_orders || []).filter(function (b) { return cat.books.indexOf(b) < 0; });
      var books = had.concat(Array.prototype.map.call(document.querySelectorAll("#m-books [data-book]:checked"), function (c) { return c.value; }));
      if (books.length) f.standing_orders = books; else delete f.standing_orders;
    }
    if (on("stations")) {
      var st = {};
      document.querySelectorAll("#m-stations [data-holder]").forEach(function (s) { if (s.value) st[s.getAttribute("data-holder")] = s.value; });
      if (Object.keys(st).length) f.stations = st; else delete f.stations;
    }
    if (on("director")) {
      var mode2 = $("m-brief-mode").value;
      var d = f.director && typeof f.director === "object" ? f.director : {};
      if (mode2 === "starter") d.brief = $("m-brief-starter").value;
      else if (mode2 === "named") d.brief = $("m-brief-named").value.trim();
      else if (mode2 === "written") {
        // the form shows a brief's name, tone, challenge, limits, cadence and budget: what
        // else the brief read holds (its examples, a limit the form has no field for) is
        // kept as it was, so that touching the form drops nothing it does not show
        var prev = d.brief && typeof d.brief === "object" ? deep(d.brief) : {};
        var now = writtenBrief();
        ["name", "tone", "challenge", "cadence"].forEach(function (k) { delete prev[k]; });
        ["limits", "budget"].forEach(function (k) {
          var shown = {};
          document.querySelectorAll('#m-brief-written [data-brief^="' + k + '."]').forEach(function (el) { shown[el.getAttribute("data-brief").split(".")[1]] = true; });
          var rest = {};
          Object.keys(prev[k] && typeof prev[k] === "object" ? prev[k] : {}).forEach(function (x) { if (!shown[x]) rest[x] = prev[k][x]; });
          delete prev[k];
          var merged = now[k] || {};
          Object.keys(rest).forEach(function (x) { merged[x] = rest[x]; });
          if (Object.keys(merged).length) now[k] = merged;
        });
        Object.keys(prev).forEach(function (k) { now[k] = prev[k]; });
        d.brief = now;
      }
      else delete d.brief;
      if (Object.keys(d).length && (d.brief === undefined || d.brief !== "")) f.director = d; else delete f.director;
    }
    return f;
  }
  harbour.collect = collect;

  function readScenario(path) {
    return api("GET", "/api/harbour/scenario?path=" + encodeURIComponent(path)).then(function (r) {
      loaded = r;
      fresh = false;
      harbour.loaded = r;
      fillForm(r.fields, r.position_deg);
      $("m-name").value = r.name;
      $("m-source").textContent = "read from " + r.path;
      show($("m-refusal"), "");
      show($("m-words"), "");
      show($("m-text"), "");
      return r;
    });
  }
  harbour.readScenario = readScenario;

  // "change this scenario" on the game tab: the scenario chosen there, read into the sheet
  $("btn-s-change").addEventListener("click", function () {
    var path = $("s-scenario").value;
    if (!path) return;
    $("m-pick").value = path;
    tab("maker");
    readScenario(path).catch(function (e) { show($("m-refusal"), e.message); });
  });
  $("btn-m-read").addEventListener("click", function () {
    readScenario($("m-pick").value).catch(function (e) { show($("m-refusal"), e.message); });
  });
  $("btn-m-new").addEventListener("click", function () {
    loaded = { path: "", name: "", fields: {} };
    fresh = true;
    fillForm({ name: "A passage of my own", seed: 7, start: "1805-06-12T05:00", ship: { file: "data/ships/cutter.yaml", heading_deg: 190, glass: true, instrument: "octant" }, nation: "britain", weather: { climatology: true }, orders: ["let go the best bower"] }, null);
    $("m-name").value = "";
    $("m-source").textContent = "a new scenario";
  });

  function proveOrSave(save) {
    var body = { fields: collect(), source: fresh ? "" : loaded.path, blocks: blocksToSend() };
    var path = "/api/harbour/scenario/prove";
    if (save) {
      body.name = $("m-name").value;
      body.book = $("m-book").value;
      body.overwrite = $("m-overwrite").checked;
      path = "/api/harbour/scenario";
    }
    show($("m-refusal"), "");
    harbour.busy = true;
    return api("POST", path, body).then(function (r) {
      show($("m-words"), (save ? "Saved as " + r.path + ".\n\n" : "Proved: it loads as the console would load it.\n\n") + r.lines.join("\n"));
      show($("m-text"), r.text);
      if (save) {
        harbour.saved = r;
        return loadCatalogue().then(function () { return readScenario(r.path); }).then(function () {
          show($("m-words"), "Saved as " + r.path + ".\n\n" + r.lines.join("\n"));
          show($("m-text"), r.text);
          return r;
        });
      }
      return r;
    }).catch(function (e) { show($("m-refusal"), e.message); throw e; }).finally(function () {
      harbour.busy = false; // the save, the lists and the form read back are all done
    });
  }
  harbour.proveOrSave = proveOrSave;
  $("btn-m-prove").addEventListener("click", function () { proveOrSave(false).catch(function () {}); });
  $("maker").addEventListener("submit", function (ev) { ev.preventDefault(); proveOrSave(true).catch(function () {}); });

  // the chart: a region's coast, the ports, the start pricked by a click
  var chart = null;
  $("m-port").addEventListener("change", function () {
    var p = cat.ports.filter(function (x) { return x.id === $("m-port").value; })[0];
    if (!p) return;
    $("m-lat").value = p.lat_deg;
    $("m-lon").value = p.lon_deg;
    var region = $("maker").querySelector('[data-field="region"]');
    if (p.region && region.value !== p.region) { region.value = p.region; markDirty("region"); }
    markDirty("position");
    drawChart();
  });
  $("maker").querySelector('[data-field="region"]').addEventListener("change", drawChart);
  ["m-lat", "m-lon"].forEach(function (id) { $(id).addEventListener("change", drawChart); });

  function frame(c) {
    var b = c.bounds, cv = $("m-chart");
    var mid = (b.south + b.north) / 2 * Math.PI / 180;
    var w = (b.east - b.west) * Math.cos(mid), h = b.north - b.south;
    var k = Math.min(cv.width / w, cv.height / h);
    return {
      x: function (lon) { return (lon - b.west) * Math.cos(mid) * k; },
      y: function (lat) { return cv.height - (lat - b.south) * k; },
      lon: function (x) { return b.west + x / (k * Math.cos(mid)); },
      lat: function (y) { return b.south + (cv.height - y) / k; },
    };
  }

  function drawChart() {
    var cv = $("m-chart");
    if (!cv || !cat || cv.offsetParent === null) return;
    var region = $("maker").querySelector('[data-field="region"]').value || "channel-west";
    if (!chart || chart.region !== region) {
      api("GET", "/api/harbour/chart?region=" + encodeURIComponent(region)).then(function (c) { chart = c; drawChart(); }).catch(function () {});
      return;
    }
    var g = cv.getContext("2d"), f = frame(chart), css = getComputedStyle(document.documentElement);
    g.fillStyle = css.getPropertyValue("--map-sea") || "#7b98a8";
    g.fillRect(0, 0, cv.width, cv.height);
    g.strokeStyle = css.getPropertyValue("--map-ink") || "#2b2925";
    g.lineWidth = 1;
    chart.coast.forEach(function (line) {
      g.beginPath();
      line.forEach(function (p, i) { (i ? g.lineTo : g.moveTo).call(g, f.x(p[0]), f.y(p[1])); });
      g.stroke();
    });
    g.fillStyle = "#2b2925";
    g.font = "11px sans-serif";
    chart.ports.forEach(function (p) {
      g.fillRect(f.x(p.lon_deg) - 2, f.y(p.lat_deg) - 2, 4, 4);
      g.fillText(p.name, f.x(p.lon_deg) + 4, f.y(p.lat_deg) - 3);
    });
    var lat = parseFloat($("m-lat").value), lon = parseFloat($("m-lon").value);
    if (isFinite(lat) && isFinite(lon)) {
      g.strokeStyle = "#9c2f22";
      g.lineWidth = 2;
      g.beginPath();
      g.arc(f.x(lon), f.y(lat), 6, 0, 2 * Math.PI);
      g.stroke();
    }
  }
  $("m-chart").addEventListener("click", function (ev) {
    if (!chart) return;
    var r = $("m-chart").getBoundingClientRect(), f = frame(chart);
    var sx = $("m-chart").width / r.width, sy = $("m-chart").height / r.height;
    $("m-lat").value = f.lat((ev.clientY - r.top) * sy).toFixed(4);
    $("m-lon").value = f.lon((ev.clientX - r.left) * sx).toFixed(4);
    var region = $("maker").querySelector('[data-field="region"]');
    if (!region.value) { region.value = chart.region; markDirty("region"); }
    markDirty("position");
    drawChart();
  });

  // -- the settings --------------------------------------------------------------------

  var settings = null;
  function fillSettings(r) {
    settings = r.settings;
    $("st-path").textContent = r.path;
    var cr = $("st-credential");
    clear(cr);
    (r.credential || []).forEach(function (w) { li(cr, w); });
    if (r.error) show($("st-refusal"), "The settings file could not be read: " + r.error);
    document.querySelectorAll("#settings [data-set]").forEach(function (el) {
      var v = getPath(settings, el.getAttribute("data-set"));
      if (el.type === "checkbox") el.checked = !!v;
      else if (el.hasAttribute("data-list")) el.value = (v || []).join(" ");
      else el.value = v === undefined || v === null ? "" : String(v);
      var key = el.getAttribute("data-set").split(".").pop();
      if (r.defaults && r.defaults[key] && !el.value) el.placeholder = r.defaults[key];
    });
    // the API door's other models (package 96b, step 9): one a line, "name" or
    // "name, dialect", as the settings keep them (a name, or {name, dialect})
    fillFlags("api", getPath(settings, "doors.api.flags") || []);
    fillFlags("local", getPath(settings, "doors.local.flags") || []);
    var others = getPath(settings, "doors.api.models") || [];
    $("st-models").value = others.map(function (m) {
      return m && typeof m === "object" ? (m.name || "") + (m.dialect ? ", " + m.dialect : "") : String(m);
    }).join("\n");
  }
  // A door's flags as named choices (package 96b, step 10): the settings keep one list of
  // flags for each door, as its command line takes them; the form shows the ones a player
  // chooses among by name and the rest as a line, and puts the list together again.
  var FLAG_FIELDS = {
    api: [["--cadence", "st-api-cadence", "value"], ["--ask-again", "st-api-ask-again", "flag"]],
    local: [["--cadence", "st-local-cadence", "value"], ["--pictures", "st-local-pictures", "value"], ["--ctx", "st-local-ctx", "value"], ["--ask-again", "st-local-ask-again", "flag"]],
  };
  function fillFlags(door, flags) {
    var rest = (flags || []).map(String);
    FLAG_FIELDS[door].forEach(function (f) {
      var el = $(f[1]), i = rest.indexOf(f[0]);
      if (f[2] === "flag") { el.checked = i >= 0; if (i >= 0) rest.splice(i, 1); return; }
      var known = i >= 0 && i + 1 < rest.length && (el.tagName !== "SELECT" || Array.prototype.some.call(el.options, function (o) { return o.value === rest[i + 1]; }));
      el.value = known ? rest[i + 1] : "";
      if (known) rest.splice(i, 2); // a value the form does not know stays in the line
    });
    $("st-" + door + "-flags").value = rest.join(" ");
  }
  function flagsOf(door) {
    var out = [];
    FLAG_FIELDS[door].forEach(function (f) {
      var el = $(f[1]);
      if (f[2] === "flag") { if (el.checked) out.push(f[0]); }
      else if (el.value.trim() !== "") out.push(f[0], el.value.trim());
    });
    return out.concat($("st-" + door + "-flags").value.split(/\s+/).filter(Boolean));
  }

  function loadSettings() { return api("GET", "/api/harbour/settings").then(fillSettings); }
  $("settings").addEventListener("submit", function (ev) {
    ev.preventDefault();
    var s = deep(settings) || {};
    document.querySelectorAll("#settings [data-set]").forEach(function (el) {
      var k = el.getAttribute("data-set"), v;
      if (el.type === "checkbox") v = el.checked;
      else if (el.hasAttribute("data-list")) v = el.value.split(/\s+/).filter(Boolean);
      else if (el.hasAttribute("data-num")) v = el.value.trim() === "" ? null : Number(el.value);
      else v = el.value.trim();
      setPath(s, k, v);
    });
    setPath(s, "doors.api.flags", flagsOf("api"));
    setPath(s, "doors.local.flags", flagsOf("local"));
    setPath(s, "doors.api.models", $("st-models").value.split("\n").map(function (line) {
      var parts = line.split(",").map(function (x) { return x.trim(); });
      if (!parts[0]) return null;
      return parts[1] ? { name: parts[0], dialect: parts[1] } : parts[0];
    }).filter(Boolean));
    show($("st-refusal"), "");
    api("POST", "/api/harbour/settings", { settings: s }).then(function (r) {
      show($("st-words"), "Kept in " + r.path + ".");
      return loadSettings().then(loadCatalogue);
    }).catch(function (e) { show($("st-refusal"), e.message); });
  });
  $("btn-shortcut-show").addEventListener("click", function () {
    api("POST", "/api/harbour/shortcut", {}).then(function (r) {
      show($("st-words"), "The shortcut would be " + r.path + ":\n\n" + r.text);
      $("btn-shortcut-write").hidden = false;
    });
  });
  $("btn-shortcut-write").addEventListener("click", function () {
    if (!window.confirm("Write the shortcut that starts the harbour?")) return;
    api("POST", "/api/harbour/shortcut", { write: true }).then(function (r) {
      show($("st-words"), "Written: " + r.path + ".");
      $("btn-shortcut-write").hidden = true;
    }).catch(function (e) { show($("st-refusal"), e.message); });
  });

  // -- the start -----------------------------------------------------------------------

  Promise.all([loadCatalogue(), loadSettings()]).then(function () {
    var g = (settings && settings.game) || {};
    $("s-time").value = g.compression || 1;
    $("s-pace").value = g.pace || "rule";
    if (g.seat && cat.seats.indexOf(g.seat) >= 0) $("s-seat").value = g.seat; // the settings' seat
    if (g.crewed) {
      $("s-crewed-cap").value = g.crewed.cap === null || g.crewed.cap === undefined ? "" : g.crewed.cap;
      $("s-crewed-range").value = g.crewed.range_nm === null || g.crewed.range_nm === undefined ? "" : g.crewed.range_nm;
    }
    briefMode("");
    setWeatherMode("");
    var t = null;
    try { t = sessionStorage.getItem("harbour-tab"); } catch (e) { /* none */ }
    if (t) tab(t);
    // the game's state read once before the page says it is ready, so that what it shows
    // of the game in play is true from the first moment
    return api("GET", "/api/harbour/state").then(onState).catch(function () {}).then(function () {
      harbour.ready = true;
      setTimeout(poll, 1500);
    });
  }).catch(function (e) {
    $("status").textContent = "the harbour could not be read: " + e.message;
    $("status").className = "bad";
  });
})();
