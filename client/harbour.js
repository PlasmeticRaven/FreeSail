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

  function scenarioOptions(sel, withNone) {
    clear(sel);
    if (withNone) option(sel, "", withNone);
    var game = document.createElement("optgroup");
    game.label = "the game's";
    var own = document.createElement("optgroup");
    own.label = "yours (" + cat.scenarios_place + ")";
    cat.scenarios.forEach(function (s) {
      var o = document.createElement("option");
      o.value = s.path;
      o.textContent = s.name + "  (" + s.path.split(/[\\/]/).pop() + ")";
      (s.own ? own : game).appendChild(o);
    });
    sel.appendChild(game);
    if (own.children.length) sel.appendChild(own);
  }

  function fillCatalogue() {
    scenarioOptions($("s-scenario"));
    scenarioOptions($("m-pick"));
    var ship = $("s-ship");
    clear(ship);
    cat.ships.forEach(function (s) { option(ship, s); });
    var seat = $("s-seat");
    clear(seat);
    cat.seats.forEach(function (s) {
      option(seat, s, s === "" ? "as the scenario says (else the captain)" : s === "captain" ? "the captain, at the prompt" : "the " + s);
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
    var st = $("g-stations");
    clear(st);
    if (!s.stations.length) li(st, "none held", "muted");
    s.stations.forEach(function (x) {
      var line = x.line || "the " + x.station;
      var said = x.holder && line.indexOf(x.holder) >= 0;
      li(st, line + (x.holder && !said ? "  [" + x.holder + (x.door ? ", " + x.door : "") + "]" : ""));
    });
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
    pane.className = "door-pane door-" + d.state;
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
    if (t.closest && t.closest("#m-wind")) markDirty("weather");
    if (t.closest && t.closest("#m-world-orders")) markDirty("world_orders");
  });
  $("maker").addEventListener("input", function (ev) {
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

  var SHIP_COLS = [
    ["id", "text"], ["description", "select", "descriptions"], ["name", "text"],
    ["nation", "select", "nations"], ["position", "text"], ["goal", "text"],
    ["colours", "select", ["shown", "none"]],
  ];
  function shipRow(item) {
    var tr = document.createElement("tr");
    tr._item = item || {};
    SHIP_COLS.forEach(function (c) {
      var opts = typeof c[2] === "string" ? cat[c[2]] : c[2];
      var el = cell(tr, tr._item[c[0]], c[1], opts);
      el.setAttribute("data-col", c[0]);
    });
    removeButton(tr, "ships");
    $("m-ships").querySelector("tbody").appendChild(tr);
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
  function fillForm(fields, positionDeg) {
    dirty = {};
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
    clear($("m-ships").querySelector("tbody"));
    (fields.ships || []).forEach(shipRow);
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
  }

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
      if (["text", "number", "select", "bool", "business", "lines", "csv"].indexOf(kind) < 0) return;
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
      var ships = rowsOf("m-ships", false);
      if (ships.length) f.ships = ships; else delete f.ships;
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
      else if (mode2 === "written") d.brief = writtenBrief();
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
    var body = { fields: collect(), source: fresh ? "" : loaded.path };
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
    harbour.ready = true;
    poll();
  }).catch(function (e) {
    $("status").textContent = "the harbour could not be read: " + e.message;
    $("status").className = "bad";
  });
})();
