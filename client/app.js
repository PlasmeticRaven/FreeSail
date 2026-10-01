/* app.js: wires the panels to the server. One websocket carries every log
 * event and the snapshots; orders and driver commands go by POST.
 *
 * Developer switches:
 *   ?facing=DEG   view the ship from a fixed bearing (0 ahead, 90 on the
 *                 starboard beam, 270 on the larboard beam) instead of the
 *                 milestone 2 default, abeam to leeward
 *   [ and ]       rotate the facing by a point (11.25 degrees); \ returns to leeward
 *
 * Package 33d, the browser's shelf: the console's completer under the order line as it
 * is typed (/api/complete; Tab takes the first or the one chosen, the arrows move through
 * them, Escape puts them away, and with none showing the arrows walk the lines given
 * before); the library and the ship's papers in a pane of their own (library.js), opened
 * by the button or a `library` line; the option to ease the clock on a station; the
 * map's centre and fit buttons.
 */
(function (root) {
  "use strict";
  var U = root.Units;
  var P = root.Projection;

  var state = {
    ship: null,
    snapshot: null,
    driver: { running: false, compression: 1 },
    facingOverride: null, // radians, or null for abeam to leeward
    history: [],
    historyIndex: -1,
    hint: { items: [], chosen: -1, asked: 0, timer: null },
  };

  var log, seaMap, svg, library;

  function $(id) {
    return document.getElementById(id);
  }

  // -- drawing ------------------------------------------------------------------

  function facingWords(facing) {
    var d = Math.round(U.deg(U.wrap2pi(facing)));
    var side;
    if (d === 90) side = "the starboard beam";
    else if (d === 270) side = "the larboard beam";
    else if (d === 0) side = "right ahead";
    else if (d === 180) side = "right astern";
    else side = (d < 180 ? "starboard" : "larboard") + ", " + Math.min(d, 360 - d) + "° from the bow";
    return side + (state.facingOverride === null ? " (to leeward)" : "");
  }

  function drawShip() {
    if (!state.ship || !state.snapshot || !svg) return;
    var snap = state.snapshot;
    var facing = state.facingOverride !== null ? state.facingOverride : P.leewardFacing(snap.ship.tack);
    var skeleton = P.buildSkeleton(state.ship, snap);
    var scene = P.project(skeleton, facing, snap.ship.heel);
    root.ShipView.render(svg, scene, {
      name: state.ship.name,
      facingWords: facingWords(facing),
      heelWords: U.formatSigned(snap.ship.heel, "to starboard", "to larboard"),
    });
  }

  function onSnapshot(snap) {
    state.snapshot = snap;
    if (snap.driver) state.driver = snap.driver;
    root.Instruments.render(snap);
    seaMap.record(snap);
    seaMap.draw(snap);
    drawShip();
    updateDriverButtons();
  }

  function updateDriverButtons() {
    var d = state.driver;
    $("btn-go").classList.toggle("active", !!d.running);
    $("btn-hold").classList.toggle("active", !d.running);
    var buttons = document.querySelectorAll("[data-time]");
    Array.prototype.forEach.call(buttons, function (b) {
      b.classList.toggle("active", Number(b.getAttribute("data-time")) === Number(d.compression));
    });
    var ease = $("opt-ease-on-station");
    if (ease && document.activeElement !== ease) ease.checked = !!d.ease_on_station;
  }

  // -- the server ------------------------------------------------------------------

  function connect() {
    var proto = location.protocol === "https:" ? "wss:" : "ws:";
    var ws = new WebSocket(proto + "//" + location.host + "/ws");
    ws.onopen = function () {
      $("status").textContent = "connected";
      $("status").className = "ok";
    };
    ws.onclose = function () {
      $("status").textContent = "disconnected; retrying";
      $("status").className = "bad";
      setTimeout(connect, 2000);
    };
    ws.onmessage = function (msg) {
      var data = JSON.parse(msg.data);
      if (data.type === "hello") {
        state.ship = data.ship;
        document.title = "FreeSail · " + (data.ship ? data.ship.name : "point ship");
        $("ship-name").textContent = data.ship ? data.ship.name + " (" + data.ship.rig + ")" : "point ship";
        log.clear();
        state.driver = data.snapshot.driver || state.driver;
        // the log as the server shows it now: rolled up at 60x and above (spec M4 §20)
        data.log.forEach(function (e) {
          log.add(e);
        });
        onSnapshot(data.snapshot);
      } else if (data.type === "event") {
        log.add(data.event);
      } else if (data.type === "rollup") {
        log.addRollup(data.rollup);
      } else if (data.type === "snapshot") {
        onSnapshot(data.snapshot);
      }
    };
  }

  function post(path, body) {
    return fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(function (r) {
      return r.json();
    });
  }

  function driver(action, value) {
    return post("/api/driver", { action: action, value: value });
  }

  // `speed N` and `time N` are the same (spec M4 §20: up to 300, the server clamps)
  var DRIVER_WORDS = { hold: 1, go: 1, speed: 1, time: 1, tick: 1 };

  function submitLine(text) {
    text = text.trim();
    if (!text) return;
    state.history.push(text);
    state.historyIndex = state.history.length;
    var words = text.split(/\s+/);
    var head = words[0].toLowerCase();
    if (head === LIBRARY_WORD) {
      // the browser's own word, like hold and go: the pane, not an order to the ship
      openLibrary(text.slice(words[0].length).trim());
      return;
    }
    if (DRIVER_WORDS[head] && words.length <= 2) {
      var value = words[1] !== undefined ? Number(words[1]) : undefined;
      if (words.length === 2 && isNaN(value)) {
        note("Say '" + head + " 30'.");
        return;
      }
      driver(head === "speed" ? "time" : head, value);
      return;
    }
    post("/api/order", { text: text });
  }

  // -- the library pane (package 33d) ------------------------------------------------

  var LIBRARY_WORD = "library";

  /** Open the pane beside the log, in the ship view's place, at what `words` ask for
   * ('library primer 3', 'library find goose-wing', 'library papers'). */
  function openLibrary(words) {
    var panel = $("library-panel");
    if (!library) {
      library = new root.LibraryPane(panel, { onClose: closeLibrary });
    }
    panel.hidden = false;
    document.body.classList.add("library-open");
    library.openWords(words || "");
  }

  function closeLibrary() {
    $("library-panel").hidden = true;
    document.body.classList.remove("library-open");
    drawShip();
    $("command").focus();
  }

  // -- completion under the order line (package 33d) ------------------------------------

  // How long the line rests before the completer is asked (ms): one request a pause in
  // the typing, not one a key.
  var HINT_DELAY_MS = 60;

  function askHint(text) {
    var h = state.hint;
    clearTimeout(h.timer);
    if (!text.trim()) {
      showHint([]);
      return;
    }
    h.timer = setTimeout(function () {
      var asked = (h.asked += 1);
      fetch("/api/complete?line=" + encodeURIComponent(text))
        .then(function (r) {
          return r.json();
        })
        .then(function (data) {
          if (asked !== h.asked || $("command").value !== text) return; // the line moved on
          var items = (data.suggestions || []).slice();
          // the browser's own word, which the console has not
          if (LIBRARY_WORD.indexOf(text.trim().toLowerCase()) === 0 && text.trim().toLowerCase() !== LIBRARY_WORD) {
            items.push(LIBRARY_WORD);
          }
          showHint(items);
        })
        .catch(function () {
          showHint([]);
        });
    }, HINT_DELAY_MS);
  }

  function showHint(items) {
    var h = state.hint;
    h.items = items;
    h.chosen = -1;
    drawHint();
  }

  function hideHint() {
    clearTimeout(state.hint.timer);
    state.hint.asked += 1; // an answer on its way is not shown
    showHint([]);
  }

  function drawHint() {
    var h = state.hint;
    var box = $("hint");
    box.innerHTML = "";
    box.hidden = !h.items.length;
    h.items.forEach(function (s, i) {
      var item = document.createElement("span");
      item.className = "hint-item" + (i === h.chosen ? " chosen" : "") + (i === 0 && h.chosen < 0 ? " first" : "");
      item.setAttribute("role", "option");
      item.textContent = s;
      item.addEventListener("mousedown", function (ev) {
        ev.preventDefault(); // keep the order line's focus
        take(s);
      });
      box.appendChild(item);
    });
    var chosen = box.querySelector(".chosen");
    if (chosen && chosen.scrollIntoView) chosen.scrollIntoView({ block: "nearest" });
  }

  /** Put a suggestion in the order line, and ask what may follow it. */
  function take(s) {
    var input = $("command");
    input.value = s;
    input.focus();
    askHint(s);
  }

  function note(text) {
    log.append({ tick: state.snapshot ? state.snapshot.tick : 0, ship_time: state.snapshot ? state.snapshot.ship_time : "T", severity: "routine", kind: "client.note", text: text, stamp: "" });
  }

  // -- wiring -----------------------------------------------------------------------

  function init() {
    log = new root.LogPanel($("log-list"));
    seaMap = new root.SeaMap($("map"));
    svg = $("ship-view");

    var params = new URLSearchParams(location.search);
    if (params.has("facing")) {
      var f = Number(params.get("facing"));
      if (!isNaN(f)) state.facingOverride = U.rad(f);
    }

    Array.prototype.forEach.call(document.querySelectorAll("[data-filter]"), function (b) {
      b.addEventListener("click", function () {
        Array.prototype.forEach.call(document.querySelectorAll("[data-filter]"), function (o) {
          o.classList.remove("active");
        });
        b.classList.add("active");
        log.setFilter(b.getAttribute("data-filter"));
      });
    });
    $("btn-go").addEventListener("click", function () {
      driver("go");
    });
    $("btn-hold").addEventListener("click", function () {
      driver("hold");
    });
    $("btn-tick").addEventListener("click", function () {
      driver("tick", 60);
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-time]"), function (b) {
      b.addEventListener("click", function () {
        driver("time", Number(b.getAttribute("data-time")));
      });
    });

    var input = $("command");
    input.addEventListener("input", function () {
      askHint(input.value);
    });
    input.addEventListener("blur", function () {
      setTimeout(hideHint, 150);
    });
    input.addEventListener("keydown", function (ev) {
      var h = state.hint;
      var showing = h.items.length > 0;
      if (ev.key === "Tab") {
        // Tab takes the first suggestion, or the one the arrows chose
        if (showing) {
          take(h.items[h.chosen >= 0 ? h.chosen : 0]);
          ev.preventDefault();
        } else if (input.value.trim()) {
          ev.preventDefault(); // nothing to take; the focus stays on the line
        }
      } else if (ev.key === "Escape") {
        hideHint();
      } else if (ev.key === "Enter") {
        if (showing && h.chosen >= 0) {
          take(h.items[h.chosen]); // the one chosen goes into the line; Enter again gives it
          ev.preventDefault();
          return;
        }
        hideHint();
        submitLine(input.value);
        input.value = "";
      } else if (ev.key === "ArrowUp" || ev.key === "ArrowDown") {
        ev.preventDefault();
        var down = ev.key === "ArrowDown";
        if (showing) {
          // the arrows move through the suggestions
          var n = h.items.length;
          h.chosen = down ? (h.chosen + 1) % n : h.chosen <= 0 ? n - 1 : h.chosen - 1;
          drawHint();
          return;
        }
        // with none showing, through the lines given before
        if (!down && state.historyIndex > 0) {
          state.historyIndex -= 1;
          input.value = state.history[state.historyIndex];
        } else if (down && state.historyIndex < state.history.length - 1) {
          state.historyIndex += 1;
          input.value = state.history[state.historyIndex];
        } else if (down) {
          state.historyIndex = state.history.length;
          input.value = "";
        }
      }
    });

    $("btn-library").addEventListener("click", function () {
      if (document.body.classList.contains("library-open")) closeLibrary();
      else openLibrary("");
    });
    var ease = $("opt-ease-on-station");
    if (ease) {
      ease.addEventListener("change", function () {
        driver("ease_on_station", ease.checked);
      });
    }
    $("btn-map-centre").addEventListener("click", function () {
      seaMap.centre();
    });
    $("btn-map-fit").addEventListener("click", function () {
      seaMap.fit();
    });

    document.addEventListener("keydown", function (ev) {
      if (ev.target === input || /^(INPUT|TEXTAREA|SELECT)$/.test(ev.target.tagName || "")) return;
      var current = state.facingOverride !== null ? state.facingOverride : state.snapshot ? P.leewardFacing(state.snapshot.ship.tack) : Math.PI / 2;
      if (ev.key === "]") state.facingOverride = U.wrap2pi(current + U.POINT);
      else if (ev.key === "[") state.facingOverride = U.wrap2pi(current - U.POINT);
      else if (ev.key === "\\") state.facingOverride = null;
      else return;
      drawShip();
    });

    window.addEventListener("resize", function () {
      if (state.snapshot) seaMap.draw(state.snapshot);
    });

    input.focus();
    connect();
  }

  root.FreeSailApp = { init: init, state: state, drawShip: drawShip };
  document.addEventListener("DOMContentLoaded", init);
})(window);
