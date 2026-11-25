# Çıkmış soruları konulara ayırır, uygulamadaki derslerle eşleştirir ve analiz üretir.
# Çıktı: build/analiz-2026.json (uygulama okur) ve kaynak/analiz-2026.md
import json, re, collections, sys
Q = json.load(open('/home/user/smmm/build/cikmis-sorular-2026.json'))

# (konu adı, regex, uygulamadaki ilgili ders id'leri)
K = {
 'Vergi Mevzuatı': [
  ('Gelir vergisi', r'193 sayılı|Gelir Vergisi|geçici vergi', ['05-vergi', '05-b4-gelir-vergisi', '05-b10-gmsi-msi']),
  ('Katma değer vergisi', r'3065|Katma Değer|KDV', ['05-vergi', '05-b5-kadeve-istisna-tevkifat']),
  ('Kurumlar vergisi', r'5520|Kurumlar Vergisi', ['05-b3-kurumlar-vergisi']),
  ('Vergi Usul Kanunu: ceza, pişmanlık, zamanaşımı, değerleme', r'213 sayılı|Vergi Usul', ['05-b2-vuk-defter-ceza', '05-b8-degerleme', '05-b9-uzlasma-dava']),
  ('Amme alacaklarının tahsili (6183)', r'6183|Amme', ['05-b7-6183-tahsil']),
  ('ÖTV, damga, MTV, emlak, veraset, harç', r'4760|Özel Tüketim|488 sayılı|Damga|197 sayılı|Motorlu Taşıtlar|1319|Emlak|7338|Veraset|492|Harç', ['05-b6-otv-damga-harc']),
 ],
 'Hukuk': [
  ('İdari yargılama usulü (2577)', r'2577|İdari Yargılama|idari yargı|Danıştay|idare mahkeme', []),
  ('İş hukuku', r'4857|İş Kanunu|işçi|işveren|kıdem|ihbar|telafi|fazla çalışma|yıllık izin', ['06-b2-is-hukuku']),
  ('Sosyal güvenlik', r'5510|sigortalı|Sosyal Güvenlik|prim', ['06-b5-sosyal-guvenlik']),
  ('Kıymetli evrak (çek, bono, poliçe)', r'kıymetli evrak|zayi|çek|bono|poliçe|ciro|aval|kambiyo|keşide', ['06-b3-kiymetli-evrak']),
  ('Şirketler hukuku', r'anonim|limited|şirket|genel kurul|yönetim kurulu|pay sahibi|sermaye|kollektif|komandit|birleşme|bölünme|tür değiştirme', ['06-hukuk', '06-b4-anonim-sirket']),
  ('Tacir, ticari işletme, ticaret sicili', r'tacir|ticari işletme|ticaret unvanı|ticaret sicili|ticari defter|acente|cari hesap', ['06-hukuk', '06-b8-ticaret-unvani-sicil']),
  ('İcra ve iflas', r'2004 sayılı|İcra|İflas|haciz|konkordato|ödeme emri|takip', ['06-b6-icra-iflas']),
  ('Borçlar hukuku', r'6098|Borçlar Kanunu|sözleşme|zamanaşımı|kefalet|temerrüt|haksız fiil|vekalet|kira', ['06-b7-borclar-genel']),
 ],
 'Meslek Hukuku': [
  ('Disiplin cezaları ve süreç', r'disiplin|uyarma|kınama|meslekten (geçici )?men|alıkonulma|meslekten çıkarma', ['07-b3-turmob-disiplin', '07-meslek-hukuku']),
  ('Etik ilkeler ve tehditler', r'etik|tehdit|tarafsızlık|objektif|önlem', []),
  ('Haksız rekabet ve reklam yasağı', r'haksız rekabet|reklam', ['07-b2-meslek-ahlaki']),
  ('Oda ve TÜRMOB örgütlenmesi', r'Oda|Birli[kğ]|TÜRMOB|Genel Kurul|Yönetim Kurulu|organ|aidat|gelir', ['07-b3-turmob-disiplin']),
  ('Meslek mensubu olma, staj, sınav, sürekli eğitim', r'şart|staj|sınav|kredi|eğitim|ruhsat', ['07-meslek-hukuku']),
  ('Çalışma usulleri, sözleşme, ücret', r'sözleşme|ücret|işyeri|iş yeri|çalışma usul|bağdaşma|ticari faaliyet|belge', ['07-b2-meslek-ahlaki']),
 ],
 'Sermaye Piyasası Mevzuatı': [
  ('Halka arz, izahname, ihraç', r'halka arz|izahname|ihraç|talep toplama|borçlanma aracı', ['08-sermaye-piyasasi', '08-b2-izahname-kurumsal-yonetim']),
  ('Kurumsal yönetim ve kamuyu aydınlatma', r'kurumsal yönetim|bağımsız (yönetim kurulu )?üye|komite|özel durum|kamuyu aydınlatma|KAP|içsel bilgi|ilişkili taraf', ['08-b2-izahname-kurumsal-yonetim']),
  ('Piyasa suçları ve yaptırımlar', r'suç|piyasa dolandırıcılığı|bilginin kötüye|güveni kötüye|idari para cezası|tedbir|yaptırım', ['08-b3-piyasa-suclari']),
  ('Yatırım kuruluşları, fonlar, kripto', r'yatırım kuruluşu|aracı kurum|fon|portföy|yatırım ortaklığı|kripto|Merkezi Kayıt|Takasbank|Borsa|Tazmin', ['08-sermaye-piyasasi']),
  ('Diğer düzenlemeler: teminat, sistemik risk, birleşme-bölünme', r'teminat|sistemik|birleşme|bölünme', []),
  ('Halka açık ortaklık, sermaye, pay alım teklifi', r'halka açık|kayıtlı sermaye|pay alım|ayrılma hakkı|sermaye artırımı|kâr payı|bedelsiz|önemli nitelikte', ['08-sermaye-piyasasi', '08-b3-piyasa-suclari']),
 ],
 'Muhasebe Denetimi': [
  ('Kalite yönetimi standartları', r'kalite', []),
  ('KGK Bağımsız Denetim Yönetmeliği: yetkilendirme, ekip, sicil, eğitim, sözleşme', r'yetkilendir|kıdemli|sorumlu denetçi|mesleki eğitim|sicil|denetim ekip|şeffaflık|sözleşme|kendi adına|kilit yönetici|kurumsal tanıtım|haksız rekabet|kısıtlama|denetim kuruluşları tarafından', []),
  ('Etik kurallar ve bağımsızlık', r'etik|bağımsızlığı|dürüstlük|tarafsızlık', ['04-b3-rapor-bagimsizlik']),
  ('Denetim raporu ve görüş', r'görüş|denetim raporu|dikkat çekilen|kilit denetim', ['04-denetim', '04-b3-rapor-bagimsizlik']),
  ('Yönetimin sorumlulukları, yazılı beyan, hile', r'ön kabul|yazılı beyan|hile|üst yönetimden sorumlu', ['04-b2-onemlilik-kanit']),
  ('Risk, önemlilik, kanıt, muhakeme', r'risk|önemlilik|kanıt|muhakeme|makul güvence|planlama|iç kontrol', ['04-denetim', '04-b2-onemlilik-kanit']),
  ('Denetimin amacı, kapsamı ve kıstası', r'kıstas|amac|kapsam|güvence|denetim talep|Türk Ticaret', ['04-denetim']),
 ],
 'Finansal Muhasebe': [
  ('TMS/TFRS uygulamaları', r'TMS|TFRS', ['01-b9-tms-tfrs']),
  ('Duran varlıklar ve amortisman', r'amortisman|demirbaş|taşıt|kamyon|bina|maddi duran|iştirak|bağlı ortaklık', ['01-b3-duran-varlik-amortisman']),
  ('Özkaynaklar ve şirket işlemleri', r'sermaye|yedek|kâr dağıtım|ihraç primi|tasfiye|birleşme|hisse senetlerini.*sat', ['01-b6-ozkaynaklar', '01-b10-birlesme-tasfiye']),
  ('Borçlanma, bono ihracı, krediler', r'ihraç ettiği|borçlanma senedi|kredi|finansman gider', ['01-b5-yabanci-kaynaklar']),
  ('Ticari alacak/borç, reeskont, şüpheli alacak', r'alacak|senet|reeskont|şüpheli|depozito|satıcı|alıcı', ['01-b2-alacaklar-reeskont', '01-b5-yabanci-kaynaklar']),
  ('Dönem sonu, tahakkuklar, karşılıklar, kur farkı', r'dönem sonu|tahakkuk|gelecek aylar|gelecek yıllar|karşılık|kambiyo|kur|vergi', ['01-b7-donem-sonu']),
  ('Stoklar, satışlar ve KDV', r'ticari mal|stok|KDV|iade|iskonto|satış', ['01-finansal-muhasebe', '01-b4-stoklar']),
  ('Hazır değerler ve menkul kıymetler', r'kasa|banka|çek|hisse senedi|menkul|tahvil|bono', ['01-b8-hazir-degerler']),
 ],
 'Finansal Tablolar ve Analizi': [
  ('İşletme sermayesi ve dönüş süreleri', r'süre|işletme sermayesi|nakit giriş|devir', ['02-b2-oranlar', '02-b5-oran-seti']),
  ('Oran analizi', r'oran|devir hızı|kârlılık|karlılık|kaldıraç|likidite|cari oran|asit', ['02-finansal-tablolar', '02-b2-oranlar', '02-b5-oran-seti']),
  ('Yatay, dikey ve trend analizi', r'dikey|yatay|trend|yüzde yöntemi|karşılaştırmalı', ['02-finansal-tablolar']),
  ('Nakit akış ve fon akım tablosu', r'nakit akış|fon akım|işletme faaliyet|yatırım faaliyet|finansman faaliyet', ['02-b3-nakit-akis']),
  ('Finansal tablolar ve TMS/TFRS', r'bilanço|gelir tablosu|TMS|TFRS|mali tablo|finansal tablo', ['02-finansal-tablolar', '01-b9-tms-tfrs']),
 ],
 'Maliyet Muhasebesi': [
  ('Safha maliyet ve eşdeğer birim', r'safha|eşdeğer|yarı mamul|fire', ['03-b3-safha-siparis']),
  ('Sipariş maliyet', r'sipariş', ['03-b3-safha-siparis']),
  ('Genel üretim giderleri ve dağıtım', r'genel üretim|GÜG|dağıtım|yükleme|gider yeri', ['03-b2-stok-gug']),
  ('Standart maliyet ve sapmalar', r'standart|sapma|fark', ['03-b4-standart-basabas']),
  ('Başabaş ve maliyet-hacim-kâr', r'başabaş|katkı payı|sabit maliyet|değişken maliyet|güvenlik payı', ['03-b4-standart-basabas']),
  ('Birleşik ürün ve yan ürün', r'birleşik|yan ürün|ortak maliyet', ['03-b5-birlesik-urun']),
  ('Üretim kayıpları ve muhasebe bilgi sistemi', r'kayıp|bozuk|bilgi sistemi', []),
  ('Stok değerleme ve maliyet kavramları', r'FIFO|ilk giren|ortalama|maliyet|direkt|işçilik|ilk madde|7/A|7A|7/B', ['03-maliyet', '03-b2-stok-gug']),
 ],
}

