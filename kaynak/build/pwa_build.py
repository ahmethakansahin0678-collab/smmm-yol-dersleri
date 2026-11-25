# site/ (Claude sayfası) -> pwa/ (telefona kurulabilen, internetsiz çalışan sürüm)
# Kullanım: python3 build/pwa_build.py
import os, shutil, re
ROOT = '/home/user/smmm'; SRC = ROOT + '/site'; OUT = ROOT + '/pwa'; K = ROOT + '/pwa-kaynak'
os.makedirs(OUT + '/ses', exist_ok=True)

html = open(SRC + '/index.html', encoding='utf-8').read()
html = html.replace('<meta charset="utf-8">\n', '', 1)

kart = '''<div class="card" id="offCard">
      <h2>İnternetsiz kullanım</h2>
      <p id="offDurum">Dersler telefona indirilmedi. İndirince internet olmadan da çalar.</p>
      <div class="bar"><i id="offBar"></i></div>
      <div class="row2">
        <button id="offIndir">Tüm dersleri indir</button>
        <button id="offSil">İndirilenleri sil</button>
      </div>
      <p class="small">Toplam yaklaşık 100 MB. Wi-Fi'deyken bir kez indirmen yeterli. İndirme sırasında uygulama açık kalsın.</p>
    </div>
    '''
anchor = '<div class="card howto">'
assert anchor in html
html = html.replace(anchor, kart + anchor, 1)

ek_js = r'''
<script>
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(() => {});
  const SES = 'ses-v1';
  let idler = [];
  async function liste() {
    if (idler.length) return idler;
    try { const d = await (await fetch('dersler.json')).json(); idler = d.dersler.filter(l => l.zaman).map(l => 'ses/' + l.id + '.mp3'); } catch {}
    return idler;
  }
  async function durum() {
    if (!('caches' in window)) { $('offDurum').textContent = 'Bu tarayıcı internetsiz kullanımı desteklemiyor.'; return; }
    const L = await liste(); const c = await caches.open(SES); let n = 0;
    for (const u of L) if (await c.match(new URL(u, location.href).href)) n++;
    $('offDurum').textContent = n === L.length && n ? 'Tüm dersler telefonda (' + n + '/' + L.length + '). İnternet olmadan çalışır.' : n + '/' + L.length + ' ders telefonda.';
    $('offBar').style.width = L.length ? Math.round(n / L.length * 100) + '%' : '0';
  }
  let calisiyor = false;
  $('offIndir').onclick = async () => {
    if (calisiyor) return; calisiyor = true; $('offIndir').textContent = 'İndiriliyor…';
    try { if (navigator.storage && navigator.storage.persist) await navigator.storage.persist(); } catch {}
    const L = await liste(); const c = await caches.open(SES); let n = 0, hata = 0;
    for (const u of L) {
      const tam = new URL(u, location.href).href;
      if (!(await c.match(tam))) {
        try { const r = await fetch(tam, { cache: 'no-store' }); if (r.ok) await c.put(tam, r); else hata++; } catch { hata++; }
      }
      n++; $('offBar').style.width = Math.round(n / L.length * 100) + '%'; $('offDurum').textContent = 'İndiriliyor: ' + n + '/' + L.length;
    }
    calisiyor = false; $('offIndir').textContent = 'Tüm dersleri indir';
    await durum();
    if (hata) $('offDurum').textContent += ' ' + hata + ' ders indirilemedi; internet bağlantısını kontrol edip tekrar bas.';
  };
  let silOnay = false;
  $('offSil').onclick = async () => {
    if (!silOnay) { silOnay = true; $('offSil').textContent = 'Emin misin? Tekrar bas'; setTimeout(() => { silOnay = false; $('offSil').textContent = 'İndirilenleri sil'; }, 4000); return; }
    silOnay = false; $('offSil').textContent = 'İndirilenleri sil';
    await caches.delete(SES); await durum();
  };
  durum();
})();
</script>
'''

head = '''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" href="icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="SMMM Dersler">
<meta name="theme-color" content="#0f1514">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font-size:14px}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
'''
html = head + html.replace('window.__au = au;', '') + ek_js + '</body>\n</html>\n'
open(OUT + '/index.html', 'w', encoding='utf-8').write(html)

shutil.copy(SRC + '/dersler.json', OUT + '/dersler.json')
for f in ('sw.js', 'manifest.webmanifest'):
    shutil.copy(K + '/' + f, OUT + '/' + f)
for f in os.listdir(SRC + '/ses'):
    s, d = SRC + '/ses/' + f, OUT + '/ses/' + f
    if not os.path.exists(d) or os.path.getmtime(s) > os.path.getmtime(d): shutil.copy(s, d)
open(OUT + '/.nojekyll', 'w').close()
print('PWA hazır:', len(os.listdir(OUT + '/ses')), 'ses dosyası')
