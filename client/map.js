/* map.js: the map. North up, the hull symbol with its heading, the last hour's
 * track, a wind arrow and a scale bar. Canvas; drawn on every snapshot. */
(function (root) {
  "use strict";
  var U = root.Units;
  var TRACK_SECONDS = 3600;

  function Map(canvas) {
    this.canvas = canvas;
    this.track = []; // {tick, x, y}
    this.lastTick = -1;
  }

  Map.prototype.record = function (snap) {
    var tick = snap.tick;
    if (tick < this.lastTick) this.track = []; // a replay or a new world
    if (tick !== this.lastTick) this.track.push({ tick: tick, x: snap.ship.x, y: snap.ship.y });
    this.lastTick = tick;
    var cutoff = tick - TRACK_SECONDS;
    while (this.track.length > 1 && this.track[0].tick < cutoff) this.track.shift();
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
    ctx.fillStyle = seaColour;
    ctx.fillRect(0, 0, cw, ch);

    var ship = snap.ship;
    // scale: fit the track and at least a few cables around the ship
    var minX = ship.x, maxX = ship.x, minY = ship.y, maxY = ship.y;
    this.track.forEach(function (p) {
      if (p.x < minX) minX = p.x;
      if (p.x > maxX) maxX = p.x;
      if (p.y < minY) minY = p.y;
      if (p.y > maxY) maxY = p.y;
    });
    var span = Math.max(maxX - minX, maxY - minY, 3 * U.CABLE) * 1.3;
    var scale = Math.min(cw, ch) / span; // px per metre
    var cx = (minX + maxX) / 2;
    var cy = (minY + maxY) / 2;
    function toPx(x, y) {
      return [cw / 2 + (x - cx) * scale, ch / 2 - (y - cy) * scale];
    }

    // a light graticule every cable or mile
    var step = span > 20 * U.CABLE ? U.NAUTICAL_MILE : U.CABLE;
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
    if (this.track.length > 1) {
      ctx.strokeStyle = trackColour;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      this.track.forEach(function (p, i) {
        var q = toPx(p.x, p.y);
        if (i === 0) ctx.moveTo(q[0], q[1]);
        else ctx.lineTo(q[0], q[1]);
      });
      ctx.stroke();
    }

    // the hull symbol: a small pointed shape, bow toward the heading
    var s = toPx(ship.x, ship.y);
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
    ctx.fillText(step === U.CABLE ? "1 cable" : "1 mile", bx, by - 6);

    // position and course made good
    ctx.textAlign = "right";
    var made = this.track.length > 1 ? this.track[this.track.length - 1] : null;
    var first = this.track.length > 1 ? this.track[0] : null;
    var cmg = made && first && (made.x !== first.x || made.y !== first.y) ? U.pointName(Math.atan2(made.x - first.x, made.y - first.y)) : "—";
    ctx.fillText("x " + (ship.x / U.NAUTICAL_MILE).toFixed(2) + " nm  y " + (ship.y / U.NAUTICAL_MILE).toFixed(2) + " nm  ·  made good " + cmg, cw - 12, ch - 8);
  };

  root.SeaMap = Map;
})(window);
