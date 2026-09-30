/* map.js: the map, and from package 32 the captain's chart (spec M5 §17, the first
 * half). North up, the hull symbol with its heading, the last hour's track, a wind
 * arrow and a scale bar; under the track, when the world has a chart region, the
 * coast and the features of data/charts/ as the captain's chart of 1804 will have them
 * (fetched once from /api/chart). The truth's position is still drawn for now, since the
 * reckoning does not exist yet (package 33 draws the reckoned position and its ellipse
 * instead and takes the truth out of the snapshot). The truth's depth tiles are never
 * drawn. Canvas; drawn on every snapshot. */
(function (root) {
  "use strict";
  var U = root.Units;
  var TRACK_SECONDS = 3600;
  var M_PER_DEG = 60 * U.NAUTICAL_MILE; // a degree of latitude: sixty miles of 1852 m

  function Map(canvas) {
    this.canvas = canvas;
    this.track = []; // {tick, x, y, lat, lon}
    this.lastTick = -1;
    this.chart = null; // {coast, features, bounds, attribution} or null
    this.chartAsked = false;
  }

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
      })
      .catch(function () {
        self.chart = null;
      });
  };

  Map.prototype.record = function (snap) {
    var tick = snap.tick;
    if (tick < this.lastTick) this.track = []; // a replay or a new world
    if (tick !== this.lastTick) {
      var p = { tick: tick, x: snap.ship.x, y: snap.ship.y };
      if (snap.position) {
        p.lat = snap.position.lat_deg;
        p.lon = snap.position.lon_deg;
      }
      this.track.push(p);
    }
    this.lastTick = tick;
    var cutoff = tick - TRACK_SECONDS;
    while (this.track.length > 1 && this.track[0].tick < cutoff) this.track.shift();
  };

  // The projection: the plane's metres when the world has no position; with one, an
  // equirectangular projection about the ship (metres east and north of her), so the
  // coast, the features, the track and the ship share one frame.
  function frameOf(snap) {
    if (snap.position) {
      var lat0 = snap.position.lat_deg, lon0 = snap.position.lon_deg;
      var k = Math.cos(lat0 * Math.PI / 180);
      return {
        geo: true,
        ship: [0, 0],
        of: function (lat, lon) {
          return [(lon - lon0) * k * M_PER_DEG, (lat - lat0) * M_PER_DEG];
        },
        track: function (p) {
          return p.lat === undefined ? null : [(p.lon - lon0) * k * M_PER_DEG, (p.lat - lat0) * M_PER_DEG];
        }
      };
    }
    return {
      geo: false,
      ship: [snap.ship.x, snap.ship.y],
      track: function (p) {
        return [p.x, p.y];
      }
    };
  }

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
    var label = scale * U.NAUTICAL_MILE > 30; // names when a mile is thirty pixels
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

    if (snap.position) this.askChart();
    var frame = frameOf(snap);
    var ship = snap.ship;
    var s0 = frame.ship;
    // scale: fit the track and at least a few cables around the ship; with a chart, a
    // few miles, so the coast is seen
    var minX = s0[0], maxX = s0[0], minY = s0[1], maxY = s0[1];
    var pts = [];
    this.track.forEach(function (p) {
      var m = frame.track(p);
      if (!m) return;
      pts.push(m);
      if (m[0] < minX) minX = m[0];
      if (m[0] > maxX) maxX = m[0];
      if (m[1] < minY) minY = m[1];
      if (m[1] > maxY) maxY = m[1];
    });
    var least = this.chart && frame.geo ? 4 * U.NAUTICAL_MILE : 3 * U.CABLE;
    var span = Math.max(maxX - minX, maxY - minY, least) * 1.3;
    var scale = Math.min(cw, ch) / span; // px per metre
    var cx = (minX + maxX) / 2;
    var cy = (minY + maxY) / 2;
    function toPx(x, y) {
      return [cw / 2 + (x - cx) * scale, ch / 2 - (y - cy) * scale];
    }

    // the chart under everything else
    var year = snap.ship_time ? parseInt(snap.ship_time.slice(0, 4), 10) : 1805;
    this.drawChart(ctx, frame, toPx, scale, cw, ch, year, inkColour, landColour);

    // a light graticule every cable or mile
    var step = span > 20 * U.CABLE ? U.NAUTICAL_MILE : U.CABLE;
    if (span > 20 * U.NAUTICAL_MILE) step = 5 * U.NAUTICAL_MILE;
    ctx.strokeStyle = "rgba(255,255,255,0.12)";
    ctx.lineWidth = 1;
    var gx0 = Math.floor((cx - span / 2) / step) * step;
    for (var gx = gx0; gx < cx + span / 2; gx += step) {
      var px = toPx(gx, 0)[0];
      ctx.beginPath();
      ctx.moveTo(px, 0);
      ctx.lineTo(px, ch);
      ctx.stroke();
    }
    var gy0 = Math.floor((cy - span / 2) / step) * step;
    for (var gy = gy0; gy < cy + span / 2; gy += step) {
      var py = toPx(0, gy)[1];
      ctx.beginPath();
      ctx.moveTo(0, py);
      ctx.lineTo(cw, py);
      ctx.stroke();
    }

    // the track
    if (pts.length > 1) {
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

    // the hull symbol: a small pointed shape, bow toward the heading
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
    ctx.fillText(step === U.CABLE ? "1 cable" : step === U.NAUTICAL_MILE ? "1 mile" : "5 miles", bx, by - 6);

    // position and course made good
    ctx.textAlign = "right";
    var made = pts.length > 1 ? pts[pts.length - 1] : null;
    var first = pts.length > 1 ? pts[0] : null;
    var cmg = made && first && (made[0] !== first[0] || made[1] !== first[1]) ? U.pointName(Math.atan2(made[0] - first[0], made[1] - first[1])) : "—";
    var where;
    if (snap.position) {
      where = dm(snap.position.lat_deg, "N", "S") + " " + dm(snap.position.lon_deg, "E", "W");
    } else {
      where = "x " + (ship.x / U.NAUTICAL_MILE).toFixed(2) + " nm  y " + (ship.y / U.NAUTICAL_MILE).toFixed(2) + " nm";
    }
    ctx.fillText(where + "  ·  made good " + cmg, cw - 12, ch - 8);
    if (this.chart && frame.geo && snap.lookout && snap.lookout.count) {
      ctx.textAlign = "left";
      ctx.fillText("in sight: " + snap.lookout.words, 12, 100);
    }
  };

  function dm(value, pos, neg) {
    var h = value >= 0 ? pos : neg;
    var v = Math.abs(value);
    var total = Math.round(v * 60);
    var d = Math.floor(total / 60), m = total % 60;
    return d + "° " + (m < 10 ? "0" : "") + m + "' " + h;
  }

  root.SeaMap = Map;
})(window);
