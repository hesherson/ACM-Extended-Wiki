import assert from 'node:assert/strict';
import { readFile, mkdir } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { chromium } from 'playwright';

const root = resolve(import.meta.dirname, '..');
const data = JSON.parse(await readFile(resolve(root, 'src/infusion-levels.json'), 'utf8'));
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_EXECUTABLE_PATH || undefined });
const page = await browser.newPage({ viewport: { width: 1905, height: 1100 }, reducedMotion: 'reduce' });
const errors = [];
page.on('pageerror', e => errors.push(e.message));
const close = (actual, expected, tolerance = .002) => assert(Math.abs(actual - expected) <= tolerance, `${actual} should be within ${tolerance} of ${expected}`);
const overflow = () => [...document.querySelectorAll('.infusion-explorer,.mixture-guide,.explorer-controls input,.explorer-controls select,.explorer-metrics>div,.mixture-stocks li,.mixture-output>div')].filter(e => {
  const box = e.getBoundingClientRect();
  return box.width && box.height && e.scrollWidth > e.clientWidth + 2;
}).map(e => `${e.className}: ${e.scrollWidth}/${e.clientWidth}`);
const visit = p => p.goto(pathToFileURL(resolve(root, 'docs/access.html')).href);
try {
  await visit(page);
  const model = async (id, options) => page.evaluate(({ row, options }) => {
    const result = window.ACMInfusionModel.project(row, options);
    return result && { plateau: result.plateau, halfLife: result.halfLifeMinutes, last: result.points.at(-1), first: result.points[0], clearance: result.clearance };
  }, { row: data.rows.find(r => r.id === id), options });
  // Independent one-compartment and half-life reference values, not snapshots.
  let r = await model('lidocaine', { rateMgMin: 2, minutes: Math.log(2) * 58.1 / .4 });
  close(r.plateau, 5); close(r.last.level, 2.5); close(r.halfLife, 100.67962797633199);
  r = await model('lidocaine', { rateMgMin: 2, minutes: 60, shock: true, esmolol: true });
  close(r.clearance, .168, .000001); close(r.plateau, 11.9047619);
  r = await model('esmolol', { rateMgMin: 3.5, minutes: Math.log(2) * 41.5 / 3.5 });
  close(r.plateau, 1); close(r.last.level, .5);
  r = await model('ketamine', { rateMgMin: 1.2, minutes: 9, stopMinutes: 6 });
  close(r.last.level, .375); close(r.last.deliveredMg, 7.2);
  r = await model('epinephrine', { rateMgMin: .006, minutes: 2 });
  close(r.plateau, .02, .000001); close(r.last.level, .01, .0001);
  r = await model('magnesium', { rateMgMin: 200, minutes: 30 });
  close(r.plateau, 250); close(r.last.level, 125, .05);
  r = await model('calcium-chloride', { rateMgMin: 400, minutes: 1 });
  close(r.plateau, 1.82); assert(r.last.level < 1.82 * (1 - 2 ** (-.5)), 'Calcium input easing delays concentration rise');
  r = await model('calcium-gluconate', { rateMgMin: 400, minutes: 60, stopMinutes: 0 });
  close(r.plateau, .62); close(r.last.level, 0); close(r.last.deliveredMg, 0);
  assert.equal(await model('propofol', { rateMgMin: 1, minutes: 60 }), null);
  assert.equal(await model('hts3', { rateMgMin: 1, minutes: 60 }), null);
  const select = page.locator('[data-level-drug]');
  for (const row of data.rows) {
    await select.selectOption(row.id);
    assert(await page.locator('[data-level-output]').isVisible(), row.id + ' has an output');
    assert.doesNotMatch(await page.locator('[data-level-output]').innerText(), /undefined|NaN|Infinity/);
    assert.equal(await page.locator('[data-level-plot]').isVisible(), row.model !== 'none');
  }
  await select.selectOption('hts3');
  assert.match(await page.locator('[data-level-current]').textContent(), /8 mmHg/);
  assert.match(await page.locator('[data-level-plateau]').textContent(), /160 mEq\/L/);
  await select.selectOption('lidocaine');
  await page.locator('[data-level-weight]').fill('');
  assert(await page.locator('[data-level-error]').isVisible());
  await select.selectOption('amiodarone');
  assert(await page.locator('[data-level-output]').isVisible(), 'Unused hidden weight must not prevent projection');
  // Restore through the visible control, then verify errors clear and time inspection works.
  await select.selectOption('lidocaine');
  await page.locator('[data-level-weight]').fill('83');
  await select.selectOption('epinephrine');
  await page.locator('[data-level-rate]').fill('6');
  assert.match(await page.locator('[data-level-plateau]').textContent(), /0\.02 mcg\/mL/);
  await page.locator('[data-level-rate]').fill('-1');
  assert(await page.locator('[data-level-error]').isVisible());
  assert(!(await page.locator('[data-level-output]').isVisible()));
  await page.locator('[data-level-rate]').fill('6');
  const time = page.locator('[data-level-time-slider]');
  await time.fill('10');
  assert.match(await page.locator('[data-level-readout]').textContent(), /^10 min/);
  await time.focus(); await page.keyboard.press('ArrowRight');
  assert(Number(await time.inputValue()) > 10);
  const plot = page.locator('[data-level-hit]');
  await plot.scrollIntoViewIfNeeded();
  const box = await plot.boundingBox();
  await page.mouse.move(box.x + box.width / 4, box.y + box.height / 2);
  assert(Math.abs(Number(await time.inputValue()) - 15) < .2);
  assert(await page.locator('[data-level-dot]').isVisible());
  await page.locator('[data-level-stop-enabled]').check();
  await page.locator('[data-level-duration]').selectOption('15');
  assert.equal(await page.locator('[data-level-stop]').inputValue(), '15');
  assert(await page.locator('[data-level-output]').isVisible());
  await page.locator('[data-level-stop-enabled]').uncheck();

  const picker = page.locator('[data-mixture-picker]');
  assert.equal(await page.locator('.mixture-recipe').count(), 5);
  assert.equal(await page.locator('.mixture-step').count(), 20);
  await picker.selectOption('ketofol');
  let recipe = page.locator('#mixture-ketofol');
  await recipe.locator('[data-mixture-next]').click();
  assert.match(await recipe.locator('[data-mixture-drawing]').textContent(), /250 mg/);
  await recipe.locator('[data-mixture-next]').click();
  close(await recipe.locator('.mixture-syringe-canvas').evaluate(e => Number(e.style.getPropertyValue('--mixture-fill'))), 1);
  await recipe.locator('[data-mixture-quantity]').fill('2');
  assert.deepEqual(await recipe.locator('[data-mixture-output] strong').allTextContents(), ['50 mg', '10 mg']);
  await picker.selectOption('push-epinephrine');
  recipe = page.locator('#mixture-push-epinephrine');
  await recipe.locator('[data-mixture-quantity]').fill('2');
  assert.deepEqual(await recipe.locator('[data-mixture-output] strong').allTextContents(), ['20 mcg']);
  await picker.selectOption('shared-pressors');
  recipe = page.locator('#mixture-shared-pressors');
  await recipe.locator('[data-mixture-quantity]').fill('60');
  assert.deepEqual(await recipe.locator('[data-mixture-output] strong').allTextContents(), ['15.686 mcg/min', '3.922 mcg/min']);
  await recipe.locator('[data-mixture-quantity]').fill('-1');
  assert(await recipe.locator('[data-mixture-error]').isVisible());
  await recipe.locator('[data-mixture-quantity]').fill('60');
  await page.evaluate(() => { location.hash = 'mixture-norepinephrine-bag'; });
  await page.waitForFunction(() => document.querySelector('[data-mixture-picker]').value === 'norepinephrine-bag');
  assert(await page.locator('#mixture-norepinephrine-bag').isVisible());

  for (const width of [320, 390, 768, 1905]) {
    await page.setViewportSize({ width, height: 1000 });
    for (const size of ['100%', '200%']) {
      await page.evaluate(size => { document.documentElement.style.fontSize = size; }, size);
      for (const row of data.rows) {
        await select.selectOption(row.id);
        assert.deepEqual(await page.evaluate(overflow), [], `${row.id} at ${width} ${size}`);
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `Page at ${width} ${size}: ` + JSON.stringify(await page.evaluate(() => [...document.querySelectorAll('body *')].filter(e => {const r=e.getBoundingClientRect();return r.width&&r.height&&r.right>innerWidth+1;}).slice(0,12).map(e => ({tag:e.tagName,cls:typeof e.className==='string'?e.className:'svg',right:e.getBoundingClientRect().right,text:e.textContent.slice(0,50)})))));
      }
      for (const id of ['ketofol', 'push-epinephrine', 'norepinephrine-bag', 'epinephrine-bag', 'shared-pressors']) {
        await picker.selectOption(id);
        assert.deepEqual(await page.evaluate(overflow), [], `${id} at ${width} ${size}`);
      }
    }
  }
  if (process.env.WIKI_SCREENSHOT_DIR) {
    await mkdir(process.env.WIKI_SCREENSHOT_DIR, { recursive: true });
    await page.evaluate(() => { document.documentElement.style.fontSize = '100%'; });
    await select.selectOption('amiodarone');
    await page.locator('[data-level-duration]').selectOption('60');
    await picker.selectOption('ketofol');
    await page.addStyleTag({ content: '.secbar,.mbar,.skip-link{visibility:hidden!important}' });
    for (const width of [390, 1905]) {
      await page.setViewportSize({ width, height: 1100 });
      await page.locator('[data-infusion-explorer]').screenshot({ path: resolve(process.env.WIKI_SCREENSHOT_DIR, `explorer-${width}.png`) });
      await page.locator('#mixture-ketofol').screenshot({ path: resolve(process.env.WIKI_SCREENSHOT_DIR, `ketofol-${width}.png`) });
    }
  }
  const noJS = await browser.newPage({ javaScriptEnabled: false, viewport: { width: 390, height: 844 } });
  await visit(noJS);
  assert.equal(await noJS.locator('.mixture-recipe:visible').count(), 5);
  assert.equal(await noJS.locator('.mixture-step:visible').count(), 20);
  assert.equal(await noJS.locator('.infusion-target').count(), 18);
  assert(!(await noJS.locator('[data-explorer-controls]').isVisible()));
  assert.deepEqual(errors, []);
  console.log('Passed 18 concentration references, source-model calculations, stop/clearance behavior, hover and keyboard inspection, five syringe recipes, shared flow, no-JS fallback and mobile/enlarged-text reflow.');
} finally { await browser.close(); }
