# Gece çalışması 2 (26 Kasım 01:40 → 07:00, kesintisiz)

## Kural
- 01:40'ta başla, 07:00'ye kadar durmadan çalış. Her değişiklikten sonra test et (test/e2e.js), geçerse yayınla.
- Yayın = (1) GitHub deposu `smmm-yol-dersleri` (telefondaki uygulama), (2) Claude artifact 3R8wQkKcyDCB2mu8Qusdux.
- Konteyner yenilenmişse önce `kaynak/kurulum.sh` ile ortamı kur.
- 06:40'ta son test + yayın + kullanıcıya sabah özeti.

## Akış (her yeni/değişen ders için)
1. metin/*.txt yaz veya düzelt
2. `node build/build.js` → `python3 build/toplu_seslendir.py --yalniz <id> --parca 0/2` (ve 1/2) → `python3 build/zaman_isle.py`
3. `python3 build/pwa_build.py`
4. Sunucular: site → `npx http-server -p 8766 -s -c-1`, pwa → 8767
5. `node test/e2e.js http://localhost:8766/index.html` ve `... 8767 ...` → ikisi de GEÇTİ olmalı
6. pwa/ → depo kopyala, commit, push; artifact'e index.html + dersler.json + yeni ses dosyaları

## Yapılacaklar (sırayla)
- [x] A. 320 çıkmış soruyu konu konu sınıflandır → `kaynak/analiz-2026.md` (ders → konu → soru sayısı, hangi derste/dersimizde karşılığı var mı)
- [x] B. Analizde karşılığı olmayan/zayıf konular için yeni ders bölümleri (her ders için en sık çıkan eksik konulardan başla). Her bölüm: anlatım + örnek + 2 soru + özet. Sayılar yazıyla.
- [x] C. Çıkmış soruların okunuşunu denetle: tablolu sorular (14 sn bekleme) tekrar okunaklı mı; "Bay (D)" gibi ifadeler, kısaltmalar, ₺ ekleri. Gerekirse cikmis_metin.py düzelt, cs-* yeniden seslendir.
- [x] D. Program: yeni bölümleri günlere yerleştir; Program sekmesine "2026 sınav analizi" özeti (ders başına en çok çıkan konular).
- [x] E. Soru-Cevap: yanlış cevapladığım soruları işaretleme ("Tekrar sor" listesi) — localStorage ile.
- [ ] F. Tam regresyon testi + yayın + sabah özeti.

## Notlar
- Çıkmış soru PDF'leri yalnızca bu konteynerde: /tmp/claude-0/cikmis/dosyalar (kamuya açık depoya KOYMA). Çıkarılmış hali: build/cikmis-sorular-2026.json.
- Ses: Fahrettin (tr_TR-fahrettin-medium) + lessac (İngilizce), sherpa-onnx 1.12.40, /tmp/tts altında.

## Ek (01:50)
- [x] 2025/3 klasik sınav (5 ders) eklendi: cs-0X-2025-3, komisyon cevaplarıyla. Testler geçti, yayında (GitHub + artifact v28).

- [x] 02:00 yayın: 5 yeni ders (07-b4, 04-b5, 06-b10, 05-b13, 08-b5) Gün 23-24; Meslek düzeltmeleri seslendirildi; Tekrar sor listesi; 2026 analizi Program sekmesinde; ses ?v= sürüm etiketi (eski indirilen sesler temizlenir). GitHub 4dcc215, artifact v29.
- [x] 03:00 yayın: çıkmış soru okunuşu düzeltildi (37 yanlış-tipi soruya ön ek, boşluk/(i)/(+)/(-)/%/eksi sayılar, A.Ş., 4/a, tarihler, kg); FTA tablo sorularına formül notu; 3 yeni ders (01-b13 kayıt mantıkları, 03-b7 maliyet hesapları, 02-b6 hedef soruları) Gün 25; 07-b4'e SMG tuzakları. Artifact v30.
- [x] 02:25 yayın: Müfredat/analizden dokunarak ders çalma; Soru-Cevap sorular arası durdurmadan geçiş (iPhone kilit ekranı). Kısaltma okunuşu test edildi (cümle içinde sorun yok). GitHub 08916d4, artifact v32.
