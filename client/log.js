/* log.js: the log panel. Severity-coloured lines, a filter, and the roll-up.
 *
 * The roll-up (spec M4 §20) is the server's view, not the client's: at 60x and above the
 * server sends notable and urgent lines and the captain's own as events, and each hour's
 * routine lines as one roll-up (freesail/core/events.py RollupView, the same view the
 * console prints and a model's samples carry). A roll-up opens to show its lines, asked
 * of the store by their ticks (/api/log?since=&until=), so nothing is lost by it. */
(function (root) {
  "use strict";
  var RANK = { routine: 0, notable: 1, urgent: 2 };
  // The actors whose routine lines the roll-up keeps as they are (events.KEPT_ACTORS).
  var KEPT_ACTORS = { captain: 1, driver: 1 };

  function LogPanel(listEl) {
    this.list = listEl;
    this.filter = "routine";
    this.count = 0;
    this.maxLines = 2000;
  }

  LogPanel.prototype.setFilter = function (severity) {
    this.filter = severity;
    this.list.setAttribute("data-filter", severity);
    this.scrollToEnd();
  };

  LogPanel.prototype.clear = function () {
    this.list.innerHTML = "";
    this.count = 0;
  };

  /** Add a line the server sent: an event, or a roll-up (kind "log.rollup"). */
  LogPanel.prototype.add = function (e) {
    if (e.kind === "log.rollup") this.addRollup(e);
    else this.append(e);
  };

  /** An hour's routine lines in one line, which opens to show them. */
  LogPanel.prototype.addRollup = function (r) {
    var details = document.createElement("details");
    details.className = "entry rollup routine";
    details.setAttribute("data-rank", 0);
    details.setAttribute("data-tick", r.tick);
    var summary = document.createElement("summary");
    var mark = document.createElement("span");
    mark.className = "mark";
    mark.textContent = "=";
    var stamp = document.createElement("span");
    stamp.className = "stamp";
    stamp.textContent = r.stamp || "";
    var text = document.createElement("span");
    text.className = "text";
    text.textContent = r.text;
    summary.appendChild(mark);
    summary.appendChild(stamp);
    summary.appendChild(text);
    details.appendChild(summary);
    var inner = document.createElement("div");
    inner.className = "rollup-lines";
    details.appendChild(inner);
    var data = r.data || {};
    details.addEventListener("toggle", function () {
      if (!details.open || inner.getAttribute("data-loaded")) return;
      inner.setAttribute("data-loaded", "1");
      var url = "/api/log?since=" + (Number(data.first_tick) - 1) + "&until=" + Number(data.last_tick) + "&limit=5000";
      fetch(url)
        .then(function (res) {
          return res.json();
        })
        .then(function (events) {
          events.forEach(function (e) {
            if (e.severity === "routine" && !KEPT_ACTORS[e.actor]) inner.appendChild(lineFor(e));
          });
        })
        .catch(function () {
          inner.removeAttribute("data-loaded");
        });
    });
    this.list.appendChild(details);
    this.count += 1;
    this.trim();
    this.scrollToEnd();
  };

  LogPanel.prototype.append = function (e) {
    this.list.appendChild(lineFor(e));
    this.count += 1;
    this.trim();
    this.scrollToEnd();
  };

  LogPanel.prototype.trim = function () {
    while (this.list.childNodes.length > this.maxLines) this.list.removeChild(this.list.firstChild);
  };

  LogPanel.prototype.scrollToEnd = function () {
    var box = this.list.parentNode || this.list;
    box.scrollTop = box.scrollHeight;
  };

  function lineFor(e) {
    var div = document.createElement("div");
    div.className = "entry " + e.severity + " kind-" + e.kind.replace(/\./g, "-");
    div.setAttribute("data-rank", RANK[e.severity] || 0);
    div.setAttribute("data-tick", e.tick);
    var mark = document.createElement("span");
    mark.className = "mark";
    mark.textContent = e.severity === "urgent" ? "!" : e.severity === "notable" ? "*" : " ";
    var stamp = document.createElement("span");
    stamp.className = "stamp";
    stamp.textContent = e.stamp || root.Units.clockOf(e.ship_time);
    stamp.title = e.ship_time.replace("T", " ") + " (tick " + e.tick + ")";
    var text = document.createElement("span");
    text.className = "text";
    // an agent's line opens with its station's mark, "[watcher] ...", inline (spec M4
    // §12, owner's ruling); the mark gets its own span so a style can pick it out
    var who = e.kind && e.kind.indexOf("agent.") === 0 ? /^\[([^\]]+)\]\s*/.exec(e.text) : null;
    if (who) {
      var station = document.createElement("span");
      station.className = "station";
      station.textContent = "[" + who[1] + "]";
      text.appendChild(station);
      text.appendChild(document.createTextNode(" " + e.text.slice(who[0].length)));
    } else {
      text.textContent = e.text;
    }
    div.appendChild(mark);
    div.appendChild(stamp);
    div.appendChild(text);
    return div;
  }

  root.LogPanel = LogPanel;
})(window);
