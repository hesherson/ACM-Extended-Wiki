import assert from 'node:assert/strict';
import {readdir,mkdir,readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {chromium} from 'playwright';

const root=resolve(import.meta.dirname,'..');
const output=process.env.WIKI_PRINT_QA_DIR;
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE_PATH||undefined});
const files=(await readdir(resolve(root,'docs'))).filter(f=>f.endsWith('.html'));
const visit=(page,file)=>page.goto(pathToFileURL(resolve(root,'docs',file)).href);
const overflow=()=>{
 const bad=[];
 if(document.documentElement.scrollWidth>innerWidth+1)bad.push(`document: ${document.documentElement.scrollWidth}/${innerWidth}`);
 for(const e of document.querySelectorAll('.main .scroll,.main table,.main td,.main th,.main .table-value,.main input,.main select,.main .rrow')){
  const r=e.getBoundingClientRect();
  if(r.width&&r.height&&e.clientWidth&&e.scrollWidth>e.clientWidth+2)bad.push(`${e.tagName}.${e.className}: ${e.scrollWidth}/${e.clientWidth} ${e.textContent.trim().slice(0,50)}`);
 }
 return bad;
};
try{
 const page=await browser.newPage({viewport:{width:390,height:844},reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 for(const width of [320,390,768,1024,1905]){
  await page.setViewportSize({width,height:900});
  for(const file of files){
   await visit(page,file);
   await page.evaluate(()=>document.querySelectorAll('details').forEach(e=>e.open=true));
   assert.deepEqual(await page.evaluate(overflow),[],`${file} must fit, including its internal tables, at ${width}px`);
  }
  console.log(`Checked ${files.length} pages and expanded table rows at ${width}px`);
 }
 for(const file of ['access.html','medications.html','ventilator.html','quick-reference.html','debug.html','tbi.html']){
  await page.setViewportSize({width:390,height:844});await visit(page,file);
  await page.evaluate(()=>{document.documentElement.style.fontSize='200%';document.querySelectorAll('details').forEach(e=>e.open=true)});
  await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
  assert.deepEqual(await page.evaluate(overflow),[],`${file} must reflow with 200% root text sizing`);
 }
 await page.setViewportSize({width:390,height:844});await visit(page,'quick-reference.html');
 assert.equal(await page.locator('.print-sheet').count(),7);
 assert.equal(await page.locator('.medication-print-table tbody tr').count(),33);
 assert.equal(await page.locator('.print-rhythm [data-rhythm]').count(),13);
 assert.equal(await page.locator('.print-unavailable').textContent(),'NOT IN GAME');
 const data=JSON.parse(await readFile(resolve(root,'src/print-medications.json'),'utf8'));
 const ids=data.groups.flatMap(g=>g.rows.map(r=>'d-'+r.id));
 assert.equal(new Set(ids).size,33);
 const medPage=await browser.newPage();await visit(medPage,'medications.html');
 assert.deepEqual((await medPage.locator('.drug').evaluateAll(es=>es.map(e=>e.id))).sort(),ids.sort());await medPage.close();
 await page.evaluate(()=>{window.__printCalls=0;window.print=()=>{window.__printCalls++;window.__printed=[...document.querySelectorAll('[data-print-pack]:not(.print-excluded)')].map(e=>e.dataset.printPack)}});
 for(const key of ['medications','ventilator','access','rhythms','tbi','all']){
  await page.locator(`[data-print-chart="${key}"]`).click();
  assert.deepEqual(await page.evaluate(()=>window.__printed),key==='all'?['medications','ventilator','access','rhythms','tbi']:[key]);
  await page.evaluate(()=>window.dispatchEvent(new Event('afterprint')));
  assert.equal(await page.locator('.print-excluded').count(),0);
 }
 assert.equal(await page.evaluate(()=>window.__printCalls),6);
 // Selective printing: ensure only one sheet enters layout, then cancellation restores all packs.
 await page.locator('[data-print-chart="access"]').click();await page.emulateMedia({media:'print'});
 assert.equal(await page.locator('.print-sheet:visible').count(),1);
 await page.emulateMedia({media:'screen'});await page.evaluate(()=>window.dispatchEvent(new Event('afterprint')));
 assert.equal(await page.locator('.print-sheet:visible').count(),7);
 if(output){
  await mkdir(output,{recursive:true});
  for(const file of ['access','medications','quick-reference','tbi']){
   await visit(page,file+'.html');
   if(file==='access')await page.locator('#full-infusion-list').evaluate(e=>e.scrollIntoView());
   if(file==='medications')await page.locator('#d-ketamine').evaluate(e=>e.scrollIntoView());
   if(file==='tbi')await page.locator('#pressure-and-recovery-gates').evaluate(e=>e.scrollIntoView());
   if(file==='quick-reference')await page.locator('[data-sheet="M1 / 3"]').evaluate(e=>e.scrollIntoView());
   await page.screenshot({path:resolve(output,file+'-mobile.png')});
  }
  await visit(page,'quick-reference.html');await page.setViewportSize({width:1440,height:1000});
  for(const format of ['A4','Letter'])await page.pdf({path:resolve(output,'quick-reference-'+format+'.pdf'),format,landscape:true,preferCSSPageSize:true,printBackground:false});
 }
 assert.deepEqual(errors,[],'No page script errors');
 const plain=await browser.newPage({javaScriptEnabled:false,viewport:{width:320,height:740}});
 await visit(plain,'access.html');assert.deepEqual(await plain.evaluate(overflow),[],'No-JS mobile tables fit');
 assert(await plain.locator('.mobile-column-label:visible').count()>0,'No-JS tables retain labels');
 await visit(plain,'quick-reference.html');assert.equal(await plain.locator('.print-sheet').count(),7);
 await plain.emulateMedia({media:'print'});assert.equal(await plain.locator('.print-sheet:visible').count(),7);
 await plain.close();
 console.log('Passed mobile row reflow, enlarged text, 33 medication entries, 13 rhythms, all print buttons, selection/reset and no-JS fallbacks.');
}finally{await browser.close()}
