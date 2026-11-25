# Tüm dersleri Fahrettin sesiyle MP3'e çevirir ve segment zaman damgalarını kaydeder.
# Çıktı: /home/user/smmm/site/ses/<id>.mp3 ve /home/user/smmm/site/zaman.json
# Kullanım: python3 toplu_seslendir.py [--yalniz id1,id2]
import sys, json, glob, os, subprocess, tempfile, argparse, time, hashlib
import numpy as np, soundfile as sf, sherpa_onnx

ap = argparse.ArgumentParser(); ap.add_argument('--yalniz', default=''); ap.add_argument('--parca', default='0/1')
a = ap.parse_args()
ROOT = '/home/user/smmm'; OUT = ROOT + '/site/ses'; os.makedirs(OUT, exist_ok=True)
SR = 22050; HIZ = 0.95

def load(name):
    d = glob.glob(f'/tmp/tts/vits-piper-*{name}*')[0]
    cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=glob.glob(d + '/*.onnx')[0], tokens=d + '/tokens.txt', data_dir=d + '/espeak-ng-data'),
        num_threads=2))
    return sherpa_onnx.OfflineTts(cfg)
tr, en = load('tr_TR-fahrettin'), load('en_US-lessac')

def say(t, lang):
    g = (en if lang == 'en' else tr).generate(t, sid=0, speed=HIZ)
    x = np.asarray(g.samples, dtype=np.float32)
    if g.sample_rate != SR:
        x = np.interp(np.linspace(0, len(x), int(len(x) * SR / g.sample_rate), endpoint=False), np.arange(len(x)), x).astype(np.float32)
    m = np.max(np.abs(x)) or 1
    return (x / m * 0.85).astype(np.float32)
def sil(s): return np.zeros(int(SR * s), dtype=np.float32)
t_ = np.arange(int(SR * 0.22)) / SR
env = np.minimum(1, np.minimum(t_ / 0.02, (0.22 - t_) / 0.08))
BIP = np.concatenate([0.3 * np.sin(2 * np.pi * 880 * t_) * env, sil(0.05), 0.3 * np.sin(2 * np.pi * 1320 * t_) * env, sil(0.3)]).astype(np.float32)

D = json.load(open(ROOT + '/site/dersler.json'))
ders = D['dersler']
if a.yalniz: ders = [l for l in ders if l['id'] in a.yalniz.split(',')]
k, n = map(int, a.parca.split('/')); ders = ders[k::n]
zaman_yolu = ROOT + f'/build/zaman-{k}.json'
zaman = json.load(open(zaman_yolu)) if os.path.exists(zaman_yolu) else {}

for L in ders:
    mp3 = f"{OUT}/{L['id']}.mp3"
    sig = hashlib.md5(json.dumps(L["seg"], ensure_ascii=False).encode()).hexdigest()
    if os.path.exists(mp3) and zaman.get(L['id'], {}).get('sig') == sig: continue
    t0 = time.time()
    parts = [say(L['title'] + '.', 'tr'), sil(0.8)]; pos = sum(len(p) for p in parts); ts = []
    for s in L['seg']:
        ts.append(round(pos / SR, 2))
        if s.get('b'): chunk = [sil(0.2), BIP]
        elif s.get('p'): chunk = [sil(s['p'])]
        else: chunk = [say(s['s'], s['l']), sil(0.55 if s['l'] == 'tr' else 0.7)]
        parts += chunk; pos += sum(len(c) for c in chunk)
    audio = np.concatenate(parts)
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as w:
        sf.write(w.name, audio, SR)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', w.name, '-ac', '1', '-ar', '22050', '-b:a', '32k', mp3], check=True)
    os.unlink(w.name)
    zaman[L['id']] = {'sig': sig, 't': ts, 'sure': round(len(audio) / SR, 1)}
    json.dump(zaman, open(zaman_yolu, 'w'))
    print(L['id'], round(len(audio) / SR / 60, 1), 'dk', round(time.time() - t0), 'sn', flush=True)
print('BİTTİ', k)
