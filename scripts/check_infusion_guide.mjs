import { chromium } from 'playwright';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import assert from 'node:assert/strict';

const root = resolve(import.meta.dirname, '..');
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_EXECUTABLE_PATH || undefined });
const page = await browser.newPage({ viewport: { width: 1905, height: 1100 }, reducedMotion: 'reduce' });
const errors = [];
page.on('pageerror', error => errors.push(error.message));
const visit = name => page.goto(pathToFileURL(resolve(root, 'docs', name + '.html')).href);
const capture = (locator, name) => process.env.WIKI_SCREENSHOT_DIR
  ? locator.screenshot({ path: resolve(process.env.WIKI_SCREENSHOT_DIR, name + '.png') }) : Promise.resolve();
try {
  await visit('access');
  const guides = page.locator('.infusion-guide');
  assert.equal(await guides.count(), 18);
  assert.equal(await guides.locator('.infusion-band').count(), 54);
  assert.equal(await page.locator('#full-infusion-list').evaluate(h => h.closest('section').querySelectorAll('tbody a[href^="#infusion-risk-"]').length), 19);
  const input = page.locator('[data-infusion-filter]');
  await input.fill('calcium');
  assert(await page.locator('.infusion-guide:visible').count() >= 2);
  await input.fill('esmolol premix');
  assert.equal(await page.locator('.infusion-guide:visible').count(), 1);
  await page.locator('[data-infusion-expand]').click();
  assert(await page.locator('#infusion-risk-esmolol').evaluate(e => e.open));
  assert.match(await page.locator('#infusion-risk-esmolol').textContent(), /1.75–7 mg\/min/);
  await page.locator('[data-infusion-expand]').click();
  assert(!(await page.locator('#infusion-risk-esmolol').evaluate(e => e.open)));
  await input.fill('no matching medicine xyz');
  assert(await page.locator('[data-infusion-empty]').isVisible());
  assert(await page.locator('[data-infusion-expand]').isDisabled());
  // A recipe link must reveal its target even when a previous filter hid it.
  await page.evaluate(() => { location.hash = 'infusion-risk-amiodarone'; });
  await page.waitForFunction(() => document.querySelector('#infusion-risk-amiodarone').open);
  assert.equal(await input.inputValue(), '');
  const amio = page.locator('#infusion-risk-amiodarone');
  assert.match(await amio.textContent(), /Above 25 to 90 mg\/min/);
  assert.match(await page.locator('#infusion-risk-magnesium').textContent(), /800 to 2,500 mg\/min/);
  for (const width of [390, 1905, 5120]) {
    await page.setViewportSize({ width, height: 1100 });
    await amio.scrollIntoViewIfNeeded();
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'Infusion overflow at ' + width);
    assert(await amio.locator('.infusion-band :is(h3,h4)').evaluateAll(headings => headings.every(h => getComputedStyle(h).color === 'rgb(241, 189, 89)')));
    await capture(amio, 'infusion-amiodarone-' + width);
  }
  await page.setViewportSize({ width: 1905, height: 1100 });
  await visit('medications');
  assert.equal(await page.locator('.drug .med-vial').count(), 33);
  await page.locator('.drug .med-vial').evaluateAll(images => {
    images.forEach(image => { image.loading = 'eager'; });
    return Promise.all(images.map(image => image.decode()));
  });
  assert(await page.locator('.med-fact dt').evaluateAll(headings => headings.every(h => getComputedStyle(h).color === 'rgb(241, 189, 89)')));
  const dim = page.locator('#d-dimercaprol');
  assert(await dim.locator('.availability-warning').isVisible());
  assert.match(await dim.locator('.availability-warning').textContent(), /NOT IN GAME/);
  assert.match(await page.locator('#d-norepinephrine .med-fact').filter({ hasText: /^Dose/ }).textContent(), /254 mL/);
  assert.equal(await page.locator('.med-art-note').count(), 2);
  const overlaps = await page.locator('.drug').evaluateAll(cards => cards.filter(card => {
    const facts = card.querySelector('.med-facts').getBoundingClientRect();
    const details = card.querySelector('.med-details').getBoundingClientRect();
    const header = card.querySelector('header').getBoundingClientRect();
    return facts.top < header.bottom - 1 || details.top < facts.bottom - 1;
  }).map(card => card.id));
  assert.deepEqual(overlaps, [], 'Warnings and added images must not overlap medication facts or curves');
  await capture(dim.locator('header').locator('..'), 'dimercaprol-warning');
  for (const width of [390, 1905]) {
    await page.setViewportSize({ width, height: 1100 });
    const card = page.locator('#d-magnesium-sulfate');
    await card.scrollIntoViewIfNeeded();
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'Medication overflow at ' + width);
    await capture(card.locator('header'), 'magnesium-card-' + width);
  }
  await visit('ventilator');
  assert.equal(await page.locator('h1').textContent(), 'Ventilator Settings & Tips');
  assert.equal(await page.locator('.nav > a[href="ventilator.html"]').textContent(), 'Ventilator Settings & Tips');
  const tips = page.locator('#ketamine-sedation-and-nystagmus');
  assert.equal(await tips.count(), 1);
  assert.match(await tips.locator('..').locator('..').textContent(), /not in cardiac arrest/);
  await capture(tips.locator('..').locator('..'), 'ventilator-ketamine-tips');
  const noJS = await browser.newPage({ javaScriptEnabled: false, viewport: { width: 1440, height: 1000 } });
  await noJS.goto(pathToFileURL(resolve(root, 'docs/access.html')).href);
  assert.equal(await noJS.locator('.infusion-guide').count(), 18);
  assert(!(await noJS.locator('[data-infusion-controls]').isVisible()));
  await noJS.locator('#infusion-risk-calcium-chloride > summary').click();
  assert(await noJS.locator('#infusion-risk-calcium-chloride .infusion-bands').isVisible());
  assert.deepEqual(errors, []);
  console.log('Passed 18 infusion guides, 19 recipe links, filters, hash navigation, dose warnings, 33 images, yellow headings, moved ventilator tips and no-JS access.');
} finally { await browser.close(); }
