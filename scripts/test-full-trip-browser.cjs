/* Optional real Chromium checks. Install playwright-core + @sparticuz/chromium
 * outside the repo, then set NODE_PATH to that installation's node_modules.
 * BASE_URL defaults to a separately running local preview (test tooling only).
 */
const assert = require('node:assert/strict');
const {chromium: playwright} = require('playwright-core');
const raw = require('@sparticuz/chromium');
const chromium = raw.default || raw;
const base = process.env.BASE_URL || 'http://127.0.0.1:8080/';
(async () => {
  const browser = await playwright.launch({args: chromium.args.filter(arg => arg !== '--single-process'), executablePath: await chromium.executablePath(), headless: true});
  try {
    const context = await browser.newContext();
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('requestfailed', r => errors.push(r.url()));
    for (const width of [320, 390, 768, 1440]) {
      await page.setViewportSize({width, height: 900});
      for (const file of ['index.html','itinerary.html#day-10','transit.html','stays.html','food-shopping.html','flagged-for-review.html','sources.html']) {
        const response = await page.goto(new URL(file, base).href);
        assert.equal(response.status(),200);
        assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), `Overflow: ${file} at ${width}`);
      }
    }
    await page.goto(new URL('itinerary.html', base).href);
    for (let i = 1; i <= 16; i++) {
      await page.locator(`[data-day="${i}"]`).click();
      await page.locator(`#day-${i}`).waitFor({state:"visible"});
      assert.equal(await page.locator('.day-section:visible').count(), 1);
      assert.equal(await page.locator('.day-section:visible').getAttribute('id'), `day-${i}`);
      assert.equal(await page.locator(`[data-day="${i}"]`).getAttribute('aria-current'), 'date');
    }
    await page.locator('#show-all').click();
    await page.locator('#day-1').waitFor({state:'visible'});
    assert.equal(await page.locator('.day-section:visible').count(), 16);
    await page.locator('#search').fill('Nurimaru');
    assert.ok(await page.locator('tr[data-search]:visible').count() > 0);
    await page.locator('#search').fill('nothing-matches-this-query');
    assert.equal(await page.locator('tr[data-search]:visible').count(), 0);
    assert.equal(await page.locator('#empty-results').isVisible(), true);
    await page.locator('#search').fill('');
    await page.locator('#status-filter').selectOption('unverified');
    assert.equal(await page.locator('tr[data-status="partial"]:visible').count(), 0);
    await page.locator('#status-filter').selectOption('all');
    await page.goto(new URL('itinerary.html#day-3', base).href);
    assert.match(await page.locator('.day-section:visible').innerText(), /Tuesday/);
    await page.locator('.day-section:visible details').first().locator('summary').click();
    assert.equal(await page.locator('.day-section:visible details').first().getAttribute('open'), '');
    await page.emulateMedia({media:'print'});
    assert.equal(await page.locator('.day-section:visible').count(),16);
    await page.emulateMedia({media:'screen'});
    const noJS = await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
    const staticPage = await noJS.newPage();
    await staticPage.goto(new URL('itinerary.html#day-16',base).href);
    assert.equal(await staticPage.locator('.day-section:visible').count(),16);
    assert.equal(await staticPage.locator('tr[data-search]').count(),105);
    await noJS.close();
    assert.deepEqual(errors,[]);
    console.log('PASS: Chromium 320/390/768/1440 px, 28 page/layout checks, 16 day switches, search/empty/filter, disclosure, print, no-JS fallback, no browser errors');
    await context.close();
  } finally { await browser.close(); }
})().catch(e => {console.error(e); process.exitCode=1;});
