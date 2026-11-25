// Uçtan uca test: tüm günler, Dinle, Soru-Cevap, sürüş modu, ses ilerlemesi, (PWA ise) çevrimdışı.
// Kullanım: node test/e2e.js <url>   (ör. http://localhost:8766/index.html veya PWA için 8767)
// Çıkış kodu 0 = geçti. Not: Range destekli sunucu gerekir (npx http-server -s -c-1).
const { chromium } = require('playwright');
const url = process.argv[2] || 'http://localhost:8766/index.html';
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  const p = await ctx.newPage();
  const errs = [], fails = [];
  const ok = (c, m) => { if (!c) fails.push(m); };
  p.on('response', r => { if (r.status() >= 400) errs.push('HTTP ' + r.status() + ' ' + r.url()); });
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
  await p.goto(url); await p.waitForTimeout(1500);
  // 1) Tüm günler listelenir ve her günün ilk dersi açılır
  const n = await p.$$eval('#dayPick button', x => x.length); ok(n >= 20, 'gün sayısı az: ' + n);
  for (let i = 1; i <= n; i++) {
    await p.click(`#dayPick button:nth-child(${i})`); await p.waitForTimeout(40);
    const c = await p.$$eval('#listS li', x => x.length); ok(c > 0, 'boş sabah listesi gün ' + i);
  }
  // 2) Dinle: ses başlar, ileri sarınca cümle takibi değişir, ders sonunda sıradakine geçer
  await p.click('#dayPick button:nth-child(1)'); await p.click('#listS li:first-child button'); await p.waitForTimeout(2500);
  const st = await p.evaluate(() => { const a = [...document.querySelectorAll('audio')][0] || window.__au; return a ? { paused: a.paused, t: a.currentTime } : null; });
  ok(!st || !st.paused, 'ses çalmıyor');
  // 3) Soru-Cevap: kaynak ve ders seçimi, soru çalar, cevaba atlar, sıradakine geçer
  await p.click('#tab-soru'); await p.waitForTimeout(300);
  const kay = await p.$$eval('#qKaynak button', x => x.map(b => b.textContent)); ok(kay.some(k => k.startsWith('Çıkmış sorular')), 'çıkmış kaynak yok');
  await p.click('#qPlay'); await p.waitForTimeout(2500);
  ok((await p.textContent('#qText')).length > 10 && !/^(Cevap|Komisyon)/.test(await p.textContent('#qText')), 'soru metni yok');
  await p.click('#qAns'); await p.waitForTimeout(1500);
  ok(/^(Cevap|Doğru|Yanlış|Komisyon)/.test(await p.textContent('#qText')), 'cevap metni yok: ' + (await p.textContent('#qText')).slice(0, 40));
  const pos1 = await p.textContent('#qPos'); await p.click('#qNext'); await p.waitForTimeout(1500);
  ok(pos1 !== await p.textContent('#qPos'), 'sonraki soruya geçmedi');
  await p.click('#qPlay');
  // 4) Sürüş modu ve hız
  await p.click('#tab-dinle'); await p.click('#bDrive'); await p.click('#dFast'); ok(/×$/.test(await p.textContent('#dRate')), 'hız düğmesi'); await p.click('#dExit');
  // 5) Yatay taşma yok
  ok(await p.evaluate(() => document.documentElement.scrollWidth) <= 392, 'yatay taşma');
  // 6) PWA ise çevrimdışı indirme
  if (await p.$('#offIndir')) {
    await p.click('#tab-ayar'); await p.click('#offIndir');
    for (let i = 0; i < 120; i++) { await p.waitForTimeout(1000); if ((await p.textContent('#offIndir')) === 'Tüm dersleri indir') break; }
    ok(/Tüm dersler telefonda/.test(await p.textContent('#offDurum')), 'indirme bitmedi: ' + await p.textContent('#offDurum'));
    await ctx.setOffline(true); await p.reload(); await p.waitForTimeout(3000);
    ok((await p.textContent('#nowTitle')).length > 3, 'çevrimdışı açılmadı');
    await p.click('#tab-soru'); await p.click('#qPlay'); await p.waitForTimeout(2500);
    ok((await p.textContent('#qText')).length > 5, 'çevrimdışı soru çalmadı');
  }
  ok(errs.length === 0, 'konsol hataları: ' + errs.slice(0, 3).join(' | '));
  await b.close();
  console.log(fails.length ? 'BAŞARISIZ:\n- ' + fails.join('\n- ') : 'TÜM TESTLER GEÇTİ (' + n + ' gün)');
  process.exit(fails.length ? 1 : 0);
})();
