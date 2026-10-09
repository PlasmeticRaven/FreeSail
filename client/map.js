/* map.js: the map, and from package 32 the captain's chart (spec M5 §17). North up,
 * the hull symbol with its heading, a wind arrow and a scale bar; under the track,
 * when the world has a chart region, the coast and the features of data/charts/ as the
 * captain's chart of 1804 has them (fetched once from /api/chart).
 *
 * Package 33a: the chart is the captain's. The hull is drawn at the reckoned position
 * (snap.reckoning, the account brought up to now) with the ellipse of the master's
 * doubt faintly about it, the track by account, the marks of the noons, the bearings
 * taken and the soundings with their ground; the truth's position is not in the
 * snapshot and nothing here draws it. On the endless plane (no reckoning) the map is
 * what it was: the ship's own metres from the start and the last hour's track. The
 * truth's depth tiles are never drawn. Canvas; drawn on every snapshot.
 *
 * Package 33d: zoom and pan (playtest 12, the owner's note 4). The wheel zooms about the
 * point under it, a drag pans, and the view then stays where it was put while the ship
 * sails on; "centre" puts the ship in the middle and follows her at the scale chosen,
 * and "fit" goes back to the view drawn from the track, as at first. The scale bar, the
 * graticule and the names follow the scale (the names when a mile is thirty pixels, as
 * before). The plane's map the same. The view's arithmetic is pure (`view`), for Node.
 *
 * Package 36: other sail. A sighting (snap.strangers, the lookout's reading) is drawn at
 * its bearing and its distance by estimation from the reckoned position, never at the
 * truth, which the snapshot does not carry; the doubt grows with the estimate (a bar
 * along the bearing, a sixth of the estimate either way, the lookout's own error, the
 * same rule as the held estimate of 33b), and the words beside it are what has been
 * made out: "a sail", "a brig, standing to the eastward", her colours.
 *
 * Package 37n: the chart's tools (the owner's note 5 of 2026-10-09). A protractor rose the
 * player drags by its centre and turns by its rim: its outer ring true degrees, north up,
 * its inner ring the thirty-two points of the compass turned by the variation the master
 * allows (snap.reckoning.variation, the account's and never the world's), and its index a
 * line through the centre across the chart whose bearing is read beside it; shown and
 * hidden by `r` or the button; its place and its turn kept in this browser only
 * (localStorage). And the player's pencil: a line laid between two clicks, a ring about a
 * point (its radius typed, or a second click), a note at a point; listed in a small pane,
 * each removable; kept with the game by the server (/api/marks, `World.chart_marks`, saved
 * and loaded with the save) and read by nothing but this chart. The old bearing lines are
 * cleaned from the drawing (BEARING_FULL_S, BEARING_DROP_S): the snapshot keeps them all.
 * Nothing here reads or draws a true position: a mark is where the player put it on the
 * chart, and the rose stands where he puts it. */
