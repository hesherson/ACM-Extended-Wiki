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
      assert(await page.locator(".brand-logo").evaluate(el => el.complete && el.naturalWidth > 0), file + ": logo failed to load");
      assert.equal(await page.locator('link[rel="icon"]').getAttribute("href"), "img/acme-favicon.png");
      assert.equal(await page.locator('.nav > a[href="flight.html"]').textContent(), "Flight Physiology");
      if (!["medications.html", "circulation.html", "settings.html", "menu.html", "bleeding.html", "oxygen.html", "flight.html", "access.html", "ventilator.html", "accessibility.html"].includes(file)) continue;
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

    assert.equal(await page.locator(".med-card-grid").count(), 1);
    const columns = await page.locator(".med-card-grid").evaluate(el => getComputedStyle(el).gridTemplateColumns.split(" ").length);
    assert.equal(columns, width >= 1280 ? 2 : 1, "Medication grid column count");
    const cards = page.locator(".med-card-grid > .drug");
    const first = await cards.nth(0).boundingBox(), second = await cards.nth(1).boundingBox();
    if (width >= 1280) assert(Math.abs(first.y-second.y)<1 && second.x>first.x, "Cards are not aligned in a grid");
    await page.goto(pathToFileURL(resolve(root, "docs/access.html")).href);
    assert.equal(await page.locator("tr[data-infusion]").count(), 33, "Incomplete medication infusion coverage");
    if (width < 820) await page.locator("#mSearch").click();
    await page.locator("#q").fill("propofol infusion");
    assert(await page.locator('#qr a[href="access.html#infusion-propofol"]').count()>0, "Infusion rows missing from search");
    await page.keyboard.press("Escape");
    await page.goto(pathToFileURL(resolve(root, "docs/accessibility.html")).href);
    assert.equal(await page.locator("h2").filter({hasText:/Screen brightness/i}).count(),0);
    await page.goto(pathToFileURL(resolve(root, "docs/ventilator.html")).href);
    assert.equal(await page.locator("#screen-brightness-amp-night-mode").count(),1);
    assert(await page.getByText("Needle decompress or Finger Thoracostomy first",{exact:true}).count()>0);
    await page.goto(pathToFileURL(resolve(root, "docs/oxygen.html")).href);
    const model = await page.evaluate(() => {
      const base={blood:6,saline:0,plasma:0,heartRate:75,saturation:97,peep:5,support:"none"};
      const shock={...base,blood:3.9,heartRate:130};
      return {baseline:ACMEWiki.calculateDO2(base),shock:ACMEWiki.calculateDO2(shock),
        saline:ACMEWiki.calculateDO2({...shock,saline:1}),blood:ACMEWiki.calculateDO2({...shock,blood:4.9}),
        ppv:ACMEWiki.calculateDO2({...shock,support:"vent"}),highPeep:ACMEWiki.calculateDO2({...shock,support:"vent",peep:15}),
        bvm:ACMEWiki.calculateDO2({...shock,support:"bvm",peep:15}),
        invalid:ACMEWiki.calculateDO2({...shock,blood:-1})};
    });
    assert(Math.abs(model.baseline.do2-1)<1e-9);
    assert(Math.abs(model.shock.do2-.6491900300)<1e-8);
    assert(Math.abs(model.saline.do2-.7444760403)<1e-8);
    assert(Math.abs(model.blood.do2-.9353673327)<1e-8);
    assert(Math.abs(model.ppv.do2-.5745465896)<1e-8);
    assert(Math.abs(model.highPeep.do2-.5372248694)<1e-8);
    assert.equal(model.bvm.do2,model.ppv.do2);
    assert.equal(model.invalid,null);
    const input=page.locator('[data-do2-calculator] input[name="blood"]');
    await input.fill("");
    assert(await page.locator('[data-do2-result="error"]').isVisible());
    assert.equal(await page.locator('[data-do2-result="delivery"]').textContent(),"Unavailable");
    await input.fill("3.9");
    assert(!(await page.locator('[data-do2-result="error"]').isVisible()));
    assert.equal(await page.locator('[data-do2-result="delivery"]').textContent(),"64.9%");
    let chartCount=0;
    for(const file of ["bleeding.html","oxygen.html","flight.html"]){
      await page.goto(pathToFileURL(resolve(root,"docs",file)).href);
      const charts=page.locator(".physiology-chart svg");chartCount+=await charts.count();
      for(const chart of await charts.all()){
        assert(await chart.locator(":scope > title").textContent());
        assert(await chart.locator(":scope > desc").textContent());
      }
    }
    assert.equal(chartCount,5,"Physiology graph count");

    // Curve readouts must track the plot and retain exact keyboard-entered time.
    await page.goto(pathToFileURL(resolve(root,"docs/medications.html")).href);
    assert.equal(await page.locator(".chart-inspector").count(),39);
    const graph=page.locator(".med-curve").first();
    await graph.evaluate(el=>el.closest("details").open=true);
    const time=graph.locator('input[type="number"]');
    await time.fill("0.5");
    assert((await graph.locator(".chart-readout").textContent()).includes("0.5 s"));
    assert((await graph.locator(".chart-readout").textContent()).includes("6 mg"));
    const half=await graph.locator(".chart-cursor circle").first().evaluate(el=>({x:+el.getAttribute("cx"),y:+el.getAttribute("cy")}));
    assert(Math.abs(half.x-(68+622*.5/15))<1e-7);
    assert(Math.abs(half.y-(184-144*Math.sin(.5/(2/3.113))))<1e-7);
    await time.press("End");
    assert((await graph.locator(".chart-readout").textContent()).includes("Relative game effect: 0%"));
    await time.fill("");
    assert((await graph.locator(".chart-readout").textContent()).includes("Enter a value"));
    const svg=graph.locator("svg");
    await svg.scrollIntoViewIfNeeded();
    // Scroll containers and SVG viewBox scaling must not change pointer coordinates.
    await svg.evaluate(el=>{const p=el.createSVGPoint();p.x=379;p.y=110;const screen=p.matrixTransform(el.getScreenCTM());el.dispatchEvent(new PointerEvent("pointermove",{clientX:screen.x,clientY:screen.y,bubbles:true}));});
    assert(Math.abs(Number(await time.inputValue())-7.5)<.001);
    assert(await graph.locator(".chart-cursor").isVisible());
    await svg.dispatchEvent("pointerleave");
    assert(!(await graph.locator(".chart-cursor").isVisible()));
    await svg.evaluate(el=>{const p=el.createSVGPoint();p.x=223.5;p.y=100;const screen=p.matrixTransform(el.getScreenCTM());el.dispatchEvent(new PointerEvent("pointerdown",{pointerType:"touch",clientX:screen.x,clientY:screen.y,bubbles:true}));});
    assert(Math.abs(Number(await time.inputValue())-3.75)<.001);
    const peakLists=page.locator("#d-atropine .route-peaks li");
    assert.equal(await peakLists.count(),2);
    assert((await peakLists.nth(0).textContent()).includes("IV / IO"));
    assert((await peakLists.nth(1).textContent()).includes("IM"));
    if(width>=1280){
      const aligned=await page.locator(".med-card-grid>.drug").evaluateAll(cards=>[cards[0],cards[1]].map(card=>Array.from(card.querySelectorAll(".med-fact")).map(el=>({y:el.getBoundingClientRect().y,h:el.getBoundingClientRect().height}))));
      for(let i=0;i<9;i++){assert(Math.abs(aligned[0][i].y-aligned[1][i].y)<1);assert(Math.abs(aligned[0][i].h-aligned[1][i].h)<1);}
      const center=await page.locator(".side-head").evaluate(el=>{const head=el.getBoundingClientRect(),logo=el.querySelector(".brand-logo").getBoundingClientRect();return Math.abs(head.x+head.width/2-logo.x-logo.width/2);});
      assert(center<1,"Sidebar logo is not centered");
    }
    await page.goto(pathToFileURL(resolve(root,"docs/bleeding.html")).href);
    const definition=page.locator('.gl[data-t="afterload"]').first();
    assert(await definition.count()>0,"Afterload is missing its definition");
    await definition.focus();await definition.press("Enter");
    assert(await page.locator("#glpop").isVisible());
    assert((await page.locator(".glpop-d").textContent()).includes("separate afterload"));
    await page.keyboard.press("Escape");
    await page.waitForTimeout(200);
    assert(!(await page.locator("#glpop").isVisible()));
    assert.equal(await page.locator('.nav > a[href="ventilator.html"]').textContent(),"Ventilator Settings");
    assert.equal(await page.locator(".chart-inspector").count(),2);
    assert.equal(await page.locator("a .gl,button .gl,summary .gl,svg .gl").count(),0,"Glossary links nested in controls");
    assert(await page.locator(".hemorrhage-classes td:nth-child(3)").first().evaluate(el=>getComputedStyle(el).whiteSpace==="nowrap"));
    await page.goto(pathToFileURL(resolve(root,"docs/access.html")).href);
    const concentrations=await page.locator("[data-concentration-mg]").evaluateAll(cells=>cells.map(el=>({actual:+el.dataset.concentrationMg,text:el.textContent,title:el.title})));
    assert.equal(concentrations.length,15);
    for(const c of concentrations){const unit=c.text.includes("mcg")?1000:1;const shown=Number(c.text.match(/[\d.]+/)[0]);assert(shown+1e-9>=c.actual*unit);assert(shown-c.actual*unit<.010001);assert(c.title.includes("Unrounded"));}
    await page.goto(pathToFileURL(resolve(root,"docs/circulation.html")).href);
    for(const label of await page.locator(".rhythm-strip-label").allTextContents())assert(label.startsWith("Pulse: "));

    assert.deepEqual(errors, [], "Browser script errors");
    await page.close();
  }
  console.log("Checked " + files.length + " pages at desktop/mobile widths; " + disclosures +
    " disclosure openings; medication fields, graphs, section menus and interaction search passed.");
} finally {
  await browser.close();
}
