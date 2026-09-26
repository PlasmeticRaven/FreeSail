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
 *   spar.x_m        root spars only; a child spar stands at its parent's x
 *   brace_angle     radians from square, positive = starboard yardarm forward
 *   sheet_angle     radians from the centreline, unsigned; the sail lies to lee
 *   heel            radians, positive = heeled to starboard
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
  var FURLED_ISH = { furled: 1 };
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
    if (tack === "larboard") return [yard.a, yard.b, yard.b, add(yard.a, down)];
    return [yard.a, yard.b, add(yard.b, down), yard.a];
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
    var snapSpars = indexBy(snapshot && snapshot.spars, "id");
    var snapSails = indexBy(snapshot && snapshot.sails, "id");
    var snapLines = indexBy(snapshot && snapshot.lines, "id");
    var tack = (snapshot && snapshot.ship && snapshot.ship.tack) || "starboard";
    var wind = windVector(snapshot && snapshot.wind ? snapshot.wind.apparent_angle : Math.PI);
    var busy = {};
    ((snapshot && snapshot.evolutions_in_progress) || []).forEach(function (e) {
      if (!e.waiting) busy[e.subject] = e.id;
    });

    var spars = {};
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
      };
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
    /** The sheet angle of the sail using this gaff or boom, if any. */
    function sheetAngleOf(sparId) {
      var list = sailsBySpar[sparId] || [];
      for (var i = 0; i < list.length; i++) {
        if (list[i].class === "gaff" || list[i].class === "sprit") return sailDyn(list[i]).sheet_angle;
      }
      return 0;
    }

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
        r.a = v(r.x, 0, deck);
        r.b = v(r.xAt(deck + H), 0, deck + H);
        r.head = r.b;
        r.foot = r.a;
      } else if (MAST_CLASSES[spec.class]) {
        // an upper mast continues the line of the one below
        r.rake = parent.rake || 0;
        r.xAt = parent.xAt || function () { return parent.x; };
        var footZ = parent.head[2];
        r.x = r.xAt(footZ);
        r.foot = v(r.x, 0, footZ);
        r.head = v(r.xAt(footZ + H), 0, footZ + H);
        r.a = v(r.xAt(footZ - DOUBLING * H), 0, footZ - DOUBLING * H); // the doubling: drawn, not a position
        r.b = r.head;
      } else if (spec.class === "bowsprit") {
        r.x = spec.x_m || 0;
        r.a = v(r.x, 0, deck);
        var dz = Math.min(H, L * 0.95);
        r.b = v(r.x + Math.sqrt(Math.max(L * L - dz * dz, 0)), 0, deck + dz);
        r.tip = r.b;
      } else if (HEAD_CLASSES[spec.class]) {
        var rootP = parent && parent.tip ? parent.tip : v(hull.length_waterline_m / 2, 0, deck);
        var tipZ = deck + H;
        var dz2 = Math.max(Math.min(tipZ - rootP[2], L * 0.7), 0);
        r.x = rootP[0];
        r.a = rootP;
        r.b = v(rootP[0] + Math.sqrt(Math.max(L * L - dz2 * dz2, 0)), 0, rootP[2] + dz2);
        r.tip = r.b;
      } else if (YARD_CLASSES[spec.class]) {
        var th = braceAngle(spec);
        r.x = parent ? (parent.xAt ? parent.xAt(deck + H) : parent.x) : spec.x_m || 0;
        r.centre = v(r.x, 0, deck + H);
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
        r.b = add(r.a, add(mul(gDir, L * Math.cos(GAFF_PEAK_ANGLE)), v(0, 0, L * Math.sin(GAFF_PEAK_ANGLE))));
        r.dir = gDir;
      } else if (spec.class === "boom") {
        r.x = parent ? (parent.xAt ? parent.xAt(deck + H) : parent.x) : spec.x_m || 0;
        var bDir = sheetDirection(sheetAngleOf(id), tack);
        r.a = v(r.x, 0, deck + H);
        r.b = add(r.a, mul(bDir, L));
        r.dir = bDir;
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
    graph.lines.forEach(function (ln) {
      if (ln.class !== "stay") return;
      var sp = spars[ln.of];
      if (!sp) return;
      var mast = lowerMastOf(sp);
      if (!mast || !MAST_CLASSES[mast.cls]) return; // bobstays and martingales: not sail stays
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
     *  dependents are. */
    function sentDown(r) {
      for (var cur = r; cur; cur = cur.parent) {
        if (cur.state === "sent_down") return true;
      }
      return false;
    }
    var lineOf = indexBy(graph.lines, "id");

    var figures = [];
    graph.spars.forEach(function (s) {
      var r = spars[s.id];
      if (sentDown(r)) return;
      figures.push({
        kind: "spar",
        id: s.id,
        cls: s.class,
        state: r.state,
        side: s.side,
        pts: [r.a, r.b],
        busy: !!busy[s.id],
      });
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
      if (!fig.stay || !fig.path) return [fig];
      var pts = flattenPath(fig.path);
      var minX = Infinity, maxX = -Infinity;
      pts.forEach(function (p) {
        minX = Math.min(minX, p[0]);
        maxX = Math.max(maxX, p[0]);
      });
      for (var i = 0; i < lowerMasts.length; i++) {
        var m = lowerMasts[i];
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

    graph.sails.forEach(function (spec) {
      var dyn = sailDyn(spec);
      var roles = spec.roles || {};
      var cls = spec.class;
      if (dyn.state === "unbent") return; // nothing on the yard: the sail is in the sail room
      var onDeck = Object.keys(roles).some(function (role) {
        var target = roles[role];
        var sp = spars[target] || (lineOf[target] ? spars[lineOf[target].of] : null);
        return sp ? sentDown(sp) : false;
      });
      if (onDeck) return; // sent down with its spar
      if (cls === "square" || cls === "lug" || cls === "lateen") {
        var Y = spars[roles.yard];
        if (!Y || !Y.arm) return;
        var L = Y.half * 2;
        var depth = (spec.area_m2 / Math.max(L, 1)) * reefFraction(spec, dyn);
        var down = v(0, 0, -depth);
        var corners = [Y.a, Y.b, add(Y.b, down), add(Y.a, down)];
        if (dyn.state === "goose_winged") {
          // the lee clew hauled up to the yard, the weather clew sheeted home: a triangle
          // from the weather clew to the yard, its foot rising to the lee yardarm (spec M3
          // §9 item 13; physics/sails.py: half the area, its centre out to weather)
          corners = gooseWingCorners(Y, down, tack);
          var gw = sailFigure(spec, dyn, corners, Y.normal, Y, depth);
          gw.path = gooseWingPath(corners, Y.normal, tack, depth);
          gw.centre = gooseWingCentre(corners, tack);
          figures.push(gw);
          return;
        }
        figures.push(sailFigure(spec, dyn, corners, Y.normal, Y, depth));
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
        if (Bm) {
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
        if (stay) {
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
    function yardBelow(Y) {
      var best = null;
      Object.keys(spars).forEach(function (id) {
        var s = spars[id];
        if (!s.arm || s === Y || s.cls === "studdingsail_boom") return;
        if (Math.abs(s.x - Y.x) > 0.5 || s.centre[2] >= Y.centre[2]) return;
        if (best === null || s.centre[2] > best.centre[2]) best = s;
      });
      return best;
    }

    graph.lines.forEach(function (ln) {
      var state = (snapLines[ln.id] || {}).state || ln.state || "belayed";
      if (ln.class === "brace") {
        var Y = spars[ln.of];
        if (!Y || !Y.arm || sentDown(Y)) return;
        var ss = sideSign(ln.side);
        var from = ss > 0 ? Y.b : Y.a;
        var m = mastAftOf(Y.x);
        var to = m ? v(m.x, ss * 0.3, Math.min(Y.centre[2], m.head[2] - 1)) : v(Y.x - Y.half * 0.8, (ss * beam) / 2, deck);
        if (state === "parted") to = add(from, v(-1.5, 0, -2.5));
        figures.push({ kind: "line", id: ln.id, cls: "brace", of: ln.of, state: state, pts: [from, to], busy: !!busy[ln.of] });
      } else if (ln.class === "sheet") {
        var sf = sailFigById[ln.of];
        if (!sf || sf.state === "furled" || !sf.corners) return;
        if (sf.state === "goose_winged" && ln.side === (tack === "starboard" ? "larboard" : "starboard")) return; // the lee clew is up
        var pts;
        if (sf.corners.length === 4 && (sf.cls === "square" || sf.cls === "lug" || sf.cls === "lateen")) {
          var s2 = sideSign(ln.side);
          var Yy = spars[((sailSpecs[ln.of] || {}).roles || {}).yard];
          var clew = s2 > 0 ? sf.corners[2] : sf.corners[3];
          var below = Yy ? yardBelow(Yy) : null;
          var lead = below ? (s2 > 0 ? below.b : below.a) : v(clew[0], (s2 * beam) / 2, deck);
          pts = [clew, lead];
        } else {
          var clew2 = sf.corners[2];
          var lee = sideSign(ln.side || (tack === "starboard" ? "larboard" : "starboard"));
          pts = [clew2, v(clew2[0] - 2, (lee * beam) / 2, deck)];
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

    // -- the hull --------------------------------------------------------------------

    figures.push.apply(figures, hullFigures(hull));

    return { figures: figures, hull: hull, spars: spars, stays: stayFoot, frame: fullRigFrame(graph, spars, hull) };
  }

  /** The full rig's reach, for the view's fixed scale (spec M3 §9 item 14): every spar in
   *  the ship file, aloft whatever its state now, with each swinging spar's reach about its
   *  pivot in all four horizontal directions, so that no brace or sheet angle and no spar
   *  sent down changes it; and the hull. */
  function fullRigFrame(graph, spars, hull) {
    var pts = [];
    var dirs = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]];
    graph.spars.forEach(function (s) {
      var r = spars[s.id];
      if (!r) return;
      var ends = r.full || [r.a, r.b];
      pts.push(ends[0], ends[1]);
      if (!SWINGING[s.class]) return;
      var pivot, reach;
      if (r.pivot) {
        pivot = r.pivot; // a studding sail boom: out beyond its yardarm, however braced
        reach = r.reach;
      } else if (r.centre) {
        pivot = r.centre; // a yard about its slings
        reach = r.half;
      } else {
        pivot = r.a; // a gaff, boom or sprit about its mast
        reach = len(sub(r.b, r.a));
      }
      dirs.forEach(function (d) {
        pts.push(add(pivot, mul(d, reach)));
      });
    });
    hullFigures(hull).forEach(function (f) {
      pts.push.apply(pts, f.pts);
    });
    return pts;
  }

  /** The hull as a lens-shaped deck with sheer and two side faces down to just
   *  below the waterline (the sea covers the rest). From length, beam,
   *  freeboard and a sheer that rises toward the bow. */
  function hullFigures(hull) {
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

  /**
   * Project a skeleton. Returns {figures, bounds} where each figure has 2D
   * points (screen x right, y down, sea line at y = 0) and a depth; figures
   * are sorted far to near.
   */
  function project(skeleton, facing, heel) {
    var proj = makeProjector(facing, heel);
    var out = [];
    var minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    function note(p) {
      if (p.x < minX) minX = p.x;
      if (p.x > maxX) maxX = p.x;
      if (p.y < minY) minY = p.y;
      if (p.y > maxY) maxY = p.y;
    }
    skeleton.figures.forEach(function (f) {
      var g = { kind: f.kind, id: f.id, cls: f.cls, state: f.state, side: f.side, part: f.part, of: f.of, busy: f.busy, backed: f.backed, reefs: f.reefs, piece: f.piece };
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
      // a sail stands where its centre is along the view axis (spec M0-M2 §12 item 9),
      // not where the mean of its outline's control points happens to fall
      g.depth = f.kind === "sail" && f.centre ? proj(f.centre).depth : meanDepth(all);
      out.push(g);
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
    gooseWingCorners: gooseWingCorners,
    gooseWingTriangle: gooseWingTriangle,
    flattenPath: flattenPath,
    splitAtX: splitAtX,
    sortFigures: sortFigures,
    constants: {
      GAFF_PEAK_ANGLE: GAFF_PEAK_ANGLE,
      LOOSE_FOOT_HEIGHT_M: LOOSE_FOOT_HEIGHT_M,
      JIB_LUFF_FRACTION: JIB_LUFF_FRACTION,
      BELLY: BELLY,
    },
  };
});
