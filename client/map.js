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
 * before). The plane's map the same. The view's arithmetic is pure (`view`), for Node. */
(function (root) {
  "use strict";
  var U = root.Units || (typeof require === "function" ? require("./units.js") : null);
  var TRACK_SECONDS = 3600;
  var M_PER_DEG = 60 * U.NAUTICAL_MILE; // a degree of latitude: sixty miles of 1852 m

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

  var view = {
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
    this.listen();
  }

  /** The wheel and the drag on the canvas. */
  Map.prototype.listen = function () {
    var self = this;
    var canvas = this.canvas;
    if (!canvas || !canvas.addEventListener) return;
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
      self.drag = { x: ev.clientX, y: ev.clientY, from: self.drawn.view, moved: false };
      if (canvas.setPointerCapture) canvas.setPointerCapture(ev.pointerId);
      canvas.classList.add("dragging");
    });
    canvas.addEventListener("pointermove", function (ev) {
      var d = self.drag;
      if (!d) return;
      var dx = ev.clientX - d.x, dy = ev.clientY - d.y;
      if (!d.moved && Math.abs(dx) + Math.abs(dy) < 3) return;
      d.moved = true;
      self.hold(panBy(d.from, dx, dy));
    });
    function end() {
      self.drag = null;
      canvas.classList.remove("dragging");
    }
    canvas.addEventListener("pointerup", end);
    canvas.addEventListener("pointercancel", end);
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
    // the bearings: a line from the mark along the reciprocal of the bearing laid down
    (rk.bearings || []).forEach(function (b) {
      var m = toPx.apply(null, frame.of(b.mark_lat_deg, b.mark_lon_deg));
      var ang = (b.bearing_deg + 180) * Math.PI / 180;
      var len = 20 * U.NAUTICAL_MILE * scale;
      ctx.save();
      ctx.setLineDash([6, 4]);
      ctx.strokeStyle = trackColour;
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
      var fm = s.depth_m === null || s.depth_m === undefined ? "no bottom" : Math.round(s.depth_m / U.FATHOM) + " fm";
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
  };

  Map.view = view;
  if (typeof module === "object" && module.exports) module.exports = { SeaMap: Map, view: view };
  else root.SeaMap = Map;
})(typeof window !== "undefined" ? window : this);
