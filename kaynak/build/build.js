// Ders metinlerini ve soru bankasını uygulamanın okuyacağı tek bir JSON'a çevirir.
// Kullanım: node build/build.js  ->  site/dersler.json
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..');
const METIN = path.join(ROOT, 'metin');
const OUT = path.join(ROOT, 'site', 'dersler.json');

const DERS_ADI = {
  '00': 'Başlarken', '01': 'Finansal Muhasebe', '02': 'Finansal Tablolar ve Analizi',
  '03': 'Maliyet Muhasebesi', '04': 'Muhasebe Denetimi', '05': 'Vergi Mevzuatı',
  '06': 'Hukuk', '07': 'Meslek Hukuku', '08': 'Sermaye Piyasası Mevzuatı', 'en': 'Mesleki İngilizce'
};

function parse(text) {
  const lines = text.split(/\r?\n/);
  let title = '';
  const seg = [];
  let buf = [];
  const flush = () => { if (buf.length) { seg.push({ l: 'tr', s: buf.join(' ') }); buf = []; } };
  for (let raw of lines) {
    const line = raw.trim();
    if (line.startsWith('BAŞLIK:')) { title = line.slice(7).trim(); continue; }
    if (!line) { flush(); continue; }
    let m;
    if ((m = line.match(/^\[\[(\d+)\]\]$/))) { flush(); seg.push({ p: +m[1] }); continue; }
    if (line === '[[bip]]') { flush(); seg.push({ b: 1 }); continue; }
    if (line.startsWith('EN:')) { flush(); seg.push({ l: 'en', s: line.slice(3).trim() }); continue; }
    buf.push(line);
  }
  flush();
  return { title, seg };
}

const lessons = [];
for (const f of fs.readdirSync(METIN).filter(f => f.endsWith('.txt')).sort()) {
  const { title, seg } = parse(fs.readFileSync(path.join(METIN, f), 'utf8'));
  const id = f.replace(/\.txt$/, '');
  // dosya adı: NN-..., NN-bM-... (ders NN, bölüm M), en-NN-..., sb-...
  let modul = 'smmm', ders = id.slice(0, 2);
  if (id.startsWith('en-')) { modul = 'en'; ders = 'en'; }
  if (id.startsWith('cs-')) { modul = 'cikmis'; ders = id.slice(3, 5); }
  const words = seg.filter(s => s.s).reduce((a, s) => a + s.s.split(/\s+/).length, 0);
  const pauses = seg.filter(s => s.p).reduce((a, s) => a + s.p, 0);
  lessons.push({ id, modul, ders, dersAdi: DERS_ADI[ders] || '', title, dk: Math.round(words / 130 + pauses / 60), seg });
}

