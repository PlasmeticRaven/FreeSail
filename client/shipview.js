/* shipview.js: draw a projected scene (projection.js) as SVG.
 *
 * Everything here is a figure from the skeleton: hull faces, spars weighted
 * by class, sails filled by state, braces and sheets as faint lines that
 * brighten while their evolution runs. Colours and stroke weights live in
 * style.css under the classes set here, so the palette is one place. */
(function (root) {
  "use strict";
  var NS = "http://www.w3.org/2000/svg";

  function el(name, attrs, parent) {
    var e = document.createElementNS(NS, name);
    Object.keys(attrs || {}).forEach(function (k) {
      e.setAttribute(k, attrs[k]);
    });
    if (parent) parent.appendChild(e);
    return e;
  }

  function polygonPoints(pts) {
    return pts
      .map(function (p) {
        return p.x.toFixed(2) + "," + p.y.toFixed(2);
      })
      .join(" ");
  }

  function title(node, text) {
    var t = el("title", {}, node);
    t.textContent = text;
  }

  /**
   * Render `scene` (from Projection.project) into the <svg> element.
   * `info` is {name, facingDeg, heelDeg, tack} for the caption.
   */
  function render(svg, scene, info) {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var b = scene.bounds;
    if (!isFinite(b.minX)) return;
    var width = Math.max(b.maxX - b.minX, 10);
    var height = Math.max(-b.minY, 10);
    var margin = 0.08 * Math.max(width, height);
    var seaDepth = Math.max(0.16 * height, 4);
    var x0 = b.minX - margin;
    var y0 = b.minY - margin;
    var w = width + 2 * margin;
    var h = height + margin + seaDepth;
    svg.setAttribute("viewBox", [x0, y0, w, h].map(function (n) { return n.toFixed(2); }).join(" "));
    svg.setAttribute("preserveAspectRatio", "xMidYMid meet");

    el("rect", { class: "sky", x: x0, y: y0, width: w, height: -y0 }, svg);
    el("rect", { class: "sea", x: x0, y: 0, width: w, height: h + y0 }, svg);

    var rig = el("g", { class: "rig" }, svg);
    scene.figures.forEach(function (f) {
      var node;
      if (f.kind === "hull") {
        node = el("polygon", { class: "hull " + f.part + (f.side ? " " + f.side : ""), points: polygonPoints(f.pts) }, rig);
        title(node, "hull " + f.part + (f.side ? " (" + f.side + " side)" : ""));
      } else if (f.kind === "spar") {
        var cls = "spar " + f.cls + " " + f.state + (f.busy ? " busy" : "");
        node = el("line", { class: cls, x1: f.pts[0].x.toFixed(2), y1: f.pts[0].y.toFixed(2), x2: f.pts[1].x.toFixed(2), y2: f.pts[1].y.toFixed(2) }, rig);
        title(node, f.id.replace(/\./g, " ") + " (" + f.cls.replace(/_/g, " ") + ", " + f.state.replace(/_/g, " ") + ")");
      } else if (f.kind === "sail") {
        var scls = "sail " + f.cls + " " + f.state + (f.backed ? " backed" : "") + (f.reefs ? " reefed" : "") + (f.busy ? " busy" : "");
        node = el("path", { class: scls, d: root.Projection.pathData(f.path, true) }, rig);
        var words = f.state.replace(/_/g, " ");
        if (f.reefs) words += ", " + f.reefs + (f.reefs > 1 ? " reefs" : " reef");
        if (f.backed) words += ", aback";
        title(node, f.id.replace(/\./g, " ") + " (" + words + ")");
      } else if (f.kind === "line") {
        var lcls = "line " + f.cls + " " + f.state + (f.busy ? " busy" : "");
        node = el("line", { class: lcls, x1: f.pts[0].x.toFixed(2), y1: f.pts[0].y.toFixed(2), x2: f.pts[1].x.toFixed(2), y2: f.pts[1].y.toFixed(2) }, rig);
        title(node, f.id.replace(/\./g, " ") + " (" + f.state + ")");
      }
    });

    el("line", { class: "sea-line", x1: x0, y1: 0, x2: x0 + w, y2: 0 }, svg);

    if (info) {
      var cap = el("text", { class: "caption", x: x0 + margin * 0.4, y: y0 + margin * 0.6 }, svg);
      cap.setAttribute("font-size", (0.035 * h).toFixed(2));
      cap.textContent = info.name + "  ·  viewed from " + info.facingWords + "  ·  heel " + info.heelWords;
    }
  }

  root.ShipView = { render: render };
})(window);
