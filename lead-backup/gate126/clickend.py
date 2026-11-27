import sys, time
from playwright.sync_api import sync_playwright
base = f"http://localhost:{sys.argv[1]}"
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")
    pg = b.new_page()
    pg.goto(base + "/harbour")
    pg.wait_for_timeout(1500)
    # start a game through the page's own API from inside the page (its mark)
    r = pg.evaluate("""async () => { const m = document.querySelector('meta[name="freesail-page"]').content;
      const s = await fetch('/api/harbour/start', {method:'POST', headers:{'Content-Type':'application/json','x-freesail-page':m}, body: JSON.stringify({scenario:'data/scenarios/tender.yaml'})});
      await fetch('/api/order', {method:'POST', headers:{'Content-Type':'application/json','x-freesail-page':m}, body: JSON.stringify({text:'set plain sail'})});
      return s.status; }""")
    print("start", r)
    pg.wait_for_timeout(3000)
    print("end button visible:", pg.is_visible("#btn-end"), "sure visible:", pg.is_visible("#btn-end-sure"))
    pg.evaluate("() => { document.getElementById('end-game').closest('details').open = true; }")
    print("end button visible after opening the panel:", pg.is_visible("#btn-end"))
    pg.click("#btn-end")
    pg.wait_for_timeout(1500)
    print("words:", pg.inner_text("#end-words"), "| refusal class:", pg.get_attribute("#end-words", "class"))
    print("sure visible:", pg.is_visible("#btn-end-sure"), pg.inner_text("#btn-end-sure"))
    pg.click("#btn-end-sure")
    pg.wait_for_timeout(2500)
    print("words:", pg.inner_text("#end-words"), "| head:", pg.inner_text("#in-play-line"))
    print("end button visible after:", pg.is_visible("#btn-end"))
    b.close()