// --- Soru bankası (Drive: smmm_exam_mobile.html) ---
const qs = require('./soru-bankasi-drive.js');
const inc = require('./inceleme.js');
const KONU = { finansal: 'Finansal Muhasebe', vergi: 'Vergi Mevzuatı', maliye: 'Maliyet Muhasebesi', denetim: 'Muhasebe Denetimi', hukuk: 'Hukuk', spk: 'Sermaye Piyasası Mevzuatı' };
const HARF = ['A', 'B', 'C', 'D', 'E'];
const DURUM = { dogru: 'Cevap anahtarı doğru.', duzeltildi: 'Dikkat, bu sorunun cevap anahtarı hatalı, düzeltiyorum.', hatali: 'Dikkat, bu soru hatalı kurgulanmış.' };
const clean = s => s.replace(/%(\d+)/g, 'yüzde $1').replace(/\bTTK\b/g, 'Türk Ticaret Kanunu').replace(/\bKDV\b/g, 'kadeve').replace(/\bSPK\b/g, 'Sermaye Piyasası Kurulu').replace(/\(ABC\)/g, '').replace(/ATM/g, 'bankamatik').replace(/Break-even/g, 'Başabaş').replace(/\bvb\./g, 've benzeri');
const soruBanka = [];
let sira = 0;
for (const k of Object.keys(KONU)) {
  const list = qs.filter(q => q.subject === k);
  const seg = [{ l: 'tr', s: `Soru bankası: ${KONU[k]}. Bu bölümde Drive'ındaki soru bankasından ${list.length} soru var. Her soruda zil sesinden sonra düşünme süresi var, ikinci zilden sonra cevabı ve değerlendirmeyi duyacaksın. Bu sorular gerçek çıkmış sınav soruları değil; bu yüzden her birini kontrol ettim ve yanlış olanları düzelttim.` }];
  list.forEach((q, i) => {
    const r = inc[q.id];
    seg.push({ b: 1 });
    seg.push({ l: 'tr', s: `Soru ${i + 1}. ${clean(q.text)}` });
    q.options.forEach((o, j) => seg.push({ l: 'tr', s: `${HARF[j]} şıkkı: ${clean(o)}.` }));
    seg.push({ p: 7 });
    seg.push({ b: 1 });
    if (r.durum === 'dogru') seg.push({ l: 'tr', s: `Doğru cevap ${HARF[r.dogru]} şıkkı: ${clean(q.options[r.dogru])}.` });
    else if (r.durum === 'duzeltildi') {
      seg.push({ l: 'tr', s: `${DURUM.duzeltildi} Dosyandaki cevap ${HARF[q.correct]} şıkkı olarak işaretlenmiş.` + (r.dogru != null ? ` Doğrusu ${HARF[r.dogru]} şıkkı: ${clean(q.options[r.dogru])}.` : ' Şıkların hiçbiri tam doğru değil.') });
    } else seg.push({ l: 'tr', s: DURUM.hatali });
    seg.push({ l: 'tr', s: r.aciklama });
    seg.push({ p: 1 });
  });
  const ozet = list.filter(q => inc[q.id].durum !== 'dogru').length;
  seg.push({ l: 'tr', s: `${KONU[k]} soru bankası bitti. Bu bölümdeki ${list.length} sorudan ${ozet} tanesinde düzeltme ya da uyarı vardı. Bu düzeltmeleri özellikle aklında tut, çünkü yanlış öğrenilen bilgi sınavda en pahalı hatadır.` });
  sira++;
  const words = seg.filter(s => s.s).reduce((a, s) => a + s.s.split(/\s+/).length, 0);
  soruBanka.push({ id: 'sb-' + k, modul: 'soru', ders: k, dersAdi: KONU[k], title: `Soru Bankası ${sira}. ${KONU[k]}`, dk: Math.round(words / 130 + list.length * 8 / 60), seg });
}

// Ekranda gösterilecek soru tablosu
const tablo = qs.map(q => ({ id: q.id, konu: KONU[q.subject], soru: q.text, siklar: q.options, eski: q.correct, ...inc[q.id] }));

