// SMMM Yol Dersleri — çevrimdışı çalışma (service worker)
// Uygulama dosyaları: önce ağ (3 sn), yoksa önbellek. Ses dosyaları: telefona indirildiyse önbellekten,
// iPhone'un istediği parça parça (Range) okumayı destekleyerek.
const SURUM = 'v4';
const KABUK = 'kabuk-' + SURUM;
const SES = 'ses-v1';
const KABUK_DOSYALARI = ['./', 'index.html', 'dersler.json', 'manifest.webmanifest', 'icon-180.png', 'icon-192.png', 'icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(KABUK).then(c => c.addAll(KABUK_DOSYALARI)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('kabuk-') && k !== KABUK).map(k => caches.delete(k)))));
  self.clients.claim();
});

function zamanAsimi(ms) { return new Promise((_, rej) => setTimeout(() => rej(new Error('zaman aşımı')), ms)); }

self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  if (u.origin !== location.origin) {
    // Yazı tipleri: önbellekte varsa oradan, yoksa ağdan alıp sakla
    if (/fonts\.(googleapis|gstatic)\.com$/.test(u.hostname)) {
      e.respondWith(caches.open('font-v1').then(c => c.match(e.request).then(r => r || fetch(e.request).then(n => { if (n.ok || n.type === 'opaque') c.put(e.request, n.clone()); return n; }))).catch(() => new Response('', { status: 200, headers: { 'Content-Type': u.hostname.startsWith('fonts.googleapis') ? 'text/css' : 'font/woff2' } })));
    }
    return;
  }
  if (u.pathname.endsWith('.mp3')) { e.respondWith(ses(e.request)); return; }
  e.respondWith(
    Promise.race([fetch(e.request), zamanAsimi(3000)])
      .then(r => { if (r && r.ok) { const k = r.clone(); caches.open(KABUK).then(c => c.put(e.request, k)); } return r; })
      .catch(() => caches.match(e.request, { ignoreSearch: true }).then(r => r || caches.match('index.html')))
  );
});

async function ses(req) {
  const url = req.url.split('#')[0].split('?')[0];
  const c = await caches.open(SES);
  const tam = await c.match(url);
  if (!tam) return fetch(req);
  const aralik = req.headers.get('range');
  if (!aralik) return tam;
  const buf = await tam.arrayBuffer();
  const boy = buf.byteLength;
  const m = /bytes=(\d*)-(\d*)/.exec(aralik) || [];
  let bas = m[1] ? parseInt(m[1], 10) : 0;
  let son = m[2] ? parseInt(m[2], 10) : boy - 1;
  if (!m[1] && m[2]) { bas = Math.max(0, boy - parseInt(m[2], 10)); son = boy - 1; }
  son = Math.min(son, boy - 1);
  return new Response(buf.slice(bas, son + 1), {
    status: 206,
    headers: { 'Content-Type': 'audio/mpeg', 'Content-Range': `bytes ${bas}-${son}/${boy}`, 'Content-Length': String(son - bas + 1), 'Accept-Ranges': 'bytes' }
  });
}
