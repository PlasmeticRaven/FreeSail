/* log.js: the log panel. Severity-coloured lines, a filter, and the roll-up of
 * routine entries per bell while the clock runs above 10x, as the console does. */
(function (root) {
  "use strict";
  var ROLLUP_ABOVE = 10;
  var RANK = { routine: 0, notable: 1, urgent: 2 };

  function LogPanel(listEl) {
    this.list = listEl;
    this.filter = "routine";
    this.rolled = [];
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
    this.rolled = [];
    this.count = 0;
  };

  /** Add an event. `driver` is the driver state the roll-up depends on. */
  LogPanel.prototype.add = function (e, driver) {
    var rolling = driver && driver.running && driver.compression > ROLLUP_ABOVE;
    if (rolling && e.severity === "routine" && e.kind !== "clock.bell") {
      this.rolled.push(e);
      return;
    }
    if (e.kind === "clock.bell" && this.rolled.length) this.flushRollup();
    this.append(e);
  };

  LogPanel.prototype.flushRollup = function () {
    if (!this.rolled.length) return;
    var n = this.rolled.length;
    var details = document.createElement("details");
    details.className = "entry rollup routine";
    var summary = document.createElement("summary");
    summary.textContent = "(" + n + " routine " + (n === 1 ? "entry" : "entries") + ")";
    details.appendChild(summary);
    var inner = document.createElement("div");
    this.rolled.forEach(function (e) {
      inner.appendChild(lineFor(e));
    });
    details.appendChild(inner);
    this.rolled = [];
    this.list.appendChild(details);
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
    mark.textContent = e.severity === "urgent" ? "!" : e.severity === "notable" ? "*" : " ";
    var stamp = document.createElement("span");
    stamp.className = "stamp";
    stamp.textContent = e.stamp || root.Units.clockOf(e.ship_time);
    stamp.title = e.ship_time.replace("T", " ") + " (tick " + e.tick + ")";
    var text = document.createElement("span");
    text.className = "text";
    text.textContent = e.text;
    div.appendChild(mark);
    div.appendChild(stamp);
    div.appendChild(text);
    return div;
  }

  root.LogPanel = LogPanel;
})(window);
