/* units.js: the small display-side mirror of freesail/units.py.
 * The snapshot is SI (metres, m/s, radians); people read knots, degrees and points. */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.Units = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";
  var KNOT = 0.514444;
  var NAUTICAL_MILE = 1852.0;
  var CABLE = 185.2;
  var POINT = Math.PI / 16;
  var TWO_PI = 2 * Math.PI;
  var POINTS = [
    "N", "N by E", "NNE", "NE by N", "NE", "NE by E", "ENE", "E by N",
    "E", "E by S", "ESE", "SE by E", "SE", "SE by S", "SSE", "S by E",
    "S", "S by W", "SSW", "SW by S", "SW", "SW by W", "WSW", "W by S",
    "W", "W by N", "WNW", "NW by W", "NW", "NW by N", "NNW", "N by W",
  ];

  function wrap2pi(a) {
    return ((a % TWO_PI) + TWO_PI) % TWO_PI;
  }
  function wrapPi(a) {
    return -(((-a + Math.PI) % TWO_PI + TWO_PI) % TWO_PI - Math.PI);
  }
  function deg(rad) {
    return (rad * 180) / Math.PI;
  }
  function rad(degrees) {
    return (degrees * Math.PI) / 180;
  }
  function knots(ms) {
    return ms / KNOT;
  }
  function pointName(angle) {
    return POINTS[Math.round(wrap2pi(angle) / POINT) % 32];
  }
  function formatHeading(angle) {
    return pointName(angle) + " " + Math.round(deg(wrap2pi(angle))) + "°";
  }
  function formatKnots(ms, digits) {
    return knots(ms).toFixed(digits == null ? 1 : digits) + " kn";
  }
  function formatSigned(rad_, pos, neg) {
    var d = Math.round(deg(rad_));
    if (d === 0) return "0°";
    return Math.abs(d) + "° " + (d > 0 ? pos : neg);
  }
  function formatBells(n) {
    return n === 1 ? "1 bell" : n + " bells";
  }
  function clockOf(isoTime) {
    return isoTime.slice(11, 16);
  }
  function windStrength(ms) {
    var kn = knots(ms);
    if (kn < 1) return "calm";
    if (kn < 4) return "light airs";
    if (kn < 7) return "a light breeze";
    if (kn < 11) return "a gentle breeze";
    if (kn < 17) return "a moderate breeze";
    if (kn < 22) return "a fresh breeze";
    if (kn < 28) return "a strong breeze";
    if (kn < 34) return "a moderate gale";
    if (kn < 41) return "a fresh gale";
    if (kn < 48) return "a strong gale";
    if (kn < 56) return "a whole gale";
    if (kn < 64) return "a storm";
    return "a hurricane";
  }
  function partName(id) {
    return id.replace(/\./g, " ").replace(/_/g, " ");
  }

  return {
    KNOT: KNOT,
    NAUTICAL_MILE: NAUTICAL_MILE,
    CABLE: CABLE,
    POINT: POINT,
    POINTS: POINTS,
    wrap2pi: wrap2pi,
    wrapPi: wrapPi,
    deg: deg,
    rad: rad,
    knots: knots,
    pointName: pointName,
    formatHeading: formatHeading,
    formatKnots: formatKnots,
    formatSigned: formatSigned,
    formatBells: formatBells,
    clockOf: clockOf,
    windStrength: windStrength,
    partName: partName,
  };
});
