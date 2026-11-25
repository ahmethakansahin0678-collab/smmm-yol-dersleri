import json, glob, subprocess, tempfile, os, sys
import numpy as np, soundfile as sf, sherpa_onnx
SR=22050
def load(name, ns, nsw):
    d=glob.glob(f'/tmp/tts/vits-piper-*{name}*')[0]
    cfg=sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=glob.glob(d+'/*.onnx')[0],tokens=d+'/tokens.txt',data_dir=d+'/espeak-ng-data',noise_scale=ns,noise_scale_w=nsw),num_threads=4))
    return sherpa_onnx.OfflineTts(cfg)
D=json.load(open('/home/user/smmm/site/dersler.json'))
L=next(l for l in D['dersler'] if l['id']=='01-finansal-muhasebe')
segs=L['seg'][20:42]
t_=np.arange(int(SR*0.22))/SR; env=np.minimum(1,np.minimum(t_/0.02,(0.22-t_)/0.08))
sil=lambda s: np.zeros(int(SR*s),dtype=np.float32)
BIP=np.concatenate([0.3*np.sin(2*np.pi*880*t_)*env,sil(0.05),0.3*np.sin(2*np.pi*1320*t_)*env,sil(0.3)]).astype(np.float32)
def render(tr,en,path,af=None):
    parts=[]
    for s in segs:
        if s.get('b'): parts+=[sil(0.2),BIP]
        elif s.get('p'): parts.append(sil(min(s['p'],3)))
        else:
            g=(en if s['l']=='en' else tr).generate(s['s'],sid=0,speed=0.95); x=np.asarray(g.samples,dtype=np.float32)
            parts+=[x/(np.max(np.abs(x)) or 1)*0.85, sil(0.55)]
    a=np.concatenate(parts)
    w=tempfile.mktemp(suffix='.wav'); sf.write(w,a,SR)
    cmd=['ffmpeg','-loglevel','error','-y','-i',w]
    if af: cmd+=['-af',af,'-ar','24000']
    cmd+=['-ac','1','-b:a','48k',path]; subprocess.run(cmd,check=True); os.unlink(w)
AF=("highpass=f=70,lowpass=f=10500,"
    "equalizer=f=180:t=q:w=1:g=2,equalizer=f=3000:t=q:w=1.2:g=3,equalizer=f=6500:t=q:w=2:g=-2,"
    "acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2,"
    "loudnorm=I=-16:TP=-1.5:LRA=7")
en=load('en_US-lessac',0.667,0.8)
render(load('tr_TR-fahrettin',0.667,0.8),en,'/home/user/smmm/ornek2/A-su-anki.mp3')
render(load('tr_TR-fahrettin',0.667,0.8),en,'/home/user/smmm/ornek2/B-temiz-ses.mp3',AF)
render(load('tr_TR-fahrettin',0.45,0.6),en,'/home/user/smmm/ornek2/C-temiz-ve-kararli.mp3',AF)
print('ok')
