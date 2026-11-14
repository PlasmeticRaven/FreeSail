/* token.js: the game's mark (package 115, part A; freesail/ui/guard.py). The server writes
 * its mark into each of its pages as they are served (<meta name="freesail-page">); this
 * sends it with every request the page makes of its own server, so that the server knows
 * its own page from any other page open in the browser. Loaded first, before the scripts
 * that fetch. The socket carries it in its address (app.js, `connect`). */
(function () {
  "use strict";
  var meta = document.querySelector('meta[name="freesail-page"]');
  window.freesailMark = meta ? meta.getAttribute("content") || "" : "";
  if (!window.fetch) return;
  var plain = window.fetch.bind(window);
  window.fetch = function (input, init) {
    var url = typeof input === "string" ? input : (input && input.url) || "";
    var own = new URL(url, location.href).origin === location.origin;
    if (!own || !window.freesailMark) return plain(input, init);
    init = init || {};
    var headers = new Headers(init.headers || (typeof input !== "string" && input.headers) || undefined);
    headers.set("X-FreeSail-Page", window.freesailMark);
    init.headers = headers;
    return plain(input, init);
  };
  // The mark of the server as it now runs, from the page's own address (a server started
  // again makes a new one); another site's page cannot read this answer.
  window.freesailFreshMark = function () {
    return plain("/", { cache: "no-store", credentials: "same-origin" })
      .then(function (r) {
        // from another device a server started again does not give its new mark to the
        // old one: the page must be opened again at the address the terminal printed
        window.freesailMarkLost = r.status === 403;
        return r.text();
      })
      .then(function (text) {
        var found = /name="freesail-page" content="([^"]+)"/.exec(text);
        if (found) window.freesailMark = found[1];
      });
  };
})();