(function (root) {
  "use strict";
  var U = root.Units || (typeof require === "function" ? require("./units.js") : null);
  var TRACK_SECONDS = 3600;
  var M_PER_DEG = 60 * U.NAUTICAL_MILE; // a degree of latitude: sixty miles of 1852 m

  // The bearings taken, cleaned from the chart's drawing (the owner's addition to 37n,
  // 2026-10-09: the bearing lines were the worst clutter in play, and an old one is
  // useless within a glass or two, the ship having run on from where it was taken). A
  // bearing is drawn full for a glass after it is taken (half an hour: at five to eight
  // knots she has run two and a half to four miles from where it was taken), fades to a
  // ghost over
  // the rest of the watch, and is dropped a watch after it was taken (four hours: the
  // officer who took it has gone below), or at once when a later bearing of the same mark
  // replaces it. The noons and the player's own lines and marks are not cleaned, and the
  // snapshot keeps every bearing: this is the drawing, not the record.
  var BEARING_FULL_S = 1800; // a glass
  var BEARING_DROP_S = 4 * 3600; // a watch
  var BEARING_GHOST_ALPHA = 0.2; // how faint an old bearing is at the end of its watch

  // The rose (package 37n): its radius on the screen, and how near the centre or the rim a
  // press takes it (pixels; judgement, a finger's breadth).
  var ROSE_RADIUS_PX = 80;
  var ROSE_CENTRE_GRIP_PX = 14;
  var ROSE_RIM_GRIP_PX = 12;
  var MARKS_MAX = 200; // the server's bound on the pencil (freesail/ui/server.py)

  // -- the view: a scale (pixels a metre) and a centre in the frame's metres -------------

  // A notch of the wheel: a quarter as much again (judgement: eight notches from a league
  // to a cable's view is about right on a 300-pixel map).
  var ZOOM_STEP = 1.25;
  // The closest and the farthest the view goes: a cable across 185 pixels at most (a pixel
  // a metre, the ship's length in fifty), and four hundred miles across three hundred
  // pixels at least.
  var MAX_SCALE = 1;
  var MIN_SCALE = 300 / (400 * U.NAUTICAL_MILE);
  // Names on the chart when a mile is this many pixels (package 32's rule).
  var NAMES_AT_PX_PER_MILE = 30;

  function clampScale(scale) {
    return Math.min(MAX_SCALE, Math.max(MIN_SCALE, scale));
  }

  /** The view drawn from the track: its points (frame metres) and the ship's, at least
   * `least` metres across, with a margin; centred on the middle of them. */
  function fitView(points, ship, least, cw, ch) {
    var minX = ship[0], maxX = ship[0], minY = ship[1], maxY = ship[1];
    points.forEach(function (m) {
      if (m[0] < minX) minX = m[0];
      if (m[0] > maxX) maxX = m[0];
      if (m[1] < minY) minY = m[1];
      if (m[1] > maxY) maxY = m[1];
    });
    var span = Math.max(maxX - minX, maxY - minY, least) * 1.3;
    return { scale: Math.min(cw, ch) / span, cx: (minX + maxX) / 2, cy: (minY + maxY) / 2 };
  }

  /** Frame metres to the canvas's pixels (y down), and back. */
  function toPixels(view, cw, ch, x, y) {
    return [cw / 2 + (x - view.cx) * view.scale, ch / 2 - (y - view.cy) * view.scale];
  }

  function fromPixels(view, cw, ch, px, py) {
    return [view.cx + (px - cw / 2) / view.scale, view.cy - (py - ch / 2) / view.scale];
  }

  /** Zoomed by `factor` about the pixel (px, py), which stays over the same spot. */
  function zoomAbout(view, factor, px, py, cw, ch) {
    var spot = fromPixels(view, cw, ch, px, py);
    var scale = clampScale(view.scale * factor);
    return { scale: scale, cx: spot[0] - (px - cw / 2) / scale, cy: spot[1] + (py - ch / 2) / scale };
  }

  /** Panned by a drag of (dx, dy) pixels: the chart moves with the hand. */
  function panBy(view, dx, dy) {
    return { scale: view.scale, cx: view.cx - dx / view.scale, cy: view.cy + dy / view.scale };
  }

  /** Whether the chart's names are drawn at this scale. */
  function namesShown(scale) {
    return scale * U.NAUTICAL_MILE > NAMES_AT_PX_PER_MILE;
  }

  /** The graticule's step and the scale bar's, for a view `span` metres across. */
  function gridStep(span) {
    if (span > 100 * U.NAUTICAL_MILE) return 20 * U.NAUTICAL_MILE;
    if (span > 20 * U.NAUTICAL_MILE) return 5 * U.NAUTICAL_MILE;
    if (span > 20 * U.CABLE) return U.NAUTICAL_MILE;
    return U.CABLE;
  }

  function stepWords(step) {
    if (step === U.CABLE) return "1 cable";
    if (step === U.NAUTICAL_MILE) return "1 mile";
    return Math.round(step / U.NAUTICAL_MILE) + " miles";
  }

  // -- the chart's tools, pure (package 37n) ---------------------------------------------

  /** The bearings to draw at `tick`, each with its strength: a bearing replaced by a later
   *  one of the same mark is dropped, as is one older than a watch; one older than a glass
   *  fades towards a ghost. [{bearing, alpha}], in the snapshot's order. */
  function bearingsShown(bearings, tick) {
    var latest = {};
    (bearings || []).forEach(function (b) {
      var key = b.id || b.name;
      if (b.tick > tick) return; // not yet taken at this tick (a drawing of the past)
      if (latest[key] === undefined || b.tick >= latest[key]) latest[key] = b.tick;
    });
    var out = [];
    (bearings || []).forEach(function (b) {
      var age = tick - b.tick;
      if (age < 0 || b.tick < latest[b.id || b.name] || age > BEARING_DROP_S) return;
      var alpha = 1;
      if (age > BEARING_FULL_S) {
        alpha = 1 - ((1 - BEARING_GHOST_ALPHA) * (age - BEARING_FULL_S)) / (BEARING_DROP_S - BEARING_FULL_S);
      }
      out.push({ bearing: b, alpha: alpha });
    });
    return out;
  }

  /** The bearing (degrees true, from north clockwise) and the distance (miles) from one
   *  point on the chart to another: latitude and longitude on the chart (the plane sailing
   *  at the middle latitude, as the master works a short run), the plane's metres on it. */
  function measure(a, b) {
    var dx, dy;
    if (a.lat !== undefined) {
      var mid = (((a.lat + b.lat) / 2) * Math.PI) / 180;
      dx = (b.lon - a.lon) * Math.cos(mid) * M_PER_DEG;
      dy = (b.lat - a.lat) * M_PER_DEG;
    } else {
      dx = b.x - a.x;
      dy = b.y - a.y;
    }
    var brg = ((Math.atan2(dx, dy) * 180) / Math.PI + 360) % 360;
    return { bearing_deg: brg, distance_nm: Math.hypot(dx, dy) / U.NAUTICAL_MILE };
  }

  function threeFigures(d) {
    var n = Math.round(d) % 360;
    return (n < 10 ? "00" : n < 100 ? "0" : "") + n + "°";
  }

  /** A bearing in the chart's words: true in degrees, and by the compass in points with the
   *  variation the master allows (west positive: the magnetic bearing is the true one and
   *  the variation west); without a variation (the plane), true alone. */
  function bearingWords(trueDeg, varWest) {
    var t = threeFigures(trueDeg) + " true";
    if (varWest === null || varWest === undefined) return t + ", " + U.pointName((trueDeg * Math.PI) / 180);
    var mag = (((trueDeg + varWest) % 360) + 360) % 360;
    return t + ", " + U.pointName((mag * Math.PI) / 180) + " by the compass (" + threeFigures(mag) + ")";
  }

  /** A distance as the chart's hand writes it: cables under a mile, miles to a tenth. */
  function distanceWords(nm) {
    if (nm < 1) return Math.max(1, Math.round(nm * 10)) + (Math.round(nm * 10) === 1 ? " cable" : " cables");
    return nm.toFixed(1) + " miles";
  }

  /** A point on the chart in words: latitude and longitude to the minute, or the plane's
   *  miles from the start. */
  function placeWords(at) {
    if (!at) return "";
    if (at.lat === undefined) return "x " + (at.x / U.NAUTICAL_MILE).toFixed(2) + " nm, y " + (at.y / U.NAUTICAL_MILE).toFixed(2) + " nm";
    function dm(v, pos, neg) {
      var a = Math.abs(v);
      var d = Math.floor(a);
      var m = Math.round((a - d) * 60);
      if (m === 60) {
        d += 1;
        m = 0;
      }
      return d + "°" + (m < 10 ? "0" : "") + m + "' " + (v >= 0 ? pos : neg);
    }
    return dm(at.lat, "N", "S") + ", " + dm(at.lon, "E", "W");
  }

  /** A mark of the player's pencil in the list's words. */
  function markWords(mark, varWest) {
    var p = mark.points || [];
    if (mark.kind === "line" && p.length === 2) {
      var m = measure(p[0], p[1]);
      return "line " + bearingWords(m.bearing_deg, varWest) + ", " + distanceWords(m.distance_nm) + (mark.text ? ": " + mark.text : "");
    }
    if (mark.kind === "ring") {
      return "ring of " + distanceWords(mark.radius_m / U.NAUTICAL_MILE) + " about " + placeWords(p[0]) + (mark.text ? ": " + mark.text : "");
    }
    return "note at " + placeWords(p[0]) + ": " + (mark.text || "");
  }

  /** What a press at (px, py) takes of a rose centred at (cx, cy) with radius r: "centre",
   *  "rim" or null. */
  function roseHit(cx, cy, r, px, py) {
    var d = Math.hypot(px - cx, py - cy);
    if (d <= ROSE_CENTRE_GRIP_PX) return "centre";
    if (Math.abs(d - r) <= ROSE_RIM_GRIP_PX) return "rim";
    return null;
  }

  /** The bearing (degrees from north, clockwise) of the pixel (px, py) from (cx, cy): the
   *  rose's index turned to it (the canvas's y runs down; north is up). */
  function bearingOfPixel(cx, cy, px, py) {
    return ((Math.atan2(px - cx, cy - py) * 180) / Math.PI + 360) % 360;
  }

  var view = {
    BEARING_FULL_S: BEARING_FULL_S,
    BEARING_DROP_S: BEARING_DROP_S,
    BEARING_GHOST_ALPHA: BEARING_GHOST_ALPHA,
    MARKS_MAX: MARKS_MAX,
    bearingsShown: bearingsShown,
    measure: measure,
    bearingWords: bearingWords,
    distanceWords: distanceWords,
    placeWords: placeWords,
    markWords: markWords,
    roseHit: roseHit,
    bearingOfPixel: bearingOfPixel,
    ZOOM_STEP: ZOOM_STEP,
    MAX_SCALE: MAX_SCALE,
    MIN_SCALE: MIN_SCALE,
    fitView: fitView,
    toPixels: toPixels,
    fromPixels: fromPixels,
    zoomAbout: zoomAbout,
    panBy: panBy,
    namesShown: namesShown,
    gridStep: gridStep,
    stepWords: stepWords,
  };

  function Map(canvas) {
    this.canvas = canvas;
    this.track = []; // the plane's track: {tick, x, y}
    this.lastTick = -1;
    this.chart = null; // {coast, features, bounds, attribution} or null
    this.chartAsked = false;
    // the player's view: null for the view drawn from the track; {scale, follow: true} to
    // follow the ship; {scale, follow: false, at} held at a place (latitude and longitude
    // on the chart, the plane's metres on the plane), so it stays put as the ship sails
    this.view = null;
    this.drawn = null; // the last drawing's {snap, frame, view, cw, ch}, for the hand
    this.drag = null;
    // package 37n: the player's pencil (the server's, given by app.js), the tool in hand
    // ("line", "ring", "note" or null), its first point laid, where the hand is over the
    // chart, the mark lit from the list, and the sink that sends a mark to the server
    this.marks = [];
    this.tool = null;
    this.pending = null;
    this.hover = null;
    this.lit = null;
    this.sink = null; // {add(mark), remove(id), changed()}: app.js
    this.ringNm = null; // a radius typed in the pane, miles
    this.noteText = ""; // the words of the next note, typed in the pane
    this.rose = loadRose(); // {shown, at, index_deg}: this browser's only
    this.roseDrawn = null; // {cx, cy, r} where it was last drawn
    this.listen();
  }

  var ROSE_KEY = "freesail.chart.rose";

  function loadRose() {
    try {
      var kept = JSON.parse(root.localStorage.getItem(ROSE_KEY) || "null");
      if (kept && typeof kept === "object") return { shown: !!kept.shown, at: kept.at || null, index_deg: Number(kept.index_deg) || 0 };
    } catch (e) {
      // no storage here (Node, a private window): the rose starts hidden
    }
    return { shown: false, at: null, index_deg: 0 };
  }

  Map.prototype.keepRose = function () {
    try {
      root.localStorage.setItem(ROSE_KEY, JSON.stringify(this.rose));
    } catch (e) {
      // kept for this page only
    }
  };

  /** The wheel and the drag on the canvas. */
  Map.prototype.listen = function () {
    var self = this;
    var canvas = this.canvas;
    if (!canvas || !canvas.addEventListener) return;
    function local(ev) {
      var r = canvas.getBoundingClientRect();
      return [ev.clientX - r.left, ev.clientY - r.top];
    }
    canvas.addEventListener(
      "wheel",
      function (ev) {
        if (!self.drawn) return;
        ev.preventDefault();
        var notches = ev.deltaMode === 1 ? ev.deltaY / 3 : ev.deltaY / 100;
        var factor = Math.pow(ZOOM_STEP, Math.max(-4, Math.min(4, -notches)));
        var r = canvas.getBoundingClientRect();
        self.zoom(factor, ev.clientX - r.left, ev.clientY - r.top);
      },
      { passive: false }
    );
    canvas.addEventListener("pointerdown", function (ev) {
      if (!self.drawn || ev.button !== 0) return;
      if (canvas.focus) canvas.focus(); // the chart's keys (app.js) while the hand is on it
      var p = local(ev);
      var rd = self.rose.shown ? self.roseDrawn : null;
      var grip = rd ? roseHit(rd.cx, rd.cy, rd.r, p[0], p[1]) : null;
      // the rose's centre drags it and its rim turns it; anywhere else the chart pans
      self.drag = { x: ev.clientX, y: ev.clientY, from: self.drawn.view, moved: false, rose: grip };
      if (canvas.setPointerCapture) canvas.setPointerCapture(ev.pointerId);
      canvas.classList.add("dragging");
    });
    canvas.addEventListener("pointermove", function (ev) {
      var d = self.drag;
      var p = local(ev);
      if (!d) {
        if (self.tool && self.drawn) {
          self.hover = self.placeAt(p[0], p[1]); // the rubber band of the line being laid
          self.redraw();
        }
        return;
      }
      var dx = ev.clientX - d.x, dy = ev.clientY - d.y;
      if (!d.moved && Math.abs(dx) + Math.abs(dy) < 3) return;
      d.moved = true;
      if (d.rose === "centre") {
        self.rose.at = self.placeAt(p[0], p[1]);
        self.redraw();
      } else if (d.rose === "rim") {
        var rd = self.roseDrawn;
        self.rose.index_deg = bearingOfPixel(rd.cx, rd.cy, p[0], p[1]);
        self.redraw();
      } else {
        self.hold(panBy(d.from, dx, dy));
      }
    });
    function end(ev) {
      var d = self.drag;
      self.drag = null;
      canvas.classList.remove("dragging");
      if (!d) return;
      if (d.rose && d.moved) self.keepRose();
      // a click (no drag) with a tool in hand lays its point
      if (!d.moved && !d.rose && self.tool && ev && ev.type === "pointerup") {
        var p = local(ev);
        self.lay(self.placeAt(p[0], p[1]));
      }
    }
    canvas.addEventListener("pointerup", end);
    canvas.addEventListener("pointercancel", end);
    canvas.addEventListener("pointerleave", function () {
      if (self.hover) {
        self.hover = null;
        self.redraw();
      }
    });
  };

  /** The place on the chart under the pixel (px, py): latitude and longitude on the chart,
   *  the plane's metres on the plane; null before the first drawing. */
  Map.prototype.placeAt = function (px, py) {
    var d = this.drawn;
    if (!d) return null;
    var m = fromPixels(d.view, d.cw, d.ch, px, py);
    return d.frame.at(m[0], m[1]);
  };

  // -- the tools (package 37n) ---------------------------------------------------------

  /** Take up a tool ("line", "ring", "note"), or put it down (the same again, or null). */
  Map.prototype.useTool = function (tool) {
    this.tool = this.tool === tool ? null : tool;
    this.pending = null;
    this.hover = null;
    if (this.canvas && this.canvas.classList) this.canvas.classList.toggle("laying", !!this.tool);
    if (this.sink && this.sink.changed) this.sink.changed();
    this.redraw();
  };

  /** Lay the tool's next point at `at`: a line's two ends, a ring's centre and then its
   *  radius (or its centre alone when a radius is typed), a note's place. */
  Map.prototype.lay = function (at) {
    if (!at || !this.tool) return;
    var mark = null;
    if (this.tool === "line") {
      if (!this.pending) this.pending = at;
      else mark = { kind: "line", points: [this.pending, at] };
    } else if (this.tool === "ring") {
      if (this.ringNm > 0) mark = { kind: "ring", points: [at], radius_m: this.ringNm * U.NAUTICAL_MILE };
      else if (!this.pending) this.pending = at;
      else mark = { kind: "ring", points: [this.pending], radius_m: measure(this.pending, at).distance_nm * U.NAUTICAL_MILE };
    } else if (this.tool === "note") {
      var text = (this.noteText || "").trim();
      if (!text && root.prompt) text = (root.prompt("The note:") || "").trim();
      if (text) mark = { kind: "note", points: [at], text: text };
    }
    if (mark) {
      if (mark.kind === "ring" && !(mark.radius_m > 0)) mark = null;
    }
    if (mark) {
      this.pending = null;
      this.hover = null;
      this.tool = null;
      if (this.canvas && this.canvas.classList) this.canvas.classList.remove("laying");
      if (this.sink && this.sink.add) this.sink.add(mark);
      if (this.sink && this.sink.changed) this.sink.changed();
    }
    this.redraw();
  };

  /** The marks as the server keeps them (on the hello and after every change). */
  Map.prototype.setMarks = function (marks) {
    this.marks = Array.isArray(marks) ? marks : [];
    if (this.sink && this.sink.changed) this.sink.changed();
    this.redraw();
  };

  /** Show or hide the rose; shown where it was, or in the middle of the chart when that
   *  is off the chart now. */
  Map.prototype.toggleRose = function () {
    this.rose.shown = !this.rose.shown;
    var d = this.drawn;
    if (this.rose.shown && d) {
      var c = this.rose.at ? d.frame.from(this.rose.at) : null;
      var q = c ? toPixels(d.view, d.cw, d.ch, c[0], c[1]) : null;
      if (!q || q[0] < 0 || q[0] > d.cw || q[1] < 0 || q[1] > d.ch) this.rose.at = this.placeAt(d.cw / 2, d.ch / 2);
    }
    this.keepRose();
    if (this.sink && this.sink.changed) this.sink.changed();
    this.redraw();
  };

  /** Escape: the tool put down, the half-laid mark forgotten. */
  Map.prototype.cancel = function () {
    if (!this.tool && !this.pending) return false;
    this.useTool(null);
    return true;
  };

  /** The variation the master allows, west positive (the account's), or null on the plane. */
  function variationOf(snap) {
    var v = snap && snap.reckoning && snap.reckoning.variation;
    return v && typeof v.deg_west === "number" ? v.deg_west : null;
  }
  view.variationOf = variationOf;

  // The player's pencil: lines, rings and notes in the chart's ink, a little lighter than
  // its print; the one lit from the list heavier. A mark laid on the other frame (the
  // plane's in a world with a chart) is not drawn.
  Map.prototype.drawMarks = function (ctx, snap, frame, toPx, scale, inkColour) {
    var self = this;
    var varWest = variationOf(snap);
    ctx.save();
    ctx.font = "italic 11px serif";
    ctx.textBaseline = "middle";
    ctx.strokeStyle = inkColour;
    ctx.fillStyle = inkColour;
    function px(at) {
      var m = at ? frame.from(at) : null;
      return m ? toPx(m[0], m[1]) : null;
    }
    function line(a, b, label) {
      ctx.beginPath();
      ctx.moveTo(a[0], a[1]);
      ctx.lineTo(b[0], b[1]);
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(a[0], a[1], 2, 0, 2 * Math.PI);
      ctx.arc(b[0], b[1], 2, 0, 2 * Math.PI);
      ctx.fill();
      if (label) {
        ctx.textAlign = "left";
        ctx.fillText(label, (a[0] + b[0]) / 2 + 5, (a[1] + b[1]) / 2 - 7);
      }
    }
    function lineLabel(p0, p1) {
      var m = measure(p0, p1);
      return threeFigures(m.bearing_deg) + " " + distanceWords(m.distance_nm);
    }
    this.marks.forEach(function (mark) {
      var pts = (mark.points || []).map(px);
      if (!pts.length || pts.some(function (q) { return !q; })) return;
      ctx.globalAlpha = 0.85;
      ctx.lineWidth = mark.id && mark.id === self.lit ? 2.5 : 1.2;
      ctx.setLineDash([]);
      if (mark.kind === "line" && pts.length === 2) {
        line(pts[0], pts[1], (mark.text ? mark.text + "  " : "") + lineLabel(mark.points[0], mark.points[1]));
      } else if (mark.kind === "ring") {
        var r = Math.max(2, mark.radius_m * scale);
        ctx.setLineDash([5, 3]);
        ctx.beginPath();
        ctx.arc(pts[0][0], pts[0][1], r, 0, 2 * Math.PI);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.beginPath();
        ctx.arc(pts[0][0], pts[0][1], 1.5, 0, 2 * Math.PI);
        ctx.fill();
        ctx.textAlign = "center";
        ctx.fillText((mark.text ? mark.text + ", " : "") + distanceWords(mark.radius_m / U.NAUTICAL_MILE), pts[0][0], pts[0][1] - r - 7);
      } else if (mark.kind === "note") {
        var q = pts[0];
        ctx.beginPath();
        ctx.moveTo(q[0] - 3, q[1] - 3);
        ctx.lineTo(q[0] + 3, q[1] + 3);
        ctx.moveTo(q[0] - 3, q[1] + 3);
        ctx.lineTo(q[0] + 3, q[1] - 3);
        ctx.stroke();
        ctx.textAlign = "left";
        ctx.fillText(mark.text || "", q[0] + 6, q[1]);
      }
    });
    // the mark being laid: from its first point to the hand, with its figures
    if (this.tool && this.pending) {
      var a = px(this.pending);
      var b = this.hover ? px(this.hover) : null;
      if (a && b) {
        ctx.globalAlpha = 0.6;
        ctx.lineWidth = 1;
        ctx.setLineDash([3, 3]);
        if (this.tool === "ring") {
          var rr = Math.hypot(b[0] - a[0], b[1] - a[1]);
          ctx.beginPath();
          ctx.arc(a[0], a[1], rr, 0, 2 * Math.PI);
          ctx.stroke();
          ctx.setLineDash([]);
          ctx.textAlign = "center";
          ctx.fillText(distanceWords(measure(this.pending, this.hover).distance_nm), a[0], a[1] - rr - 7);
        } else {
          line(a, b, lineLabel(this.pending, this.hover) + "  (" + bearingWords(measure(this.pending, this.hover).bearing_deg, varWest) + ")");
        }
      }
    }
    ctx.restore();
  };

  // The protractor rose (package 37n): north up, its outer ring the true degrees, its inner
  // ring the compass's points turned by the variation the master allows (a westerly
  // variation puts the compass's north west of true north), its index a line through the
  // centre right across the chart, and the index's bearing written under it.
  Map.prototype.drawRose = function (ctx, snap, frame, toPx, cw, ch, inkColour) {
    if (!this.rose.shown) {
      this.roseDrawn = null;
      return;
    }
    var c = this.rose.at ? frame.from(this.rose.at) : null;
    var q = c ? toPx(c[0], c[1]) : [cw / 2, ch / 2];
    var r = Math.max(30, Math.min(ROSE_RADIUS_PX, 0.42 * Math.min(cw, ch)));
    var cx = q[0], cy = q[1];
    this.roseDrawn = { cx: cx, cy: cy, r: r };
    var varWest = variationOf(snap);
    var DEG = Math.PI / 180;
    function at(brgDeg, rad) {
      return [cx + rad * Math.sin(brgDeg * DEG), cy - rad * Math.cos(brgDeg * DEG)];
    }
    ctx.save();
    ctx.strokeStyle = inkColour;
    ctx.fillStyle = "rgba(244,241,234,0.45)"; // the horn of the protractor, the chart under it
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(cx, cy, r - 16, 0, 2 * Math.PI);
    ctx.stroke();
    // the true degrees: every five, longer every ten, figures every thirty
    ctx.fillStyle = inkColour;
    ctx.font = "9px serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    for (var d = 0; d < 360; d += 5) {
      var len = d % 10 === 0 ? 6 : 3;
      var p0 = at(d, r), p1 = at(d, r - len);
      ctx.beginPath();
      ctx.moveTo(p0[0], p0[1]);
      ctx.lineTo(p1[0], p1[1]);
      ctx.stroke();
      if (d % 30 === 0) {
        var t = at(d, r - 11);
        ctx.fillText(String(d), t[0], t[1]);
      }
    }
    // the compass's thirty-two points, turned by the variation: its north at the true
    // bearing 360 less the variation west
    var turn = varWest === null ? 0 : -varWest;
    var inner = r - 18;
    for (var k = 0; k < 32; k++) {
      var b = turn + k * 11.25;
      var l = k % 8 === 0 ? 14 : k % 4 === 0 ? 10 : k % 2 === 0 ? 7 : 4;
      var s0 = at(b, inner), s1 = at(b, inner - l);
      ctx.beginPath();
      ctx.moveTo(s0[0], s0[1]);
      ctx.lineTo(s1[0], s1[1]);
      ctx.stroke();
    }
    // the fleur at the compass's north, and its letters at the four cardinal points
    var nTip = at(turn, inner - 2), nL = at(turn - 4, inner - 14), nR = at(turn + 4, inner - 14);
    ctx.beginPath();
    ctx.moveTo(nTip[0], nTip[1]);
    ctx.lineTo(nL[0], nL[1]);
    ctx.lineTo(nR[0], nR[1]);
    ctx.closePath();
    ctx.fill();
    ctx.font = "10px serif";
    ["N", "E", "S", "W"].forEach(function (name, i) {
      if (i === 0) return;
      var lp = at(turn + i * 90, inner - 20);
      ctx.fillText(name, lp[0], lp[1]);
    });
    // the centre, where it is dragged
    ctx.beginPath();
    ctx.arc(cx, cy, 3, 0, 2 * Math.PI);
    ctx.stroke();
    // the index: right across the chart, faint, and firm from the centre to the rim
    var idx = this.rose.index_deg;
    var far = Math.hypot(cw, ch);
    var e0 = at(idx, far), e1 = at(idx + 180, far), rim = at(idx, r);
    ctx.globalAlpha = 0.5;
    ctx.setLineDash([6, 4]);
    ctx.beginPath();
    ctx.moveTo(e1[0], e1[1]);
    ctx.lineTo(e0[0], e0[1]);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.globalAlpha = 1;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(rim[0], rim[1]);
    ctx.stroke();
    // the reading, under the rose
    ctx.font = "11px serif";
    ctx.fillStyle = inkColour;
    ctx.fillText(bearingWords(idx, varWest), cx, cy + r + 12);
    if (varWest !== null) {
      var vw = Math.abs(varWest);
      ctx.fillText("variation " + vw.toFixed(1) + "° " + (varWest >= 0 ? "W" : "E") + " allowed", cx, cy + r + 25);
    }
    ctx.restore();
  };

  /** Zoom by `factor` about the pixel (px, py); following the ship, about the ship. */
  Map.prototype.zoom = function (factor, px, py) {
    var d = this.drawn;
    if (!d) return;
    if (this.view && this.view.follow) {
      this.view = { scale: clampScale(d.view.scale * factor), follow: true };
      this.redraw();
      return;
    }
    this.hold(zoomAbout(d.view, factor, px, py, d.cw, d.ch));
  };

  /** Hold the view at this scale and centre (frame metres), as a place on the chart. */
  Map.prototype.hold = function (v) {
    var d = this.drawn;
    if (!d) return;
    this.view = { scale: v.scale, follow: false, at: d.frame.at(v.cx, v.cy) };
    this.redraw();
  };

  /** "centre": the ship in the middle, followed, at the scale now drawn. */
  Map.prototype.centre = function () {
    var scale = this.drawn ? this.drawn.view.scale : null;
    this.view = scale ? { scale: scale, follow: true } : null;
    this.redraw();
  };

  /** "fit": the view drawn from the track again. */
  Map.prototype.fit = function () {
    this.view = null;
    this.redraw();
  };

  Map.prototype.redraw = function () {
    if (this.drawn) this.draw(this.drawn.snap);
  };

  /** The view to draw: the player's, else the fit; a place held in another frame than
   * this one's (the world changed) is let go and the ship followed. */
  Map.prototype.viewFor = function (fit, frame) {
    var v = this.view;
    if (!v) return fit;
    if (v.follow) return { scale: v.scale, cx: frame.ship[0], cy: frame.ship[1] };
    var c = frame.from(v.at);
    if (!c) return { scale: v.scale, cx: frame.ship[0], cy: frame.ship[1] };
    return { scale: v.scale, cx: c[0], cy: c[1] };
  };

  Map.prototype.askChart = function () {
    if (this.chartAsked) return;
    this.chartAsked = true;
    var self = this;
    fetch("/api/chart")
      .then(function (r) {
        return r.ok ? r.json() : null;
      })
      .then(function (chart) {
        self.chart = chart;
        self.redraw(); // the coast at once, not at the next snapshot (a held clock sends none)
      })
      .catch(function () {
        self.chart = null;
      });
  };

  Map.prototype.record = function (snap) {
    var tick = snap.tick;
    if (tick < this.lastTick) {
      this.track = []; // a replay or a new world
      this.view = null;
    }
    if (snap.reckoning) {
      // the sphere: the track is the account's, carried in the snapshot
      this.lastTick = tick;
      return;
    }
    if (tick !== this.lastTick) this.track.push({ tick: tick, x: snap.ship.x, y: snap.ship.y });
    this.lastTick = tick;
    var cutoff = tick - TRACK_SECONDS;
    while (this.track.length > 1 && this.track[0].tick < cutoff) this.track.shift();
  };

  // The projection: the plane's metres when the world has no reckoning; with one, an
  // equirectangular projection about the reckoned position (metres east and north of
  // it), so the coast, the features, the track by account and the ship share one frame.
  function frameOf(snap) {
    if (snap.reckoning) {
      var lat0 = snap.reckoning.lat_deg, lon0 = snap.reckoning.lon_deg;
      var k = Math.cos(lat0 * Math.PI / 180);
      return {
        geo: true,
        ship: [0, 0],
        of: function (lat, lon) {
          return [(lon - lon0) * k * M_PER_DEG, (lat - lat0) * M_PER_DEG];
        },
        // a place held by the player's view, and back (package 33d)
        at: function (x, y) {
          return { lat: lat0 + y / M_PER_DEG, lon: lon0 + x / (k * M_PER_DEG) };
        },
        from: function (at) {
          return at && at.lat !== undefined ? [(at.lon - lon0) * k * M_PER_DEG, (at.lat - lat0) * M_PER_DEG] : null;
        }
      };
    }
    return {
      geo: false,
      ship: [snap.ship.x, snap.ship.y],
      at: function (x, y) {
        return { x: x, y: y };
      },
      from: function (at) {
        return at && at.x !== undefined ? [at.x, at.y] : null;
      }
    };
  }
  view.frameOf = frameOf;

  var SYMBOL = {
    headland: "point", island: "point", hill: "point", town: "point", place: "point",
    castle: "square", tower: "square", church: "square", mill: "square", beacon: "square", mark: "square",
    light: "star",
    rock: "cross", ledge: "cross", drying: "cross",
    shoal: "dotted", bank: "dotted",
    anchorage: "anchor", road: "anchor",
    bottom: "none", transit: "none"
  };
  var NAMED = { headland: 1, island: 1, town: 1, place: 1, light: 1, castle: 1, rock: 1, ledge: 1, bank: 1, shoal: 1, anchorage: 1, road: 1, hill: 1 };

  function lit(feature, year) {
    if (!feature.lit) return true;
    if (feature.lit.from !== undefined && feature.lit.from !== null && year < feature.lit.from) return false;
    if (feature.lit.until !== undefined && feature.lit.until !== null && year >= feature.lit.until) return false;
    return true;
  }

  Map.prototype.drawChart = function (ctx, frame, toPx, scale, cw, ch, year, inkColour, landColour) {
    var chart = this.chart;
    if (!chart || !frame.geo) return;
    // the coast
    ctx.strokeStyle = inkColour;
    ctx.fillStyle = landColour;
    ctx.lineWidth = 1;
    var margin = 40;
    chart.coast.forEach(function (line) {
      var first = true, seen = false;
      ctx.beginPath();
      for (var i = 0; i < line.length; i++) {
        var m = frame.of(line[i][1], line[i][0]);
        var q = toPx(m[0], m[1]);
        if (q[0] > -margin && q[0] < cw + margin && q[1] > -margin && q[1] < ch + margin) seen = true;
        if (first) ctx.moveTo(q[0], q[1]);
        else ctx.lineTo(q[0], q[1]);
        first = false;
      }
      if (seen) ctx.stroke();
    });
    // the features, by kind; a light that was not lit in the scenario's year is not on
    // the captain's chart of that year
    var byId = {};
    chart.features.forEach(function (f) {
      byId[f.id] = f;
    });
    var label = namesShown(scale); // names when a mile is thirty pixels
    ctx.font = "11px serif";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    chart.features.forEach(function (f) {
      if (f.kind === "light" && !lit(f, year)) return;
      var sym = SYMBOL[f.kind] || "point";
      if (sym === "none") {
        if (f.kind === "transit" && f.marks && f.marks.length === 2 && byId[f.marks[0]] && byId[f.marks[1]]) {
          var a = byId[f.marks[0]], b = byId[f.marks[1]];
          var pa = toPx.apply(null, frame.of(a.lat_deg, a.lon_deg));
          var pb = toPx.apply(null, frame.of(b.lat_deg, b.lon_deg));
          ctx.save();
          ctx.setLineDash([4, 4]);
          ctx.strokeStyle = inkColour;
          ctx.beginPath();
          ctx.moveTo(pa[0], pa[1]);
          ctx.lineTo(pb[0], pb[1]);
          ctx.stroke();
          ctx.restore();
        }
        return;
      }
      var m = frame.of(f.lat_deg, f.lon_deg);
      var q = toPx(m[0], m[1]);
      if (q[0] < -20 || q[0] > cw + 20 || q[1] < -20 || q[1] > ch + 20) return;
      ctx.fillStyle = inkColour;
      ctx.strokeStyle = inkColour;
      ctx.lineWidth = 1;
      if (sym === "point") {
        ctx.beginPath();
        ctx.arc(q[0], q[1], 2.5, 0, 2 * Math.PI);
        ctx.fill();
      } else if (sym === "square") {
        ctx.fillRect(q[0] - 3, q[1] - 3, 6, 6);
      } else if (sym === "star") {
        ctx.beginPath();
        for (var r = 0; r < 8; r++) {
          var ang = r * Math.PI / 4;
          ctx.moveTo(q[0], q[1]);
          ctx.lineTo(q[0] + 6 * Math.cos(ang), q[1] + 6 * Math.sin(ang));
        }
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(q[0], q[1], 2, 0, 2 * Math.PI);
        ctx.fill();
      } else if (sym === "cross") {
        ctx.beginPath();
        ctx.moveTo(q[0] - 4, q[1]);
        ctx.lineTo(q[0] + 4, q[1]);
        ctx.moveTo(q[0], q[1] - 4);
        ctx.lineTo(q[0], q[1] + 4);
        ctx.stroke();
      } else if (sym === "dotted") {
        ctx.save();
        ctx.setLineDash([2, 2]);
        ctx.beginPath();
        ctx.arc(q[0], q[1], 5, 0, 2 * Math.PI);
        ctx.stroke();
        ctx.restore();
      } else if (sym === "anchor") {
        ctx.fillText("⚓", q[0] - 5, q[1]);
      }
      if (label && NAMED[f.kind]) ctx.fillText(f.name, q[0] + 6, q[1]);
    });
    ctx.textBaseline = "alphabetic";
  };

  // The captain's account on the chart (spec M5 §17): the track by account, the noons,
  // the soundings with their ground, the bearings taken as lines from their marks, and
  // the ellipse of the master's doubt about the reckoned position, faintly.
  Map.prototype.drawAccount = function (ctx, snap, frame, toPx, scale, inkColour, trackColour) {
    var rk = snap.reckoning;
    if (!rk || !frame.geo) return;
    var pts = (rk.track || []).map(function (p) {
      return toPx.apply(null, frame.of(p[1], p[2]));
    });
    if (pts.length > 1) {
      ctx.strokeStyle = trackColour;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      pts.forEach(function (q, i) {
        if (i === 0) ctx.moveTo(q[0], q[1]);
        else ctx.lineTo(q[0], q[1]);
      });
      ctx.stroke();
      // the hourly pricks of the traverse
      ctx.fillStyle = trackColour;
      pts.forEach(function (q) {
        ctx.beginPath();
        ctx.arc(q[0], q[1], 1.5, 0, 2 * Math.PI);
        ctx.fill();
      });
    }
    ctx.font = "10px serif";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    // the bearings: a line from the mark along the reciprocal of the bearing laid down; an
    // old one fading and dropped, a replaced one dropped (package 37n: bearingsShown)
    bearingsShown(rk.bearings, snap.tick).forEach(function (shown) {
      var b = shown.bearing;
      var m = toPx.apply(null, frame.of(b.mark_lat_deg, b.mark_lon_deg));
      var ang = (b.bearing_deg + 180) * Math.PI / 180;
      var len = 20 * U.NAUTICAL_MILE * scale;
      ctx.save();
      ctx.setLineDash([6, 4]);
      ctx.strokeStyle = trackColour;
      ctx.globalAlpha = shown.alpha;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(m[0], m[1]);
      ctx.lineTo(m[0] + len * Math.sin(ang), m[1] - len * Math.cos(ang));
      ctx.stroke();
      ctx.restore();
    });
    // the soundings: the fathoms in small figures and the ground, as a chart prints them
    (rk.soundings || []).forEach(function (s) {
      var q = toPx.apply(null, frame.of(s.lat_deg, s.lon_deg));
      ctx.fillStyle = inkColour;
      // a depth that is not a finite number is drawn as no bottom, never as "NaN fm" (the
      // owner's note of 2026-10-09; the source is looked for in the soundings' record)
      var fm = !Number.isFinite(s.depth_m) ? "no bottom" : Math.round(s.depth_m / U.FATHOM) + " fm";
      ctx.fillText(fm + (s.ground ? " " + s.ground : ""), q[0] + 4, q[1] - 6);
      ctx.beginPath();
      ctx.arc(q[0], q[1], 2, 0, 2 * Math.PI);
      ctx.fill();
    });
    // the noons: a circle with a dot, the log-book's page turned
    (rk.noons || []).forEach(function (n) {
      var q = toPx.apply(null, frame.of(n.lat_deg, n.lon_deg));
      ctx.strokeStyle = inkColour;
      ctx.fillStyle = inkColour;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(q[0], q[1], 5, 0, 2 * Math.PI);
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(q[0], q[1], 1.5, 0, 2 * Math.PI);
      ctx.fill();
      ctx.fillText("noon", q[0] + 7, q[1] + 8);
    });
    // the ellipse of the master's doubt, faintly, about the reckoned position
    var e = rk.ellipse;
    if (e) {
      var s0 = toPx(0, 0);
      var a = Math.max(2, e.semi_major_nm * U.NAUTICAL_MILE * scale);
      var b = Math.max(2, e.semi_minor_nm * U.NAUTICAL_MILE * scale);
      ctx.save();
      ctx.translate(s0[0], s0[1]);
      // the major axis's bearing from north, clockwise; the canvas's y runs down
      ctx.rotate(e.major_bearing_deg * Math.PI / 180);
      ctx.strokeStyle = trackColour;
      ctx.globalAlpha = 0.5;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.ellipse(0, 0, b, a, 0, 0, 2 * Math.PI);
      ctx.stroke();
      ctx.globalAlpha = 0.12;
      ctx.fillStyle = trackColour;
      ctx.fill();
      ctx.restore();
    }
    ctx.textBaseline = "alphabetic";
  };

  // The lookout's estimate of a distance is a sixth out either way (one sigma;
  // freesail/world/lookout.py, DISTANCE_BY_ESTIMATION_FRACTION): the bar's half-length.
  var ESTIMATE_DOUBT = 0.15;

  // other sail in sight (package 36): each at its bearing and estimated distance from
  // the reckoned position, a sail glyph with a bar of doubt along the bearing and the
  // words made out; nothing here knows where she truly is.
  Map.prototype.drawStrangers = function (ctx, snap, frame, toPx, scale, inkColour) {
    var st = snap.strangers;
    if (!st || !st.items || !st.items.length) return;
    var s0 = frame.ship;
    ctx.font = "10px serif";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    st.items.forEach(function (it) {
      if (it.estimate_m === null || it.estimate_m === undefined) return;
      var ang = it.bearing_deg * Math.PI / 180;
      var est = it.estimate_m;
      var near = toPx(s0[0] + est * (1 - ESTIMATE_DOUBT) * Math.sin(ang), s0[1] + est * (1 - ESTIMATE_DOUBT) * Math.cos(ang));
      var far = toPx(s0[0] + est * (1 + ESTIMATE_DOUBT) * Math.sin(ang), s0[1] + est * (1 + ESTIMATE_DOUBT) * Math.cos(ang));
      var at = toPx(s0[0] + est * Math.sin(ang), s0[1] + est * Math.cos(ang));
      ctx.save();
      ctx.strokeStyle = inkColour;
      ctx.globalAlpha = 0.5;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(near[0], near[1]);
      ctx.lineTo(far[0], far[1]);
      ctx.stroke();
      ctx.restore();
      // the glyph: a small sail, point up
      ctx.fillStyle = inkColour;
      ctx.beginPath();
      ctx.moveTo(at[0], at[1] - 6);
      ctx.lineTo(at[0] + 4, at[1] + 4);
      ctx.lineTo(at[0] - 4, at[1] + 4);
      ctx.closePath();
      ctx.fill();
      ctx.fillText(it.words.split(",")[0], at[0] + 7, at[1]);
    });
    ctx.textBaseline = "alphabetic";
  };

  Map.prototype.draw = function (snap) {
    var canvas = this.canvas;
    var ctx = canvas.getContext("2d");
    var dpr = window.devicePixelRatio || 1;
    var cw = canvas.clientWidth || 300;
    var ch = canvas.clientHeight || 300;
    if (canvas.width !== Math.round(cw * dpr) || canvas.height !== Math.round(ch * dpr)) {
      canvas.width = Math.round(cw * dpr);
      canvas.height = Math.round(ch * dpr);
    }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var styles = getComputedStyle(document.documentElement);
    var seaColour = styles.getPropertyValue("--map-sea").trim() || "#7b98a8";
    var inkColour = styles.getPropertyValue("--map-ink").trim() || "#2b2b2b";
    var trackColour = styles.getPropertyValue("--map-track").trim() || "#f2e9d6";
    var landColour = styles.getPropertyValue("--map-land").trim() || "#d9cfb4";
    ctx.fillStyle = seaColour;
    ctx.fillRect(0, 0, cw, ch);

    if (snap.reckoning) this.askChart();
    var frame = frameOf(snap);
    var ship = snap.ship;
    var s0 = frame.ship;
    // scale: fit the track (the last hour's on the plane, the account's last few hours
    // on the chart) and at least a few cables around the ship; with a chart, a few miles,
    // so the coast is seen; and the whole ellipse. The player's zoom and pan (33d) are
    // drawn instead when given.
    var pts = [];
    if (frame.geo) {
      var rk = snap.reckoning;
      var tail = (rk.track || []).slice(-4);
      tail.forEach(function (p) {
        pts.push(frame.of(p[1], p[2]));
      });
      if (rk.ellipse) {
        var r = rk.ellipse.semi_major_nm * U.NAUTICAL_MILE;
        pts.push([-r, -r], [r, r]);
      }
    } else {
      this.track.forEach(function (p) {
        pts.push([p.x, p.y]);
      });
    }
    var least = this.chart && frame.geo ? 4 * U.NAUTICAL_MILE : 3 * U.CABLE;
    var v = this.viewFor(fitView(pts, s0, least, cw, ch), frame);
    this.drawn = { snap: snap, frame: frame, view: v, cw: cw, ch: ch };
    var scale = v.scale; // px per metre
    var span = Math.min(cw, ch) / scale; // the view's width, the shorter way, in metres
    var cx = v.cx;
    var cy = v.cy;
    function toPx(x, y) {
      return toPixels(v, cw, ch, x, y);
    }

    // the chart under everything else
    var year = snap.ship_time ? parseInt(snap.ship_time.slice(0, 4), 10) : 1805;
    this.drawChart(ctx, frame, toPx, scale, cw, ch, year, inkColour, landColour);

    // a light graticule every cable or mile (or five or twenty miles, zoomed out)
    var step = gridStep(span);
    var halfW = cw / 2 / scale, halfH = ch / 2 / scale;
    ctx.strokeStyle = "rgba(255,255,255,0.12)";
    ctx.lineWidth = 1;
    var gx0 = Math.floor((cx - halfW) / step) * step;
    for (var gx = gx0; gx < cx + halfW; gx += step) {
      var px = toPx(gx, 0)[0];
      ctx.beginPath();
      ctx.moveTo(px, 0);
      ctx.lineTo(px, ch);
      ctx.stroke();
    }
    var gy0 = Math.floor((cy - halfH) / step) * step;
    for (var gy = gy0; gy < cy + halfH; gy += step) {
      var py = toPx(0, gy)[1];
      ctx.beginPath();
      ctx.moveTo(0, py);
      ctx.lineTo(cw, py);
      ctx.stroke();
    }

    // the track: the account's on the chart, the plane's own on the plane
    if (frame.geo) {
      this.drawAccount(ctx, snap, frame, toPx, scale, inkColour, trackColour);
      this.drawStrangers(ctx, snap, frame, toPx, scale, inkColour);
    } else if (pts.length > 1) {
      ctx.strokeStyle = trackColour;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      pts.forEach(function (m, i) {
        var q = toPx(m[0], m[1]);
        if (i === 0) ctx.moveTo(q[0], q[1]);
        else ctx.lineTo(q[0], q[1]);
      });
      ctx.stroke();
    }

    // the player's pencil (package 37n), over the account and under the ship
    this.drawMarks(ctx, snap, frame, toPx, scale, inkColour);

    // the hull symbol: a small pointed shape, bow toward the heading, at the reckoned
    // position on the chart
    var s = toPx(s0[0], s0[1]);
    var size = Math.max(10, Math.min(18, 30 * scale));
    ctx.save();
    ctx.translate(s[0], s[1]);
    ctx.rotate(ship.heading);
    ctx.fillStyle = inkColour;
    ctx.beginPath();
    ctx.moveTo(0, -size);
    ctx.quadraticCurveTo(size * 0.42, -size * 0.2, size * 0.32, size * 0.7);
    ctx.lineTo(-size * 0.32, size * 0.7);
    ctx.quadraticCurveTo(-size * 0.42, -size * 0.2, 0, -size);
    ctx.closePath();
    ctx.fill();
    // the heading line
    ctx.strokeStyle = inkColour;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, -size);
    ctx.lineTo(0, -size * 2.2);
    ctx.stroke();
    ctx.restore();

    // north
    ctx.fillStyle = inkColour;
    ctx.font = "12px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("N", cw - 18, 16);
    ctx.beginPath();
    ctx.moveTo(cw - 18, 20);
    ctx.lineTo(cw - 18, 40);
    ctx.moveTo(cw - 22, 26);
    ctx.lineTo(cw - 18, 20);
    ctx.lineTo(cw - 14, 26);
    ctx.stroke();

    // the wind arrow: points where the air goes; labelled with where it comes from
    var wind = snap.wind;
    var ax = 34, ay = 40, alen = 22;
    var toward = wind.true_from + Math.PI;
    ctx.save();
    ctx.translate(ax, ay);
    ctx.rotate(toward);
    ctx.strokeStyle = inkColour;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, alen);
    ctx.lineTo(0, -alen);
    ctx.moveTo(-6, -alen + 8);
    ctx.lineTo(0, -alen);
    ctx.lineTo(6, -alen + 8);
    ctx.stroke();
    ctx.restore();
    ctx.textAlign = "left";
    ctx.fillText("wind " + U.pointName(wind.true_from) + " " + Math.round(U.knots(wind.true_speed)) + " kn", 12, 80);

    // the scale bar
    var barMetres = step;
    var barPx = barMetres * scale;
    var bx = 12, by = ch - 14;
    ctx.strokeStyle = inkColour;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(bx, by);
    ctx.lineTo(bx + barPx, by);
    ctx.moveTo(bx, by - 4);
    ctx.lineTo(bx, by + 4);
    ctx.moveTo(bx + barPx, by - 4);
    ctx.lineTo(bx + barPx, by + 4);
    ctx.stroke();
    ctx.fillText(stepWords(step), bx, by - 6);

    // the position by account and the course made good, in the master's words
    ctx.textAlign = "right";
    var where, cmg;
    if (snap.reckoning) {
      where = snap.reckoning.words;
      cmg = snap.reckoning.course_made_good_deg === null || snap.reckoning.course_made_good_deg === undefined
        ? "—" : U.pointName(snap.reckoning.course_made_good_deg * Math.PI / 180);
    } else {
      var made = pts.length > 1 ? pts[pts.length - 1] : null;
      var first = pts.length > 1 ? pts[0] : null;
      cmg = made && first && (made[0] !== first[0] || made[1] !== first[1]) ? U.pointName(Math.atan2(made[0] - first[0], made[1] - first[1])) : "—";
      where = "x " + (ship.x / U.NAUTICAL_MILE).toFixed(2) + " nm  y " + (ship.y / U.NAUTICAL_MILE).toFixed(2) + " nm";
    }
    ctx.fillText(where + "  ·  made good " + cmg, cw - 12, ch - 8);
    if (snap.reckoning) {
      ctx.textAlign = "left";
      ctx.fillText(snap.reckoning.uncertainty, 12, ch - 36); // above the scale bar's words
    }
    if (this.chart && frame.geo && snap.lookout && snap.lookout.count) {
      ctx.textAlign = "left";
      ctx.fillText("in sight: " + snap.lookout.words, 12, 100);
    }
    // the tool in hand, in words, top middle
    if (this.tool) {
      ctx.textAlign = "center";
      ctx.font = "12px sans-serif";
      var asks = { line: this.pending ? "click the line's other end" : "click where the line begins", ring: this.pending ? "click at the ring's radius" : this.ringNm > 0 ? "click the ring's centre (" + this.ringNm + " miles)" : "click the ring's centre", note: "click where the note goes" };
      ctx.fillText(asks[this.tool] + "; Escape puts the tool down", cw / 2, 16);
    }
    // the rose over everything (package 37n)
    this.drawRose(ctx, snap, frame, toPx, cw, ch, inkColour);
  };

  Map.view = view;
  if (typeof module === "object" && module.exports) module.exports = { SeaMap: Map, view: view };
  else root.SeaMap = Map;
})(typeof window !== "undefined" ? window : this);
