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
 *
 * Package 37n, the chart's tools: the rose, the line, the ring, the note and the list of
 * marks, by the map's buttons or by a key while the focus is off the order line (a click
 * on the chart gives it the focus): r the rose, l a line, o a ring, n a note, m the list,
 * Escape puts a tool down. The marks are sent to /api/marks and come back on the socket.
 *
 * Package 42, the pictures: a model's `chart` or `ship_view` tool asks the open page, on
 * the socket ({type: "picture", id, view, facing, span, max_px}), for the chart or the
 * ship from the facing asked; the page draws it with its own drawing, scales it to max_px
 * on its longer side and posts it as a PNG to /api/picture/{id}, or says why it could not.
 *
 * Package 45: each picture is drawn on an offscreen canvas of a fixed size that owes
 * nothing to the page's layout or the pane shown (the chart CHART_PX, 1200 by 900, centred
 * on the account at the span asked or the page's view; the ship's view SHIP_PX, 960 by
 * 720, on its own sky), since the page's own canvas was the picture before and the ship's
 * view came out blank: the offscreen <svg> carried the style that hid it (position:
 * absolute; left: -10000px) into the serialised picture, which the SVG image honoured,
 * and the stylesheet's colours were keyed on the page's #ship-view, which the copy had
 * not, so every fill computed to black. The copy now has the class the stylesheet keys on
 * (.ship-view) and is hidden by a holder round it, never by its own style.
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
        seaMap.setMarks(data.marks || []); // the player's pencil, kept with the game (37n)
        state.driver = data.snapshot.driver || state.driver;
        // the log as the server shows it now: rolled up at 60x and above (spec M4 §20)
        data.log.forEach(function (e) {
          log.add(e);
        });
        onSnapshot(data.snapshot);
      } else if (data.type === "event") {
        if (data.event.kind === "query.director_log") openDirectorLog(data.event);
        else if (data.event.kind === "query.director_word") channelSaid(data.event);
        else log.add(data.event);
      } else if (data.type === "channel") {
        addChannelLine(data.line);
      } else if (data.type === "rollup") {
        log.addRollup(data.rollup);
      } else if (data.type === "snapshot") {
        onSnapshot(data.snapshot);
      } else if (data.type === "marks") {
        seaMap.setMarks(data.marks);
      } else if (data.type === "picture") {
        paintFor(data);
      } else if (data.type === "restart") {
        // a new game taken up from the harbour (package 59): the page reads it from its start
        location.reload();
      }
    };
  }

  // -- the pictures (package 42; package 45 the fixed canvases and the spans) -----------

  var CHART_PX = [1200, 900];
  var SHIP_PX = [960, 720];
  // the styles written into the ship's picture, which an image does not read from the page
  var STYLED = ["fill", "fill-opacity", "stroke", "stroke-width", "stroke-opacity", "stroke-dasharray", "stroke-linecap", "stroke-linejoin", "vector-effect", "opacity", "font-size", "font-family", "display", "visibility"];
  var lastPaint = { view: "", ms: 0, span: "" }; // the last picture's drawing time, for a measure

  /** A canvas no larger than `maxPx` on its longer side, drawn from `source`. */
  function fitted(source, maxPx) {
    var w = source.width, h = source.height;
    var k = Math.min(1, (maxPx || 1568) / Math.max(w, h, 1));
    if (k >= 1) return source;
    var c = document.createElement("canvas");
    c.width = Math.max(1, Math.round(w * k));
    c.height = Math.max(1, Math.round(h * k));
    c.getContext("2d").drawImage(source, 0, 0, c.width, c.height);
    return c;
  }

  /** The chart as a picture: an offscreen canvas of CHART_PX, the chart drawn on it by
   *  the map's own renderer, centred on the account at the span asked (harbour, coast,
   *  passage, whole) or at the page's view when none is said (package 45). */
  function chartPicture(req) {
    if (!state.snapshot) return Promise.reject(new Error("the chart has no snapshot yet"));
    var c = document.createElement("canvas");
    c.width = CHART_PX[0];
    c.height = CHART_PX[1];
    var t0 = root.performance ? root.performance.now() : 0;
    var span = seaMap.paint(state.snapshot, c, req.span || "");
    lastPaint = { view: "chart", ms: (root.performance ? root.performance.now() : 0) - t0, span: span };
    return Promise.resolve(c);
  }

  /** The ship's view as a picture: the viewer's drawing again at the facing asked, in an
   *  offscreen <svg> of SHIP_PX with the stylesheet's class, its computed styles written
   *  into it, serialised and drawn through an Image onto a canvas filled first with the
   *  view's own sky (package 45: see the head of this file for what was blank before). */
  function shipPicture(req) {
    if (!state.ship || !state.snapshot) return Promise.reject(new Error("the viewer has no ship drawn yet"));
    var snap = state.snapshot;
    var facing = req.facing === null || req.facing === undefined ? P.leewardFacing(snap.ship.tack) : U.rad(req.facing);
    var w = SHIP_PX[0], h = SHIP_PX[1];
    var t0 = root.performance ? root.performance.now() : 0;
    // the holder hides the copy; the copy's own style carries nothing but the viewer's
    var holder = document.createElement("div");
    holder.style.position = "absolute";
    holder.style.left = "-10000px";
    holder.style.top = "0";
    holder.style.width = w + "px";
    holder.style.height = h + "px";
    var off = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    off.setAttribute("class", "ship-view");
    off.setAttribute("width", w);
    off.setAttribute("height", h);
    holder.appendChild(off);
    document.body.appendChild(holder);
    var sky;
    try {
      var scene = P.project(P.buildSkeleton(state.ship, snap), facing, snap.ship.heel);
      root.ShipView.render(off, scene, {
        name: state.ship.name,
        facingWords: req.facing_words || facingWords(facing),
        heelWords: U.formatSigned(snap.ship.heel, "to starboard", "to larboard"),
      });
      sky = getComputedStyle(off).backgroundColor;
      // the page's styles written into the picture, which an image does not read
      Array.prototype.forEach.call(off.querySelectorAll("*"), function (node) {
        var cs = getComputedStyle(node);
        var said = STYLED.map(function (k) { return k + ":" + cs.getPropertyValue(k); }).join(";");
        node.setAttribute("style", said);
      });
      var text = new XMLSerializer().serializeToString(off);
    } finally {
      document.body.removeChild(holder);
    }
    return new Promise(function (ok, no) {
      var img = new Image();
      img.onload = function () {
        var c = document.createElement("canvas");
        c.width = w;
        c.height = h;
        var ctx = c.getContext("2d");
        ctx.fillStyle = sky && sky !== "rgba(0, 0, 0, 0)" ? sky : "#dfe7ea";
        ctx.fillRect(0, 0, w, h);
        ctx.drawImage(img, 0, 0, w, h);
        lastPaint = { view: "ship", ms: (root.performance ? root.performance.now() : 0) - t0, span: "" };
        ok(c);
      };
      img.onerror = function () { no(new Error("the ship's view did not draw")); };
      img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(text);
    });
  }

  /** A picture drawn on request, for a measure or a test: `picture('chart', 'whole')` or
   *  `picture('ship', 90)`; resolves to {width, height, ms, span, png} (a data URL). */
  function picture(view, arg) {
    var made = view === "chart" ? chartPicture({ span: arg || "" }) : shipPicture({ facing: arg });
    return made.then(function (c) {
      return { width: c.width, height: c.height, ms: lastPaint.ms, span: lastPaint.span, png: c.toDataURL("image/png") };
    });
  }

  function paintFor(req) {
    var made;
    try {
      made = req.view === "chart" ? chartPicture(req) : shipPicture(req);
    } catch (e) {
      made = Promise.reject(e);
    }
    made
      .then(function (canvas) {
        var c = fitted(canvas, req.max_px);
        return new Promise(function (ok, no) {
          c.toBlob(function (blob) {
            if (blob) ok({ blob: blob, w: c.width, h: c.height });
            else no(new Error("the canvas gave no picture"));
          }, "image/png");
        });
      })
      .then(function (p) {
        if (req.max_bytes && p.blob.size > req.max_bytes) throw new Error("the picture is larger than the bound");
        return fetch("/api/picture/" + req.id + "?width=" + p.w + "&height=" + p.h, {
          method: "POST",
          headers: { "Content-Type": "image/png" },
          body: p.blob,
        });
      })
      .catch(function (e) {
        var why = encodeURIComponent(String((e && e.message) || e));
        fetch("/api/picture/" + req.id + "?failed=" + why, { method: "POST" });
      });
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

  // `speed N` and `time N` are the same (spec M4 §20 said 300, now 1000; the server clamps)
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

  // -- the director's log (spec M7b §6; package 50) --------------------------------------
  // Shut during play; opened by the player's own request at the order line ('the
  // director's log'), which the game records and tells the director of. Shown beside the
  // play log, in the ship view's place, every act with its stamp and its reason.

  function openDirectorLog(e) {
    var lines = (e.data && e.data.lines) || String(e.text || "").split("\n");
    $("director-log").textContent = lines.join("\n");
    $("director-panel").hidden = false;
    document.body.classList.add("director-open");
  }

  function closeDirectorLog() {
    $("director-panel").hidden = true;
    document.body.classList.remove("director-open");
    drawShip();
    $("command").focus();
  }

  // -- the channel between the player and the director (package 67) ---------------------
  // 'director: <words>' at the order line goes to the director's log and its next sample;
  // its answer comes here. Neither is a line of the play log.

  function addChannelLine(line) {
    if (!line || !line.text) return;
    var row = document.createElement("div");
    row.className = "channel-line " + (line.from === "the director" ? "from-director" : "from-player");
    var who = line.from === "the director" ? "The director" : "You";
    row.textContent = (line.stamp ? line.stamp + "  " : "") + who + ": " + line.text;
    $("channel-lines").appendChild(row);
    $("channel-lines").scrollTop = $("channel-lines").scrollHeight;
    $("channel-panel").hidden = false;
  }

  function channelSaid(e) {
    var row = document.createElement("div");
    row.className = "channel-line channel-note";
    row.textContent = String(e.text || "");
    $("channel-lines").appendChild(row);
    $("channel-panel").hidden = false;
  }

  function closeChannel() {
    $("channel-panel").hidden = true;
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

  // -- the chart's tools (package 37n) ------------------------------------------------
  //
  // The rose and the pencil are the chart's (map.js); here the buttons, the keys, the list
  // of marks and the server's route (/api/marks). A mark goes to the server, which keeps
  // it with the game and sends the list back to every page on the socket; nothing else
  // reads it.

  var MAP_KEYS = { r: "rose", l: "line", o: "ring", n: "note", m: "marks" };

  function markSink() {
    return {
      add: function (mark) {
        if (mark.kind === "note") {
          $("mark-note-text").value = ""; // a note's words are spent on it
          seaMap.noteText = "";
        }
        post("/api/marks", mark).then(function (r) {
          if (r && r.detail) note("The chart: " + r.detail);
        });
      },
      remove: function (id) {
        fetch("/api/marks/" + encodeURIComponent(id), { method: "DELETE" });
      },
      changed: drawMarksPane,
    };
  }

  function mapTool(what) {
    if (what === "rose") seaMap.toggleRose();
    else if (what === "marks") {
      var pane = $("marks-pane");
      pane.hidden = !pane.hidden;
      drawMarksPane();
    } else {
      seaMap.useTool(what);
      if (what === "note" && seaMap.tool === "note" && !$("mark-note-text").value.trim()) {
        $("marks-pane").hidden = false; // the words first, then the place
        drawMarksPane();
        $("mark-note-text").focus();
      }
    }
  }

  function drawMarksPane() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-tool]"), function (b) {
      b.classList.toggle("active", seaMap.tool === b.getAttribute("data-tool"));
    });
    $("btn-map-rose").classList.toggle("active", !!seaMap.rose.shown);
    $("btn-map-marks").classList.toggle("active", !$("marks-pane").hidden);
    var list = $("marks-list");
    if ($("marks-pane").hidden) return;
    list.innerHTML = "";
    var varWest = root.SeaMap.view.variationOf(state.snapshot);
    if (!seaMap.marks.length) {
      var none = document.createElement("li");
      none.className = "none";
      none.textContent = "No lines, rings or notes laid down.";
      list.appendChild(none);
    }
    seaMap.marks.forEach(function (mark) {
      var li = document.createElement("li");
      var words = document.createElement("span");
      words.textContent = root.SeaMap.view.markWords(mark, varWest);
      var rm = document.createElement("button");
      rm.type = "button";
      rm.textContent = "remove";
      rm.title = "rub it out";
      rm.addEventListener("click", function () {
        seaMap.sink.remove(mark.id);
      });
      li.addEventListener("mouseenter", function () {
        seaMap.lit = mark.id;
        seaMap.redraw();
      });
      li.addEventListener("mouseleave", function () {
        seaMap.lit = null;
        seaMap.redraw();
      });
      li.appendChild(words);
      li.appendChild(rm);
      list.appendChild(li);
    });
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
    $("btn-director-close").addEventListener("click", closeDirectorLog);
    $("btn-channel-close").addEventListener("click", closeChannel);
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
    // the spans as zoom stops (package 45): the ship followed, so many miles across
    Array.prototype.forEach.call(document.querySelectorAll("[data-span]"), function (b) {
      b.addEventListener("click", function () {
        seaMap.showSpan(b.getAttribute("data-span"));
      });
    });
    // the chart's tools (package 37n)
    seaMap.sink = markSink();
    $("btn-map-rose").addEventListener("click", function () {
      mapTool("rose");
    });
    $("btn-map-marks").addEventListener("click", function () {
      mapTool("marks");
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-tool]"), function (b) {
      b.addEventListener("click", function () {
        mapTool(b.getAttribute("data-tool"));
      });
    });
    $("mark-note-text").addEventListener("input", function () {
      seaMap.noteText = $("mark-note-text").value;
    });
    $("mark-ring-nm").addEventListener("input", function () {
      var nm = Number($("mark-ring-nm").value);
      seaMap.ringNm = isFinite(nm) && nm > 0 ? nm : null;
      seaMap.redraw();
    });
    $("btn-marks-clear").addEventListener("click", function () {
      if (seaMap.marks.length && root.confirm("Rub out every line, ring and note?")) {
        fetch("/api/marks", { method: "DELETE" });
      }
    });
    drawMarksPane();

    document.addEventListener("keydown", function (ev) {
      if (ev.target === input || /^(INPUT|TEXTAREA|SELECT)$/.test(ev.target.tagName || "")) return;
      if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
      if (ev.key === "Escape" && seaMap.cancel()) return;
      if (MAP_KEYS[ev.key]) {
        mapTool(MAP_KEYS[ev.key]);
        return;
      }
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

  root.FreeSailApp = { init: init, state: state, drawShip: drawShip, picture: picture };
  document.addEventListener("DOMContentLoaded", init);
})(window);
