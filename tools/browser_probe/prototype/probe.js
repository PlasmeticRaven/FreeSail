// probe.js: drive the real FreeSail browser client as the player sees it, live.
//
//   node probe.js <base-url> <plan.json> <out-dir>
//
// The plan is a JSON list of steps, run in order:
//   "where am I"                         a line typed at the order line and Enter pressed
//   {"say": "go ashore", "setup": true}  the same, marked as setup in the report
//   {"tick": 600}                        the clock advanced (the page's own `tick N` word)
//   {"until": "ashore", "tick": 60, "max": 60}
//                                        tick until the "Where you are" instrument contains
//                                        the words (or the snapshot JSON does), at most max
//   {"label": "ON DECK"}                 a section heading in the report
//   {"shot": "name"}                     a screenshot to <out-dir>/name.png
// For every typed line it records: the HTTP answer of POST /api/order (what the server
// said), the websocket messages that arrived after it (what the server sent the page),
// the new rows of the log pane (#log-list), and the "Where you are" instrument; and it
// says SHOWN, SHOWN-OTHER (a line appeared, not the answer) or NOT SHOWN.
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const [base, planFile, outDir] = process.argv.slice(2);
if (!base || !planFile || !outDir) {
  console.error("usage: node probe.js <base-url> <plan.json> <out-dir>");
  process.exit(2);
}
fs.mkdirSync(outDir, { recursive: true });
const plan = JSON.parse(fs.readFileSync(planFile, "utf8"));
const SETTLE_MS = Number(process.env.SETTLE_MS || 800); // wait for the socket after the answer

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  const consoleLines = [];
  page.on("console", (m) => consoleLines.push(`[${m.type()}] ${m.text()}`));
  page.on("pageerror", (e) => consoleLines.push(`[pageerror] ${e.message}`));
  // every websocket frame the page receives, kept in the page for us to read
  await page.addInitScript(() => {
    window.__wire = [];
    const Real = window.WebSocket;
    window.WebSocket = function (url, protos) {
      const ws = protos ? new Real(url, protos) : new Real(url);
      ws.addEventListener("message", (m) => {
        try {
          const d = JSON.parse(m.data);
          if (d.type !== "snapshot") window.__wire.push({ t: Date.now(), d });
          else window.__lastSnap = d.snapshot;
        } catch (e) {}
      });
      return ws;
    };
    window.WebSocket.prototype = Real.prototype;
    Object.assign(window.WebSocket, { OPEN: 1, CLOSED: 3, CONNECTING: 0, CLOSING: 2 });
  });
  await page.goto(base, { waitUntil: "domcontentloaded" });
  await page.waitForFunction(() => window.__wire.some((w) => w.d.type === "hello"), null, { timeout: 60000 });

  const rows = () => page.$$eval("#log-list > *", (els) => els.map((e) => e.innerText.replace(/\s+/g, " ").trim()));
  const where = () => page.$eval("#i-knowledge", (e) => e.textContent).catch(() => "");
  const wireLen = () => page.evaluate(() => window.__wire.length);
  const wireFrom = (n) => page.evaluate((n) => window.__wire.slice(n).map((w) => w.d), n);

  async function type(text) {
    const before = (await rows()).length;
    const w0 = await wireLen();
    const t0 = Date.now();
    const input = page.locator("#command");
    await input.fill(text);
    const answerP = page
      .waitForResponse((r) => r.url().endsWith("/api/order") || r.url().endsWith("/api/driver"), { timeout: Number(process.env.ANSWER_MS || 10000) })
      .then((r) => r.json())
      .catch(() => ({ error: "no request reached the server: the page handled the line itself" }));
    await input.press("Enter");
    const answer = await answerP;
    const ms = Date.now() - t0;
    await page.waitForTimeout(SETTLE_MS);
    const after = await rows();
    const newRows = after.slice(before);
    const wire = (await wireFrom(w0)).map((d) => ({ type: d.type, kind: (d.event || d.rollup || {}).kind, text: (d.event || d.rollup || d.line || {}).text }));
    const said = answer && answer.text ? String(answer.text) : "";
    const head = said.split("\n")[0].slice(0, 60);
    let shown = "NOT SHOWN";
    if (newRows.some((r) => head && r.includes(head))) shown = "SHOWN";
    else if (newRows.length) shown = "SHOWN-OTHER";
    return { text, ms, answer: answer.kind ? { kind: answer.kind, text: said } : answer, wire, newRows, where: await where(), shown };
  }

  const tick = (n) => page.evaluate((n) => fetch("/api/driver", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ action: "tick", value: n }) }).then((r) => r.json()), n);
  const report = [];
  let shotN = 0;
  for (const step of plan) {
    if (typeof step === "string" || step.say) {
      const r = await type(typeof step === "string" ? step : step.say);
      r.setup = !!step.setup;
      report.push(r);
      const a = r.answer.kind ? `${r.answer.kind}: ${r.answer.text.replace(/\s+/g, " ").slice(0, 110)}` : JSON.stringify(r.answer).slice(0, 110);
      console.log(`${r.shown.padEnd(11)} ${String(r.ms).padStart(5)}ms  > ${r.text}\n             server: ${a}\n             wire:   ${r.wire.map((w) => w.kind || w.type).join(", ") || "(nothing)"}\n             pane:   ${r.newRows.map((x) => x.slice(0, 110)).join(" | ") || "(nothing)"}`);
    } else if (step.label) {
      report.push({ label: step.label });
      console.log(`\n=== ${step.label} === (${await where()})`);
    } else if (step.until) {
      let ok = false;
      for (let i = 0; i < (step.max || 60); i++) {
        await tick(step.tick || 60);
        await page.waitForTimeout(200);
        const w = await where();
        const snap = await page.evaluate(() => JSON.stringify(window.__lastSnap || {}));
        if (w.includes(step.until) || snap.includes(step.until)) { ok = true; break; }
      }
      console.log(`  (until "${step.until}": ${ok ? "reached" : "NOT reached"}; where: ${await where()})`);
    } else if (step.tick) {
      await tick(step.tick);
      await page.waitForTimeout(SETTLE_MS);
    } else if (step.shot) {
      await page.screenshot({ path: path.join(outDir, `${String(++shotN).padStart(2, "0")}-${step.shot}.png`) });
    }
  }
  fs.writeFileSync(path.join(outDir, "report.json"), JSON.stringify(report, null, 2));
  fs.writeFileSync(path.join(outDir, "console.txt"), consoleLines.join("\n"));
  const typed = report.filter((r) => r.text && !r.setup);
  console.log(`\n${typed.filter((r) => r.shown === "NOT SHOWN").length} of ${typed.length} lines typed got no line in the log pane.`);
  await browser.close();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
