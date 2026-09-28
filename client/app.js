/* app.js: wires the panels to the server. One websocket carries every log
 * event and the snapshots; orders and driver commands go by POST.
 *
 * Developer switches:
 *   ?facing=DEG   view the ship from a fixed bearing (0 ahead, 90 on the
 *                 starboard beam, 270 on the larboard beam) instead of the
 *                 milestone 2 default, abeam to leeward
 *   [ and ]       rotate the facing by a point (11.25 degrees); \ returns to leeward
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
  };

  var log, seaMap, svg;

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
    input.addEventListener("keydown", function (ev) {
      if (ev.key === "Enter") {
        submitLine(input.value);
        input.value = "";
      } else if (ev.key === "ArrowUp") {
        if (state.historyIndex > 0) {
          state.historyIndex -= 1;
          input.value = state.history[state.historyIndex];
        }
        ev.preventDefault();
      } else if (ev.key === "ArrowDown") {
        if (state.historyIndex < state.history.length - 1) {
          state.historyIndex += 1;
          input.value = state.history[state.historyIndex];
        } else {
          state.historyIndex = state.history.length;
          input.value = "";
        }
        ev.preventDefault();
      }
    });

    document.addEventListener("keydown", function (ev) {
      if (ev.target === input) return;
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
