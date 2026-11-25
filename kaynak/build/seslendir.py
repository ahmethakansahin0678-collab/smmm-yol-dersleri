# Ders segmentlerini (dersler.json) MP3'e çevirir. Çevrimdışı: sherpa-onnx + piper sesleri.
# Kullanım: python3 seslendir.py <ders_id> <cikti.mp3> [--tr fahrettin] [--en lessac] [--from N] [--to N]
import sys, json, glob, argparse, subprocess, os, tempfile
import numpy as np, soundfile as sf, sherpa_onnx

ap = argparse.ArgumentParser()
ap.add_argument('ders'); ap.add_argument('out')
ap.add_argument('--tr', default='fahrettin'); ap.add_argument('--en', default='lessac')
ap.add_argument('--from', dest='f', type=int, default=0); ap.add_argument('--to', type=int, default=None)
ap.add_argument('--hiz', type=float, default=0.95)
ap.add_argument('--json', default='/home/user/smmm/site/dersler.json')
a = ap.parse_args()

def load(name):
    d = glob.glob(f'/tmp/tts/vits-piper-*{name}*')[0]
    cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=glob.glob(d + '/*.onnx')[0], tokens=d + '/tokens.txt', data_dir=d + '/espeak-ng-data'),
        num_threads=4))
    return sherpa_onnx.OfflineTts(cfg)

tr, en = load('tr_TR-' + a.tr), load('en_US-' + a.en)
SR = 22050
def say(t, lang):
    g = (en if lang == 'en' else tr).generate(t, sid=0, speed=a.hiz)
    x = np.asarray(g.samples, dtype=np.float32)
    if g.sample_rate != SR:
        x = np.interp(np.linspace(0, len(x), int(len(x) * SR / g.sample_rate), endpoint=False), np.arange(len(x)), x).astype(np.float32)
    return x
def sil(s): return np.zeros(int(SR * s), dtype=np.float32)
def bip():
    t = np.arange(int(SR * 0.22)) / SR
    env = np.minimum(1, np.minimum(t / 0.02, (0.22 - t) / 0.08))
    b1 = 0.3 * np.sin(2 * np.pi * 880 * t) * env; b2 = 0.3 * np.sin(2 * np.pi * 1320 * t) * env
    return np.concatenate([b1, sil(0.05), b2, sil(0.3)]).astype(np.float32)

D = json.load(open(a.json))
L = next(l for l in D['dersler'] if l['id'] == a.ders)
parts = [say(L['title'] + '.', 'tr'), sil(0.8)]
for s in L['seg'][a.f:a.to]:
    if s.get('b'): parts += [sil(0.2), bip()]
    elif s.get('p'): parts.append(sil(s['p']))
    else: parts += [say(s['s'], s['l']), sil(0.55 if s['l'] == 'tr' else 0.7)]
audio = np.concatenate(parts)
peak = np.max(np.abs(audio)) or 1
audio = (audio / peak * 0.9).astype(np.float32)
with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as w:
    sf.write(w.name, audio, SR)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', w.name, '-ac', '1', '-b:a', '64k', a.out], check=True)
os.unlink(w.name)
print(a.out, round(len(audio) / SR / 60, 1), 'dk')
