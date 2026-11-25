#!/bin/bash
# Yeni konteynerde çalışma ortamını depodan yeniden kurar.
# Kullanım: bash /home/user/smmm-yol-dersleri/kaynak/kurulum.sh
set -e
REPO=/home/user/smmm-yol-dersleri
W=/home/user/smmm
mkdir -p $W/site/ses $W/pwa /tmp/tts
cp -r $REPO/kaynak/metin $REPO/kaynak/build $REPO/kaynak/pwa-kaynak $REPO/kaynak/test $W/
cp $REPO/kaynak/GECE-PLANI-2.md $W/ 2>/dev/null || true
cp $REPO/kaynak/site-index.html $W/site/index.html
cp $REPO/ses/*.mp3 $W/site/ses/
pip install -q sherpa-onnx==1.12.40 soundfile pdfplumber
cd /tmp/tts
for v in tr_TR-fahrettin-medium en_US-lessac-medium; do
  [ -d vits-piper-$v ] || { curl -sL -o $v.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-$v.tar.bz2 && tar xjf $v.tar.bz2; }
done
cd $W && node build/build.js && python3 build/zaman_isle.py && python3 build/pwa_build.py
echo "Kurulum tamam."
