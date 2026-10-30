/* projection.js: the ship as a small 3D skeleton, and its orthographic projection.
 *
 * Pure functions, no DOM, so this file can be tested in Node or reused by a
 * later renderer. Two steps:
 *
 *   buildSkeleton(graph, snapshot) -> skeleton
 *       From the ship graph (/api/ship: spars, sails, lines, hull) and the
 *       current snapshot (brace angles, sheet angles, sail states, reefs,
 *       apparent wind) build figures in SHIP COORDINATES: x forward, y to
 *       starboard, z up from the waterline, metres. Every figure carries the
 *       id and class of the part it stands for; nothing is drawn that is
 *       not a part or a hull dimension.
 *
 *   project(skeleton, facing, heel) -> scene
 *       Heel the skeleton about the waterline, then project it
 *       orthographically for a viewer at bearing `facing` from the ship
 *       (radians clockwise from the bow: 0 ahead, pi/2 on the starboard
 *       beam, pi astern, 3pi/2 on the larboard beam). Screen x is to the
 *       right, screen y is DOWN (SVG), the sea line is y = 0. Figures come
 *       back sorted far to near for painter's drawing.
 *
 * Conventions the skeleton relies on (from the ship files, spec section 6):
 *   spar.height_m   above the deck at midships; for a bowsprit-family spar,
 *                   the height of its outer end
 *   spar.x_m        root spars only; a child spar stands at its parent's x, but
 *                   a yard under the bowsprit or the jib-boom at its own (package 75)
 *   brace_angle     radians from square, positive = starboard yardarm forward
 *   sheet_angle     radians from the centreline, unsigned; the sail lies to lee
 *   heel            radians, positive = heeled to starboard
 *
 * Package 37n (the owner's note 6 of 2026-10-09): a square sail is cut as its ship file's
 * notes say it was worked, between its yard and the yardarms below (CLEW_SPREAD,
 * HEAD_SPREAD, `squareCut`), and a yard stands at its hoist: lowered on the cap while its
 * sail is not set, down with each reef, halfway while the halyards are worked, on the
 * lower cap with a struck topmast housed beside the lower mast head (YARD_ON_CAP_M,
 * HOUSED_ABOVE_CAP_M, STEP_HOIST). The frame stays the ship file's rig at its hoists.
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.Projection = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // Drawing constants: judgements that stand in for data the files do not carry.
  var GAFF_PEAK_ANGLE = (35 * Math.PI) / 180; // a gaff peaks about this much above the horizontal
  var LOOSE_FOOT_HEIGHT_M = 1.5; // foot of a loose-footed gaff sail above the deck
  var JIB_LUFF_FRACTION = 0.7; // a jib's head stops this far up its stay
  var JIB_TACK_FRACTION = 0.04; // and its tack this far up from the stay's foot
  var BELLY = 0.12; // belly of a drawing sail, as a fraction of its shorter side
  var FOOT_SAG = 0.06; // sag of a square sail's foot, fraction of its depth
  var IN_GEAR_DEPTH = 0.35; // a sail in the gear hangs this fraction of its depth
  var DOUBLING = 0.12; // an upper mast overlaps the one below by this fraction of its height
  var MAST_CLASSES = { mast: 1, topmast: 1, topgallant_mast: 1, royal_mast: 1 };
  var HEAD_CLASSES = { bowsprit: 1, jib_boom: 1, flying_jib_boom: 1 };
  var YARD_CLASSES = { yard: 1, lug_yard: 1, lateen_yard: 1 };
  var FURLED_ISH = { furled: 1, sent_down: 1 }; // sent_down: a flying sail stowed (package 57)
  var GATHERED = { in_the_gear: 1, loosed: 1 };
  // States in which a sail draws and bellies: set, and goose-winged (half of it set).
  var DRAWING = { set: 1, goose_winged: 1 };
  // Spars that swing about a pivot (a yard about its slings, a gaff or boom about the mast):
  // the fixed frame reaches as far as they can swing (spec M3 §9 item 14).
  var SWINGING = { yard: 1, lug_yard: 1, lateen_yard: 1, gaff: 1, boom: 1, sprit: 1, studdingsail_boom: 1 };
  // Sails at the same depth along the view axis are drawn in this order, nearest last (spec
  // M0-M2 §12 item 9, judgement): staysails and jibs in the centreline plane, then the gaff
  // sails, then the square sails whose belly stands out from their yards, then the studding
  // sails outside them.
  var SAIL_CLASS_RANK = { jibheaded: 0, gaff: 1, sprit: 1, lateen: 2, lug: 2, square: 3, studding: 4 };
  var WATER_SAIL_FOOT_M = 0.5; // a save-all or water sail comes down to this height off the water (the ship files)
  var UNDER_BOOM_HEAD = 0.6; // and its head spreads along this much of its boom's outer end (the ship files)
  var CURVE_SAMPLES = 6; // points per curved edge when a sail is cut in two at a mast
  // A stay with no run to another spar (the frigate's storm mizzen's, "hooked under the after
  // trestle-tree, and set up on deck", Luce 1884 ch. X; "a horse, abaft and parallel to the
  // mizen-mast", Steel 1794): it hangs parallel to its mast, this far abaft it (judgement:
  // the after end of the trestle-trees), and the sail on it is placed from the ship file.
  var STAY_ABAFT_M = 0.6;
  // Package 37n: a square sail as its file has it (the owner's note 6 of 2026-10-09: the
  // cutter's square sail drawn too short). The ship files' sails are worked by
  // tools/gen_ships.py on one rule, which their notes state ("between its yard and the
  // yardarms below (head 0.82 of the yard)"): the clews spread to nine-tenths of the yard
  // below, and the head is what the area leaves over the depth between the two yards; a
  // sail with no yard below it (a course, the cutter's square sail) is as broad as
  // nine-tenths of its own yard, head and foot, and as deep as its area over that. The
  // viewer drew every square sail the whole yard broad and its area over the whole yard
  // deep: a tenth too shallow for a course, and a topgallant or royal too deep by a sixth.
  var CLEW_SPREAD = 0.9; // the clews at nine-tenths of the yard below (gen_ships.py)
  var HEAD_SPREAD = 0.9; // a sail with no yard below: head and foot nine-tenths of its yard
  // Package 37n: a yard at its hoist (the owner's note 6). A yard that hoists (one on an
  // upper mast with a halyard, its square sail bent) stands at the ship file's height while
  // its sail is set, comes down with each reef by the depth the reef takes out of the sail,
  // and is lowered on the cap of the mast below while the sail is not set ("sheeted home and
  // not hoisted", loosed, in the gear, furled); a step of hoisting or settling the halyards
  // in hand draws it halfway, the work in its stages (docs/design/Presentation.md). Struck
  // topmasts (strike_topmasts.yaml: "topsail yards lowered on the caps") are housed, the
  // topmast's head just above the lower cap and its yard on that cap; a yard or a mast sent
  // down on deck is not drawn, as before. A yard on a lower mast does not move: the lower
  // yards hang in their slings, and the cutter's square-sail yard, which the file crosses
  // "as a yard the engine can hoist and brace", is the yard her topsail sheets to.
  var YARD_ON_CAP_M = 0.3; // a lowered yard's slings above the cap it rests on (judgement)
  var HOUSED_ABOVE_CAP_M = 0.6; // a housed topmast's head above the lower cap: its own cap's depth (judgement)
  var HOISTED_STATES = { set: 1, goose_winged: 1, blown_out: 1, wrecked: 1 };
  // the steps of the square sail's evolutions that move its yard (data/evolutions/*_square.yaml):
  // hoisting or settling the halyards, halfway; reefing or shaking out, down on the cap
  var STEP_HOIST = { hoist: 0.5, settle_halyards: 0.5, clew_down: 0.5, reef: 0, shake_out: 0 };
  // Package 57 (the owner's notes 4 and 5 of the Éclair's first cruise; the lead's finding
  // of 18:29). A square yard is slung before its mast, the sail hanging before the yard, so
  // that from ahead the sail hides the mast and from astern the mast hides the sail: the
  // yard's slings stand this fraction of the beam before the mast (judgement: the mast's
  // half-diameter and the yard's, about a twentieth of the beam). A lug lies on the lee side
  // of its mast, slung a third of its yard from the fore end with two thirds of the sail
  // abaft the mast (Forfait 1788 pp. 5 to 6; Steel 1794, LUGGER), the whole cut swung about
  // its slings by the sheet's angle: the slings this fraction of the beam to leeward of the
  // mast (judgement: the mast's half-diameter). A lug lowered, or a sail set flying and sent
  // down, lies on deck with its yard, this high above the deck (judgement).
  var YARD_BEFORE_MAST_OF_BEAM = 0.05;
  var LUG_LEE_OF_MAST_OF_BEAM = 0.03;
  var ON_DECK_M = 0.6;
  // Package 75 (B5.3; docs/design/Design-ShipsEngineExtensions.md §6.2). A yard under the
  // bowsprit or the jib-boom (the spritsail yard, the sprit-topsail yard) stands at its own
  // station, where its file has it. Its braces lead to the fore stay and up to the fore top,
  // drawn to the fore mast's head less a metre; the spritsail's sheets lead aft along the side
  // to a sheave abaft the foremost fore shroud (Lavery I30), drawn to the side at the deck this
  // far abaft the fore mast (judgement).
  var SPRIT_SHEET_ABAFT_M = 1.0;
  var FORE_TOP_BELOW_HEAD_M = 1.0;
  // Package 75 (B5.1; docs/design/Build-Ships.md §6): a hull whose file gives a profile
  // (`hull.profile`, §5.1: x forward of midships, z above her waterline) is drawn from it, as
  // herself. Each side is drawn in strips, one polygon between each two neighbouring stations,
  // so that the views ahead and astern are filled (one polygon a side left about 40% of the
  // hull unfilled dead ahead, measured in the hull design's scratch); the seams are not drawn,
  // and an outline strokes the rail, the stem, the low edge and the stern. The stations are the
  // rail's and the half-breadths' x's with a grid of sixteen between the taffrail and the stem
  // head, and the points where the stern's and the stem's lines come up out of the cut.
  var CUT_Z_M = -0.8; // the side's low edge, below the water (today's cut, judgement)
  var CUT_SHARE = 0.92; // of the water's half-breadth there, without a midship section (today's)
  var STATION_GRID = 16;
  var DECK_SHARE = 0.95; // a deck at this share of the rail's half-breadth: inside the bulwark (judgement)
  // A deck lies inside the side, but a strip of the side near the ends is tall, and its middle
  // can sort behind a deck it hides (the 64's counter seen on the quarter, by 3 cm, measured):
  // each deck strip is sorted this much farther than its middle (judgement).
  var DECK_BEHIND_M = 0.5;
  // Each deck's strake of ports drawn as a band, from the sill up the port's depth: optional,
  // kept only if the owner's screenshot check keeps it (§6). No port is drawn: they are 81's.
  var PORT_BANDS = true;
  // Package 75 (B5.6; Build-Ships.md §6, the form's drawing): where the graph serves the hull as
  // drawn (`hull.stations`, freesail/ship/form.py's rule), the strips stand on those stations and
  // go down to the drawn depth D(x) = max(0.8 m, the water's half-breadth there x tan 20 deg), no
  // deeper than the hull: so no cut edge rises out of the water below 20 degrees of heel (the
  // flat cut does at 8.5 degrees on the frigate, measured in the hull design's scratch).
  var UNDERWATER_HEEL_DEG = 20; // judgement
  // The hull below the waterline, drawn as the owner chooses on the sheets (§19.1 item 16):
  // "hidden" by the sea, as in life, so that only what heel lifts out of it shows (proposed);
  // "faint", seen through the sea; or "solid", a band as the hull was drawn before. `project`
  // takes another in its options; a hull with no profile is drawn as before whatever it says.
  var UNDERWATER = "hidden";
  var UNDERWATER_WAYS = { hidden: 1, faint: 1, solid: 1 };
  // A quarter gallery is a plain box on each quarter (§5.0 principle 9), standing out from the
  // side by this much (judgement: about 2 ft 6 in; no source the files hold gives it).
  var GALLERY_OUT_M = 0.75;
  // A stern light is a plain dark mark in its bay, this share of the bay's breadth across the
  // band (judgement: the rest are the pilasters and mullions between). No opening is drawn.
  var LIGHT_SHARE = 0.6;
  // The plain shape on the knee of the head (`form.head`), at its top: a figure this share of the
  // head's height above the water tall and half that deep, a scroll a third of it across, a
  // billet half of it tall and a quarter deep (judgement; carving is later work).
  var FIGURE_SHARE = 0.3;
  // The knee of the head has breadth, its half-siding this much each side of the middle line
  // (judgement: about a 64's stem's, unread), so that seen ahead or astern it is a strip, not a
  // hairline; the figure on it stands as broad as it is deep, a scroll or a billet as the knee.
  var HEAD_SIDING_M = 0.2;
  // Where a deck ends with another running on under it, a bulkhead closes the space between
  // them (`deckEndFigures`): not within this of the rail's ends, and only where the deck below
  // runs on this far each way (judgement), its face drawn through this many heights of the side.
  var DECK_END_CLEAR_M = 0.5;
  var DECK_END_LEVELS = 6;
  // A served station's lowest point lies on the stern's or the stem's line within this (the
  // stations are served to the millimetre).
  var ON_LINE_M = 0.002;
  var ROUND_UP_SAMPLES = 8; // points along each half of a transom's rounded foot

  // -- vectors ----------------------------------------------------------------

  function v(x, y, z) {
    return [x, y, z];
  }
  function add(a, b) {
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
  }
  function sub(a, b) {
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
  }
  function mul(a, k) {
    return [a[0] * k, a[1] * k, a[2] * k];
  }
  function lerp(a, b, t) {
    return add(a, mul(sub(b, a), t));
  }
  function dot(a, b) {
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  }
  function len(a) {
    return Math.sqrt(dot(a, a));
  }
  function norm(a) {
    var l = len(a);
    return l > 1e-9 ? mul(a, 1 / l) : [0, 0, 0];
  }
  function cross(a, b) {
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  }

  // -- the skeleton ------------------------------------------------------------

  function indexBy(list, key) {
    var out = {};
    (list || []).forEach(function (item) {
      out[item[key]] = item;
    });
    return out;
  }

  function sideSign(side) {
    return side === "larboard" ? -1 : 1;
  }

  /** The horizontal direction a fore-and-aft sail's foot lies along: aft, swung
   *  to the lee side by the sheet angle. tack is "starboard" or "larboard". */
  function sheetDirection(sheetAngle, tack) {
    var lee = tack === "larboard" ? 1 : -1; // wind on the larboard side: sail to starboard
    var g = Math.abs(sheetAngle || 0);
    return [-Math.cos(g), lee * Math.sin(g), 0];
  }

  /** The direction the air moves, in ship coordinates, from the apparent wind angle
   *  (positive on the starboard bow). */
  function windVector(apparentAngle) {
    var a = apparentAngle || 0;
    return [-Math.cos(a), -Math.sin(a), 0];
  }

  /** Where a sail's belly goes: along its normal, away from the wind. */
  function bellyDirection(normal, wind) {
    var n = norm(normal);
    var s = dot(n, wind);
    if (Math.abs(s) < 1e-6) return [0, 0, 0];
    return mul(n, s > 0 ? 1 : -1);
  }

  /** A goose-winged sail's four corners in the square sail's order (larboard yardarm,
   *  starboard yardarm, starboard clew, larboard clew), so a sheet finds its clew: the
   *  weather clew sheeted home `down` below its yardarm, the lee clew hauled up to its
   *  yardarm. `yard` has the skeleton's `a` (larboard arm) and `b` (starboard arm); `tack`
   *  is the side the wind is on. */
  function gooseWingCorners(yard, down, tack) {
    return gooseWingOf([yard.a, yard.b, add(yard.b, down), add(yard.a, down)], tack);
  }

  /** The same from a square sail's own corners [larboard head, starboard head, starboard
   *  clew, larboard clew] (package 37n: the head inside the yardarms, the clews at the yard
   *  below's): the lee clew hauled up to the lee end of the head. */
  function gooseWingOf(c, tack) {
    if (tack === "larboard") return [c[0], c[1], c[1], c[3]];
    return [c[0], c[1], c[2], c[0]];
  }

  /** The triangle of a goose-winged sail from its corners: [lee yardarm, weather
   *  yardarm, weather clew]. */
  function gooseWingTriangle(corners, tack) {
    return tack === "larboard" ? [corners[1], corners[0], corners[3]] : [corners[0], corners[1], corners[2]];
  }

  function gooseWingCentre(corners, tack) {
    var t = gooseWingTriangle(corners, tack);
    return mul(add(add(t[0], t[1]), t[2]), 1 / 3);
  }

  function centroid(points) {
    var s = [0, 0, 0];
    points.forEach(function (p) {
      s = add(s, p);
    });
    return points.length ? mul(s, 1 / points.length) : s;
  }

  /** The points of a path ([[P], [C, P], ...]) as a polyline, each quadratic edge
   *  sampled at CURVE_SAMPLES points. */
  function flattenPath(path) {
    var out = [path[0][0]];
    var prev = path[0][0];
    for (var i = 1; i < path.length; i++) {
      var seg = path[i];
      if (seg.length === 2) {
        for (var k = 1; k <= CURVE_SAMPLES; k++) {
          var t = k / CURVE_SAMPLES;
          var a = lerp(prev, seg[0], t), b = lerp(seg[0], seg[1], t);
          out.push(lerp(a, b, t));
        }
        prev = seg[1];
      } else {
        out.push(seg[0]);
        prev = seg[0];
      }
    }
    return out;
  }

  /** Cut a closed polygon (3D points) by the plane x = x0: [the part forward of it,
   *  the part abaft it] (Sutherland-Hodgman against each half-space). */
  function splitAtX(points, x0) {
    function clip(keep) {
      var out = [];
      for (var i = 0; i < points.length; i++) {
        var p = points[i], q = points[(i + 1) % points.length];
        var pin = keep(p[0]), qin = keep(q[0]);
        if (pin) out.push(p);
        if (pin !== qin) {
          var t = (x0 - p[0]) / (q[0] - p[0]);
          out.push(lerp(p, q, t));
        }
      }
      return out;
    }
    return [
      clip(function (x) {
        return x >= x0;
      }),
      clip(function (x) {
        return x < x0;
      }),
    ];
  }

  /**
   * Build the skeleton. `graph` is /api/ship; `snapshot` is /api/state (may be
   * null for a static drawing: then brace angles and states come from the graph).
   */
  function buildSkeleton(graph, snapshot) {
    var hull = graph.hull;
    var deck = hull.deck_height_m || 1.5;
    var profile = drawnProfile(hull); // package 75: her side, decks and stem, where the file gives them
    var snapSpars = indexBy(snapshot && snapshot.spars, "id");
    var snapSails = indexBy(snapshot && snapshot.sails, "id");
    var snapLines = indexBy(snapshot && snapshot.lines, "id");
    var tack = (snapshot && snapshot.ship && snapshot.ship.tack) || "starboard";
    var wind = windVector(snapshot && snapshot.wind ? snapshot.wind.apparent_angle : Math.PI);
    var busy = {};
    var stepOn = {}; // the step in hand on each subject (package 37n: a yard's hoist)
    ((snapshot && snapshot.evolutions_in_progress) || []).forEach(function (e) {
      if (e.waiting) return;
      busy[e.subject] = e.id;
      if (e.step) stepOn[e.subject] = e.step;
    });

    var sailsBySpar = {}; // spar id -> sails with a role on it
    graph.sails.forEach(function (s) {
      Object.keys(s.roles || {}).forEach(function (role) {
        var target = s.roles[role];
        (sailsBySpar[target] = sailsBySpar[target] || []).push(s);
      });
    });
    var sparSpecs = indexBy(graph.spars, "id");
    var sailSpecs = indexBy(graph.sails, "id");

    function sparState(id) {
      var s = snapSpars[id];
      return s ? s.state : "sound";
    }
    function braceAngle(spec) {
      var s = snapSpars[spec.id];
      return s ? s.brace_angle : spec.brace_angle || 0;
    }
    function sailDyn(spec) {
      var s = snapSails[spec.id] || {};
      return {
        state: s.state || spec.state || "furled",
        reefs: s.reefs != null ? s.reefs : spec.reefs || 0,
        sheet_angle: s.sheet_angle != null ? s.sheet_angle : spec.sheet_angle || 0,
        backed: !!s.backed,
        lug_side: s.lug_side != null ? s.lug_side : spec.lug_side || null,
      };
    }
    var beamM = hull.beam_m || 8;
    var yardBefore = YARD_BEFORE_MAST_OF_BEAM * beamM;
    var lugLee = LUG_LEE_OF_MAST_OF_BEAM * beamM;
    /** A sail set flying and stowed (package 57): sent down on deck with its yard. */
    function sentDownFlying(spec) {
      // the game says `sent_down` for a flying sail stowed (the owner's finding of 2026-10-18:
      // the lugger's topsails drawn at the masthead while sent down), `furled` for a bent one
      var st = sailDyn(spec).state;
      return !!(spec && spec.flying) && (st === "sent_down" || st === "furled");
    }
    /** The sail whose yard this is, if any. */
    function sailOnYard(yardId) {
      var on = (sailsBySpar[yardId] || []).filter(function (s) {
        return (s.roles || {}).yard === yardId;
      });
      var bent = on.filter(function (s) {
        return sailDyn(s).state !== "unbent";
      });
      return bent[0] || on[0] || null;
    }
    /** Whether a yard is on deck with its flying sail sent down (package 57). */
    function yardOnDeck(yardId) {
      var list = (sailsBySpar[yardId] || []).filter(function (s) {
        return (s.roles || {}).yard === yardId;
      });
      return list.length > 0 && list.every(sentDownFlying);
    }
    /** The side a lug lies on, +1 starboard: its own (package 43b), its lower lug's for a lug
     *  topsail (package 57), else the lee side of the tack. */
    function lugSideSign(spec) {
      var host = spec.sheeted_to ? sailSpecs[spec.sheeted_to] : null;
      var side = host ? sailDyn(host).lug_side : spec.dipping ? sailDyn(spec).lug_side : null;
      // a standing lug (the mizen, the taille-vent) is not dipped: its sheet holds it to
      // leeward of the tack it is on, whichever side of the mast its yard hangs
      if (!side) side = tack === "starboard" ? "larboard" : "starboard";
      return sideSign(side);
    }
    /** Whether a lug is hoisted (set, or drawn as set: blown out, wrecked, goose-winged). */
    function lugHoisted(spec) {
      var st = sailDyn(spec).state;
      return st === "set" || st === "goose_winged" || st === "blown_out" || st === "wrecked";
    }
    /** A lug cut from its file (package 57): its corners [tack, throat, peak, clew] in the
     *  fore-and-aft plane, swung about its slings (a third along the yard from the throat;
     *  a lug topsail about its lower lug's, to whose peak its clew is sheeted) by the
     *  sheet's angle to the side it lies on, two thirds of it abaft the mast, the slings on
     *  the lee side of the mast; lowered, along the deck. `mastAt(id)` places a mast.
     *  Returns {pts, pivotMast, sling, along, normal, onDeck}, or null with no cut. */
    function lugCut(spec, mastAt) {
      if (!spec || !spec.corners_m || spec.corners_m.length !== 4) return null;
      var host = spec.sheeted_to ? sailSpecs[spec.sheeted_to] : null;
      var pivot = host && host.corners_m ? host : spec;
      var pc = pivot.corners_m;
      var sx = pc[1][0] + (pc[2][0] - pc[1][0]) / 3;
      var sz = pc[1][1] + (pc[2][1] - pc[1][1]) / 3;
      var M = mastAt((pivot.roles || {}).mast);
      var shift = M && M.xAt ? M.xAt(deck + sz) - sx : 0;
      var down = !lugHoisted(spec) || (host && !lugHoisted(host));
      var a = sailDyn(host || spec).sheet_angle || 0;
      var ss = lugSideSign(spec);
      var ca = Math.cos(a), sa = Math.sin(a);
      var pts = spec.corners_m.map(function (q) {
        var dx = q[0] - sx;
        if (down) return v(sx + shift + dx, 0, deck + ON_DECK_M);
        return v(sx + shift + dx * ca, ss * (lugLee - dx * sa), deck + q[1]);
      });
      var along = down ? [-1, 0, 0] : [-ca, ss * sa, 0];
      return {
        pts: pts,
        pivotMast: M,
        along: along,
        normal: cross(along, [0, 0, 1]),
        onDeck: down,
      };
    }
    /** Package 75 (B5.2; docs/design/Design-ShipsEngineExtensions.md §6.1): a lateen cut at
     *  the mast (the 64's and the 74's mizen course), its corners [tack, throat, peak, clew]
     *  swung whole about its mast's raked line, where its luff is laced, by the sheet's angle
     *  to the sheet's side, as a gaff is (`sheetDirection`); `inPlane`, not swung, as the file
     *  has it (the fixed frame's rig). The yard's truss is on the mast at the throat's height.
     *  `mastAt(id)` places a mast. Returns {pts, truss, aft, normal, mast}, aft the swung
     *  direction of the ship's stern, or null for any other sail. `swungBy`, another sail
     *  whose sheet swings these corners (B5.5; Ext §17.6: the mizen yard laid on the course's
     *  corners and swung by the driver's sheet while the driver is bent). */
    function mastCut(spec, mastAt, inPlane, swungBy) {
      if (!spec || !spec.cut_at_mast || !spec.corners_m || spec.corners_m.length !== 4) return null;
      var M = mastAt((spec.roles || {}).mast);
      if (!M || !M.xAt) return null;
      var tz = deck + spec.corners_m[1][1];
      var truss = v(M.xAt(tz), 0, tz);
      var axis = norm(v(M.xAt(tz + 1) - M.xAt(tz), 0, 1)); // up the mast's raked line
      var lee = tack === "larboard" ? 1 : -1; // as `sheetDirection`: to starboard on the larboard tack
      var turn = inPlane ? 0 : -lee * Math.abs(sailDyn(swungBy || spec).sheet_angle || 0);
      var c = Math.cos(turn), s = Math.sin(turn);
      function swing(p) {
        // about the axis through the truss, by `turn` (Rodrigues)
        return add(add(mul(p, c), mul(cross(axis, p), s)), mul(axis, dot(axis, p) * (1 - c)));
      }
      var pts = spec.corners_m.map(function (q) {
        return add(truss, swing(sub(v(q[0], 0, deck + q[1]), truss)));
      });
      return { pts: pts, truss: truss, aft: swing(v(-1, 0, 0)), normal: swing(v(0, 1, 0)), mast: M };
    }
    /** The sails cut at the mast whose yard this is, bent or not, in the file's order (package
     *  75, B5.5; Ext §17.6): the mizen course, and the driver where she carries one. */
    function cutAtMastOn(yardId) {
      return (sailsBySpar[yardId] || []).filter(function (s) {
        return (s.roles || {}).yard === yardId && !!s.cut_at_mast;
      });
    }
    /** Whether a sail cut at the mast is spread on this boom, bent or not (package 75, B5.5;
     *  Ext §17.6: the driver's boom). */
    /** A gaff sail filed with its four corners [tack, throat, peak, clew], on a hull drawn from
     *  her profile (package 75, the razee's spanker, her stage B): the run and the rise of its head
     *  and the length of its foot, by which its gaff and its sail are drawn as they are filed, in
     *  place of the fixed peak (GAFF_PEAK_ANGLE) and the whole of its spars; or null. */
    function gaffCutOn(gaffId) {
      if (!profile) return null;
      var sail = (sailsBySpar[gaffId] || []).filter(function (s) {
        return s.class === "gaff" && s.corners_m && s.corners_m.length === 4;
      })[0];
      if (!sail) return null;
      var c = sail.corners_m;
      var run = c[1][0] - c[2][0], rise = c[2][1] - c[1][1];
      return { angle: Math.atan2(rise, run), head: Math.hypot(run, rise), foot: Math.abs(c[0][0] - c[3][0]) };
    }

    function boomOfCut(sparId) {
      return (sailsBySpar[sparId] || []).some(function (s) {
        return !!s.cut_at_mast && (s.roles || {}).boom === sparId;
      });
    }
    /** Whether a studding sail boom is rigged out: the snapshot's state (spec 3b §7), else
     *  the ship file's (booms start rigged in), else out while a sail on it is not stowed. */
    function riggedOut(spec) {
      var s = snapSpars[spec.id];
      if (s && s.rigged_out != null) return !!s.rigged_out;
      if (spec.rigged_out != null) return !!spec.rigged_out;
      var sail = (sailsBySpar[spec.id] || [])[0];
      return sail ? !FURLED_ISH[sailDyn(sail).state] : true;
    }
    /** The sheet angle of the sail using this gaff or boom, if any: a gaff or sprit sail's, or
     *  a lateen cut at the mast that is not unbent (package 75, B5.5; Ext §17.6: the driver on
     *  its boom). With the driver in the sail room its boom lies amidships, as a boom with no
     *  sail does. */
    function sheetAngleOf(sparId) {
      var list = sailsBySpar[sparId] || [];
      for (var i = 0; i < list.length; i++) {
        if (list[i].class === "gaff" || list[i].class === "sprit") return sailDyn(list[i]).sheet_angle;
        if (list[i].cut_at_mast && sailDyn(list[i]).state !== "unbent") return sailDyn(list[i]).sheet_angle;
      }
      return 0;
    }

    // -- where each spar is (package 37n) --------------------------------------------

    var halyardOf = {};
    graph.lines.forEach(function (ln) {
      if (ln.class === "halyard") halyardOf[ln.of] = ln.id;
    });
    /** The lower mast a spar stands on, by the ship file's parents. */
    function chainTop(spec) {
      var cur = spec;
      while (cur && cur.parent && sparSpecs[cur.parent]) cur = sparSpecs[cur.parent];
      return cur ? cur.id : null;
    }
    /** The square sail bent to a yard, if any. */
    function squareSailOn(yardId) {
      return (
        (sailsBySpar[yardId] || []).filter(function (s) {
          return s.class === "square" && (s.roles || {}).yard === yardId;
        })[0] || null
      );
    }
    /** The yard below each square yard on the same mast, by the ship file's heights: the
     *  yard whose arms its sail's clews are sheeted to. */
    var yardBelowId = {};
    (function () {
      var yards = graph.spars.filter(function (s) {
        return s.class === "yard";
      });
      yards.forEach(function (y) {
        var top = chainTop(y);
        var best = null;
        yards.forEach(function (o) {
          if (o === y || chainTop(o) !== top || (o.height_m || 0) >= (y.height_m || 0)) return;
          if (best === null || o.height_m > best.height_m) best = o;
        });
        if (best) yardBelowId[y.id] = best.id;
      });
    })();
    function isUpperMast(spec) {
      return !!(spec && MAST_CLASSES[spec.class] && spec.parent);
    }
    /** A yard crossed under the bowsprit or the jib-boom (package 75, B5.3; Ext §6.2): a spar
     *  of class `yard` whose chain roots at a bowsprit, as `Ship.under_bowsprit` has it. */
    function underBowsprit(spec) {
      return !!(spec && spec.class === "yard" && (sparSpecs[chainTop(spec)] || {}).class === "bowsprit");
    }
    /** A topsail over a bare yard the ship file does not carry (the schooner's fore yard,
     *  "a bare spread yard for the topsail's foot; it is not a part here", gen_ships.py):
     *  its sail's foot where that yard is, at its hoist, the file's centre midway down the
     *  sail as the generator puts a sail's between two yards; {z, depth}, or null for any
     *  other yard. */
    function bareFoot(spec) {
      if (yardBelowId[spec.id] || !isUpperMast(sparSpecs[spec.parent])) return null;
      var sail = squareSailOn(spec.id);
      if (!sail) return null;
      var top = deck + (spec.height_m || 0);
      var depth = 2 * (top - (sail.centre_height_m || 0));
      return depth > 0.5 ? { z: top - depth, depth: depth } : null;
    }
    /** Whether a yard hoists: on an upper mast, with a halyard and a square sail bent. */
    function hoists(spec) {
      return spec.class === "yard" && isUpperMast(sparSpecs[spec.parent]) && !!halyardOf[spec.id] && !!squareSailOn(spec.id);
    }
    /** A struck topmast (strike_topmasts.yaml): housed, not on deck. */
    function housed(spec) {
      return spec.class === "topmast" && sparState(spec.id) === "sent_down";
    }
    /** A yard on a topmast sent down with it, by the strike: lowered on the lower cap. Only
     *  the strike sends a topmast's yards down; the light yards sent down go on deck. */
    function onCap(spec) {
      return spec.class === "yard" && sparState(spec.id) === "sent_down" && (sparSpecs[spec.parent] || {}).class === "topmast";
    }
    /** How far up a hoisting yard is: 1 at its hoist, 0 lowered, a half while the halyards
     *  are worked (STEP_HOIST). */
    function hoistFraction(spec) {
      if (onCap(spec)) return 0;
      var sail = squareSailOn(spec.id);
      if (!sail) return 1;
      var h = HOISTED_STATES[sailDyn(sail).state] ? 1 : 0;
      var step = stepOn[sail.id];
      if (step !== undefined && STEP_HOIST[step] !== undefined) h = STEP_HOIST[step];
      return h;
    }

    /** Every spar placed: `where` false for the ship file's rig, every spar aloft at its own
     *  height (the view's fixed frame); true for where each is now, a yard at its hoist and a
     *  struck topmast housed (package 37n). */
    function placeSpars(where) {
      var spars = {};
      function resolve(id) {
        if (spars[id]) return spars[id];
        var spec = sparSpecs[id];
        if (!spec) return null;
        var parent = spec.parent ? resolve(spec.parent) : null;
        var L = spec.length_m || 0;
        var H = spec.height_m || 0;
        var r = { id: id, cls: spec.class, spec: spec, parent: parent, state: sparState(id), side: spec.side };
        if (spec.class === "mast" || (MAST_CLASSES[spec.class] && !parent)) {
          // a lower mast: its rake (positive aft) carries every point on it aft as it rises
          r.x = spec.x_m || 0;
          r.rake = spec.rake || 0;
          var slope = -Math.tan(r.rake);
          r.xAt = function (z) { return (spec.x_m || 0) + slope * (z - deck); };
          // package 75 (B5.1): with a profile, the foot on the uppermost deck where the rake
          // line meets it (`deckAt`), the head where the file has it
          var footZ = profile ? footOnDeck(profile, r.xAt) : null;
          if (footZ === null) footZ = deck;
          r.a = v(r.xAt(footZ), 0, footZ);
          r.b = v(r.xAt(deck + H), 0, deck + H);
          r.head = r.b;
          r.foot = r.a;
        } else if (MAST_CLASSES[spec.class]) {
          // an upper mast continues the line of the one below
          r.rake = parent.rake || 0;
          r.xAt = parent.xAt || function () { return parent.x; };
          var footZ = parent.head[2];
          if (where && housed(spec)) {
            // struck (package 37n): lowered through the cap until its head stands just
            // above the lower cap, its heel down abaft the lower mast head
            footZ = parent.head[2] + HOUSED_ABOVE_CAP_M - H;
            r.housed = true;
          }
          r.x = r.xAt(footZ);
          r.foot = v(r.x, 0, footZ);
          r.head = v(r.xAt(footZ + H), 0, footZ + H);
          // the doubling: drawn, not a position; a housed mast is drawn from its heel
          r.a = r.housed ? r.foot : v(r.xAt(footZ - DOUBLING * H), 0, footZ - DOUBLING * H);
          r.b = r.head;
        } else if (spec.class === "bowsprit") {
          r.x = spec.x_m || 0;
          r.a = v(r.x, 0, deck);
          var dz = Math.min(H, L * 0.95);
          // package 75 (B5.1, B5.3; Indf §12.3; the lead's ruling of 2026-10-29): with a
          // profile, the heel at the stem head, or the rail there if that is lower, and the
          // whole spar from there, its length rising to its end's height as the file has it,
          // so that the yards under it hang from a bowsprit that stands where the file has
          // it; the jib-boom roots at its end. B5.1 drew the heel there and left the end where
          // a heel on the datum put it, short of the file's length
          var heel = profile ? stemHead(profile) : null;
          if (heel) {
            r.a = v(heel[0], 0, heel[1]);
            dz = Math.min(Math.max(deck + H - heel[1], 0), L * 0.95);
          }
          r.b = v(r.a[0] + Math.sqrt(Math.max(L * L - dz * dz, 0)), 0, r.a[2] + dz);
          r.tip = r.b;
        } else if (HEAD_CLASSES[spec.class]) {
          var rootP = parent && parent.tip ? parent.tip : v(hull.length_waterline_m / 2, 0, deck);
          var tipZ = deck + H;
          var dz2 = Math.max(Math.min(tipZ - rootP[2], L * 0.7), 0);
          r.x = rootP[0];
          r.a = rootP;
          r.b = v(rootP[0] + Math.sqrt(Math.max(L * L - dz2 * dz2, 0)), 0, rootP[2] + dz2);
          r.tip = r.b;
        } else if (spec.class === "lateen_yard" && mastCut(sailOnYard(id), resolve)) {
          // package 75 (B5.2; Ext §6.1): the mizen yard of a course cut at the mast, slung at
          // its truss on the mast at the throat's height, its after part along the sail's head
          // to the peak, swung with the sail to the sheet's side; its bare fore part on the
          // same line forward of the mast by the rest of its length, so that it lies to
          // windward as the after part lies to leeward. Aloft in every state: it is not
          // lowered to set, take in or furl its sail. The frame takes it in the file's plane
          // and reaches its swing about the truss (`fullRigFrame`: `pivot` and `reach`) at the
          // heights of the yard's ends and the sail's foot (`heights`), so that the swung peak
          // and clew stay inside it when she heels.
          // B5.5 (Ext §17.6): the yard's line is the course's, the sail cut at the mast with no
          // boom, bent or not, swung by the sheet of the sail bent on the yard; so the yard does
          // not move when the driver is shifted for the course. The frame reaches each sail cut
          // at the mast on it, bent or not: the driver's peak on its driver yard, and its foot
          // at the boom's height
          var bentOn = sailOnYard(id);
          var cuts = cutAtMastOn(id);
          var lineBy = cuts.filter(function (s) {
            return !(s.roles || {}).boom;
          })[0] || bentOn;
          var mc = mastCut(lineBy, resolve, !where, bentOn) || mastCut(bentOn, resolve, !where);
          var truss = mc.truss, peakY = mc.pts[2];
          var headL = len(sub(peakY, truss));
          var fore = Math.max((spec.length_m || headL) - headL, 0);
          r.x = truss[0];
          r.arm = norm(sub(peakY, truss));
          r.a = sub(truss, mul(r.arm, fore)); // the heel, forward of the mast and to windward
          r.b = peakY;
          r.centre = lerp(r.a, r.b, 0.5);
          r.half = (spec.length_m || headL) / 2;
          r.normal = mc.normal;
          r.brace = 0;
          r.hoist = 1;
          r.truss = truss;
          r.cutAtMast = true;
          r.pivot = truss;
          r.reach = Math.max(headL, fore);
          r.heights = [r.a[2], r.b[2], mc.pts[0][2], mc.pts[3][2]]; // heel, peak, tack, clew
          cuts.forEach(function (s) {
            var other = s === lineBy ? null : mastCut(s, resolve, true);
            if (!other) return;
            r.reach = Math.max(r.reach, len(sub(other.pts[2], truss)));
            r.heights.push(other.pts[2][2], other.pts[0][2], other.pts[3][2]); // peak, tack, clew
          });
        } else if (
          where &&
          (spec.class === "lug_yard" || spec.class === "lateen_yard") &&
          lugCut(sailOnYard(id), resolve)
        ) {
          // package 57: a lug's yard from its cut, slung a third from its fore end on its
          // side of the mast, or on deck while its lug is lowered or sent down; and so a whole
          // lateen's yard with its cut (package 75, B5.2; Ext §6.1), as a standing sail on its
          // lee side, until the package that builds a whole lateen draws it as its own
          var lc = lugCut(sailOnYard(id), resolve);
          var lsp = sailOnYard(id);
          var throatP = lc.pts[1], peakP = lc.pts[2];
          r.x = lc.pivotMast ? lc.pivotMast.x : spec.x_m || 0;
          r.a = throatP;
          r.b = peakP;
          r.centre = lerp(throatP, peakP, 1 / 3);
          r.half = (spec.length_m || len(sub(peakP, throatP))) / 2;
          r.arm = norm(sub(peakP, throatP));
          r.normal = lc.normal;
          r.brace = 0;
          r.hoist = lc.onDeck ? 0 : 1;
          r.onDeck = lc.onDeck;
          r.flyingDown = sentDownFlying(lsp);
        } else if (where && spec.class === "yard" && yardOnDeck(id)) {
          // package 57: a royal set flying and sent down: its yard on deck, fore and aft,
          // beside the foot of its lower mast
          var lowerM = resolve(chainTop(spec));
          var Ld = spec.length_m || 0;
          r.x = lowerM ? lowerM.x : spec.x_m || 0;
          // on the drawn deck at the mast where a profile gives one (package 75: a datum
          // above the waist, as the razee's under D18 (c), would float it over her rail)
          var onDeck = profile ? deckAt(profile, r.x) : null;
          r.centre = v(r.x, 0.25 * beamM, (onDeck === null ? deck : onDeck) + ON_DECK_M);
          r.arm = [1, 0, 0];
          r.half = Ld / 2;
          r.a = sub(r.centre, mul(r.arm, r.half));
          r.b = add(r.centre, mul(r.arm, r.half));
          r.normal = [0, 1, 0];
          r.brace = 0;
          r.hoist = 0;
          r.onDeck = true;
          r.flyingDown = true;
        } else if (YARD_CLASSES[spec.class]) {
          var th = braceAngle(spec);
          // at its hoist (package 37n): the file's height, or lowered on the cap of the mast
          // below, or between while the halyards are worked; reefed, its sail's depth less
          // what the reefs take out above the yard below
          var z = deck + H;
          r.hoist = 1;
          if (where && parent && parent.parent && (onCap(spec) || hoists(spec))) {
            var lowered = parent.parent.head[2] + YARD_ON_CAP_M;
            var hoisted = z;
            var sailOn = squareSailOn(id);
            var belowId = yardBelowId[id];
            var bare = bareFoot(spec);
            if (sailOn && !onCap(spec)) {
              var rf = reefFraction(sailOn, sailDyn(sailOn));
              if (belowId) {
                var below = resolve(belowId);
                var gap = z - (deck + (sparSpecs[belowId].height_m || 0));
                hoisted = below.centre[2] + gap * rf;
              } else if (bare) {
                hoisted = bare.z + bare.depth * rf;
              }
            }
            // never below its cap (a sail set over a yard below that is lowered: the clews
            // are sheeted to it, and the halyards can bring the yard no lower)
            hoisted = Math.max(hoisted, lowered);
            r.hoist = hoistFraction(spec);
            r.onCap = onCap(spec);
            z = lowered + r.hoist * (hoisted - lowered);
          }
          r.x = parent ? (parent.xAt ? parent.xAt(z) : parent.x) : spec.x_m || 0;
          // package 75 (B5.3; Ext §6.2): a yard under the bowsprit or the jib-boom at its own
          // station (its file's `x_m`; its spar's x where a file gives none), not at its spar's
          // heel, where the trial's spritsail hung with its foot under the water (Eng §5); it
          // neither hoists nor is slung before a mast
          if (underBowsprit(spec)) {
            r.x = spec.x_m || r.x;
            r.everyWay = true; // the frame reaches its swing every way (`fullRigFrame`)
            // and at the foot of the sail hanging from it, as well as at its slings, so that the
            // foot stays inside the frame when she heels: on the razee, with no sprit-topsail
            // yard above it, the spritsail set and braced passed the frame by 2 cm (measured)
            var hangs = yardBelowId[id] ? null : squareSailOn(id);
            if (hangs) r.heights = [z, z - hangs.area_m2 / Math.max(HEAD_SPREAD * L, 1)];
          }
          // package 57: a square yard is slung before its mast (YARD_BEFORE_MAST_OF_BEAM)
          if (spec.class === "yard" && parent && MAST_CLASSES[parent.cls]) r.x += yardBefore;
          r.centre = v(r.x, 0, z);
          r.arm = [Math.sin(th), Math.cos(th), 0]; // direction of the starboard yardarm
          r.half = L / 2;
          r.brace = th;
          var tilt = spec.class === "lateen_yard" ? 0.8 : spec.class === "lug_yard" ? 0.35 : 0;
          if (tilt) {
            // a lug or lateen yard slopes up toward its after end
            r.arm = norm([r.arm[0] * Math.cos(tilt), r.arm[1] * Math.cos(tilt), Math.sin(tilt)]);
          }
          r.a = sub(r.centre, mul(r.arm, r.half)); // larboard arm
          r.b = add(r.centre, mul(r.arm, r.half)); // starboard arm
          r.normal = [Math.cos(th), -Math.sin(th), 0];
        } else if (spec.class === "gaff") {
          r.x = parent ? (parent.xAt ? parent.xAt(deck + H) : parent.x) : spec.x_m || 0;
          var gDir = sheetDirection(sheetAngleOf(id), tack);
          r.a = v(r.x, 0, deck + H); // the throat, at the mast
          var gCut = gaffCutOn(id);
          var gPeak = gCut ? gCut.angle : GAFF_PEAK_ANGLE;
          r.b = add(r.a, add(mul(gDir, L * Math.cos(gPeak)), v(0, 0, L * Math.sin(gPeak))));
          r.dir = gDir;
        } else if (spec.class === "boom") {
          r.x = parent ? (parent.xAt ? parent.xAt(deck + H) : parent.x) : spec.x_m || 0;
          var bDir = sheetDirection(sheetAngleOf(id), tack);
          r.a = v(r.x, 0, deck + H);
          r.b = add(r.a, mul(bDir, L));
          r.dir = bDir;
          // package 75 (B5.5; Ext §17.6): a driver's boom reaches far beyond the taffrail, and
          // swung to the quarter past the frame's four directions: its swing is reached every
          // way, so that the view does not rescale as it is sheeted or as the driver is shifted.
          // So does the razee's spanker boom, as long, 7.4 m past the four directions seen on the
          // quarter (measured): every boom on a hull drawn from her profile (her stage B)
          if (boomOfCut(id) || profile) r.everyWay = true;
        } else if (spec.class === "sprit") {
          r.x = parent ? parent.x : spec.x_m || 0;
          var sDir = sheetDirection(sheetAngleOf(id), tack);
          r.a = v(r.x, 0, deck + 1.0);
          r.b = add(r.a, add(mul(sDir, L * Math.cos(0.9)), v(0, 0, L * Math.sin(0.9))));
          r.dir = sDir;
        } else if (spec.class === "studdingsail_boom") {
          var rigged = riggedOut(spec);
          r.rigged = rigged;
          if (parent && parent.dir && !parent.arm) {
            // the ringtail boom: run out beyond the end of the gaff sail's boom, along it,
            // or lashed alongside it when rigged in (Steel 1794: "lashed occasionally to the
            // outer end of the main-sail-boom")
            var endP = parent.b;
            r.x = parent.x;
            r.dir = parent.dir;
            r.a = rigged ? endP : sub(endP, mul(parent.dir, L));
            r.b = rigged ? add(endP, mul(parent.dir, L)) : endP;
            r.full = [endP, add(endP, mul(parent.dir, L))];
            r.normal = cross(parent.dir, [0, 0, 1]);
            r.pivot = parent.a; // it swings with the boom about the mast
            r.reach = len(sub(parent.b, parent.a)) + L;
            if (parent.everyWay) r.everyWay = true; // and is reached as its boom is
          } else {
            var ss = sideSign(spec.side);
            var yard = parent && parent.arm ? parent : null;
            var arm = yard ? yard.arm : [0, 1, 0];
            var cx = yard ? yard.x : parent ? parent.x : 0;
            var reach = yard ? yard.half : 0;
            // rigged out beyond the yardarm below it; run in along the yard when rigged in
            r.x = cx;
            var inboard = v(cx + ss * reach * arm[0], ss * reach * arm[1], deck + H);
            r.a = rigged ? inboard : add(inboard, mul(arm, -ss * L));
            r.b = rigged ? add(inboard, mul(arm, ss * L)) : inboard;
            r.full = [inboard, add(inboard, mul(arm, ss * L))];
            r.arm = arm;
            r.normal = yard ? yard.normal : [1, 0, 0];
            r.pivot = yard ? yard.centre : v(cx, 0, deck + H);
            r.reach = reach + L;
          }
        } else {
          r.x = parent ? parent.x : spec.x_m || 0;
          r.a = v(r.x, 0, deck);
          r.b = v(r.x, 0, deck + H);
        }
        spars[id] = r;
        return r;
      }
      graph.spars.forEach(function (s) {
        resolve(s.id);
      });
      return spars;
    }
    var home = placeSpars(false);
    var spars = placeSpars(true);

    // Masts (lower) in order along the ship, and the head rig, for stay landings.
    var lowerMasts = graph.spars
      .filter(function (s) {
        return s.class === "mast";
      })
      .map(function (s) {
        return spars[s.id];
      })
      .sort(function (p, q) {
        return q.x - p.x;
      }); // foremost first
    var headRig = graph.spars
      .filter(function (s) {
        return HEAD_CLASSES[s.class];
      })
      .map(function (s) {
        return spars[s.id];
      })
      .sort(function (p, q) {
        return p.tip[0] - q.tip[0];
      }); // innermost first
    var stemX = hull.length_waterline_m / 2;
    if (headRig.length) stemX = Math.min(stemX, headRig[0].a[0]);

    function lowerMastOf(spar) {
      var cur = spar;
      while (cur && cur.parent) cur = cur.parent;
      return cur;
    }
    function mastChainTops(mast) {
      // the heads of a lower mast and everything stepped on it, lowest first
      var tops = [];
      graph.spars.forEach(function (s) {
        if (!MAST_CLASSES[s.class]) return;
        var r = spars[s.id];
        if (lowerMastOf(r) === mast) tops.push(r.head);
      });
      tops.sort(function (p, q) {
        return p[2] - q[2];
      });
      return tops;
    }

    /** Where each stay lands, by the level of the spar it is of (lower mast 0,
     *  topmast 1, topgallant 2, royal 3), as the period rig did it: from the
     *  foremost mast, level k lands on the k-th spar of the head rig (the stem,
     *  the bowsprit end, the jib boom end, the flying jib boom end), or the
     *  outermost when the rig runs out; from an after mast, level k lands on
     *  the head of level k-1 of the mast ahead, and level 0 at its foot. */
    var stayFoot = {};
    function mastLevel(spar) {
      var k = 0;
      var cur = spar;
      while (cur && cur.parent) {
        k += 1;
        cur = cur.parent;
      }
      return k;
    }
    /** Whether a stay has no run forward to another spar: the sails hanked to it lie abaft
     *  the mast it is of (the storm mizzen's vertical stay under the mizzen trestle-trees),
     *  where every stay that runs forward carries its sails forward of its mast. */
    function hangsAbaft(ln, sp) {
      var on = (sailsBySpar[ln.id] || []).filter(function (s) {
        return s.class === "jibheaded";
      });
      return on.length > 0 && on.every(function (s) {
        return (s.x_m || 0) < (sp.x || 0);
      });
    }

    graph.lines.forEach(function (ln) {
      if (ln.class !== "stay") return;
      var sp = spars[ln.of];
      if (!sp) return;
      var mast = lowerMastOf(sp);
      if (!mast || !MAST_CLASSES[mast.cls]) return; // bobstays and martingales: not sail stays
      if (hangsAbaft(ln, sp)) {
        // parallel to the mast, under the after end of its trestle-trees, down to the deck
        var aft = v(-STAY_ABAFT_M, 0, 0);
        stayFoot[ln.id] = { head: add(sp.head, aft), foot: add(sp.foot, aft), abaft: true };
        return;
      }
      var level = mastLevel(sp);
      var idx = lowerMasts.indexOf(mast);
      var land;
      if (idx <= 0) {
        var outer = headRig.map(function (h) {
          return h.tip;
        });
        land = level === 0 || !outer.length ? v(stemX, 0, deck) : outer[Math.min(level - 1, outer.length - 1)];
      } else {
        var ahead = lowerMasts[idx - 1];
        var tops = mastChainTops(ahead); // lowest first
        land = level === 0 || !tops.length ? ahead.foot : tops[Math.min(level - 1, tops.length - 1)];
      }
      stayFoot[ln.id] = { head: sp.head, foot: land };
    });

    // -- sails -------------------------------------------------------------------

    /** A spar sent down (the topgallant masts in a gale), or stepped on one: it is on
     *  deck, and it and everything on it are drawn no more than a wrecked spar's
     *  dependents are. A wreck cleared away (package 30b: "cleared") is on deck or over
     *  the side, and is not drawn either. A struck topmast is housed and the yard struck
     *  with it lies on the lower cap (package 37n): both are drawn where they are. */
    function sentDown(r) {
      for (var cur = r; cur; cur = cur.parent) {
        if (cur.state === "cleared") return true;
        if (cur.state === "sent_down" && !cur.housed && !cur.onCap) return true;
      }
      return false;
    }
    var lineOf = indexBy(graph.lines, "id");

    /** Where a sheet from forward of the fore mast ends on side `sign`: at the deck, a little
     *  abaft that mast (SPRIT_SHEET_ABAFT_M), half the beam out, or on a hull drawn from her
     *  profile on her drawn side there, which is narrower so far forward (package 75, her
     *  stage B: on the 64 the beam's half stood 1.5 m outboard of her side). */
    function foreSheetLead(sign) {
      var x = lowerMasts[0].x - SPRIT_SHEET_ABAFT_M;
      return v(x, sign * (profile ? drawnSideAt(hull)(x, deck) : beam / 2), deck);
    }

    var figures = [];
    graph.spars.forEach(function (s) {
      var r = spars[s.id];
      if (sentDown(r)) return;
      var fig = {
        kind: "spar",
        id: s.id,
        cls: s.class,
        // a housed topmast and the yard on the cap are struck, not on deck (package 37n)
        state: r.housed || r.onCap ? "struck" : r.state,
        side: s.side,
        pts: [r.a, r.b],
        busy: !!busy[s.id],
      };
      if (r.hoist !== undefined) fig.hoist = r.hoist; // a yard: 1 at its hoist, 0 lowered
      if (r.flyingDown) fig.state = "sent_down_flying"; // package 57: on deck with its sail
      if (s.class === "yard" && !r.onDeck) fig.brace = r.brace || 0; // package 57: said in its title
      // package 75 (B5.3): a yard under the bowsprit or the jib-boom hangs from no mast, and is
      // sorted at its own middle; that correction would move it half its spar's run forward
      if (YARD_CLASSES[s.class] && r.parent && !r.onDeck && !underBowsprit(s)) {
        fig.mastId = r.parent.id; // the painter's correction for the mast's rake (package 57)
        fig.centre = r.centre;
      }
      // package 75 (the 64's stage B): a jib-boom with a yard hung under it is sorted at its
      // heel: the sprit topsail stands forward of the spar all the way up to that yard, and sorted
      // at the spar's middle the spar was drawn over the sail from ahead, ending in its cloth
      if (s.class === "jib_boom" && graph.spars.some(function (y) { return y.parent === s.id && underBowsprit(y); })) {
        fig.sortAt = r.a;
      }
      // package 75 (the 64's stage B): the mizen yard reaches far fore and aft of its mast, its
      // after part up to 8.3 m abaft the mizzen topsail, so as one figure it stood on the wrong
      // side of that sail either way: from astern the topsail hid the part that carries the
      // course's head, and from the bow that part crossed the topsail. It is cut at its truss
      // into two pieces, each sorted at its own middle, as a lower mast's foot is below
      if (r.cutAtMast) {
        var foreOfYard = {};
        Object.keys(fig).forEach(function (key) {
          foreOfYard[key] = fig[key];
        });
        foreOfYard.pts = [r.a, r.truss];
        foreOfYard.piece = "fore";
        delete foreOfYard.mastId;
        delete foreOfYard.centre;
        foreOfYard.sortAt = lerp(r.a, r.truss, 0.5);
        figures.push(foreOfYard);
        fig.pts = [r.truss, r.b];
        delete fig.mastId;
        delete fig.centre;
        fig.sortAt = lerp(r.truss, r.b, 0.5);
      }
      // package 75 (B5.6): with a profile, a lower mast's foot, from the deck it stands on up to
      // the top of the side there, is a piece of its own sorted at its own middle, so that the
      // near side is drawn over it however the ship heels (one figure, sorted at the middle of
      // the mast, came nearer than the near side heeled 20 degrees toward the viewer); the rest
      // is sorted at the whole mast's middle, as the mast was
      var side = profile && MAST_CLASSES[s.class] && !r.parent ? lineAt(profile.rail_m, r.a[0]) : null;
      if (side !== null && side > r.a[2] + 1e-6 && side < r.b[2] - 1e-6) {
        var cut = v(r.xAt(side), 0, side);
        var foot = {};
        Object.keys(fig).forEach(function (key) {
          foot[key] = fig[key];
        });
        foot.pts = [r.a, cut];
        foot.piece = "foot";
        figures.push(foot);
        fig.pts = [cut, r.b];
        fig.sortAt = lerp(r.a, r.b, 0.5);
      }
      figures.push(fig);
    });

    function quadArea(p) {
      // planar-ish quad area by two triangles
      function tri(a, b, c) {
        return 0.5 * len(cross(sub(b, a), sub(c, a)));
      }
      return tri(p[0], p[1], p[2]) + tri(p[0], p[2], p[3]);
    }

    /** A four-cornered sail: head A->B, then leech B->C, foot C->D, leech D->A.
     *  Returns a 3D path: [[P], [C, P], ...] with quadratic control points. */
    function quadSail(corners, normal, dyn, depthHint) {
      var A = corners[0], B = corners[1], C = corners[2], D = corners[3];
      var depth = depthHint || len(sub(D, A));
      var width = len(sub(B, A));
      // control points sit at twice the offset: a quadratic curve peaks halfway to its control
      var belly = [0, 0, 0];
      if (DRAWING[dyn.state]) belly = mul(bellyDirection(normal, wind), 2 * BELLY * Math.min(depth, width));
      var sag = mul(v(0, 0, -1), 2 * FOOT_SAG * depth);
      var midBC = add(lerp(B, C, 0.5), belly);
      var midCD = add(add(lerp(C, D, 0.5), belly), DRAWING[dyn.state] ? sag : [0, 0, 0]);
      var midDA = add(lerp(D, A, 0.5), belly);
      return [[A], [lerp(A, B, 0.5), B], [midBC, C], [midCD, D], [midDA, A]];
    }

    /** A goose-winged course or topsail: the triangle head (lee yardarm to weather
     *  yardarm), weather leech down to the weather clew, and the foot rising from the
     *  weather clew to the lee clew hauled up at the lee yardarm. */
    function gooseWingPath(corners, normal, tackSide, depth) {
      var t = gooseWingTriangle(corners, tackSide);
      var lee = t[0], weather = t[1], clew = t[2];
      var belly = mul(bellyDirection(normal, wind), 2 * BELLY * Math.min(depth, len(sub(weather, lee))));
      return [[lee], [lerp(lee, weather, 0.5), weather], [add(lerp(weather, clew, 0.5), mul(belly, 0.5)), clew], [add(lerp(clew, lee, 0.5), belly), lee]];
    }

    /** A bundle along a spar from a to b: a thin lens. */
    function bundle(a, b, thickness) {
      var down = v(0, 0, -thickness);
      var up = v(0, 0, thickness * 0.4);
      return [[a], [add(lerp(a, b, 0.5), down), b], [add(lerp(a, b, 0.5), up), a]];
    }

    /** A sail hauled up in its gear: hanging IN_GEAR_DEPTH of its depth in festoons. */
    function gathered(A, B, depth, hang) {
      var dir = norm(sub(B, A));
      var w = len(sub(B, A));
      var n = 3;
      var path = [[A], [lerp(A, B, 0.5), B]];
      var down = mul(hang, depth * IN_GEAR_DEPTH);
      var prev = B;
      for (var i = 1; i <= n; i++) {
        var t = 1 - i / n;
        var p = add(add(A, mul(dir, w * t)), i === n ? [0, 0, 0] : down);
        var c = add(lerp(prev, p, 0.5), mul(hang, depth * IN_GEAR_DEPTH * 0.6));
        path.push([c, p]);
        prev = p;
      }
      return path;
    }

    /** A torn outline of the same quad. */
    function torn(corners) {
      var A = corners[0], B = corners[1], C = corners[2], D = corners[3];
      var path = [[A], [lerp(A, B, 0.5), B]];
      var steps = 5;
      for (var i = 1; i <= steps; i++) {
        var t = i / steps;
        var p = lerp(B, C, t * 0.6);
        var jag = mul(sub(A, B), (i % 2 ? 0.06 : -0.02));
        path.push([add(lerp(B, C, (t - 0.5 / steps) * 0.6), jag), p]);
      }
      for (var j = 1; j <= steps; j++) {
        var u = j / steps;
        var q = lerp(D, A, 0.4 + u * 0.6);
        var jag2 = mul(sub(B, A), (j % 2 ? 0.05 : -0.02));
        path.push([add(lerp(D, A, 0.4 + (u - 0.5 / steps) * 0.6), jag2), q]);
      }
      return path;
    }

    /** Drooping, for a wrecked sail: one clew fallen. */
    function drooping(corners) {
      var A = corners[0], B = corners[1], C = corners[2], D = corners[3];
      var fall = v(0, 0, -0.4 * len(sub(D, A)));
      var C2 = add(C, fall);
      return [[A], [lerp(A, B, 0.5), B], [add(lerp(B, C2, 0.5), mul(fall, 0.3)), C2], [lerp(C2, D, 0.5), D], [lerp(D, A, 0.5), A]];
    }

    function sailFigure(spec, dyn, corners, normal, spar, depth) {
      var fig = {
        kind: "sail",
        id: spec.id,
        cls: spec.class,
        state: dyn.state,
        backed: dyn.backed,
        reefs: dyn.reefs,
        busy: !!busy[spec.id],
      };
      if (dyn.state === "furled") {
        fig.path = bundle(spar.a, spar.b, 0.25 + 0.03 * len(sub(spar.b, spar.a)));
      } else if (dyn.state === "in_the_gear") {
        fig.path = gathered(corners[0], corners[1], depth, norm(sub(corners[3], corners[0])));
      } else if (dyn.state === "blown_out") {
        fig.path = torn(corners);
      } else if (dyn.state === "wrecked") {
        fig.path = drooping(corners);
      } else {
        fig.path = quadSail(corners, normal, dyn, depth);
      }
      fig.corners = corners;
      fig.centre = centroid(corners); // its place along the view axis (project)
      return fig;
    }

    /** A staysail whose cloth reaches from one side of a lower mast to the other, cut at
     *  the mast into the part forward and the part abaft, each with its own centre, so
     *  that the mast can be drawn between them; any other sail as it is. */
    function piecesAtMast(fig) {
      if (!(fig.stay || fig.cutMast) || !fig.path) return [fig];
      var pts = flattenPath(fig.path);
      var minX = Infinity, maxX = -Infinity;
      pts.forEach(function (p) {
        minX = Math.min(minX, p[0]);
        maxX = Math.max(maxX, p[0]);
      });
      var cutAt = fig.cutMast ? [fig.cutMast] : lowerMasts; // a lug at its own mast (package 57)
      for (var i = 0; i < cutAt.length; i++) {
        var m = cutAt[i];
        var mx = m.xAt ? m.xAt(fig.centre[2]) : m.x;
        if (mx <= minX + 0.3 || mx >= maxX - 0.3) continue;
        var halves = splitAtX(pts, mx);
        var out = [];
        halves.forEach(function (poly, k) {
          if (poly.length < 3) return;
          var piece = {};
          Object.keys(fig).forEach(function (key) {
            piece[key] = fig[key];
          });
          piece.path = poly.map(function (p) {
            return [p];
          });
          piece.centre = centroid(poly);
          piece.piece = k === 0 ? "forward" : "abaft";
          piece.mast = m.id;
          piece.cut = mx; // the mast's x at the sail's centre height, where it is cut
          out.push(piece);
        });
        return out.length ? out : [fig];
      }
      return [fig];
    }

    function reefFraction(spec, dyn) {
      var bands = spec.reef_bands || 0;
      var reefs = Math.min(Math.max(dyn.reefs || 0, 0), bands);
      return Math.max(1 - (spec.reef_factor || 0) * reefs, 0.2);
    }

    /** A square sail's corners from its file (package 37n; CLEW_SPREAD, HEAD_SPREAD):
     *  [larboard head, starboard head, starboard clew, larboard clew], the head along its
     *  yard where the yard is now and the clews at the arms of the yard below where that is
     *  now; and the depth it is reckoned by for its belly and its festoons, its own between
     *  the yards at their hoists, less the reefs. A sail with no yard below hangs from its
     *  yard as deep as its area over its breadth, less the reefs (a course's reef bands are
     *  at its head: its foot rises). A sprit topsail, between two yards under the bowsprit
     *  (package 75, the 64's stage B; Ext §6.2, risk 9): its depth is the slant between the
     *  yards, along which the sail lies, not the heights between them. */
    function squareCut(spec, dyn, Y) {
      var L = Y.half * 2;
      var belowId = yardBelowId[Y.id];
      var B = belowId ? spars[belowId] : null;
      var gap = belowId ? (Y.spec.height_m || 0) - (sparSpecs[belowId].height_m || 0) : 0;
      if (B && B.arm && !sentDown(B) && gap > 0.5) {
        var along = underBowsprit(Y.spec) ? len(sub(Y.centre, B.centre)) : gap;
        var foot = CLEW_SPREAD * B.half * 2;
        var head = Math.min(Math.max((2 * spec.area_m2) / along - foot, 0.5 * L), L);
        // the clews at the yard below's arms; where that yard is lowered further than the
        // sail reaches (a topgallant set over a topsail on the cap), at the sail's own depth
        var reach = Y.centre[2] - gap * reefFraction(spec, dyn);
        var fc = B.centre[2] >= reach - 0.05 ? B.centre : v(B.centre[0], B.centre[1], reach);
        return {
          corners: [sub(Y.centre, mul(Y.arm, head / 2)), add(Y.centre, mul(Y.arm, head / 2)), add(fc, mul(B.arm, foot / 2)), sub(fc, mul(B.arm, foot / 2))],
          depth: along * reefFraction(spec, dyn),
          head: head,
          foot: foot,
        };
      }
      var spread = HEAD_SPREAD * L;
      var bare = bareFoot(Y.spec);
      if (bare) {
        // over a bare yard the file does not carry: the foot where that yard is, as broad as
        // the area leaves over the depth at the hoist
        var wide = Math.min(Math.max((2 * spec.area_m2) / bare.depth - spread, spread), 2 * L);
        var fx = Y.parent && Y.parent.xAt ? Y.parent.xAt(bare.z) : Y.x;
        var fc = v(fx, 0, bare.z);
        return {
          corners: [sub(Y.centre, mul(Y.arm, spread / 2)), add(Y.centre, mul(Y.arm, spread / 2)), add(fc, mul(Y.arm, wide / 2)), sub(fc, mul(Y.arm, wide / 2))],
          depth: bare.depth * reefFraction(spec, dyn),
          head: spread,
          foot: wide,
        };
      }
      var deep = (spec.area_m2 / Math.max(spread, 1)) * reefFraction(spec, dyn);
      var a = sub(Y.centre, mul(Y.arm, spread / 2));
      var b = add(Y.centre, mul(Y.arm, spread / 2));
      var down = v(0, 0, -deep);
      return { corners: [a, b, add(b, down), add(a, down)], depth: deep, head: spread, foot: spread };
    }

    graph.sails.forEach(function (spec) {
      var dyn = sailDyn(spec);
      var roles = spec.roles || {};
      var cls = spec.class;
      if (dyn.state === "unbent") return; // nothing on the yard: the sail is in the sail room
      if (sentDownFlying(spec)) return; // package 57: sent down on deck with its yard
      var onDeck = Object.keys(roles).some(function (role) {
        var target = roles[role];
        var sp = spars[target] || (lineOf[target] ? spars[lineOf[target].of] : null);
        return sp ? sentDown(sp) : false;
      });
      if (onDeck) return; // sent down with its spar
      if (cls === "lateen" && spec.cut_at_mast) {
        // package 75 (B5.2; Ext §6.1): the mizen course cut at the mast, on its corners swung
        // about the mast (`mastCut`), its luff on the mast and its head along its yard. The
        // reef raises the foot as a gaff sail's does: the tack up the mast and the clew with
        // it. Brailed up in the gear, it is gathered to the mast and up under the yard;
        // furled, a bundle along the yard's after part, aloft (Falconer 1780, YARD).
        // B5.5 (Ext §17.6): the driver, cut at the mast and spread on its boom, in the same
        // way: its throat and peak on its corners swung about the mast, the head straight
        // along the yard's line and on beyond the yard's peak; its tack at the boom's jaws and
        // its clew along the boom at the file's foot, the boom swung by its sheet as a gaff
        // sail's is; no reef (Steel names none in the driver). Brailed in the gear as the
        // course is; furled, a bundle along its head, the yard's after part and the driver yard
        var mcs = mastCut(spec, function (mid) {
          return spars[mid];
        });
        if (!mcs) return;
        var mp = mcs.pts; // tack, throat, peak, clew
        var rfc = reefFraction(spec, dyn);
        var tackC = lerp(mp[0], mp[1], 1 - rfc);
        var clewC = add(mp[3], v(0, 0, tackC[2] - mp[0][2]));
        var BmC = roles.boom ? spars[roles.boom] : null;
        if (BmC && BmC.dir) {
          tackC = BmC.a;
          clewC = add(BmC.a, mul(BmC.dir, Math.min(len(sub(mp[3], mp[0])), len(sub(BmC.b, BmC.a)))));
        }
        var luffC = len(sub(mp[1], tackC));
        var cfig = sailFigure(spec, dyn, [mp[1], mp[2], clewC, tackC], mcs.normal, spars[roles.yard] || mcs.mast, luffC);
        cfig.mastId = mcs.mast.id;
        cfig.clewAt = clewC; // where its sheet is drawn from
        // its luff is laced to the mast (Falconer 1780; Ext §3.4), so it does not belly as a leech
        // does: drawn it stood a metre off the mast (the 64's course and driver, measured)
        if (cfig.path.length === 5) cfig.path[4] = [lerp(tackC, mp[1], 0.5), mp[1]];
        // Steel's driver yard, which "expands the head of the driver without the peek of the
        // gaff" (Steel 1794 vol. I, OCR l. 20863), is not filed as a spar: it goes aloft with
        // the sail and comes down with it. Beyond the mizen yard's peak the head is drawn on
        // it, a spar line drawn with the sail; its inner part lies along the mizen yard and is
        // drawn as it
        var Yc = spars[roles.yard];
        var driverYard = null;
        if (BmC && Yc && Yc.cutAtMast && len(sub(mp[2], Yc.truss)) > len(sub(Yc.b, Yc.truss))) {
          driverYard = { kind: "spar", id: spec.id, cls: "driver_yard", of: spec.id, state: "sound", pts: [Yc.b, mp[2]], busy: !!busy[spec.id], mastId: mcs.mast.id, centre: lerp(Yc.b, mp[2], 0.5) };
        }
        if (dyn.state === "furled") {
          cfig.path = bundle(mp[1], mp[2], 0.35);
        } else if (dyn.state === "in_the_gear") {
          var upC = lerp(mp[1], mp[0], IN_GEAR_DEPTH); // the foot hauled up the mast
          var underC = lerp(mp[1], mp[2], IN_GEAR_DEPTH); // and the leech in under the yard
          cfig.path = [[mp[1]], [lerp(mp[1], underC, 0.5), underC], [add(lerp(underC, upC, 0.5), mul(mcs.aft, 0.8)), upC], [lerp(upC, mp[1], 0.5), mp[1]]];
          // the clew brailed in with the foot and the leech: on the bundle's after side, the
          // middle of the curve between them, not where it stood with the sail set
          cfig.clewAt = add(lerp(underC, upC, 0.5), mul(mcs.aft, 0.4));
        }
        figures.push(cfig);
        if (driverYard) figures.push(driverYard);
      } else if (cls === "square" || cls === "lug" || cls === "lateen") {
        var Y = spars[roles.yard];
        if (!Y || !Y.arm) return;
        var corners, depth;
        if (cls === "square") {
          // from the file's figures (package 37n): squareCut
          var cut = squareCut(spec, dyn, Y);
          corners = cut.corners;
          depth = cut.depth;
        } else if ((cls === "lug" || cls === "lateen") && spec.corners_m) {
          // package 57: a lug from its cut, on its side of the mast (`lugCut`); and a whole
          // lateen with its cut (package 75, B5.2; Ext §6.1), as a standing lug on its lee side
          var lcut = lugCut(spec, function (mid) {
            return spars[mid];
          });
          var lp = lcut.pts; // tack, throat, peak, clew
          var lfig = sailFigure(spec, dyn, [lp[1], lp[2], lp[3], lp[0]], lcut.normal, Y, len(sub(lp[2], lp[3])));
          if (lcut.onDeck) lfig.path = bundle(lp[1], lp[2], 0.3);
          lfig.cutMast = lcut.pivotMast;
          lfig.mastId = lcut.pivotMast ? lcut.pivotMast.id : null;
          piecesAtMast(lfig).forEach(function (f) {
            figures.push(f);
          });
          return;
        } else {
          // a lug or a lateen: from its yard's ends, its area over the yard
          var L = Y.half * 2;
          depth = (spec.area_m2 / Math.max(L, 1)) * reefFraction(spec, dyn);
          var down = v(0, 0, -depth);
          corners = [Y.a, Y.b, add(Y.b, down), add(Y.a, down)];
        }
        if (dyn.state === "goose_winged") {
          // the lee clew hauled up to the yard, the weather clew sheeted home: a triangle
          // from the weather clew to the yard, its foot rising to the lee yardarm (spec M3
          // §9 item 13; physics/sails.py: half the area, its centre out to weather)
          corners = gooseWingOf(corners, tack);
          var gw = sailFigure(spec, dyn, corners, Y.normal, Y, depth);
          gw.path = gooseWingPath(corners, Y.normal, tack, depth);
          gw.centre = gooseWingCentre(corners, tack);
          figures.push(gw);
          return;
        }
        var sqFig = sailFigure(spec, dyn, corners, Y.normal, Y, depth);
        // sorted against its mast; a sail under the bowsprit or the jib-boom at its own centre
        // (package 75, B5.3)
        sqFig.mastId = Y.parent && !underBowsprit(Y.spec) ? Y.parent.id : null;
        figures.push(sqFig);
      } else if (cls === "gaff" || cls === "sprit") {
        var M = spars[roles.mast];
        var G = spars[roles.gaff || roles.sprit];
        var Bm = roles.boom ? spars[roles.boom] : null;
        if (!M || !G) return;
        var throat = G.a;
        var peak = G.b;
        var footZ = Bm ? Bm.a[2] : deck + LOOSE_FOOT_HEIGHT_M;
        var luff = throat[2] - footZ;
        var raise = luff * (1 - reefFraction(spec, dyn));
        var tackPt = v(M.x, 0, footZ + raise);
        var clew;
        var cutG = Bm && Bm.dir && cls === "gaff" ? gaffCutOn(roles.gaff) : null;
        if (cutG) {
          // her spanker on its file's cut: its head and foot the file's along the gaff and the
          // boom, which it does not fill, its tack at the jaws. By the fixed rule it was drawn 215
          // m2 against the filed 191, its peak 1.6 m farther aft (the razee, measured)
          var gaffL = len(sub(G.b, G.a));
          peak = lerp(G.a, G.b, Math.min(cutG.head / gaffL, 1));
          tackPt = add(Bm.a, v(0, 0, raise));
          clew = add(add(Bm.a, mul(Bm.dir, Math.min(cutG.foot, len(sub(Bm.b, Bm.a))))), v(0, 0, raise));
        } else if (Bm) {
          clew = add(Bm.b, v(0, 0, raise));
        } else {
          // loose-footed: the clew from the area, in the plane of the sail
          var px = len(sub(v(peak[0], peak[1], 0), v(throat[0], throat[1], 0)));
          var c = (2 * spec.area_m2 - px * (throat[2] - footZ)) / Math.max(peak[2] - footZ, 1);
          c = Math.max(Math.min(c, (G.spec.length_m || 5) * 2.5), 1);
          clew = add(v(M.x, 0, footZ + raise), mul(G.dir, c));
        }
        var normalG = cross(G.dir, [0, 0, 1]);
        var cornersG = [throat, peak, clew, tackPt];
        var fig = sailFigure(spec, dyn, cornersG, normalG, Bm || M, luff);
        fig.mastId = M.id;
        if (dyn.state === "furled") {
          fig.path = Bm ? bundle(Bm.a, Bm.b, 0.3 + 0.02 * (Bm.spec.length_m || 0)) : bundle(v(M.x, 0.15, footZ), v(M.x, 0.15, throat[2]), 0.5);
        } else if (dyn.state === "in_the_gear") {
          // brailed in to the mast: a narrow gathered shape along the luff
          var brailW = 0.25;
          fig.path = [[throat], [lerp(throat, peak, 0.15), lerp(throat, peak, brailW)], [add(lerp(lerp(throat, peak, brailW), lerp(tackPt, clew, brailW), 0.5), mul(G.dir, 0.8)), lerp(tackPt, clew, brailW)], [lerp(lerp(tackPt, clew, brailW), tackPt, 0.5), tackPt], [lerp(tackPt, throat, 0.5), throat]];
        }
        figures.push(fig);
      } else if (cls === "jibheaded") {
        var stay = roles.stay ? stayFoot[roles.stay] : null;
        var Mm = roles.mast ? spars[roles.mast] : null;
        var head, tackJ, clewJ, along, normalJ, sparFor;
        var nockJ = null;
        if (spec.corners_m && spec.corners_m.length >= 3) {
          // package 57: a staysail cut as its file has it (Steel's shapes: a triangle, or
          // four-sided with a bunt), its head on the stay and its tack fast, the clew swung
          // to leeward about the tack by the sheet
          var cm = spec.corners_m;
          var four = cm.length === 4;
          var tq = cm[0], pq = four ? cm[2] : cm[1], cq = four ? cm[3] : cm[2];
          tackJ = v(tq[0], 0, deck + tq[1]);
          head = v(pq[0], 0, deck + pq[1]);
          if (four) nockJ = v(cm[1][0], 0, deck + cm[1][1]);
          along = sheetDirection(dyn.sheet_angle, tack);
          clewJ = add(add(tackJ, mul(along, Math.abs(cq[0] - tq[0]))), v(0, 0, cq[1] - tq[1]));
          normalJ = cross(along, norm(sub(head, nockJ || tackJ)));
          sparFor = { a: tackJ, b: lerp(tackJ, head, 0.35) };
        } else if (stay && stay.abaft) {
          // a jib-headed sail on a stay with no run (the storm mizzen), from its file: a
          // right-angled triangle whose luff stands up the stay from its tack and whose foot
          // runs aft towards the taffrail ("the foot is extended towards the taffarel by a
          // sheet", Steel 1794, 'Storm mizen'). The file's centre is the triangle's centroid,
          // so the foot is three times its distance abaft the stay's foot, the luff is twice
          // the area over the foot, and the tack lies a third of the luff below the centre.
          var Sa = stay.head, Fa = stay.foot;
          var upA = sub(Sa, Fa);
          var footLen = Math.max(3 * (Fa[0] + STAY_ABAFT_M - (spec.x_m || 0)), 1);
          var luffA = (2 * spec.area_m2) / footLen;
          var tackZ = Math.max((spec.centre_height_m || 0) - luffA / 3, Fa[2] + 0.3);
          var headZ = Math.min(tackZ + luffA, Sa[2]);
          var rise = Math.max(upA[2], 0.1);
          tackJ = add(Fa, mul(upA, (tackZ - Fa[2]) / rise));
          head = add(Fa, mul(upA, (headZ - Fa[2]) / rise));
          along = sheetDirection(dyn.sheet_angle, tack);
          clewJ = add(tackJ, mul(along, footLen));
          normalJ = cross(along, norm(upA));
          sparFor = { a: tackJ, b: lerp(tackJ, head, 0.35) };
        } else if (stay) {
          var S = stay.head, F = stay.foot;
          var up = sub(S, F);
          var f = JIB_LUFF_FRACTION * reefFraction(spec, dyn);
          tackJ = add(F, mul(up, JIB_TACK_FRACTION));
          head = add(F, mul(up, f));
          var luffLen = len(sub(head, tackJ));
          var horiz = len(v(up[0], up[1], 0));
          var theta = Math.atan2(up[2], Math.max(horiz, 0.1));
          var b = (2 * spec.area_m2) / Math.max(luffLen * Math.sin(Math.max(theta, 0.2)), 1);
          b = Math.min(b, Math.max(luffLen * 0.9, 2));
          along = sheetDirection(dyn.sheet_angle, tack);
          clewJ = add(tackJ, mul(along, b));
          normalJ = cross(along, norm(up));
          sparFor = { a: F, b: lerp(F, S, 0.3) };
        } else if (Mm) {
          head = Mm.head;
          tackJ = Mm.foot;
          var gaffBelow = null;
          graph.spars.forEach(function (s) {
            if (s.class === "gaff" && Mm.parent && s.parent === Mm.parent.id) gaffBelow = spars[s.id];
          });
          along = gaffBelow ? gaffBelow.dir : sheetDirection(dyn.sheet_angle, tack);
          if (gaffBelow) {
            clewJ = gaffBelow.b;
          } else {
            var luff2 = head[2] - tackJ[2];
            clewJ = add(tackJ, mul(along, (2 * spec.area_m2) / Math.max(luff2, 1)));
          }
          normalJ = cross(along, [0, 0, 1]);
          sparFor = { a: tackJ, b: lerp(tackJ, head, 0.35) };
        } else {
          return;
        }
        var figJ = {
          kind: "sail",
          id: spec.id,
          cls: cls,
          state: dyn.state,
          backed: dyn.backed,
          reefs: dyn.reefs,
          busy: !!busy[spec.id],
          corners: [tackJ, head, clewJ],
          centre: centroid([tackJ, head, clewJ]),
          stay: roles.stay || null,
        };
        if (dyn.state === "furled" || GATHERED[dyn.state]) {
          figJ.path = bundle(sparFor.a, sparFor.b, 0.35);
        } else if (dyn.state === "blown_out") {
          figJ.path = torn([tackJ, head, clewJ, lerp(clewJ, tackJ, 0.5)]);
        } else if (dyn.state === "wrecked") {
          figJ.path = [[tackJ], [lerp(tackJ, head, 0.5), head], [add(lerp(head, clewJ, 0.5), v(0, 0, -2)), add(clewJ, v(0, 0, -1.5))], [lerp(clewJ, tackJ, 0.5), tackJ]];
        } else {
          var bellyJ = dyn.state === "set" ? mul(bellyDirection(normalJ, wind), 2 * BELLY * Math.min(len(sub(clewJ, tackJ)), len(sub(head, tackJ)))) : [0, 0, 0];
          figJ.path = [[tackJ], [lerp(tackJ, head, 0.5), head], [add(lerp(head, clewJ, 0.5), bellyJ), clewJ], [add(lerp(clewJ, tackJ, 0.5), mul(bellyJ, 0.6)), tackJ]];
          if (nockJ) {
            // four-sided: the head from the nock to the peak along the stay, the bunt from
            // the tack up to the nock
            figJ.path = [[nockJ], [lerp(nockJ, head, 0.5), head], [add(lerp(head, clewJ, 0.5), bellyJ), clewJ], [add(lerp(clewJ, tackJ, 0.5), mul(bellyJ, 0.6)), tackJ], [lerp(tackJ, nockJ, 0.5), nockJ]];
            figJ.centre = centroid([tackJ, nockJ, head, clewJ]);
          }
        }
        // a staysail that crosses a mast is drawn in two parts, each in its own place along
        // the view axis (spec M0-M2 §12 item 9)
        piecesAtMast(figJ).forEach(function (f) {
          figures.push(f);
        });
      } else if (cls === "studding") {
        var boom = spars[roles.boom];
        var Yd = roles.yard ? spars[roles.yard] : null;
        if (!boom) return;
        if (dyn.state === "furled") return; // a studding sail not set is below, on deck
        var Lb = boom.spec.length_m || 5;
        var normalS = boom.normal || [1, 0, 0];
        var cornersS;
        if (spec.centre_height_m < Math.min(boom.a[2], boom.b[2])) {
          // a save-all or a water sail: spread under its boom, the head along its outer
          // part, the foot down near the water (the ship files' shapes)
          var hA = lerp(boom.a, boom.b, 1 - UNDER_BOOM_HEAD);
          var hB = boom.b;
          cornersS = [hA, hB, v(hB[0], hB[1], WATER_SAIL_FOOT_M), v(hA[0], hA[1], WATER_SAIL_FOOT_M)];
          if (boom.dir) normalS = cross(boom.dir, [0, 0, 1]);
        } else if (Yd && Yd.arm) {
          var ss2 = sideSign(spec.side);
          var headA = ss2 > 0 ? Yd.b : Yd.a;
          cornersS = [headA, add(headA, mul(boom.arm || [0, 1, 0], ss2 * Lb)), boom.b, boom.a];
        } else if (boom.dir) {
          // the ringtail: outside the gaff sail's after leech, from the gaff end down to the
          // boom end, its foot on the ringtail boom (Kipping 1847, 'Ringtail Sails')
          var hostBoom = spars[boom.spec.parent];
          var host = ((hostBoom && sailsBySpar[hostBoom.id]) || []).filter(function (s) {
            return s.class === "gaff" || s.class === "sprit";
          })[0];
          var Gh = host ? spars[(host.roles || {}).gaff] : null;
          var clewH = hostBoom ? hostBoom.b : boom.a;
          var peakH = Gh ? Gh.b : add(clewH, v(0, 0, spec.area_m2 / Math.max(Lb, 1)));
          var deep = Math.max(peakH[2] - clewH[2], 1);
          var headW = Math.max((2 * spec.area_m2) / deep - Lb, 0.5);
          cornersS = [peakH, add(peakH, mul(boom.dir, headW)), boom.b, clewH];
          normalS = cross(boom.dir, [0, 0, 1]);
        } else {
          var hZ = boom.a[2] + spec.area_m2 / Math.max(Lb, 1);
          cornersS = [v(boom.a[0], boom.a[1], hZ), v(boom.b[0], boom.b[1], hZ), boom.b, boom.a];
        }
        var depthS = Math.max(cornersS[0][2] - cornersS[3][2], 0.5);
        figures.push(sailFigure(spec, dyn, cornersS, normalS, boom, depthS));
      }
    });

    // -- braces and sheets ----------------------------------------------------------

    var sailFigById = {};
    figures.forEach(function (f) {
      if (f.kind === "sail") sailFigById[f.id] = f;
    });
    var beam = hull.beam_m || 8;

    function mastAftOf(x) {
      var best = null;
      lowerMasts.forEach(function (m) {
        if (m.x < x - 0.5 && (best === null || m.x > best.x)) best = m;
      });
      return best;
    }
    // the yard below on the same mast by the file's heights (package 37n), whatever their
    // hoists now; it was the nearest yard below within half a metre fore and aft, which a
    // raked mast's yards could miss
    function yardBelow(Y) {
      var id = yardBelowId[Y.id];
      var B = id ? spars[id] : null;
      return B && B.arm && !sentDown(B) ? B : null;
    }

    graph.lines.forEach(function (ln) {
      var state = (snapLines[ln.id] || {}).state || ln.state || "belayed";
      if (ln.class === "brace") {
        var Y = spars[ln.of];
        if (!Y || !Y.arm || sentDown(Y) || Y.onDeck) return;
        var ss = sideSign(ln.side);
        var from = ss > 0 ? Y.b : Y.a;
        var m = mastAftOf(Y.x);
        var to = m ? v(m.x, ss * 0.3, Math.min(Y.centre[2], m.head[2] - 1)) : v(Y.x - Y.half * 0.8, (ss * beam) / 2, deck);
        if (underBowsprit(Y.spec) && lowerMasts.length) {
          // package 75 (B5.3; Ext §6.2): a yard under the bowsprit or the jib-boom is braced
          // up to the fore top (Lavery I30), not level aft
          var foreM = lowerMasts[0];
          var topZ = foreM.head[2] - FORE_TOP_BELOW_HEAD_M;
          to = v(foreM.xAt ? foreM.xAt(topZ) : foreM.x, ss * 0.3, topZ);
        }
        if (state === "parted") to = add(from, v(-1.5, 0, -2.5));
        figures.push({ kind: "line", id: ln.id, cls: "brace", of: ln.of, state: state, pts: [from, to], busy: !!busy[ln.of] });
      } else if (ln.class === "lift") {
        // package 75 (B5.1; the owner's answer, Build-Ships.md §19.1 item 7): faint, from the
        // yard's arm on its side up to the head of the mast it hangs on. A spar with no arms
        // (a gaff) has none drawn. The mizen yard of a course cut at the mast (B5.2; Ext §6.1)
        // is held up by its after part, where the sail hangs: its lifts from about the middle
        // of that part, the starboard one a twentieth of it nearer the peak and the larboard
        // one a twentieth nearer the mast, so that the pair are not drawn one over the other;
        // the derrick (its lift with no side) from two-thirds along it toward the peak,
        // "between the slings and the peak" (Steel 1794 vol. I p. 207; judgement)
        // A yard under the bowsprit or the jib-boom (B5.3; Ext §6.2) is lifted as every yard is,
        // up to the head of the spar it hangs on: that spar's end.
        var Yl = spars[ln.of];
        var liftedFrom = Yl && Yl.parent ? Yl.parent.head || (underBowsprit(Yl.spec) ? Yl.parent.tip : null) : null;
        if (!Yl || !Yl.arm || sentDown(Yl) || Yl.onDeck || !liftedFrom) return;
        var arm = sideSign(ln.side) > 0 ? Yl.b : Yl.a;
        if (Yl.cutAtMast) {
          arm = lerp(Yl.truss, Yl.b, ln.side ? 0.5 + 0.05 * sideSign(ln.side) : 2 / 3);
        }
        var up = state === "parted" ? add(arm, v(0, 0, -2.5)) : liftedFrom;
        figures.push({ kind: "line", id: ln.id, cls: "lift", of: ln.of, state: state, pts: [arm, up], busy: !!busy[ln.of] });
      } else if (ln.class === "sheet") {
        var sf = sailFigById[ln.of];
        if (!sf || sf.state === "furled" || !sf.corners) return;
        if (sf.state === "goose_winged" && ln.side === (tack === "starboard" ? "larboard" : "starboard")) return; // the lee clew is up
        var pts;
        var sheetSpec = sailSpecs[ln.of] || {};
        if (sheetSpec.cut_at_mast) {
          // package 75 (B5.2; Ext §6.1): the mizen course's one sheet, from its clew (brailed
          // in with the sail in the gear) to the taffrail on the centreline, where its horse is
          // (Steel 1794 vol. I p. 208). The driver's (B5.5; Ext §17.6) is rove through its
          // boom's end, its tackle to the taffrail: drawn from the boom's end, set or in the
          // gear, and not furled, as every sheet
          var BmS = spars[(sheetSpec.roles || {}).boom];
          pts = [BmS && BmS.dir ? BmS.b : sf.clewAt || sf.corners[2], taffrail(hull)];
        } else if ((sf.cls === "lug" || sf.cls === "lateen") && sheetSpec.corners_m) {
          // package 57: a lug's sheet from its clew aft to the lee side, and a whole lateen's
          // drawn as a lug (package 75); a lug topsail's is at its lower lug's peak, where its
          // clew is, and is not drawn
          if (sheetSpec.sheeted_to) return;
          var lc2 = sf.corners[2];
          var lugLeeSide = lc2[1] >= 0 ? 1 : -1;
          pts = [lc2, v(lc2[0] - 1, (lugLeeSide * beam) / 2, deck)];
        } else if (sf.corners.length === 4 && (sf.cls === "square" || sf.cls === "lug" || sf.cls === "lateen")) {
          var s2 = sideSign(ln.side);
          var Yy = spars[((sailSpecs[ln.of] || {}).roles || {}).yard];
          var clew = s2 > 0 ? sf.corners[2] : sf.corners[3];
          var below = Yy ? yardBelow(Yy) : null;
          var lead = below ? (s2 > 0 ? below.b : below.a) : v(clew[0], (s2 * beam) / 2, deck);
          if (!below && Yy && underBowsprit(Yy.spec) && lowerMasts.length) {
            // package 75 (B5.3; Ext §6.2): the spritsail's sheets aft to the side abaft the
            // fore mast, at the deck (Lavery I30), not abreast the clew forward of the stem; the
            // sprit topsail's go to the spritsail yard's arms, as every topsail's to the yard below
            lead = foreSheetLead(s2);
          }
          pts = [clew, lead];
        } else {
          var clew2 = sf.corners[2];
          var lee = sideSign(ln.side || (tack === "starboard" ? "larboard" : "starboard"));
          pts = [clew2, v(clew2[0] - 2, (lee * beam) / 2, deck)];
          // package 75 (her stage B): on a hull drawn from her profile the sheet of a sail forward
          // of the fore mast, whose rule above stopped abreast the knee of the head, in the air,
          // leads aft to her drawn side abaft the fore mast, as the spritsail's does
          if (profile && lowerMasts.length && sheetSpec.x_m > lowerMasts[0].x) pts = [clew2, foreSheetLead(lee)];
          // package 75 (the razee, her stage B): on a hull drawn from her profile the sheet of a
          // sail on a boom swung about the mast (her spanker's, her ringtail's) is drawn from its
          // clew to the taffrail on the centreline, as the driver's is (Ext §17.6), not to the
          // side abaft the clew: that boom overhangs her stern by 9 m, and that lead stood 11 m
          // abaft her, in the air. It is rove at the boom's end, as the driver's is
          var boomS = spars[(sheetSpec.roles || {}).boom];
          if (profile && boomS && boomS.dir) pts = [sheetSpec.class === "gaff" ? boomS.b : clew2, taffrail(hull)];
        }
        if (state === "parted") pts = [pts[0], add(pts[0], v(-1, 0, -2))];
        figures.push({ kind: "line", id: ln.id, cls: "sheet", of: ln.of, state: state, pts: pts, busy: !!busy[ln.of] });
      } else if (ln.class === "bowline") {
        // hauled out (spec 3b §4): a faint line from the middle of the leech forward, to
        // the mast ahead or, from the foremast, to the head rig (spec 3b §8)
        var snapB = snapLines[ln.id] || {};
        var hauled = snapB.hauled != null ? snapB.hauled : ln.hauled;
        if (state !== "belayed" || !(hauled >= 1 - 1e-9)) return;
        var bf = sailFigById[ln.of];
        if (!bf || !bf.corners || bf.corners.length !== 4 || !DRAWING[bf.state]) return;
        var sb = sideSign(ln.side);
        var leech = sb > 0 ? lerp(bf.corners[1], bf.corners[2], 0.5) : lerp(bf.corners[0], bf.corners[3], 0.5);
        figures.push({ kind: "line", id: ln.id, cls: "bowline", of: ln.of, state: state, pts: [leech, bowlineLead(leech)], busy: !!busy[ln.of] });
      }
    });

    /** Where a bowline leads: to the mast ahead of the leech, a little below it, or from
     *  the foremast to the bowsprit's end (the stem if there is none). */
    function bowlineLead(p) {
      var best = null;
      lowerMasts.forEach(function (m) {
        if (m.x > p[0] + 0.5 && (best === null || m.x < best.x)) best = m;
      });
      if (best) {
        var z = Math.min(p[2] - 1, best.head[2] - 1);
        return v(best.xAt ? best.xAt(z) : best.x, 0, z);
      }
      return headRig.length ? headRig[0].b : v(stemX, 0, deck);
    }

    // Package 57 (the owner's note 5): the painter sets a sail or a yard against its mast
    // as it stands at its own height, not the mast's middle: a raked mast's middle is
    // forward of its upper part, and a topsail set before the topmast's head was drawn
    // behind the mast from ahead. Each carries the point it is sorted by, its centre moved
    // fore and aft by the mast's middle less the mast where the sail is.
    figures.forEach(function (f) {
      if (!f.mastId || !f.centre) return;
      var mr = spars[f.mastId];
      if (!mr || !mr.a || !mr.b) return;
      var mid = lerp(mr.a, mr.b, 0.5);
      var here = mr.xAt ? mr.xAt(f.centre[2]) : mr.x;
      f.sortAt = add(f.centre, v(mid[0] - here, 0, 0));
    });

    // -- the hull --------------------------------------------------------------------

    figures.push.apply(figures, hullFigures(hull));

    return { figures: figures, hull: hull, spars: spars, stays: stayFoot, frame: fullRigFrame(graph, home, hull) };
  }

  /** The full rig's reach, for the view's fixed scale (spec M3 §9 item 14): every spar in
   *  the ship file, aloft whatever its state now, with each swinging spar's reach about its
   *  pivot in all four horizontal directions (at each height its swing reaches from, for the
   *  mizen yard of a course cut at the mast: package 75), so that no brace or sheet angle
   *  and no spar sent down changes it; and the hull. A yard under the bowsprit (package 75,
   *  B5.3) stands foremost of the rig, where braced its arm reaches past the four directions
   *  seen on the bow: its swing is reached every way, by sixteen points about its slings whose
   *  figure's sides touch the circle its arms sweep, at the height of its slings and of the
   *  foot of a sail hanging from it. So is a driver's boom about its jaws
   *  (B5.5): it reaches far beyond the taffrail, and sheeted to the quarter its end reaches
   *  past the four directions seen on the quarter; and every boom on a hull drawn from her
   *  profile (the razee's spanker's, her stage B). */
  function fullRigFrame(graph, spars, hull) {
    var pts = [];
    var dirs = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]];
    var everyWay = [];
    for (var k = 0; k < 16; k++) {
      everyWay.push(mul([Math.cos((k * Math.PI) / 8), Math.sin((k * Math.PI) / 8), 0], 1 / Math.cos(Math.PI / 16)));
    }
    graph.spars.forEach(function (s) {
      var r = spars[s.id];
      if (!r) return;
      var ends = r.full || [r.a, r.b];
      pts.push(ends[0], ends[1]);
      if (!SWINGING[s.class]) return;
      var pivot, reach;
      if (r.pivot) {
        // a studding sail boom: out beyond its yardarm, however braced; the mizen yard of a
        // course cut at the mast about its truss (package 75)
        pivot = r.pivot;
        reach = r.reach;
      } else if (r.centre) {
        pivot = r.centre; // a yard about its slings
        reach = r.half;
      } else {
        pivot = r.a; // a gaff, boom or sprit about its mast
        reach = len(sub(r.b, r.a));
      }
      // at the pivot's height, or at each height a swing reaches from (the mizen yard's)
      (r.heights || [pivot[2]]).forEach(function (z) {
        var at = v(pivot[0], pivot[1], z);
        (r.everyWay ? everyWay : dirs).forEach(function (d) {
          pts.push(add(at, mul(d, reach)));
        });
      });
    });
    hullFigures(hull).forEach(function (f) {
      pts.push.apply(pts, f.pts);
    });
    return pts;
  }

  /** The hull as a lens-shaped deck with sheer and two side faces down to just
   *  below the waterline (the sea covers the rest). From length, beam,
   *  freeboard and a sheer that rises toward the bow. A hull whose file gives a
   *  profile is drawn from it instead (package 75): on the stations the graph serves
   *  (`formHullFigures`, B5.6), or on B5.1's from the profile where it serves none
   *  (`profileHullFigures`). */
  function hullFigures(hull) {
    if (servedStations(hull)) return formHullFigures(hull);
    if (drawnProfile(hull)) return profileHullFigures(hull);
    var L = hull.length_waterline_m;
    var B = hull.beam_m;
    var F = hull.deck_height_m || 1.5;
    var sternX = -L / 2 - 0.02 * L;
    var bowX = L / 2 + 0.06 * L;
    var n = 14;
    var stbd = [], larb = [], stbdLow = [], larbLow = [];
    for (var i = 0; i <= n; i++) {
      var t = -1 + (2 * i) / n; // -1 stern, +1 bow
      var x = sternX + ((t + 1) / 2) * (bowX - sternX);
      var half = i === n ? 0 : (B / 2) * Math.pow(1 - Math.pow(Math.abs(t), 2.2), 0.55);
      if (i === 0) half = B * 0.28; // the transom
      var z = F * (1 + 0.12 * t * t + 0.1 * t);
      stbd.push([x, half, z]);
      larb.push([x, -half, z]);
      stbdLow.push([x, half * 0.92, -0.8]);
      larbLow.push([x, -half * 0.92, -0.8]);
    }
    var deckPoly = stbd.concat(larb.slice().reverse());
    var stbdFace = stbd.concat(stbdLow.slice().reverse());
    var larbFace = larb.concat(larbLow.slice().reverse());
    var transom = [stbd[0], larb[0], larbLow[0], stbdLow[0]];
    return [
      { kind: "hull", part: "deck", pts: deckPoly },
      { kind: "hull", part: "side", side: "starboard", pts: stbdFace },
      { kind: "hull", part: "side", side: "larboard", pts: larbFace },
      { kind: "hull", part: "transom", pts: transom },
    ];
  }

  // -- the hull from her profile (package 75, B5.1) --------------------------------------

  /** The hull's profile where the file gives one the drawing can stand on (`rail_m` and
   *  `breadth_m`, which §5.2 requires of every profile), else null. */
  function drawnProfile(hull) {
    var p = hull && hull.profile;
    return p && p.rail_m && p.rail_m.length && p.breadth_m && p.breadth_m.length ? p : null;
  }

  /** The value at `x` of a line of [x, value, ...] points, x increasing: straight between two
   *  points, held at the first and the last beyond them (freesail/ship/profile.py's `interp`).
   *  `k` picks which of a point's numbers is the value: its second by default. */
  function lineAt(points, x, k) {
    k = k || 1;
    var n = points.length;
    if (x <= points[0][0]) return points[0][k];
    if (x >= points[n - 1][0]) return points[n - 1][k];
    for (var i = 1; i < n; i++) {
      if (x <= points[i][0]) {
        var p = points[i - 1], q = points[i];
        return p[k] + ((q[k] - p[k]) * (x - p[0])) / (q[0] - p[0]);
      }
    }
    return points[n - 1][k];
  }

  /** Where a line of [x, z] points, z rising (the stem's or the stern's), stands at height z:
   *  its x, held beyond its ends. */
  function xAtHeight(line, z) {
    var n = line.length;
    if (z <= line[0][1]) return line[0][0];
    if (z >= line[n - 1][1]) return line[n - 1][0];
    for (var i = 1; i < n; i++) {
      if (z <= line[i][1]) {
        var p = line[i - 1], q = line[i];
        return q[1] === p[1] ? p[0] : p[0] + ((q[0] - p[0]) * (z - p[1])) / (q[1] - p[1]);
      }
    }
    return line[n - 1][0];
  }

  /** The lowest height, not below `floor`, at which such a line stands at `x`; null where it
   *  never does. */
  function heightAtX(line, x, floor) {
    for (var i = 1; i < line.length; i++) {
      var p = line[i - 1], q = line[i];
      if ((p[0] - x) * (q[0] - x) > 0) continue;
      var z = q[0] === p[0] ? Math.max(p[1], floor) : p[1] + ((q[1] - p[1]) * (x - p[0])) / (q[0] - p[0]);
      if (z >= floor - 1e-9 && z <= Math.max(p[1], q[1]) + 1e-9) return Math.max(z, floor);
    }
    return null;
  }

  /** The uppermost deck at `x` (freesail/ship/profile.py's `deck_at`): of the decks whose
   *  extent holds x, the highest there; beyond every deck's extent, the nearest deck's end,
   *  held; null, a profile that gives no decks. */
  function deckAt(profile, x) {
    var decks = profile.decks_m || {};
    var words = Object.keys(decks);
    if (!words.length) return null;
    var best = null;
    words.forEach(function (w) {
      var pts = decks[w];
      if (pts[0][0] <= x && x <= pts[pts.length - 1][0]) {
        var z = lineAt(pts, x);
        if (best === null || z > best) best = z;
      }
    });
    if (best !== null) return best;
    function gap(pts) {
      return x < pts[0][0] ? pts[0][0] - x : x - pts[pts.length - 1][0];
    }
    var nearest = Infinity;
    words.forEach(function (w) {
      nearest = Math.min(nearest, gap(decks[w]));
    });
    words.forEach(function (w) {
      if (gap(decks[w]) !== nearest) return;
      var z = lineAt(decks[w], x);
      if (best === null || z > best) best = z;
    });
    return best;
  }

  /** A lower mast's foot on the drawn deck: the height at which its rake line (`xAt`) meets
   *  the uppermost deck there; null without decks. */
  function footOnDeck(profile, xAt) {
    var z = deckAt(profile, xAt(0));
    if (z === null) return null;
    for (var k = 0; k < 3; k++) z = deckAt(profile, xAt(z)); // the rake moves it a hair
    return z;
  }

  /** The taffrail on the centreline, where a sheet led to the stern is drawn to (package 75,
   *  B5.2; Ext §6.1): the rail's after end where the file gives a profile, else the stern of
   *  the hull `hullFigures` draws without one (0.52 of her length abaft midships, at its
   *  sheer there). */
  function taffrail(hull) {
    var p = drawnProfile(hull);
    if (p) return v(p.rail_m[0][0], 0, p.rail_m[0][1]);
    var L = hull.length_waterline_m;
    return v(-L / 2 - 0.02 * L, 0, (hull.deck_height_m || 1.5) * 1.02);
  }

  /** The stem head, the top of the stem's fore edge (`stem_m`'s last point; the rail's last
   *  without a stem), as [x, z]: lowered to the rail at its x where that is lower (§6), where
   *  the bowsprit's heel is drawn. */
  function stemHead(profile) {
    var stem = profile.stem_m && profile.stem_m.length ? profile.stem_m : null;
    var rail = profile.rail_m;
    var head = stem ? stem[stem.length - 1] : rail[rail.length - 1];
    return [head[0], Math.min(head[1], lineAt(rail, head[0]))];
  }

  /**
   * The hull as her profile draws it (B5.1, §6): the stations aft to forward, each {x, pts},
   * its points [z, half-breadth] from its low edge up to the top of the side. Pure; the
   * served `hull.stations` (form.py's rule) take its place at B5.6.
   *
   * - The top of the side is `rail_m`; forward of it, where the rail ends abaft the stem head
   *   (a beakhead bulkhead), the head rule, straight from the rail's end to the stem head.
   * - The low edge is the cut, CUT_Z_M below the water, but abaft the post and forward of the
   *   stem, where it is the stern's and the stem's lines, so that the side closes along them:
   *   the stem on the middle line up to the stem head, the post on it up to the counter's
   *   knuckle (`form.stern.knuckle_z_m`; the water where the file gives none, form.py's
   *   default), and above the knuckle the transom's edge.
   * - The half-breadths are `breadth_m`'s at the water and at the rail, the water's run in to
   *   nothing at the post and the stem, the rail's to nothing at the stem head and held aft
   *   (the transom). Below the water the midship section (`section_m`) is scaled by the
   *   water's half-breadth against its own at the water (judgement); without one, the side
   *   runs straight to CUT_SHARE of it at the cut.
   * - Above the water, where the side tumbles home, the section's upper shape is fitted between
   *   the water's and the rail's half-breadths, its height stretched to the station's top; where
   *   it flares toward the bow the side runs straight from one to the other, and abaft
   *   midships it reaches the rail's at the knuckle and stands at it above (judgement: scaled by
   *   the water's half-breadth alone, as §6 has it, the counter and the bow's upper works were
   *   pinched to a sliver, the 64's counter 0.26 m from the middle line under a rail 3.51 m out).
   *   Abaft the post, above the knuckle, the counter stands at the rail's half-breadth
   *   (judgement: the transom's own half-breadths are B5.6's).
   */
  function profileHull(profile) {
    var rail = profile.rail_m;
    var br = profile.breadth_m;
    var stem = profile.stem_m && profile.stem_m.length > 1 ? profile.stem_m : null;
    var stern = profile.stern_m && profile.stern_m.length > 1 ? profile.stern_m : null;
    var sec = profile.section_m && profile.section_m.length > 1 ? profile.section_m : null;
    var sternForm = (profile.form || {}).stern || {};
    var taffrail = rail[0];
    var railEnd = rail[rail.length - 1];
    var head = stem ? stem[stem.length - 1] : railEnd;
    var headRule = head[0] > railEnd[0] + 1e-6;
    var xAft = taffrail[0];
    var xFore = Math.max(head[0], railEnd[0]);
    var postCut = stern ? xAtHeight(stern, CUT_Z_M) : -Infinity;
    var postWater = stern ? xAtHeight(stern, 0) : -Infinity;
    var stemCut = stem ? xAtHeight(stem, CUT_Z_M) : Infinity;
    var stemWater = stem ? xAtHeight(stem, 0) : Infinity;
    var knuckle = sternForm.knuckle_z_m != null ? sternForm.knuckle_z_m : stern ? 0 : CUT_Z_M;
    var b0 = br[0], b1 = br[br.length - 1];

    function topAt(x) {
      if (headRule && x > railEnd[0]) return railEnd[1] + ((head[1] - railEnd[1]) * (x - railEnd[0])) / (head[0] - railEnd[0]);
      return lineAt(rail, x);
    }
    /** The low edge, and the line it is on: "cut", "post", "transom" or "stem". */
    function lowAt(x) {
      var z = null, on = "cut";
      if (stern && x < postCut) {
        z = heightAtX(stern, x, CUT_Z_M);
        on = z !== null && z >= knuckle - 1e-9 ? "transom" : "post";
      } else if (stem && x > stemCut) {
        z = heightAtX(stem, x, CUT_Z_M);
        on = "stem";
      } else {
        z = CUT_Z_M;
      }
      return { z: z === null ? Infinity : z, on: on };
    }
    function waterHB(x) {
      if (stern && x < b0[0]) return x <= postWater ? 0 : (b0[1] * (x - postWater)) / (b0[0] - postWater);
      if (stem && x > b1[0]) return x >= stemWater ? 0 : (b1[1] * (stemWater - x)) / (stemWater - b1[0]);
      return lineAt(br, x, 1);
    }
    function railHB(x) {
      if (stem && x > b1[0]) return x >= xFore ? 0 : (b1[2] * (xFore - x)) / (xFore - b1[0]);
      return lineAt(br, x, 2);
    }
    // the section's upper shape, from the water to the top of the side at midships
    var s0 = sec ? lineAt(sec, 0) : 0;
    var zRef = sec ? Math.min(Math.max(topAt(0), 0.1), sec[sec.length - 1][0]) : 0;
    var sRef = sec ? lineAt(sec, zRef) : 0;
    var shaped = !!sec && s0 > 0 && Math.abs(sRef - s0) > 1e-6;
    function sideHB(z, top, w, r, counter) {
      if (z < 0) return sec && s0 > 0 ? (lineAt(sec, z) * w) / s0 : w * (1 - ((1 - CUT_SHARE) * z) / CUT_Z_M);
      var t = top > 1e-6 ? Math.min(z / top, 1) : 1;
      if (shaped && r < w) return w + ((r - w) * (lineAt(sec, t * zRef) - s0)) / (sRef - s0);
      if (counter) return w + (r - w) * Math.min(z / knuckle, 1);
      return w + (r - w) * t;
    }

    function station(x) {
      var top = topAt(x);
      var low = lowAt(x);
      var z0 = Math.min(low.z, top);
      var w = waterHB(x), r = railHB(x);
      // abaft midships, where the side flares out to the counter, it reaches the rail's
      // half-breadth at the knuckle, the counter's foot, and stands at it above (judgement)
      var counter = x < 0 && r > w && knuckle > 0 && knuckle < top;
      var zs = [z0, top];
      if (z0 < 0 && top > 0) zs.push(0);
      if (counter) zs.push(knuckle);
      if (sec) {
        sec.forEach(function (p) {
          if (p[0] < 0) zs.push(p[0]);
          else if (p[0] > 0 && p[0] < zRef && shaped && r < w) zs.push((p[0] * top) / zRef);
        });
      }
      zs = zs
        .filter(function (z) {
          return z >= z0 && z <= top;
        })
        .sort(function (a, b) {
          return a - b;
        })
        .filter(function (z, i, all) {
          return i === 0 || z - all[i - 1] > 1e-6;
        });
      var pts = zs.map(function (z) {
        if (low.on === "transom") return [z, r]; // the counter, at the rail's half-breadth
        return [z, sideHB(z, top, w, r, counter)];
      });
      if (low.on === "post" || low.on === "stem") pts[0][1] = 0; // on the middle line
      // at the knuckle the counter's underside closes in to the post: the station there
      // starts on the middle line, for the strip forward of it (`post`)
      var post = low.on === "transom" && Math.abs(z0 - knuckle) < 1e-6 && z0 < top;
      if (post) pts.unshift([z0, 0]);
      return { x: x, pts: pts, on: z0 < top ? low.on : "end", post: post };
    }

    var xs = [];
    rail.forEach(function (p) {
      xs.push(p[0]);
    });
    br.forEach(function (p) {
      xs.push(p[0]);
    });
    for (var k = 0; k <= STATION_GRID; k++) xs.push(xAft + ((xFore - xAft) * k) / STATION_GRID);
    [stern, stem].forEach(function (line) {
      (line || []).forEach(function (p) {
        if (p[1] > CUT_Z_M) xs.push(p[0]);
      });
    });
    if (stern) xs.push(postCut, postWater, xAtHeight(stern, knuckle));
    if (stem) xs.push(stemCut, stemWater);
    xs = xs
      .filter(function (x) {
        return x >= xAft - 1e-9 && x <= xFore + 1e-9;
      })
      .sort(function (a, b) {
        return a - b;
      })
      .filter(function (x, i, all) {
        return i === 0 || x - all[i - 1] > 1e-4;
      });
    return {
      stations: xs.map(station),
      station: station,
      knuckle: knuckle,
      railEnd: railEnd,
      head: head,
      headRule: headRule,
      railHB: railHB,
    };
  }

  /** A station's points on the side: at the knuckle, without its point on the post. */
  function sidePts(st) {
    return st.post ? st.pts.slice(1) : st.pts;
  }

  /** A station's half-breadth at height z on the side, straight between its points, held
   *  beyond them. */
  function hbOnStation(st, z) {
    var pts = sidePts(st);
    if (z <= pts[0][0]) return pts[0][1];
    for (var i = 1; i < pts.length; i++) {
      if (z <= pts[i][0]) {
        var p = pts[i - 1], q = pts[i];
        return q[0] === p[0] ? q[1] : p[1] + ((q[1] - p[1]) * (z - p[0])) / (q[0] - p[0]);
      }
    }
    return pts[pts.length - 1][1];
  }

  /** Whether a deck's ports are cut in the side, so that its strake is drawn as a band: each
   *  port's middle below the rail at its x. Not where the guns fire over the rail, as the 64's
   *  forecastle and roundhouse carronades do, their middles 0.3 m above it; a port cut in the
   *  side may reach the rail (the 64's foremost quarterdeck port, 2 cm over it), and its band
   *  is held to the top of the side. */
  function portsInSide(profile, ports, size) {
    return ports.every(function (p) {
      return p[1] + size[1] / 2 <= lineAt(profile.rail_m, p[0]);
    });
  }

  /** The normal of a face of four points, away from the middle line on its side (`sign`, +1 the
   *  starboard), or up where `sign` is 0: taken across its diagonals, so that a face cut to a
   *  triangle keeps it. A figure carrying it as `outward` is seen only from that side of its
   *  face (`project`): a wale or band on the outside of the side, not through the far bulwark
   *  seen from inboard; a deck from above. */
  function faceOut(pts, sign) {
    var n = cross(sub(pts[2], pts[0]), sub(pts[3], pts[1]));
    var along = sign ? sign * n[1] : n[2];
    return along < 0 ? mul(n, -1) : n;
  }

  /**
   * The faces across the ship where a deck ends with another running on under it (`part:
   * bulkhead`, B5.6): the 64's roundhouse front, her quarterdeck's breast and her forecastle's
   * after end, the razee's breast and forecastle. Each stands at the deck's end, from the deck
   * below there up to the top of the side, between the drawn side's half-breadths at its
   * heights (`hbAt`), sorted at its middle: so that the decks beyond it, and the space under the
   * higher deck, are not seen through where a two-decker has a bulkhead or a breastwork
   * (judgement: no opening drawn; derived from `decks_m` and `rail_m` alone). A deck's end within
   * DECK_END_CLEAR_M of the rail's ends, or with no deck running on under it by as much each way,
   * has none.
   */
  function deckEndFigures(profile, topAt, hbAt) {
    var decks = profile.decks_m || {};
    var words = Object.keys(decks);
    var rail = profile.rail_m;
    var xAft = rail[0][0], xFore = rail[rail.length - 1][0];
    var figs = [];
    words.forEach(function (word) {
      var pts = decks[word];
      [pts[0][0], pts[pts.length - 1][0]].forEach(function (x) {
        if (x - xAft < DECK_END_CLEAR_M || xFore - x < DECK_END_CLEAR_M) return;
        var z = lineAt(pts, x);
        var below = null;
        words.forEach(function (other) {
          var q = decks[other];
          if (q[0][0] > x - DECK_END_CLEAR_M || q[q.length - 1][0] < x + DECK_END_CLEAR_M) return;
          var zq = lineAt(q, x);
          if (zq < z && (below === null || zq > below)) below = zq;
        });
        var top = topAt(x);
        if (below === null || !(top - below > 1e-6)) return;
        var side = [];
        for (var k = 0; k <= DECK_END_LEVELS; k++) {
          var zk = below + ((top - below) * k) / DECK_END_LEVELS;
          side.push(v(x, hbAt(x, zk), zk));
        }
        var face = side.concat(
          side
            .slice()
            .reverse()
            .map(function (p) {
              return v(p[0], -p[1], p[2]);
            })
        );
        figs.push({ kind: "hull", part: "bulkhead", deck: word, pts: face, sortAt: centroid(face) });
      });
    });
    return figs;
  }

  var PROFILE_HULLS = typeof WeakMap === "function" ? new WeakMap() : null; // drawn once a profile

  /**
   * The hull's figures from her profile (B5.1, §6), in SHIP COORDINATES as `hullFigures`, each
   * long line cut at the stations so that the painter sorts it piece by piece:
   * - `deck` strips (class `strip`), each deck of `decks_m` at its own heights and over its
   *   extent, at DECK_SHARE of the rail's half-breadth (or of the side's at the deck's height,
   *   where the side flares below the rail), the lowest first, each sorted DECK_BEHIND_M
   *   farther than its middle and seen only from above (`outward`);
   * - `bottom` strips across the cut, between the two sides' low edges;
   * - `side` strips, one polygon a side between each two neighbouring stations from the low
   *   edge to the top of the side, each sorted at its middle (`sortAt`); on each, a hair nearer
   *   (the same point, later), the main `wale` and the `band` of each deck's ports, each seen
   *   only from outboard (`outward`), and the `outline` along its top and its low edge (the cut, the stem, the post, the transom's
   *   edge), stroked with no fill. One outline a side, sorted at one depth, is painted over by
   *   its own near strips, or paints the far rail over the near side seen on the bow;
   * - `transom` strips across the stern, up its line from the counter's knuckle to the
   *   taffrail, with the outline across the knuckle and the taffrail;
   * - the `bulkhead`, where the rail ends abaft the stem head: the face across the bow between
   *   the two sides' tops along the head rule, so that the bow is not hollow seen from ahead;
   *   and one across the ship where a deck ends with another running on under it
   *   (`deckEndFigures`).
   */
  function profileHullFigures(hull) {
    var profile = drawnProfile(hull);
    var kept = PROFILE_HULLS && PROFILE_HULLS.get(profile);
    if (kept) return kept;
    var H = profileHull(profile);
    var st = H.stations;
    var figs = [];
    function at(s, sign, p) {
      return v(s.x, sign * p[1], p[0]);
    }
    function low(s) {
      return s.pts[0];
    }
    function top(s) {
      return s.pts[s.pts.length - 1];
    }
    /** A band between two lines of height along a strip, on the drawn side: `zl(x)` and `zu(x)`
     *  over [x0, x1], cut to the side's low edge and top; null where nothing is left. */
    function band(a, b, sign, x0, x1, zl, zu) {
      var xa = Math.max(a.x, x0), xb = Math.min(b.x, x1);
      if (xb - xa < 1e-6) return null;
      function edge(x, upper) {
        var t = b.x > a.x ? (x - a.x) / (b.x - a.x) : 0;
        var lo = low(a)[0] + (low(b)[0] - low(a)[0]) * t;
        var hi = top(a)[0] + (top(b)[0] - top(a)[0]) * t;
        var z = Math.min(Math.max(upper ? zu(x) : zl(x), lo), hi);
        var hb = hbOnStation(a, z) + (hbOnStation(b, z) - hbOnStation(a, z)) * t;
        return v(x, sign * hb, z);
      }
      var pts = [edge(xa, false), edge(xb, false), edge(xb, true), edge(xa, true)];
      return pts[3][2] - pts[0][2] > 1e-6 || pts[2][2] - pts[1][2] > 1e-6 ? pts : null;
    }
    var wales = profile.wales_m && profile.wales_m.length ? profile.wales_m : null;
    // a deck's band where its ports are cut in the side (`portsInSide`): not where the guns fire
    // over it (the 64's forecastle and roundhouse carronades)
    var portRuns = [];
    if (PORT_BANDS) {
      Object.keys(profile.ports_m || {}).forEach(function (word) {
        var ports = profile.ports_m[word];
        var size = (profile.port_size_m || {})[word];
        if (!ports || !ports.length || !size) return;
        if (portsInSide(profile, ports, size)) portRuns.push({ deck: word, ports: ports, x0: ports[0][0] - size[0] / 2, x1: ports[ports.length - 1][0] + size[0] / 2, depth: size[1] });
      });
    }

    // the decks first, the lowest first: at the same depth a higher deck is drawn over a lower
    // one, and the side over a deck (dead ahead or astern a deck and the strip beside it tie)
    var decks = profile.decks_m || {};
    Object.keys(decks)
      .map(function (word) {
        var pts = decks[word];
        var mean = 0;
        pts.forEach(function (p) {
          mean += p[1] / pts.length;
        });
        return { word: word, pts: pts, mean: mean };
      })
      .sort(function (p, q) {
        return p.mean - q.mean;
      })
      .forEach(function (d) {
        var d0 = d.pts[0][0], d1 = d.pts[d.pts.length - 1][0];
        function edge(x, sign) {
          // inside the rail, and inside the side at its own height where the side flares
          // below the rail toward the ends
          var z = lineAt(d.pts, x);
          var hb = Math.min(H.railHB(x), hbOnStation(H.station(x), z));
          return v(x, sign * DECK_SHARE * hb, z);
        }
        for (var j = 0; j + 1 < st.length; j++) {
          var xa = Math.max(st[j].x, d0), xb = Math.min(st[j + 1].x, d1);
          if (xb - xa < 1e-6) continue;
          var plank = [edge(xa, 1), edge(xb, 1), edge(xb, -1), edge(xa, -1)];
          figs.push({ kind: "hull", part: "deck", cls: "strip", deck: d.word, pts: plank, sortBias: DECK_BEHIND_M, outward: faceOut(plank, 0) });
        }
      });

    // the bottom across the cut, between the two sides' low edges, so that a hull heeled away
    // from the viewer does not show her low decks through it (the drawn depth is B5.6's)
    for (var c = 0; c + 1 < st.length; c++) {
      var ca = low(st[c]), cb = low(st[c + 1]);
      if (ca[0] > CUT_Z_M + 1e-9 || cb[0] > CUT_Z_M + 1e-9) continue;
      var floor = [at(st[c], 1, ca), at(st[c + 1], 1, cb), at(st[c + 1], -1, cb), at(st[c], -1, ca)];
      figs.push({ kind: "hull", part: "bottom", cls: "strip", pts: floor });
    }

    for (var i = 0; i + 1 < st.length; i++) {
      var a = st[i], b = st[i + 1];
      var bPts = sidePts(b); // the strip abaft the knuckle's station stands on the side
      [1, -1].forEach(function (sign) {
        var side = sign > 0 ? "starboard" : "larboard";
        var la = at(a, sign, low(a)), ta = at(a, sign, top(a)), lb = at(b, sign, bPts[0]), tb = at(b, sign, top(b));
        var mid = centroid([la, ta, tb, lb]);
        var pts = a.pts
          .map(function (p) {
            return at(a, sign, p);
          })
          .concat(
            bPts
              .slice()
              .reverse()
              .map(function (p) {
                return at(b, sign, p);
              })
          );
        figs.push({ kind: "hull", part: "side", side: side, cls: "strip", pts: pts, sortAt: mid });
        if (wales) {
          var w = band(a, b, sign, wales[0][0], wales[wales.length - 1][0], function (x) {
            return lineAt(wales, x, 1);
          }, function (x) {
            return lineAt(wales, x, 2);
          });
          if (w) figs.push({ kind: "hull", part: "wale", side: side, cls: "strip", pts: w, sortAt: mid, outward: faceOut(w, sign) });
        }
        portRuns.forEach(function (run) {
          var sill = function (x) {
            return lineAt(run.ports, x, 1);
          };
          var p = band(a, b, sign, run.x0, run.x1, sill, function (x) {
            return sill(x) + run.depth;
          });
          if (p) figs.push({ kind: "hull", part: "band", side: side, cls: "strip", deck: run.deck, pts: p, sortAt: mid, outward: faceOut(p, sign) });
        });
        figs.push({ kind: "hull", part: "outline", side: side, pts: [ta, tb], sortAt: mid });
        figs.push({ kind: "hull", part: "outline", side: side, pts: [la, lb], sortAt: mid });
        // at the knuckle, from the post out to the transom's edge
        if (a.post) figs.push({ kind: "hull", part: "outline", side: side, pts: [la, at(a, sign, a.pts[1])], sortAt: mid });
        // the ends' own edges: the stern's or the bow's where a station stands upright there
        [[i === 0, a], [i + 2 === st.length, b]].forEach(function (end) {
          if (!end[0] || sidePts(end[1]).length < 2) return;
          figs.push({
            kind: "hull",
            part: "outline",
            side: side,
            pts: sidePts(end[1]).map(function (p) {
              return at(end[1], sign, p);
            }),
            sortAt: mid,
          });
        });
      });
    }

    // the transom: up the stern's line from the knuckle to the taffrail, on the sides' after
    // edges (the stations whose low edge is the transom's), or the aftmost station's
    var aft = st.filter(function (s) {
      return s.on === "transom";
    });
    var edgeAft = aft.length
      ? aft
          .map(function (s) {
            return at(s, 1, sidePts(s)[0]);
          })
          .reverse()
      : st[0].pts
          .filter(function (p) {
            return p[0] >= H.knuckle - 1e-9;
          })
          .map(function (p) {
            return at(st[0], 1, p);
          });
    var stern0 = st[0];
    var taff = at(stern0, 1, top(stern0));
    if (!edgeAft.length || len(sub(edgeAft[edgeAft.length - 1], taff)) > 1e-9) edgeAft.push(taff);
    // in strips across the stern too, each sorted at its own middle on the stern's line, so that
    // the decks inside are drawn behind it seen from astern
    function across(p) {
      return v(p[0], -p[1], p[2]);
    }
    for (var e = 0; e + 1 < edgeAft.length; e++) {
      var p0 = edgeAft[e], p1 = edgeAft[e + 1];
      var face = [p0, p1, across(p1), across(p0)];
      var middle = centroid(face);
      figs.push({ kind: "hull", part: "transom", cls: "strip", pts: face, sortAt: middle });
      if (e === 0) figs.push({ kind: "hull", part: "outline", pts: [p0, across(p0)], sortAt: middle }); // the knuckle
      if (e + 2 === edgeAft.length) figs.push({ kind: "hull", part: "outline", pts: [p1, across(p1)], sortAt: middle }); // the taffrail
    }

    // where a deck ends with another running on under it, the face across the ship between them
    figs.push.apply(
      figs,
      deckEndFigures(
        profile,
        function (x) {
          return top(H.station(x))[0];
        },
        function (x, z) {
          return hbOnStation(H.station(x), z);
        }
      )
    );

    // a profile with no stem ends forward in an upright station: its face closes the bow
    var foremost = st[st.length - 1];
    if (foremost.pts.length > 1) {
      var bow = foremost.pts.map(function (p) {
        return at(foremost, 1, p);
      });
      figs.push({ kind: "hull", part: "bulkhead", pts: bow.concat(bow.slice().reverse().map(across)) });
    }
    // the head rule's face across the bow, from the rail's end to the stem head
    if (H.headRule) {
      var fore = st.filter(function (s) {
        return s.x >= H.railEnd[0] - 1e-9;
      });
      var cap = fore.map(function (s) {
        return at(s, 1, top(s));
      });
      if (cap.length > 1) {
        figs.push({
          kind: "hull",
          part: "bulkhead",
          pts: cap.concat(
            cap
              .slice()
              .reverse()
              .map(function (p) {
                return v(p[0], -p[1], p[2]);
              })
          ),
        });
      }
    }
    figs.forEach(function (f) {
      f.sea = true; // below the water as the owner chooses (UNDERWATER)
    });
    if (PROFILE_HULLS) PROFILE_HULLS.set(profile, figs);
    return figs;
  }

  // -- the hull's form as served (package 75, B5.6) ----------------------------------------

  /** The hull as drawn, served by /api/ship for a file with a profile (`hull.stations`, stage
   *  0H: freesail/ship/form.py's stations, the stern's closure first and the stem's last, each
   *  station its [x, z, hb] from its lowest point up to the top of the side), else null. */
  function servedStations(hull) {
    var st = hull && hull.stations;
    return drawnProfile(hull) && st && st.length >= 3 ? st : null;
  }

  /** The last of a station's points at or below height z, its index; -1 below its lowest. */
  function belowOn(pts, z) {
    for (var i = pts.length - 1; i >= 0; i--) if (pts[i][1] <= z) return i;
    return -1;
  }

  /** A station's point at height z, [x, z, hb] (x moves up a closure): straight between its
   *  points, held at its lowest and its highest; where two points stand at one height (a
   *  transom's foot), the upper from that height up (form.py's `_hb_on`). */
  function pointOn(pts, z) {
    var n = pts.length;
    if (z <= pts[0][1]) return [pts[0][0], z, pts[0][2]];
    if (z >= pts[n - 1][1]) return [pts[n - 1][0], z, pts[n - 1][2]];
    var i = belowOn(pts, z);
    var p = pts[i], q = pts[i + 1];
    if (q[1] <= p[1]) return [p[0], z, p[2]];
    var t = (z - p[1]) / (q[1] - p[1]);
    return [p[0] + (q[0] - p[0]) * t, z, p[2] + (q[2] - p[2]) * t];
  }

  function samePoint(p, q) {
    return Math.abs(p[0] - q[0]) < 1e-9 && Math.abs(p[1] - q[1]) < 1e-9 && Math.abs(p[2] - q[2]) < 1e-9;
  }

  /**
   * The served stations as the viewer draws them (B5.6, §6), aft to forward, each {pts, x, cut,
   * low, top}: its points [x, z, hb] low to high, cut at the drawn depth D = max(0.8 m, its
   * half-breadth at the water x tan UNDERWATER_HEEL_DEG) where it goes deeper, and kept whole
   * where it does not (no deeper than the hull). The first and the last are the stern's and the
   * stem's closures, whose x follows their line up (x null); the others stand at one x each.
   *
   * The low line runs aft to forward round the hull's lower edge: down the stern's line from
   * the taffrail to its cut, along the bottom through the stations that reach the cut, and up
   * the stem's line to the stem head. A station over the counter or along the bow (form.py's
   * end stations, at the rail's points beyond the others) stands on it where the stern's or the
   * stem's line crosses its x; each station's `pos` is its lowest point's place on it. Between
   * two stations the side's low edge is the low line between their places.
   *
   * Also: `hbAt(x, z)`, the drawn side's half-breadth (form.py's rule: straight at each height
   * from station to station and on to the stern's and the stem's lines, nothing outside them
   * or above the top of the side); `topAt(x)` and `lowAt(x)`, the side's top and low edge.
   */
  function formHull(hull) {
    var tanHeel = Math.tan((UNDERWATER_HEEL_DEG * Math.PI) / 180);
    var served = servedStations(hull);
    var all = served.map(function (pts, i) {
      var top = pts[pts.length - 1];
      var water = pts[0][1] < 0 && top[1] > 0 ? pointOn(pts, 0)[2] : 0;
      var floor = -Math.max(-CUT_Z_M, water * tanHeel);
      var cut = pts[0][1] < floor - 1e-9;
      var kept = pts;
      if (cut) {
        kept = [pointOn(pts, floor)];
        pts.forEach(function (p) {
          if (p[1] > floor + 1e-9) kept.push(p);
        });
      }
      var end = i === 0 || i === served.length - 1;
      return { pts: kept, x: end ? null : pts[0][0], cut: cut, low: kept[0], top: kept[kept.length - 1], depth: -floor };
    });
    var aft = all[0], fore = all[all.length - 1];
    var mid = all.slice(1, -1).filter(function (s) {
      return s.top[1] - s.low[1] > 1e-6;
    });
    var S = [aft].concat(mid, [fore]);

    /** The segment of a closure's line on which a point stands (its index), or -1. */
    function segmentOn(line, p) {
      for (var i = 0; i + 1 < line.length; i++) {
        var a = line[i], b = line[i + 1];
        if (p[1] < Math.min(a[1], b[1]) - 1e-9 || p[1] > Math.max(a[1], b[1]) + 1e-9) continue;
        var x = b[1] > a[1] ? a[0] + ((b[0] - a[0]) * (p[1] - a[1])) / (b[1] - a[1]) : a[0];
        if (Math.abs(x - p[0]) <= ON_LINE_M) return i;
      }
      return -1;
    }
    var onAft = {}, onFore = {};
    mid.forEach(function (s) {
      if (s.cut) return;
      var j = segmentOn(aft.pts, s.low);
      if (j >= 0) {
        s.on = "aft";
        (onAft[j] = onAft[j] || []).push(s);
        return;
      }
      j = segmentOn(fore.pts, s.low);
      if (j >= 0) {
        s.on = "fore";
        (onFore[j] = onFore[j] || []).push(s);
      }
    });
    var L = [];
    function place(s) {
      if (L.length && samePoint(L[L.length - 1], s.low)) s.pos = L.length - 1;
      else {
        s.pos = L.length;
        L.push(s.low);
      }
    }
    function pushLine(p) {
      if (!L.length || !samePoint(L[L.length - 1], p)) L.push(p);
    }
    // down the stern's line, the stations over the counter in their places on it
    for (var k = aft.pts.length - 1; k >= 0; k--) {
      pushLine(aft.pts[k]);
      if (k > 0) {
        (onAft[k - 1] || [])
          .sort(function (p, q) {
            return q.low[1] - p.low[1];
          })
          .forEach(place);
      }
    }
    var bottomFrom = L.length - 1;
    mid.forEach(function (s) {
      if (!s.on) place(s);
    });
    var bottomTo = L.length;
    // up the stem's line, the stations along the bow in their places on it
    for (k = 0; k < fore.pts.length; k++) {
      pushLine(fore.pts[k]);
      (onFore[k] || [])
        .sort(function (p, q) {
          return p.low[1] - q.low[1];
        })
        .forEach(place);
    }
    aft.pos = 0;
    fore.pos = L.length - 1;

    var tops = S.map(function (s) {
      return [s.top[0], s.top[1]];
    });
    function topAt(x) {
      return lineAt(tops, x);
    }
    function lowAt(x) {
      var best = Infinity;
      for (var i = 1; i < L.length; i++) {
        var p = L[i - 1], q = L[i];
        if ((p[0] - x) * (q[0] - x) > 0) continue;
        var z = q[0] === p[0] ? Math.min(p[1], q[1]) : p[1] + ((q[1] - p[1]) * (x - p[0])) / (q[0] - p[0]);
        best = Math.min(best, z);
      }
      return best;
    }
    function hbAt(x, z) {
      if (z > topAt(x) + 1e-6 || z < lowAt(x) - 1e-6) return 0;
      // the side at height z, aft to forward: the stern's line, each station that stands there
      // (held at its top where the top of the side rises between it and the next), the stem's
      var line = [];
      function add(s, closure) {
        if (z < s.low[1] - 1e-9 || (closure && z > s.top[1] + 1e-9)) return;
        var p = pointOn(s.pts, Math.min(z, s.top[1]));
        var px = closure ? p[0] : s.x;
        if (!line.length || px > line[line.length - 1][0] + 1e-9) line.push([px, p[2]]);
      }
      add(aft, true);
      mid.forEach(function (s) {
        add(s, false);
      });
      add(fore, true);
      if (!line.length || x < line[0][0] - 1e-9 || x > line[line.length - 1][0] + 1e-9) return 0;
      return lineAt(line, x);
    }
    return { stations: S, aft: aft, fore: fore, mid: mid, low: L, bottom: [bottomFrom, bottomTo], hbAt: hbAt, topAt: topAt, lowAt: lowAt };
  }

  var FORM_HULLS = typeof WeakMap === "function" ? new WeakMap() : null; // drawn once a graph
  var DRAWN_SIDES = typeof WeakMap === "function" ? new WeakMap() : null; // reckoned once a profile

  /** Her drawn side's half-breadth, (x, z) => metres, on a hull drawn from its profile. */
  function drawnSideAt(hull) {
    var profile = drawnProfile(hull);
    var kept = DRAWN_SIDES && DRAWN_SIDES.get(profile);
    if (kept) return kept;
    var hb;
    if (servedStations(hull)) {
      hb = formHull(hull).hbAt;
    } else {
      var H = profileHull(profile);
      hb = function (x, z) {
        return hbOnStation(H.station(x), z);
      };
    }
    if (DRAWN_SIDES) DRAWN_SIDES.set(profile, hb);
    return hb;
  }

  /**
   * The hull's figures on the served stations (B5.6, §6), in SHIP COORDINATES as `hullFigures`,
   * each marked `sea` (drawn below the water as UNDERWATER has it):
   * - `side` strips, one polygon a side between each two neighbouring stations, from the low
   *   line to the top of the side, each sorted at its middle; on each, a hair nearer (its middle,
   *   later), the main `wale`, the channel wale (`wale`, class `channel`) and the `band` of
   *   each deck's ports, each seen only from outboard (`outward`, so not on the far bulwark's
   *   inside seen over the near side); and the `outline` along its top and its stretch of the low
   *   line;
   * - `bottom` strips across the low line where it runs along the bottom;
   * - `deck` strips, each deck at DECK_SHARE of the drawn side's half-breadth at its height, each
   *   seen only from above;
   * - a `bulkhead` across the ship where a deck ends with another running on under it
   *   (`deckEndFigures`);
   * - the stern by `form.stern.type`: square or raked, the `transom` from its knuckle at its
   *   edges, its foot rounded up by `round_up_m` to the middle line, up the stern's line to the
   *   taffrail at `transom_hb_m`; round, none, the strips closing to the middle line;
   * - each band of `lights_m`, n plain dark marks (`light`) spread within its half-breadth across
   *   the transom or the drawn face of a round stern; no opening (the ports are package 81's);
   * - each tier of `galleries_m`, a plain box (`gallery`) on each quarter at its extent and
   *   heights, standing GALLERY_OUT_M out from the side;
   * - `head`: the knee between `head_m` and the stem, HEAD_SIDING_M each side of the middle line,
   *   from the drawn depth to the head's top and back to the stem head, with a plain shape (class
   *   `figure`, `scroll` or `billet`) at its top as `form.head` says;
   * - the `bulkhead` across the bow under the head rule, where the rail ends abaft the stem head.
   */
  function formHullFigures(hull) {
    var served = servedStations(hull);
    var kept = FORM_HULLS && FORM_HULLS.get(served);
    if (kept) return kept;
    var profile = drawnProfile(hull);
    var H = formHull(hull);
    var S = H.stations, L = H.low;
    var figs = [];
    function at(p, sign) {
      return v(p[0], sign * p[2], p[1]);
    }
    function across(p) {
      return v(p[0], -p[1], p[2]);
    }
    function between(lo, hi, z) {
      return Math.min(Math.max(z, lo), hi);
    }

    // the decks first, the lowest first: at the same depth a higher deck is drawn over a lower
    // one, and the side over a deck
    var decks = profile.decks_m || {};
    Object.keys(decks)
      .map(function (word) {
        var pts = decks[word];
        var mean = 0;
        pts.forEach(function (p) {
          mean += p[1] / pts.length;
        });
        return { word: word, pts: pts, mean: mean };
      })
      .sort(function (p, q) {
        return p.mean - q.mean;
      })
      .forEach(function (d) {
        var d0 = d.pts[0][0], d1 = d.pts[d.pts.length - 1][0];
        var xs = d.pts.map(function (p) {
          return p[0];
        });
        H.mid.forEach(function (s) {
          if (s.x > d0 && s.x < d1) xs.push(s.x);
        });
        xs.sort(function (a, b) {
          return a - b;
        });
        function edge(x, sign) {
          var z = lineAt(d.pts, x);
          return v(x, sign * DECK_SHARE * H.hbAt(x, z), z);
        }
        for (var j = 0; j + 1 < xs.length; j++) {
          var xa = xs[j], xb = xs[j + 1];
          if (xb - xa < 1e-6) continue;
          var plank = [edge(xa, 1), edge(xb, 1), edge(xb, -1), edge(xa, -1)];
          figs.push({ kind: "hull", part: "deck", cls: "strip", deck: d.word, pts: plank, sortBias: DECK_BEHIND_M, outward: faceOut(plank, 0) });
        }
      });

    // the bottom along the low line where it runs from the stern's cut to the stem's
    for (var c = H.bottom[0]; c < H.bottom[1]; c++) {
      var ca = L[c], cb = L[c + 1];
      figs.push({ kind: "hull", part: "bottom", cls: "strip", pts: [at(ca, 1), at(cb, 1), at(cb, -1), at(ca, -1)] });
    }

    // the bands on the side: the main wale, the channel wale, and each deck's strake of ports
    // where they are cut in the side below the rail (not where the guns fire over it)
    var bands = [];
    [["wales_m", ""], ["channel_wales_m", "channel"]].forEach(function (w) {
      var line = profile[w[0]];
      if (!line || !line.length) return;
      bands.push({
        part: "wale",
        cls: w[1] ? "strip " + w[1] : "strip",
        x0: line[0][0],
        x1: line[line.length - 1][0],
        zl: function (x) {
          return lineAt(line, x, 1);
        },
        zu: function (x) {
          return lineAt(line, x, 2);
        },
      });
    });
    if (PORT_BANDS) {
      Object.keys(profile.ports_m || {}).forEach(function (word) {
        var ports = profile.ports_m[word];
        var size = (profile.port_size_m || {})[word];
        if (!ports || !ports.length || !size || !portsInSide(profile, ports, size)) return;
        bands.push({
          part: "band",
          cls: "strip",
          deck: word,
          x0: ports[0][0] - size[0] / 2,
          x1: ports[ports.length - 1][0] + size[0] / 2,
          zl: function (x) {
            return lineAt(ports, x, 1);
          },
          zu: function (x) {
            return lineAt(ports, x, 1) + size[1];
          },
        });
      });
    }
    /** A band over one strip, [xa, xb] cut to its extent and, beside a closure, to where the
     *  stern's or the stem's line stands at its heights; its edges on the drawn side, within
     *  the side's low edge and top. Null where nothing is left. */
    function bandOn(A, B, sign, b) {
      var xa = Math.max(A === H.aft ? -Infinity : A.x, b.x0);
      var xb = Math.min(B === H.fore ? Infinity : B.x, b.x1);
      if (A === H.aft) xa = Math.max(xa, pointOn(A.pts, b.zl(xa))[0], pointOn(A.pts, b.zu(xa))[0]);
      if (B === H.fore) xb = Math.min(xb, pointOn(B.pts, b.zl(xb))[0], pointOn(B.pts, b.zu(xb))[0]);
      if (xb - xa < 1e-6) return null;
      function edge(x, upper) {
        var z = between(H.lowAt(x), H.topAt(x), upper ? b.zu(x) : b.zl(x));
        return v(x, sign * H.hbAt(x, z), z);
      }
      var pts = [edge(xa, false), edge(xb, false), edge(xb, true), edge(xa, true)];
      return pts[3][2] - pts[0][2] > 1e-6 || pts[2][2] - pts[1][2] > 1e-6 ? pts : null;
    }

    // the side, strip by strip: up the after station, down the forward one, and back along the
    // low line between their places on it (the stern's or the stem's line beside a closure)
    var stripOf = { starboard: [], larboard: [] };
    for (var i = 0; i + 1 < S.length; i++) {
      var A = S[i], B = S[i + 1];
      if (A === H.aft && B === H.fore) continue;
      var ring = [];
      var k;
      if (A === H.aft) {
        for (k = B.pos; k >= 0; k--) ring.push(L[k]);
        for (k = B.pts.length - 1; k >= 1; k--) ring.push(B.pts[k]);
      } else {
        A.pts.forEach(function (p) {
          ring.push(p);
        });
        if (B === H.fore) for (k = L.length - 1; k > A.pos; k--) ring.push(L[k]);
        else {
          for (k = B.pts.length - 1; k >= 0; k--) ring.push(B.pts[k]);
          for (k = B.pos - 1; k > A.pos; k--) ring.push(L[k]);
        }
      }
      var lowPath = L.slice(A.pos, B.pos + 1);
      [1, -1].forEach(function (sign) {
        var side = sign > 0 ? "starboard" : "larboard";
        var pts = ring.map(function (p) {
          return at(p, sign);
        });
        var mid = centroid(pts);
        var strip = { kind: "hull", part: "side", side: side, cls: "strip", pts: pts, sortAt: mid };
        figs.push(strip);
        stripOf[side].push({ A: A, B: B, fig: strip });
        bands.forEach(function (b) {
          var p = bandOn(A, B, sign, b);
          if (p) figs.push({ kind: "hull", part: b.part, side: side, cls: b.cls, deck: b.deck, pts: p, sortAt: mid, outward: faceOut(p, sign) });
        });
        figs.push({ kind: "hull", part: "outline", side: side, pts: [at(A.top, sign), at(B.top, sign)], sortAt: mid });
        figs.push({
          kind: "hull",
          part: "outline",
          side: side,
          pts: lowPath.map(function (p) {
            return at(p, sign);
          }),
          sortAt: mid,
        });
      });
    }

    var stern = (profile.form || {}).stern || null;
    var face = stern && stern.type !== "round" && stern.transom_hb_m ? transomFigures(H.aft, stern) : null;
    if (face) figs.push.apply(figs, face.figs);
    if (stern) figs.push.apply(figs, lightFigures(H, stern, face, stripOf));
    if (stern) figs.push.apply(figs, galleryFigures(H, stern));
    figs.push.apply(figs, headFigures(H, profile));
    figs.push.apply(figs, deckEndFigures(profile, H.topAt, H.hbAt));

    // the head rule's face across the bow, from the rail's end to the stem head, so that the bow
    // is not hollow seen from ahead (B5.1's bulkhead)
    var railEnd = profile.rail_m[profile.rail_m.length - 1];
    if (H.fore.top[0] > railEnd[0] + 1e-6) {
      var cap = S.filter(function (s) {
        return s.top[0] >= railEnd[0] - 1e-9;
      }).map(function (s) {
        return at(s.top, 1);
      });
      if (cap.length > 1) figs.push({ kind: "hull", part: "bulkhead", pts: cap.concat(cap.slice().reverse().map(across)) });
    }
    figs.forEach(function (f) {
      f.sea = true;
    });
    if (FORM_HULLS) FORM_HULLS.set(served, figs);
    return figs;
  }

  /**
   * A square or raked stern's transom (B5.6): the face across the stern between the two sides'
   * edges on the stern's line, from its foot to the taffrail, in strips at the line's points
   * and at each band of lights' heights, each sorted at its middle. Its foot at its edges is the
   * knuckle (`knuckle_z_m`), where the served stern's line closes to the transom's half-breadth
   * (`transom_hb_m`'s second); from there it is rounded up `round_up_m` to the middle line, as a
   * beam rounds up (the 64's wing transom, 4 in higher at the middle line than at its ends, on
   * her body plan), an arch on the stern's line at its heights. Under the arch, the tuck, the
   * planking's end below the wing transom, is drawn as the side (class `tuck`), so that the
   * stern is not open there. Its top the taffrail across `transom_hb_m`'s first. The outline
   * along its foot and across its top. Returns {figs, strips (each {z0, z1, fig}), on (the edge
   * at a height)}, or null.
   */
  function transomFigures(aft, stern) {
    var pts = aft.pts;
    var first = -1;
    for (var i = 0; i < pts.length; i++) {
      if (pts[i][2] > 1e-9) {
        first = i;
        break;
      }
    }
    if (first < 0) return null;
    var edge = pts.slice(first); // the transom's edge, its foot up to the taffrail
    var zk = edge[0][1], top = edge[edge.length - 1][1];
    if (top - zk < 1e-6) return null;
    var rise = Math.min(Math.max(stern.round_up_m || 0, 0), top - zk);
    function on(z) {
      return pointOn(edge, z);
    }
    var lights = (stern.lights_m || []).map(function (b) {
      return [b[0], b[1]];
    });
    var inside = function (z) {
      return lights.some(function (b) {
        return z > b[0] + 1e-9 && z < b[1] - 1e-9;
      });
    };
    // the levels above the arch's crown: the lowest strip runs from the arch up to the first
    var crown = zk + rise;
    var zs = [zk, top];
    edge.forEach(function (p) {
      if (p[1] > crown && p[1] < top && !inside(p[1])) zs.push(p[1]);
    });
    lights.forEach(function (b) {
      b.forEach(function (z) {
        if (z > crown && z < top) zs.push(z);
      });
    });
    zs = zs
      .sort(function (a, b) {
        return a - b;
      })
      .filter(function (z, j, all) {
        return j === 0 || z - all[j - 1] > 1e-6;
      });
    var figs = [], strips = [];
    function corner(z, sign) {
      var p = on(z);
      return v(p[0], sign * p[2], z);
    }
    // the foot, an arch from the knuckle at the edges up to its crown at the middle line
    var half = on(zk)[2];
    var foot = [];
    for (var j = -ROUND_UP_SAMPLES; j <= ROUND_UP_SAMPLES; j++) {
      var t = j / ROUND_UP_SAMPLES;
      var z = zk + rise * (1 - t * t);
      foot.push(v(on(z)[0], half * t, z));
    }
    for (var e = 0; e + 1 < zs.length; e++) {
      var lower = e === 0 && rise > 1e-6 ? foot : [corner(zs[e], -1), corner(zs[e], 1)];
      var quad = lower.concat([corner(zs[e + 1], 1), corner(zs[e + 1], -1)]);
      var middle = centroid([corner(zs[e], -1), corner(zs[e], 1), corner(zs[e + 1], 1), corner(zs[e + 1], -1)]);
      var strip = { kind: "hull", part: "transom", cls: "strip", pts: quad, sortAt: middle };
      figs.push(strip);
      strips.push({ z0: zs[e], z1: zs[e + 1], fig: strip });
      // under the arch, the tuck, sorted with the strip above it
      if (e === 0 && rise > 1e-6) figs.push({ kind: "hull", part: "transom", cls: "strip tuck", pts: foot, sortAt: middle });
    }
    var low = strips[0].fig.sortAt, high = strips[strips.length - 1].fig.sortAt;
    figs.push({ kind: "hull", part: "outline", pts: foot, sortAt: low }); // the knuckle
    figs.push({ kind: "hull", part: "outline", pts: [corner(top, -1), corner(top, 1)], sortAt: high }); // the taffrail
    return { figs: figs, strips: strips, on: on };
  }

  /**
   * Each band of `lights_m` (B5.6; §5.0 principle 9): n plain dark marks across the stern's face
   * in n even bays within ±hb, each LIGHT_SHARE of its bay across, from the band's low z to its
   * high: on the transom (on its strip there, and sorted with it), cut to the transom's foot and
   * top, or on the drawn face of a round stern (the side at that half-breadth and height, sorted
   * with the side's strip there).
   */
  function lightFigures(H, stern, face, stripOf) {
    var figs = [];
    (stern.lights_m || []).forEach(function (band, b) {
      var zl = band[0], zh = band[1], n = Math.round(band[2]), hb = band[3];
      if (face) {
        // on the transom and nowhere above or below it: the razee's band, filed above her
        // taffrail (her short roundhouse not yet in her profile), is cut to it
        zl = Math.max(zl, face.strips[0].z0);
        zh = Math.min(zh, face.strips[face.strips.length - 1].z1);
      }
      if (!(n >= 1) || !(hb > 0) || !(zh > zl + 1e-6)) return;
      var bay = (2 * hb) / n;
      var host = null;
      if (face) {
        var zm = 0.5 * (zl + zh);
        face.strips.forEach(function (s) {
          if (zm >= s.z0 - 1e-9 && zm <= s.z1 + 1e-9 && !host) host = s.fig;
        });
        if (!host) host = face.strips[zm < face.strips[0].z0 ? 0 : face.strips.length - 1].fig;
      }
      var xl = face ? face.on(zl)[0] : 0, xh = face ? face.on(zh)[0] : 0;
      for (var i = 0; i < n; i++) {
        var yc = -hb + bay * (i + 0.5);
        var y0 = yc - (LIGHT_SHARE * bay) / 2, y1 = yc + (LIGHT_SHARE * bay) / 2;
        // each seen only from abaft its face (`outward`): aft and down the transom's rake, or
        // out round a round stern
        var mark = { kind: "hull", part: "light", band: b };
        if (face) {
          mark.pts = [v(xl, y0, zl), v(xl, y1, zl), v(xh, y1, zh), v(xh, y0, zh)];
          mark.sortAt = host.sortAt;
          mark.outward = v(-1, 0, (xh - xl) / (zh - zl));
        } else {
          mark.pts = [roundFace(H, y0, zl), roundFace(H, y1, zl), roundFace(H, y1, zh), roundFace(H, y0, zh)];
          if (mark.pts.indexOf(null) >= 0) continue;
          mark.sortAt = roundHost(stripOf, yc, centroid(mark.pts));
          mark.outward = v(-1, yc / hb, 0);
        }
        figs.push(mark);
      }
    });
    return figs;
  }

  /** On a round stern, the drawn side's point at half-breadth |y| and height z, nearest the
   *  stern: where the side, straight at that height from the stern's line forward station by
   *  station, first reaches |y|; null where it never does. */
  function roundFace(H, y, z) {
    var want = Math.abs(y);
    var prev = null;
    var line = [H.aft].concat(H.mid);
    for (var i = 0; i < line.length; i++) {
      var s = line[i];
      if (z < s.low[1] - 1e-9 || z > s.top[1] + 1e-9) continue;
      var p = pointOn(s.pts, z);
      var here = [s.x === null ? p[0] : s.x, p[2]];
      if (prev && here[1] >= want && prev[1] <= want) {
        var t = here[1] > prev[1] ? (want - prev[1]) / (here[1] - prev[1]) : 0;
        return v(prev[0] + (here[0] - prev[0]) * t, y, z);
      }
      if (!prev && here[1] >= want) return v(here[0], y, z);
      prev = here;
    }
    return null;
  }

  /** The side strip a mark on a round stern lies on (its side by y, its strip by x), whose sort
   *  point it takes; its own middle where there is none. */
  function roundHost(stripOf, y, mid) {
    var list = stripOf[y >= 0 ? "starboard" : "larboard"];
    for (var i = 0; i < list.length; i++) {
      var A = list[i].A, B = list[i].B;
      var x0 = A.x === null ? -Infinity : A.x, x1 = B.x === null ? Infinity : B.x;
      if (mid[0] >= x0 && mid[0] <= x1) return list[i].fig.sortAt;
    }
    return mid;
  }

  /**
   * Each tier of `galleries_m` (B5.6; §5.0 principle 9): a plain box on each quarter at its
   * extent [x_aft, x_fore] and heights [z_low, z_high], its inner edges on the drawn side, its
   * outer face GALLERY_OUT_M beyond the side's widest there; five faces a side, each sorted at
   * its own middle. No opening. A gallery hangs on the side: a tier is cut to the top of the side
   * over its extent and to the stern's line at its heights (the razee's, filed above and abaft
   * her taffrail, her short roundhouse not yet in her profile).
   */
  function galleryFigures(H, stern) {
    var figs = [];
    /** The side's half-breadth at x, at z or at the top of the side where z stands above it; the
     *  stern's line's at z abaft it. */
    function inner(x, z) {
      var hb = H.hbAt(x, Math.min(Math.max(z, H.lowAt(x)), H.topAt(x)));
      return hb > 0 ? hb : pointOn(H.aft.pts, z)[2];
    }
    (stern.galleries_m || []).forEach(function (tier, t) {
      var x0 = tier[0], x1 = tier[1], zl = tier[2], zh = tier[3];
      var tops = [x0, x1];
      H.mid.forEach(function (s) {
        if (s.x > x0 && s.x < x1) tops.push(s.x);
      });
      zh = Math.min.apply(null, [zh].concat(tops.map(H.topAt)));
      x0 = Math.max(x0, pointOn(H.aft.pts, zl)[0], pointOn(H.aft.pts, zh)[0]);
      if (!(x1 - x0 > 1e-6) || !(zh - zl > 1e-6)) return;
      var yi = { al: inner(x0, zl), ah: inner(x0, zh), fl: inner(x1, zl), fh: inner(x1, zh) };
      var out = Math.max(yi.al, yi.ah, yi.fl, yi.fh, inner(0.5 * (x0 + x1), 0.5 * (zl + zh))) + GALLERY_OUT_M;
      [1, -1].forEach(function (sign) {
        var side = sign > 0 ? "starboard" : "larboard";
        var faces = [
          [v(x0, out, zl), v(x1, out, zl), v(x1, out, zh), v(x0, out, zh)], // outboard
          [v(x0, yi.al, zl), v(x0, out, zl), v(x0, out, zh), v(x0, yi.ah, zh)], // aft
          [v(x1, yi.fl, zl), v(x1, out, zl), v(x1, out, zh), v(x1, yi.fh, zh)], // forward
          [v(x0, yi.ah, zh), v(x1, yi.fh, zh), v(x1, out, zh), v(x0, out, zh)], // its top
          [v(x0, yi.al, zl), v(x1, yi.fl, zl), v(x1, out, zl), v(x0, out, zl)], // its foot
        ];
        faces.forEach(function (f) {
          var pts = f.map(function (p) {
            return v(p[0], sign * p[1], p[2]);
          });
          figs.push({ kind: "hull", part: "gallery", side: side, tier: t, pts: pts, sortAt: centroid(pts) });
        });
      });
    });
    return figs;
  }

  /**
   * The head (B5.6): the knee of the head between its fore edge (`head_m`) and the stem
   * (`stem_m`), from the drawn depth there (or where the knee leaves the stem, if higher) up the
   * knee to its top, straight back to the stem head and down the stem, a block HEAD_SIDING_M each
   * side of the middle line: its two sides, each seen only from its own side, and its fore edge
   * in strips (class `strip`) up the knee, and along its top back to the stem head where nothing
   * stands on it. At its top, its front on the knee, a plain shape for what `form.head` stands
   * there (FIGURE_SHARE): an upright oval for a figure, as broad across the ship as it is deep,
   * a round for a scroll and a block for a billet, each as broad as the knee; each drawn as its
   * two sides and its face across the ship at its middle, and the knee's fore edge stopping at
   * its foot. Seen ahead or astern, the head is a strip with the shape at its top.
   */
  function headFigures(H, profile) {
    var knee = profile.head_m, stem = profile.stem_m;
    if (!knee || knee.length < 2 || !stem || stem.length < 2) return [];
    var floor = Math.max(-H.fore.depth, knee[0][1]);
    /** A line of [x, z] points, z rising, from `floor` up. */
    function cutLine(line) {
      var out = [[xAtHeight(line, floor), floor]];
      line.forEach(function (p) {
        if (p[1] > floor + 1e-9) out.push(p);
      });
      return out;
    }
    var front = cutLine(knee), back = cutLine(stem);
    if (front.length < 2 || back.length < 1) return [];
    var figs = [];
    /** A shape of [x, z] points (along the ship) or [y, z] (across it at x) as figures: its two
     *  sides at ±half, each seen from its own side, or its face across the ship. */
    function sides(outline, half, cls) {
      [1, -1].forEach(function (sign) {
        var pts = outline.map(function (p) {
          return v(p[0], sign * half, p[1]);
        });
        var f = { kind: "hull", part: "head", side: sign > 0 ? "starboard" : "larboard", pts: pts, sortAt: centroid(pts), outward: v(0, sign, 0) };
        if (cls) f.cls = cls;
        figs.push(f);
      });
    }
    sides(front.concat(back.slice().reverse()), HEAD_SIDING_M, null);
    var word = (profile.form || {}).head;
    var topZ = knee[knee.length - 1][1];
    var tall = FIGURE_SHARE * topZ;
    var shaped = tall > 0 && (word === "figure" || word === "scroll" || word === "billet");
    var foot = topZ; // where the knee's fore edge stops: under the shape, or at its top
    if (shaped) {
      var w = word === "figure" ? tall / 2 : word === "scroll" ? tall / 3 : tall / 4;
      var h = word === "figure" ? tall : word === "scroll" ? tall / 3 : tall / 2;
      var half = word === "figure" ? w / 2 : HEAD_SIDING_M;
      var zc = topZ - h / 2;
      var xc = xAtHeight(knee, zc) - w / 2;
      foot = topZ - h;
      var along = [], across = [];
      if (word === "billet") {
        along = [[xc - w / 2, foot], [xc + w / 2, foot], [xc + w / 2, topZ], [xc - w / 2, topZ]];
        across = [[-half, foot], [half, foot], [half, topZ], [-half, topZ]];
      } else {
        for (var j = 0; j < 16; j++) {
          var a = (2 * Math.PI * j) / 16;
          along.push([xc + (w / 2) * Math.cos(a), zc + (h / 2) * Math.sin(a)]);
          across.push([half * Math.cos(a), zc + (h / 2) * Math.sin(a)]);
        }
      }
      sides(along, half, word);
      var face = across.map(function (p) {
        return v(xc, p[0], p[1]);
      });
      figs.push({ kind: "hull", part: "head", cls: word, pts: face, sortAt: centroid(face) });
    }
    // the knee's fore edge, across the ship, up to the shape's foot or along the top to the stem
    // head
    var edge = front.filter(function (p) {
      return p[1] <= foot + 1e-9;
    });
    if (shaped && edge[edge.length - 1][1] < foot - 1e-9) edge.push([xAtHeight(knee, foot), foot]);
    if (!shaped) edge.push(back[back.length - 1]);
    for (var k = 0; k + 1 < edge.length; k++) {
      var p = edge[k], q = edge[k + 1];
      var strip = [v(p[0], -HEAD_SIDING_M, p[1]), v(q[0], -HEAD_SIDING_M, q[1]), v(q[0], HEAD_SIDING_M, q[1]), v(p[0], HEAD_SIDING_M, p[1])];
      figs.push({ kind: "hull", part: "head", cls: "strip", pts: strip, sortAt: centroid(strip) });
    }
    return figs;
  }

  // -- projection --------------------------------------------------------------------

  /** Heel a point about the waterline (the x axis), positive to starboard. */
  function heelPoint(p, heel) {
    var c = Math.cos(heel), s = Math.sin(heel);
    return [p[0], p[1] * c + p[2] * s, -p[1] * s + p[2] * c];
  }

  /** Orthographic projection for a viewer at bearing `facing` from the ship. */
  function makeProjector(facing, heel) {
    var d = [-Math.cos(facing), -Math.sin(facing), 0]; // viewer -> ship
    var right = [Math.sin(facing), -Math.cos(facing), 0]; // up x d
    return function (p) {
      var q = heelPoint(p, heel || 0);
      return { x: dot(q, right), y: -q[2], depth: dot(q, d) };
    };
  }

  function projectPath(path, proj) {
    return path.map(function (seg) {
      return seg.map(proj);
    });
  }

  function meanDepth(points) {
    var s = 0;
    points.forEach(function (p) {
      s += p.depth;
    });
    return points.length ? s / points.length : 0;
  }

  /** A projected polygon cut at the sea line (screen y = 0): the part above it (`below` false)
   *  or under it (true), as one polygon of three points or more; null where none is left. */
  function clipAtSea(pts, below) {
    function keep(p) {
      return below ? p.y >= 0 : p.y <= 0;
    }
    function cross(p, q) {
      var t = p.y / (p.y - q.y);
      return { x: p.x + (q.x - p.x) * t, y: 0, depth: p.depth + (q.depth - p.depth) * t };
    }
    var out = [];
    for (var i = 0; i < pts.length; i++) {
      var p = pts[i], q = pts[(i + 1) % pts.length];
      if (keep(p)) out.push(p);
      if (keep(p) !== keep(q) && p.y !== q.y) out.push(cross(p, q));
    }
    return out.length >= 3 ? out : null;
  }

  /** A projected line cut at the sea line: its runs above it (`below` false) or under it. */
  function runsAtSea(pts, below) {
    function keep(p) {
      return below ? p.y >= 0 : p.y <= 0;
    }
    var runs = [], run = [];
    for (var i = 0; i < pts.length; i++) {
      var p = pts[i], q = pts[i + 1];
      if (keep(p)) run.push(p);
      if (q && keep(p) !== keep(q) && p.y !== q.y) {
        var t = p.y / (p.y - q.y);
        var c = { x: p.x + (q.x - p.x) * t, y: 0, depth: p.depth + (q.depth - p.depth) * t };
        run.push(c);
        if (!keep(q)) {
          if (run.length > 1) runs.push(run);
          run = [];
        }
      }
    }
    if (run.length > 1) runs.push(run);
    return runs;
  }

  /** A hull figure as the sea leaves it (B5.6, UNDERWATER): above the sea line as drawn; under
   *  it, nothing ("hidden"), or the part there marked `under` ("faint"). Each piece keeps the
   *  figure's depth, so that the painter's order does not change. */
  function atSea(g, way) {
    var under = false, over = false;
    g.pts.forEach(function (p) {
      if (p.y > 0) under = true;
      if (p.y < 0) over = true;
    });
    if (!under) return [g];
    var line = g.part === "outline";
    var pieces = [];
    function piece(pts, below) {
      var h = {};
      Object.keys(g).forEach(function (key) {
        h[key] = g[key];
      });
      h.pts = pts;
      if (below) h.under = true;
      pieces.push(h);
    }
    [false, true].forEach(function (below) {
      if (below && way !== "faint") return;
      if (!below && !over) return;
      if (line) {
        runsAtSea(g.pts, below).forEach(function (run) {
          piece(run, below);
        });
      } else {
        var pts = clipAtSea(g.pts, below);
        if (pts) piece(pts, below);
      }
    });
    return pieces;
  }

  /**
   * Project a skeleton. Returns {figures, bounds} where each figure has 2D
   * points (screen x right, y down, sea line at y = 0) and a depth; figures
   * are sorted far to near. `options.underwater` names how a hull drawn from her
   * profile is drawn below the water: "hidden", "faint" or "solid" (UNDERWATER by
   * default; package 75, B5.6). The bounds hold the whole drawn hull whichever it is.
   */
  function project(skeleton, facing, heel, options) {
    var proj = makeProjector(facing, heel);
    var way = (options && options.underwater) || UNDERWATER;
    if (!UNDERWATER_WAYS[way]) throw new Error("the hull below the water is drawn hidden, faint or solid, not '" + way + "'");
    var toViewer = [Math.cos(facing), Math.sin(facing), 0];
    var out = [];
    var minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    function note(p) {
      if (p.x < minX) minX = p.x;
      if (p.x > maxX) maxX = p.x;
      if (p.y < minY) minY = p.y;
      if (p.y > maxY) maxY = p.y;
    }
    skeleton.figures.forEach(function (f) {
      var g = { kind: f.kind, id: f.id, cls: f.cls, state: f.state, side: f.side, part: f.part, of: f.of, busy: f.busy, backed: f.backed, reefs: f.reefs, piece: f.piece, hoist: f.hoist, brace: f.brace };
      var all = [];
      if (f.path) {
        g.path = projectPath(f.path, proj);
        g.path.forEach(function (seg) {
          seg.forEach(function (p) {
            all.push(p);
          });
        });
      } else {
        g.pts = f.pts.map(proj);
        all = g.pts;
      }
      all.forEach(note);
      // package 75 (B5.6): a figure on one face of the hull (a stern light, a wale or a band on
      // the outside of the side, a deck's top, a side of the head) is seen only from that face's
      // side, and not edge on (within rounding: dead astern, sin(pi) leaves a hair)
      if (f.outward && dot(norm(heelPoint(f.outward, heel || 0)), toViewer) <= 1e-9) return;
      // a sail stands where its centre is along the view axis (spec M0-M2 §12 item 9),
      // not where the mean of its outline's control points happens to fall
      // package 57: a sail or a yard by its point against its mast (`sortAt`)
      var at = f.sortAt || (f.kind === "sail" ? f.centre : null);
      g.depth = at ? proj(at).depth : meanDepth(all);
      // package 75: a figure inside another (a deck within the side) sorts this much farther
      if (f.sortBias) g.depth += f.sortBias;
      // package 75 (B5.6): a hull drawn from her profile, below the water as `way` has it
      if (f.sea && g.pts && way !== "solid") out.push.apply(out, atSea(g, way));
      else out.push(g);
    });
    // The fixed scale (spec M3 §9 item 14): the frame of the full rig, every spar as the
    // ship file has it aloft and swung as far as it swings, so that spars sent down leave
    // the sky they filled and bracing round does not rescale the view.
    (skeleton.frame || []).forEach(function (p) {
      note(proj(p));
    });
    return { figures: sortFigures(out), bounds: { minX: minX, maxX: maxX, minY: minY, maxY: maxY } };
  }

  /** Painter's order, far first (spec M0-M2 §12 item 9). Depths within DEPTH_TIE of each
   *  other are a tie: then hull before rig, lines, sails before their spars, and among
   *  sails by class (SAIL_CLASS_RANK). The sort is stable, so the ship file's order
   *  settles what is left. */
  var DEPTH_TIE = 1e-3; // metres
  var KIND_RANK = { hull: 0, line: 1, sail: 2, spar: 3 };
  function sortFigures(figs) {
    return figs
      .map(function (f, i) {
        return { f: f, i: i };
      })
      .sort(function (p, q) {
        var a = p.f, b = q.f;
        if (Math.abs(a.depth - b.depth) > DEPTH_TIE) return b.depth - a.depth;
        var k = (KIND_RANK[a.kind] || 0) - (KIND_RANK[b.kind] || 0);
        if (k) return k;
        if (a.kind === "sail") {
          var c = (SAIL_CLASS_RANK[a.cls] || 0) - (SAIL_CLASS_RANK[b.cls] || 0);
          if (c) return c;
        }
        return p.i - q.i;
      })
      .map(function (e) {
        return e.f;
      });
  }

  /** SVG path data from a projected path ([[P], [C, P], ...]). */
  function pathData(path, closed) {
    var d = "";
    path.forEach(function (seg, i) {
      if (i === 0) d += "M" + seg[0].x.toFixed(2) + " " + seg[0].y.toFixed(2);
      else if (seg.length === 2) d += " Q" + seg[0].x.toFixed(2) + " " + seg[0].y.toFixed(2) + " " + seg[1].x.toFixed(2) + " " + seg[1].y.toFixed(2);
      else d += " L" + seg[0].x.toFixed(2) + " " + seg[0].y.toFixed(2);
    });
    return closed ? d + " Z" : d;
  }

  /** The facing for the viewer abeam to leeward: the milestone 2 default. */
  function leewardFacing(tack) {
    return tack === "larboard" ? Math.PI / 2 : (3 * Math.PI) / 2;
  }

  return {
    buildSkeleton: buildSkeleton,
    project: project,
    pathData: pathData,
    leewardFacing: leewardFacing,
    heelPoint: heelPoint,
    makeProjector: makeProjector,
    sheetDirection: sheetDirection,
    windVector: windVector,
    hullFigures: hullFigures,
    profileHull: profileHull,
    profileHullFigures: profileHullFigures,
    formHull: formHull,
    formHullFigures: formHullFigures,
    gooseWingCorners: gooseWingCorners,
    gooseWingOf: gooseWingOf,
    gooseWingTriangle: gooseWingTriangle,
    flattenPath: flattenPath,
    splitAtX: splitAtX,
    sortFigures: sortFigures,
    constants: {
      GAFF_PEAK_ANGLE: GAFF_PEAK_ANGLE,
      LOOSE_FOOT_HEIGHT_M: LOOSE_FOOT_HEIGHT_M,
      JIB_LUFF_FRACTION: JIB_LUFF_FRACTION,
      BELLY: BELLY,
      CLEW_SPREAD: CLEW_SPREAD,
      HEAD_SPREAD: HEAD_SPREAD,
      YARD_ON_CAP_M: YARD_ON_CAP_M,
      HOUSED_ABOVE_CAP_M: HOUSED_ABOVE_CAP_M,
      YARD_BEFORE_MAST_OF_BEAM: YARD_BEFORE_MAST_OF_BEAM,
      LUG_LEE_OF_MAST_OF_BEAM: LUG_LEE_OF_MAST_OF_BEAM,
      ON_DECK_M: ON_DECK_M,
      CUT_Z_M: CUT_Z_M,
      CUT_SHARE: CUT_SHARE,
      DECK_SHARE: DECK_SHARE,
      UNDERWATER_HEEL_DEG: UNDERWATER_HEEL_DEG,
      UNDERWATER: UNDERWATER,
      GALLERY_OUT_M: GALLERY_OUT_M,
      LIGHT_SHARE: LIGHT_SHARE,
      FIGURE_SHARE: FIGURE_SHARE,
      HEAD_SIDING_M: HEAD_SIDING_M,
      DECK_END_CLEAR_M: DECK_END_CLEAR_M,
    },
  };
});
