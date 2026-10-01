/* library.js: the reference library and the ship's papers in a pane of their own
 * (package 33d; playtest 12, the owner's note 1: "the ability to read the docs and
 * whatever readable documents you have onboard ... pop-out window, probably, to avoid
 * cluttering the log").
 *
 * Every page is the model's `library` tool's own (/api/library, freesail/agents/tools.py):
 * the same text from the same Markdown, rendered here; nothing is shown the model cannot
 * ask for, and nothing it can ask for is left out. The index down the side is the topics
 * and sections the contents page names (/api/library/topics); a `library(topic=...)`
 * named in a page's words opens that page. `find` searches the whole library as the tool's
 * find= does. The ship's papers (/api/library/papers) are the answers of `the booms`, `the
 * sail room` and `the boatswain's store` at the order line, read without a line in the
 * log, and the papers that wait are named with what they wait for.
 *
 * The pane is the same in the main page (beside the log, in the ship view's place) and in
 * its own window (/client/library.html). Markdown.render is pure, for Node. */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else {
    root.LibraryPane = api.LibraryPane;
    root.Markdown = api.Markdown;
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // -- Markdown, the little the library's pages use ----------------------------------
  // Headings, paragraphs (a page's own line breaks kept: the grammar and the catalogue are
  // laid out by line), fenced code, lists, tables, quotes; inline code, bold, italics and
  // a link's words. Everything is escaped first; no HTML in a page reaches the document.

  function escape(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  // `library(topic='primer 3', section='reefing')` in a page's words, as a link
  var CALL = /library\(((?:\s*(?:topic|section|find)\s*=\s*'[^']*'\s*,?)*)\)/g;

  function callArgs(inner) {
    var out = { topic: "", section: "", find: "" };
    inner.replace(/(topic|section|find)\s*=\s*'([^']*)'/g, function (_, k, v) {
      out[k] = v;
      return "";
    });
    return out;
  }

  function inline(text) {
    // code spans first, kept whole; then emphasis and links in what is left
    var parts = String(text).split(/(`[^`]*`)/);
    return parts
      .map(function (p) {
        if (p.length > 1 && p.charAt(0) === "`" && p.charAt(p.length - 1) === "`") {
          return "<code>" + linkCalls(escape(p.slice(1, -1))) + "</code>";
        }
        var s = escape(p);
        s = s.replace(/\[([^\]]+)\]\([^)]*\)/g, "$1");
        s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
        s = s.replace(/(^|[^*\w])\*([^*\s][^*]*?)\*(?![*\w])/g, "$1<em>$2</em>");
        s = s.replace(/(^|[^_\w])_([^_\s][^_]*?)_(?![_\w])/g, "$1<em>$2</em>");
        return linkCalls(s);
      })
      .join("");
  }

  function linkCalls(escaped) {
    // the call's quotes were escaped as themselves (only " is), so the pattern still reads
    return escaped.replace(CALL, function (whole, inner) {
      var a = callArgs(inner);
      return (
        '<a href="#" class="library-call" data-topic="' + escape(a.topic) + '" data-section="' + escape(a.section) +
        '" data-find="' + escape(a.find) + '">' + whole + "</a>"
      );
    });
  }

  function isTableRule(line) {
    return /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/.test(line);
  }

  function cells(line) {
    var s = line.trim();
    if (s.charAt(0) === "|") s = s.slice(1);
    if (s.charAt(s.length - 1) === "|") s = s.slice(0, -1);
    return s.split("|").map(function (c) {
      return c.trim();
    });
  }

  function render(md) {
    var lines = String(md || "").replace(/\r\n?/g, "\n").split("\n");
    var out = [];
    var para = [];
    var i = 0;

    function flush() {
      if (para.length) out.push("<p>" + para.map(inline).join("\n") + "</p>");
      para = [];
    }

    while (i < lines.length) {
      var line = lines[i];
      var m;
      if (/^\s*```/.test(line)) {
        flush();
        var code = [];
        i += 1;
        while (i < lines.length && !/^\s*```/.test(lines[i])) {
          code.push(lines[i]);
          i += 1;
        }
        i += 1;
        out.push("<pre><code>" + escape(code.join("\n")) + "</code></pre>");
        continue;
      }
      if (!line.trim()) {
        flush();
        i += 1;
        continue;
      }
      if ((m = /^(#{1,6})\s+(.*?)\s*#*\s*$/.exec(line))) {
        flush();
        var level = Math.min(6, m[1].length + 1); // the pane's own title is the h1
        out.push("<h" + level + ">" + inline(m[2]) + "</h" + level + ">");
        i += 1;
        continue;
      }
      if (/^\s*\|/.test(line) && i + 1 < lines.length && isTableRule(lines[i + 1])) {
        flush();
        var head = cells(line);
        var rows = [];
        i += 2;
        while (i < lines.length && /^\s*\|/.test(lines[i])) {
          rows.push(cells(lines[i]));
          i += 1;
        }
        out.push(
          "<table><thead><tr>" + head.map(function (c) { return "<th>" + inline(c) + "</th>"; }).join("") +
          "</tr></thead><tbody>" +
          rows.map(function (r) {
            return "<tr>" + r.map(function (c) { return "<td>" + inline(c) + "</td>"; }).join("") + "</tr>";
          }).join("") +
          "</tbody></table>"
        );
        continue;
      }
      if (/^\s*>/.test(line)) {
        flush();
        var quote = [];
        while (i < lines.length && /^\s*>/.test(lines[i])) {
          quote.push(lines[i].replace(/^\s*>\s?/, ""));
          i += 1;
        }
        out.push("<blockquote>" + render(quote.join("\n")) + "</blockquote>");
        continue;
      }
      if (/^\s{0,3}([-*+]|\d+\.)\s+/.test(line)) {
        flush();
        // a numbered line keeps its own number (a listing's "4." is the section's, and the
        // browser's own count would not be)
        var numbered = /^\s{0,3}\d+\./.test(line);
        var items = [];
        while (i < lines.length && lines[i].trim()) {
          // "4." and a listing's "4.2" both mark an item
          var item = /^(\s*)([-*+]|\d+\.(?:\d+\.?)*)\s+(.*)$/.exec(lines[i]);
          if (item) items.push({ depth: Math.floor(item[1].length / 2), mark: item[2], text: item[3] });
          else if (items.length) items[items.length - 1].text += " " + lines[i].trim();
          i += 1;
        }
        out.push(
          '<ul class="' + (numbered ? "numbered" : "bulleted") + '">' +
          items.map(function (it) {
            var mark = /\d/.test(it.mark) ? escape(it.mark) + " " : "";
            return '<li class="depth-' + Math.min(it.depth, 3) + '">' + mark + inline(it.text) + "</li>";
          }).join("") +
          "</ul>"
        );
        continue;
      }
      para.push(line);
      i += 1;
    }
    flush();
    return out.join("\n");
  }

  var Markdown = { render: render, inline: inline, callArgs: callArgs };

  // -- the pane --------------------------------------------------------------------------

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  }

  function getJSON(url) {
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    });
  }

  function query(args) {
    var q = [];
    ["topic", "section", "find"].forEach(function (k) {
      if (args[k]) q.push(k + "=" + encodeURIComponent(args[k]));
    });
    return q.join("&");
  }

  /** The pane in `container`: an index down the side, the page beside it, a find box and
   * (in the main page) a button to pop it out and one to close it. */
  function LibraryPane(container, options) {
    options = options || {};
    this.container = container;
    this.popped = !!options.popped;
    this.onClose = options.onClose || null;
    this.topics = null;
    this.current = null;
    this.build();
  }

  LibraryPane.prototype.build = function () {
    var self = this;
    var c = this.container;
    c.innerHTML = "";
    c.classList.add("library");
    var head = el("div", "panel-head library-head");
    head.appendChild(el("span", "", "Library"));
    var tools = el("span", "library-tools");
    var form = el("form", "library-find");
    var find = el("input");
    find.type = "search";
    find.placeholder = "find in the library";
    find.setAttribute("aria-label", "find in the library");
    form.appendChild(find);
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var words = find.value.trim();
      if (words) self.open({ find: words });
    });
    tools.appendChild(form);
    if (!this.popped) {
      var pop = el("button", "", "pop out");
      pop.type = "button";
      pop.title = "open the library in a window of its own";
      pop.addEventListener("click", function () {
        self.popOut();
      });
      tools.appendChild(pop);
      var close = el("button", "", "close");
      close.type = "button";
      close.title = "close the library (the order line's 'library' opens it again)";
      close.addEventListener("click", function () {
        if (self.onClose) self.onClose();
      });
      tools.appendChild(close);
    }
    head.appendChild(tools);
    c.appendChild(head);
    var body = el("div", "library-body");
    this.index = el("nav", "library-index");
    this.page = el("article", "library-page");
    body.appendChild(this.index);
    body.appendChild(this.page);
    c.appendChild(body);
    this.findInput = find;
    c.addEventListener("click", function (ev) {
      var a = ev.target.closest ? ev.target.closest("a.library-call, a.library-link") : null;
      if (!a) return;
      ev.preventDefault();
      if (a.getAttribute("data-paper") !== null) {
        self.openPapers(a.getAttribute("data-paper"));
        return;
      }
      self.open({
        topic: a.getAttribute("data-topic") || "",
        section: a.getAttribute("data-section") || "",
        find: a.getAttribute("data-find") || "",
      });
    });
  };

  LibraryPane.prototype.popOut = function () {
    var cur = this.current || {};
    var url = "/client/library.html" + (cur.papers !== undefined ? "#papers" : "#" + query(cur));
    root().open(url, "freesail-library", "width=780,height=900");
    if (this.onClose) this.onClose();
  };

  function root() {
    return typeof window !== "undefined" ? window : {};
  }

  LibraryPane.prototype.loadIndex = function () {
    var self = this;
    if (this.topics) return Promise.resolve(this.topics);
    return getJSON("/api/library/topics").then(function (data) {
      self.topics = data.topics || [];
      self.drawIndex();
      return self.topics;
    });
  };

  LibraryPane.prototype.drawIndex = function () {
    var nav = this.index;
    nav.innerHTML = "";
    var list = el("ul", "library-topics");
    var contents = el("li");
    contents.appendChild(link("Contents", { topic: "contents" }));
    list.appendChild(contents);
    var cur = this.current || {};
    (this.topics || []).forEach(function (top) {
      var li = el("li");
      // a chapter by its number and title ("3. Making and shortening sail"), the rest by name
      var chapter = /^primer (\d+): (.*)$/.exec(top.title);
      var words = chapter ? chapter[1] + ". " + chapter[2] : top.name.charAt(0).toUpperCase() + top.name.slice(1);
      li.appendChild(link(words, { topic: top.key }));
      if (chapter) li.classList.add("chapter");
      if (top.sections.length && cur.topic === top.key) {
        var sub = el("ul", "library-sections");
        top.sections.forEach(function (sec) {
          var s = el("li", "level-" + Math.min(sec.level, 3));
          s.appendChild(link(sec.label, { topic: top.key, section: sec.ask }));
          if (cur.section && cur.section === sec.ask) s.classList.add("current");
          sub.appendChild(s);
        });
        li.appendChild(sub);
      }
      if (cur.topic === top.key) li.classList.add("current");
      list.appendChild(li);
    });
    var papers = el("li", "library-papers-link");
    var a = el("a", "library-link", "The ship's papers");
    a.href = "#";
    a.setAttribute("data-paper", "");
    papers.appendChild(a);
    if (cur.papers !== undefined) papers.classList.add("current");
    list.appendChild(papers);
    nav.appendChild(list);
  };

  function link(words, args) {
    var a = el("a", "library-link", words);
    a.href = "#";
    a.setAttribute("data-topic", args.topic || "");
    a.setAttribute("data-section", args.section || "");
    a.setAttribute("data-find", args.find || "");
    return a;
  }

  /** Open a page: {topic, section, find}, as the tool takes them. */
  LibraryPane.prototype.open = function (args) {
    var self = this;
    args = { topic: args.topic || "", section: args.section || "", find: args.find || "" };
    if (!args.topic && !args.find) args.topic = "contents";
    this.current = args;
    this.loadIndex()
      .catch(function () {
        return [];
      })
      .then(function () {
        self.drawIndex();
      });
    return getJSON("/api/library?" + query(args))
      .then(function (page) {
        if (self.current !== args) return;
        self.page.innerHTML = "";
        var title = el("h1", "library-title", page.title.charAt(0).toUpperCase() + page.title.slice(1));
        self.page.appendChild(title);
        var asked = el("div", "library-asked", "as the model reads it: " + page.reopen);
        self.page.appendChild(asked);
        var text = el("div", "library-text");
        text.innerHTML = render(page.text);
        self.page.appendChild(text);
        self.page.scrollTop = 0;
        if (args.find) self.findInput.value = args.find;
      })
      .catch(function () {
        self.page.textContent = "The library could not be reached; the server may have stopped.";
      });
  };

  /** The ship's papers: each as its query answers it, and those that wait. */
  LibraryPane.prototype.openPapers = function (which) {
    var self = this;
    this.current = { papers: which || "" };
    this.drawIndex();
    return getJSON("/api/library/papers")
      .then(function (data) {
        self.page.innerHTML = "";
        self.page.appendChild(el("h1", "library-title", "The ship's papers"));
        self.page.appendChild(
          el("div", "library-asked", "each as its words answer it at the order line, read without a line in the log")
        );
        var text = el("div", "library-text");
        if (data.words) text.appendChild(el("p", "", data.words));
        (data.papers || []).forEach(function (p) {
          var h = el("h2", "", p.handle.charAt(0).toUpperCase() + p.handle.slice(1));
          h.id = "paper-" + p.handle.replace(/\W+/g, "-");
          text.appendChild(h);
          text.appendChild(el("div", "library-asked", p.words + "; at the order line: '" + p.handle + "'"));
          p.lines.forEach(function (ln) {
            text.appendChild(el("p", "", ln));
          });
        });
        if ((data.waiting || []).length) {
          text.appendChild(el("h2", "", "Papers that wait"));
          var ul = el("ul");
          data.waiting.forEach(function (w) {
            var li = el("li");
            li.appendChild(el("strong", "", w.handle.charAt(0).toUpperCase() + w.handle.slice(1) + ". "));
            li.appendChild(document.createTextNode(w.words));
            ul.appendChild(li);
          });
          text.appendChild(ul);
        }
        self.page.appendChild(text);
        self.page.scrollTop = 0;
      })
      .catch(function () {
        self.page.textContent = "The ship's papers could not be reached; the server may have stopped.";
      });
  };

  /** What a `library ...` line at the order line asks for: `library` the contents,
   * `library find <words>` a search, `library papers` the ship's papers, `library <topic>
   * [, <section>]` a topic or one of its sections ('library primer 3, reefing'). */
  LibraryPane.prototype.openWords = function (words) {
    var w = String(words || "").trim();
    var m;
    if (!w) return this.open({ topic: "contents" });
    if ((m = /^find\s+(.+)$/i.exec(w))) return this.open({ find: m[1] });
    if (/^(the\s+)?(ship's\s+)?papers$/i.test(w)) return this.openPapers("");
    var comma = w.indexOf(",");
    if (comma > 0) return this.open({ topic: w.slice(0, comma).trim(), section: w.slice(comma + 1).trim() });
    return this.open({ topic: w });
  };

  /** From a location hash (the pop-out window): '#topic=primer%203&section=2', '#papers'. */
  LibraryPane.prototype.openHash = function (hash) {
    var h = String(hash || "").replace(/^#/, "");
    if (h === "papers") return this.openPapers("");
    var args = { topic: "", section: "", find: "" };
    h.split("&").forEach(function (kv) {
      var i = kv.indexOf("=");
      if (i > 0) {
        var k = kv.slice(0, i);
        if (k in args) args[k] = decodeURIComponent(kv.slice(i + 1));
      }
    });
    return this.open(args);
  };

  return { LibraryPane: LibraryPane, Markdown: Markdown };
});