fs.mkdirSync(path.dirname(OUT), { recursive: true });
const all = [...lessons, ...soruBanka];
const program = require('./program.js');
for (const l of all) { const i = l.seg.findIndex(s => s.b); l.tekrar = i < 0 ? 0 : i; }
for (const l of all) { const i = l.seg.findIndex(s => s.s && /^(Şimdi )?(Dersin özeti|dersin özetine|Harika\. Bugünkü özet|Bugünkü özet)/i.test(s.s)); l.ozet = i < 0 ? l.tekrar : i; }
// --- Çıkmış soru günleri: her ders için bir gün (sabah 2026-1, akşam 2026-2 + o dersin özetleri)
{
  const cs = all.filter(l => l.modul === 'cikmis');
  const dersler = [...new Set(cs.map(l => l.ders))].sort();
  dersler.forEach(d => {
    const sets = cs.filter(l => l.ders === d).sort((a, b) => a.id.localeCompare(b.id));
    const ozet = all.filter(l => l.modul === 'smmm' && l.ders === d && !/-seti$|-set$|-numaralari$/.test(l.id)).map(l => l.id + '@ozet');
    program.gunler.push({ ad: 'Çıkmış: ' + (sets[0].dersAdi), not: `Gerçek sınav soruları (${sets.map(x => x.id.slice(-6)).join(', ')}). Şıklar okunmaz: soru, düşünme süresi, cevap.`,
      sabah: [sets[0].id, ...ozet.slice(0, Math.ceil(ozet.length / 2))], aksam: [...sets.slice(1).map(x => x.id), ...ozet.slice(Math.ceil(ozet.length / 2))] });
  });
}
// --- Karışık deneme: tüm SMMM derslerindeki soruları dersler arası karıştır ---
{
  const blocksBy = {};
  for (const l of all.filter(x => x.modul === 'smmm' && x.id !== '00-baslarken' && !/(-seti|-set|-numaralari|-stratejisi)$/.test(x.id))) {
    const end = l.ozet > l.tekrar ? l.ozet : l.seg.length;
    const bips = []; for (let i = l.tekrar; i < end; i++) if (l.seg[i].b) bips.push(i);
    for (let k = 0; k < bips.length; k += 2) {
      const st = bips[k], en = k + 2 < bips.length ? bips[k + 2] : end;
      const seg = l.seg.slice(st, en).filter(x => !(x.s && /^(Bir soru daha|Şimdi sınav tarzında bir soru)\.?$/.test(x.s.trim())));
      (blocksBy[l.ders] = blocksBy[l.ders] || []).push({ ders: l.dersAdi, seg });
    }
  }
  const keys = Object.keys(blocksBy).sort(); const mixed = [];
  let more = true; for (let r = 0; more; r++) { more = false; for (const k of keys) if (blocksBy[k][r]) { mixed.push(blocksBy[k][r]); more = true; } }
  const SIZE = 15, den = [];
  for (let i = 0; i < mixed.length; i += SIZE) {
    const part = mixed.slice(i, i + SIZE), n = den.length + 1;
    const seg = [{ l: 'tr', s: `Karışık deneme ${n}. Bu bölümde farklı derslerden ${part.length} soru var, tıpkı sınavdaki gibi konudan konuya atlayacağız. Her sorudan önce dersin adını söyleyeceğim.` }];
    part.forEach((b, j) => { seg.push({ l: 'tr', s: `Soru ${j + 1}. ${b.ders}.` }); seg.push(...b.seg); });
    seg.push({ l: 'tr', s: `Karışık deneme ${n} bitti. Yanlış yaptığın soruların derslerini akşam tekrar listesinden yeniden dinle.` });
    const words = seg.filter(x => x.s).reduce((a, x) => a + x.s.split(/\s+/).length, 0), pz = seg.filter(x => x.p).reduce((a, x) => a + x.p, 0);
    const d = { id: 'deneme-' + n, modul: 'soru', ders: 'deneme', dersAdi: 'Karışık Deneme', title: `Karışık Deneme ${n}`, dk: Math.round(words / 130 + pz / 60), seg, tekrar: 0, ozet: 0 };
    den.push(d);
  }
  all.push(...den);
  const h = Math.ceil(den.length / 2);
  program.gunler.push({ ad: 'Deneme', not: `Tüm derslerden ${mixed.length} soru, ${den.length} karışık deneme halinde. Sınav provası için.`, sabah: ['00-b2-sinav-stratejisi', ...den.slice(0, h).map(d => d.id)], aksam: den.slice(h).map(d => d.id) });
}
// Ayrı İngilizce günü: tüm İngilizce bölümler
{
  const en = all.filter(l => l.modul === 'en');
  const h = Math.ceil(en.length / 2);
  program.gunler.push({ ad: 'İngilizce', not: 'Sadece mesleki İngilizce: terim, Türkçesi, İngilizce cümle, cümlenin Türkçesi. İstediğin gün ayrıca dinle.', sabah: en.slice(0, h).map(l => l.id), aksam: en.slice(h).map(l => l.id) });
}
const bno = id => { const m = id.match(/-b(\d+)-/); return m ? +m[1] : 1; };
// Hızlı tekrar günü: tüm özetler (soru bankaları hariç)
{
  const smmm = all.filter(l => l.modul === 'smmm' && l.id !== '00-baslarken').sort((a, b) => a.ders.localeCompare(b.ders) || bno(a.id) - bno(b.id));
  const en = all.filter(l => l.modul === 'en');
  const half = Math.ceil(smmm.length / 2);
  program.gunler.push({ ad: 'Hızlı Tekrar', not: 'Tüm derslerin sadece özet kısımları. Sınavdan önceki son günler ve kısa yollar için.',
    sabah: smmm.slice(0, half).map(l => l.id + '@ozet'), aksam: [...smmm.slice(half), ...en].map(l => l.id + '@ozet') });
}
const ids = new Set(all.map(l => l.id));
for (const g of program.gunler) for (const x of [...g.sabah, ...g.aksam]) if (!ids.has(x.split('@')[0])) throw new Error('planda olmayan ders: ' + x);
fs.writeFileSync(OUT, JSON.stringify({ surum: new Date().toISOString(), dersler: all, sorular: tablo, program }));
console.log('ders:', lessons.length, 'soru bankası:', soruBanka.length, 'toplam dk:', [...lessons, ...soruBanka].reduce((a, l) => a + l.dk, 0), 'boyut KB:', Math.round(fs.statSync(OUT).size / 1024));