out = collections.OrderedDict()
for ders, kurallar in K.items():
    qs = [q for q in Q if q['ders'] == ders]
    sayac = collections.OrderedDict((k[0], {'konu': k[0], 'sayi': 0, 'dersler': k[2], 'ornek': []}) for k in kurallar)
    sayac['Diğer'] = {'konu': 'Diğer', 'sayi': 0, 'dersler': [], 'ornek': []}
    for q in qs:
        t = q['soru'] + ' ' + q['cevap']
        for ad, rx, _ in kurallar:
            if re.search(rx, t, re.I):
                sayac[ad]['sayi'] += 1; sayac[ad]['ornek'].append(f"{q['sinav']}/{q['no']}"); break
        else:
            sayac['Diğer']['sayi'] += 1; sayac['Diğer']['ornek'].append(f"{q['sinav']}/{q['no']}: {q['soru'][:90]}")
    out[ders] = {'toplam': len(qs), 'konular': sorted([v for v in sayac.values() if v['sayi']], key=lambda v: -v['sayi'])}

if '--yaz' in sys.argv:
    json.dump(out, open('/home/user/smmm/build/analiz-2026.json', 'w'), ensure_ascii=False, indent=1)
for d, v in out.items():
    print(f"\n== {d} ({v['toplam']})")
    for k in v['konular']:
        print(f"  {k['sayi']:2d}  {k['konu']}" + ('' if k['konu'] != 'Diğer' else '\n      ' + '\n      '.join(k['ornek'])))
