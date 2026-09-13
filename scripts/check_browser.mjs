import assert from "node:assert/strict";
import { readdir } from "node:fs/promises";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { chromium } from "playwright";

const root = resolve(import.meta.dirname, "..");
const files = (await readdir(resolve(root, "docs"))).filter(f => f.endsWith(".html"));
const browser = await chromium.launch();
let disclosures = 0;
try {
  for (const width of [1440, 390]) {
    const page = await browser.newPage({ viewport: { width, height: 900 }, reducedMotion: "reduce" });
    const errors = [];
    page.on("pageerror", error => errors.push(error.message));
    for (const file of files) {
      await page.goto(pathToFileURL(resolve(root, "docs", file)).href);
      assert.equal(await page.locator('a[href*="ov_traps"]').count(), 0, file + ": removed page remains linked");
      if (!["medications.html", "circulation.html", "settings.html", "menu.html"].includes(file)) continue;
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1),
        file + ": page overflows at " + width);
      const summaries = page.locator("details.dd > summary");
      for (let i = 0; i < await summaries.count(); i++) {
        const summary = summaries.nth(i);
        await summary.evaluate(el => el.scrollIntoView({ block: "center", behavior: "instant" }));
        await page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
        const before = await summary.boundingBox();
        const documentBefore = await summary.evaluate(el => el.getBoundingClientRect().top + scrollY);
        await summary.click();
        await page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
        assert(await summary.evaluate(el => el.parentElement.open), file + ": disclosure did not open");
        const after = await summary.boundingBox();
        const documentAfter = await summary.evaluate(el => el.getBoundingClientRect().top + scrollY);
        assert(Math.abs(documentAfter - documentBefore) < 1, file + ": opening moved summary in document");
        assert(Math.abs(after.y - before.y) < 1, file + ": opening moved summary in viewport");
        await summary.click();
        disclosures++;
      }
      if (await page.locator("#sbNow").count()) {
        await page.evaluate(() => scrollTo(0, 0));
        await page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
        const button = page.locator("#sbNow");
        const before = await button.boundingBox();
        await button.click();
        assert(await page.locator("#sbList").isVisible(), "Section list did not open");
        const after = await button.boundingBox();
        assert(Math.abs(after.y - before.y) < 1 && Math.abs(after.height - before.height) < 1,
          "Section button moved when opened");
        await page.keyboard.press("Escape");
        assert(!(await page.locator("#sbList").isVisible()), "Section list did not close");
      }
    }
    await page.goto(pathToFileURL(resolve(root, "docs/medications.html")).href);
    assert.equal(await page.locator(".drug").count(), 33);
    const required = ["Indications", "Contraindications", "Route", "Dose", "Onset", "Peak effect",
      "Side effects", "Special considerations", "Medication interactions"];
    for (const card of await page.locator(".drug").all()) {
      assert.deepEqual(await card.locator("dt").allTextContents(), required);
      for (const value of await card.locator("dd:not(.dd)").allTextContents()) assert(value.trim());
    }
    assert.equal(await page.locator(".med-curve svg").count(), 39);
    for (const graph of await page.locator(".med-curve svg").all()) {
      const labels = await graph.locator("text").allTextContents();
      for (const label of ["0%", "50%", "100%"]) assert(labels.includes(label), "Missing graph axis mark");
    }
    if (width < 820) await page.locator("#mSearch").click();
    await page.locator("#q").fill("rocuronium sugammadex");
    assert(await page.locator('#qr a[href*="medications.html#d-rocuronium"]').count() > 0,
      "Medication interactions are missing from search");
    await page.keyboard.press("Escape");
    assert.deepEqual(errors, [], "Browser script errors");
    await page.close();
  }
  console.log("Checked " + files.length + " pages at desktop/mobile widths; " + disclosures +
    " disclosure openings; medication fields, graphs, section menus and interaction search passed.");
} finally {
  await browser.close();
}
