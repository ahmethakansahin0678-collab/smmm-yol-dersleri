const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] }); const p = await b.newPage({ viewport: { width: 390, height: 844 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type()==='error' && errs.push(m.text()));
  await p.goto('http://localhost:8766/index.html'); await p.waitForTimeout(1000);
  await p.click('#tab-soru'); await p.waitForTimeout(200);
  console.log((await p.$$eval('#qKaynak button', x => x.map(b => b.textContent))).join(', '));
  console.log((await p.$$eval('#qDers button', x => x.map(b => b.textContent))).join(', '));
  await p.click('#qDers button:nth-child(6)'); await p.waitForTimeout(200);
  console.log(await p.textContent('#qMeta'), await p.textContent('#qPos'), '|', await p.textContent('#qTitle'), '|', (await p.textContent('#qText')).slice(0,90));
  await p.click('#qPlay'); await p.waitForTimeout(2500); console.log('play', (await p.textContent('#qText')).slice(0,60));
  await p.click('#qAns'); await p.waitForTimeout(1500); console.log('ans', (await p.textContent('#qText')).slice(0,80));
  await p.click('#tab-dinle'); const days = await p.$$eval('#dayPick button', x => x.map(b => b.textContent)); console.log(days.slice(22).join(' | '));
  await p.screenshot({ path: '/tmp/claude-0/soru2.png' });
  console.log('errors', errs, await p.evaluate(() => document.documentElement.scrollWidth)); await b.close();
})();
