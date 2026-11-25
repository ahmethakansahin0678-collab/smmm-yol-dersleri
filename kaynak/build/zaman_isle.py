# Seslendirme zaman damgalarını dersler.json'a işler (yalnızca metni değişmemiş dersler için).
# Sıra: node build/build.js -> python3 build/toplu_seslendir.py -> python3 build/zaman_isle.py
import json, glob, hashlib, os
ROOT = '/home/user/smmm'
D = json.load(open(ROOT + '/site/dersler.json'))
Z = {}
for f in glob.glob(ROOT + '/build/zaman-*.json'):
    Z.update(json.load(open(f)))
ok = eksik = 0
for L in D['dersler']:
    z = Z.get(L['id'])
    sig = hashlib.md5(json.dumps(L['seg'], ensure_ascii=False).encode()).hexdigest()
    if z and z['sig'] == sig and os.path.exists(f"{ROOT}/site/ses/{L['id']}.mp3"):
        L['zaman'] = z['t']; L['sure'] = z['sure']; L['dk'] = round(z['sure'] / 60); ok += 1
    else:
        L.pop('zaman', None); eksik += 1
json.dump(D, open(ROOT + '/site/dersler.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('sesli:', ok, 'sessiz:', eksik, 'toplam ses saati:', round(sum(L.get('sure', 0) for L in D['dersler']) / 3600, 1))
