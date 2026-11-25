# 2025/3 klasik (yazılı) sınav soruları + Sınav Komisyonu cevapları → sesli ders metinleri (metin/cs-XX-2025-3.txt)
# Sorular taranmış sayfalardan elle aktarıldı; cevaplar komisyon cevap anahtarından alındı. Rakamlar seslendir() ile yazıya çevrilir.
import sys
sys.path.insert(0, '/home/user/smmm/build')
from cikmis_metin import seslendir, sayi

def kayit(borc, alacak):
    b = ', '.join(f'{h} {t}' for h, t in borc); a = ', '.join(f'{h} {t}' for h, t in alacak)
    return f'Borç tarafı: {b}. Alacak tarafı: {a}.'

def yaz(fn, baslik, giris, maddeler, kapanis, bekle=10):
    L = [f'BAŞLIK: {baslik}', '', seslendir(giris), '']
    for i, (soru, cevap, *aciklama) in enumerate(maddeler, 1):
        L += ['[[bip]]', seslendir(soru), '', 'Düşün.', f'[[{bekle}]]', '[[bip]]', 'Komisyon cevabı: ' + seslendir(cevap)]
        if aciklama and aciklama[0]: L += ['', seslendir(aciklama[0])]
        L += ['', '[[1]]', '']
    L += [seslendir(kapanis), '']
    open(fn, 'w').write('\n'.join(L))

M = '/home/user/smmm/metin/'

# ---------------- FİNANSAL MUHASEBE ----------------
fm_giris = ('İki bin yirmi beş yılı üçüncü dönem Finansal Muhasebe klasik sınavı. Bu sınavda tek bir büyük soru var: X Ticaret İşletmesinin dönem başı bilançosu verilmiş, '
            'dönem içinde on yedi işlem ve dönem sonunda sekiz işlem yapılmış. Kayıtlar Tekdüzen Hesap Planına göre, sürekli envanter ve yedi A seçeneğiyle, KDV oranı %20 alınarak yapılacak. '
            'Dönem başı bilançoda önemli kalemler şunlar: Kasa 7.000, Bankalar 45.000, Hisse Senetleri 45.000, Alıcılar 5.000, Alacak Senetleri 52.000, Alacak Senetleri Reeskontu 2.000, '
            'Şüpheli Ticari Alacaklar 10.000 ve karşılığı 7.000, Ticari Mallar 80.000, Binalar 100.000, Demirbaşlar 40.000, Birikmiş Amortismanlar 25.000. Pasifte Satıcılar 5.000, '
            'Borç Senetleri 67.300, Borç Senetleri Reeskontu 2.300 ve Sermaye 280.000. Her işlemi dinle, kaydı kafanda kur, sonra komisyonun kaydını dinle. '
            'Önce açılışta reeskontların ters kaydı yapılır: 122 Alacak Senetleri Reeskontu 2.000 borç, 647 Reeskont Faiz Gelirleri 2.000 alacak; 657 Reeskont Faiz Giderleri 2.300 borç, 322 Borç Senetleri Reeskontu 2.300 alacak.')
fm = [
 ('İşlem bir. Alış maliyeti 70.000 lira olan ticari mallar, kadevesi ve 30.000 lirası banka tahsilatı, kalanı senetli olmak üzere 100.000 lira artı KDV bedelle satılmıştır. Satış anında işletmenin nakit olarak ödediği 2.500 lira artı KDV taşıma giderini alıcı işletme üstlenmiştir.',
  kayit([('102 Bankalar', '50.000'), ('121 Alacak Senetleri', '70.000')], [('600 Yurt İçi Satışlar', '100.000'), ('391 Hesaplanan KDV', '20.000')]) + ' Maliyet kaydı: 621 Satılan Ticari Mallar Maliyeti 70.000 borç, 153 Ticari Mallar 70.000 alacak. Alıcı adına ödenen taşıma gideri: 120 Alıcılar ya da 127 Diğer Ticari Alacaklar 3.000 borç, 100 Kasa 3.000 alacak.',
  'Bankaya giren tutar KDV 20.000 artı 30.000, yani 50.000; kalan 70.000 senede bağlanmış. Alıcının üstlendiği taşıma gideri işletmenin gideri değil, alıcıdan alacaktır.'),
 ('İşlem iki. İşletme boş binasını üç yıllığına kiraya vermiştir. Üç yıllık kira tutarı ve KDV banka aracılığıyla tahsil edilmiştir. Aylık kira 5.000 lira, işlem bilanço hesaplarında izlenmiştir.',
  kayit([('102 Bankalar', '216.000')], [('380 Gelecek Aylara Ait Gelirler', '60.000'), ('480 Gelecek Yıllara Ait Gelirler', '120.000'), ('391 Hesaplanan KDV', '36.000')]),
  'Otuz altı aylık kira 180.000; on iki aylık kısmı kısa vadeli 380, kalan yirmi dört ayı uzun vadeli 480 hesabında izlenir.'),
 ('İşlem üç. İşletme binası için asansör tesisatı inşaatına başlamış, 8.000 lira artı KDV gider için bono düzenlemiştir.',
  kayit([('258 Yapılmakta Olan Yatırımlar', '8.000'), ('191 İndirilecek KDV', '1.600')], [('321 Borç Senetleri', '9.600')])),
 ('İşlem dört. İşletme, 150.000 lira sermayeli Z İşletmesinin sermaye payının 76.000 liralık kısmını satın almayı taahhüt etmiş ve taahhüdün 30.000 liralık kısmını banka aracılığıyla ödemiştir.',
  kayit([('245 Bağlı Ortaklıklar', '76.000')], [('246 Bağlı Ortaklıklara Sermaye Taahhütleri', '76.000')]) + ' Ödeme: 246 Bağlı Ortaklıklara Sermaye Taahhütleri 30.000 borç, 102 Bankalar 30.000 alacak.',
  '76.000 bölü 150.000, yüzde elliyi aştığı için iştirak değil bağlı ortaklıktır.'),
 ('İşlem beş. Daha önce adedi 1,8 liradan alınan 25.000 adet hisse senedinin değeri adet başına 1 liraya düşmüş ve karşılık ayrılmıştır.',
  kayit([('654 Karşılık Giderleri', '20.000')], [('119 Menkul Kıymetler Değer Düşüklüğü Karşılığı', '20.000')]),
  'Değer kaybı adet başına 0,8 lira çarpı 25.000 adet, yani 20.000.'),
 ('İşlem altı. Önceki dönemde şüpheli hale gelen 10.000 liralık alacağın 3.500 lirası nakit tahsil edilmiştir.',
  kayit([('100 Kasa', '3.500'), ('129 Şüpheli Ticari Alacaklar Karşılığı', '7.000')], [('128 Şüpheli Ticari Alacaklar', '10.000'), ('644 Konusu Kalmayan Karşılıklar ya da 671 Önceki Dönem Gelir ve Kârları', '500')]),
  'Daha önce 7.000 karşılık ayrılmıştı; tahsil edilmeyen 6.500 karşılıktan kapanır, karşılığın artan 500 lirası gelir yazılır.'),
 ('İşlem yedi. İşletme yeni bir binek oto alımı için satıcıyla anlaşmış ve bankadan 6.000 lira avans ödemiştir. Komisyon cevabında tutar 8.000 olarak kaydedilmiştir.',
  kayit([('259 Verilen Avanslar', '8.000')], [('102 Bankalar', '8.000')]),
  'Duran varlık alımı için verilen avans 259 hesabında izlenir. Soru metninde 6.000, komisyon cevabında 8.000 yazıyor; kayıt mantığı aynıdır.'),
 ('İşlem sekiz. İşletme satıcıya olan 5.000 liralık borcunu ödeyemeyeceğini bildirmiş, iki ay vadeli 5.500 liralık senet verme teklifi kabul edilmiş ve senet verilmiştir.',
  kayit([('320 Satıcılar', '5.000'), ('780 Finansman Giderleri', '500')], [('321 Borç Senetleri', '5.500')]),
  'Vade farkı olan 500 lira finansman gideridir.'),
 ('İşlem dokuz. İşletme bir Kasımda nominal değeri 44.800 lira olan altı ay vadeli %24 faizli bono ihraç etmiş ve aynı tarihte banka aracılığıyla 40.000 liraya satmıştır.',
  kayit([('102 Bankalar', '40.000'), ('308 Menkul Kıymetler İhraç Farkı', '4.800')], [('305 Çıkarılmış Bonolar ve Senetler', '44.800')])),
 ('İşlem on. kadevesi ve 25.000 lirası bankadan ödenerek, kalanı çek keşide edilerek 90.000 lira artı KDV ticari mal alınmıştır.',
  kayit([('153 Ticari Mallar', '90.000'), ('191 İndirilecek KDV', '18.000')], [('102 Bankalar', '43.000'), ('103 Verilen Çekler ve Ödeme Emirleri', '65.000')]),
  'Bankadan çıkan KDV 18.000 artı 25.000, yani 43.000; kalan 65.000 verilen çekle ödenir.'),
 ('İşlem on bir. Asansör için senet cirosuyla 2.000 lira artı KDV ek gider yapılmış ve inşaat tamamlanmıştır.',
  kayit([('258 Yapılmakta Olan Yatırımlar', '2.000'), ('191 İndirilecek KDV', '400')], [('121 Alacak Senetleri', '2.400')]) + ' Tamamlanınca: 252 Binalar 10.000 borç, 258 Yapılmakta Olan Yatırımlar 10.000 alacak.',
  'Asansör binanın parçası olduğu için toplam 10.000 lira binalara aktarılır.'),
 ('İşlem on iki. Ticari alacağı olmadığı halde başka bir işletmeden 7.000 liralık bono alınmış, yirmi gün sonra bankada iskonto ettirilmiş; 500 lira kesinti yapan banka kalanı hesaba yatırmıştır.',
  kayit([('121 Alacak Senetleri ya da 136 Diğer Çeşitli Alacaklar', '7.000')], [('336 Diğer Çeşitli Borçlar', '7.000')]) + ' İskonto: 102 Bankalar 6.500 ve 780 Finansman Giderleri 500 borç, 121 ya da 136 hesabı 7.000 alacak.'),
 ('İşlem on üç. İşletme 10.000 liralık borç senedini vadesinde ödeyememiş; hukuki süreç sonunda senet tutarını, 800 lira gecikme faizini ve 1.200 lira tazminatı bankadan ödemiştir.',
  kayit([('321 Borç Senetleri', '10.000'), ('780 Finansman Giderleri', '800'), ('689 Diğer Olağandışı Gider ve Zararlar', '1.200')], [('102 Bankalar', '12.000')]),
  'Gecikme faizi finansman gideri, tazminat ise olağandışı giderdir.'),
 ('İşlem on dört. Banka aracılığıyla nominal değeri 1.000 lira olan hazine bonolarından 100 adet alınmış, 500 lira komisyon bankadan ödenmiştir.',
  kayit([('112 Kamu Kesimi Tahvil, Senet ve Bonoları', '100.000'), ('653 Komisyon Giderleri', '500')], [('102 Bankalar', '100.500')])),
 ('İşlem on beş. Yangında 80.000 liralık ticari malın tamamı kullanılamaz hale gelmiş, sigorta şirketi 70.000 lira tazminat tahakkuk ettirmiştir.',
  kayit([('127 Diğer Ticari Alacaklar ya da 136 Diğer Çeşitli Alacaklar', '70.000'), ('689 Diğer Olağandışı Gider ve Zararlar', '10.000')], [('153 Ticari Mallar', '80.000')])),
 ('İşlem on altı. Alıcılardan vadesi dolan alacağın bir kısmına karşılık nakit 500 dolar tahsil edilmiştir. İşlem günü bir dolar 42 lira.',
  kayit([('100 Kasa', '21.000')], [('120 Alıcılar', '21.000')])),
 ('İşlem on yedi. Nakliyede zarar gören ve alış maliyeti 20.000 lira olan, satış tutarı 25.000 lira malları alıcı iade etmiş; toplam tutar için alıcıya senet ciro edilmiştir.',
  kayit([('610 Satıştan İadeler', '25.000'), ('191 İndirilecek KDV', '5.000')], [('121 Alacak Senetleri', '30.000')]) + ' Maliyet kaydı: 153 Ticari Mallar 20.000 borç, 621 Satılan Ticari Mallar Maliyeti 20.000 alacak.'),
 ('Dönem sonu işlemi bir. KDV tahakkuk işlemi yapılmıştır.',
  kayit([('391 Hesaplanan KDV', '56.000')], [('191 İndirilecek KDV', '25.000'), ('360 Ödenecek Vergi ve Fonlar', '31.000')])),
 ('Dönem sonu işlemi iki. Kasa sayımında 2.000 lira noksanlık bulunmuş; fark bankaya yatırılıp kaydedilmeyen tutardan kaynaklanıyor.',
  kayit([('102 Bankalar', '2.000')], [('100 Kasa', '2.000')])),
 ('Dönem sonu işlemi üç. Tahsil edilen kiranın altı aylık kısmı bu döneme aittir.',
  kayit([('380 Gelecek Aylara Ait Gelirler', '30.000')], [('649 Diğer Olağan Gelir ve Kârlar', '30.000')]) + ' Ayrıca uzun vadeden kısa vadeye aktarma: 480 Gelecek Yıllara Ait Gelirler 30.000 borç, 380 Gelecek Aylara Ait Gelirler 30.000 alacak.'),
 ('Dönem sonu işlemi dört. Pazarlama bölümünün kullandığı duran varlıklar için 5.000 lira amortisman ayrılmıştır.',
  kayit([('760 Pazarlama, Satış ve Dağıtım Giderleri', '5.000')], [('257 Birikmiş Amortismanlar', '5.000')])),
 ('Dönem sonu işlemi beş. Dönem sonunda bir dolar 45 lira.',
  kayit([('100 Kasa', '1.500')], [('646 Kambiyo Kârları', '1.500')]), 'Kasadaki 500 dolar, kur farkı üç lira, kâr 1.500.'),
 ('Dönem sonu işlemi altı. İhraç edilen bonoyla ilgili dönem sonunda hesaplanan faiz bankadan ödenmiştir.',
  'Faiz gideri: 780 Finansman Giderleri 1.600 borç, 308 Menkul Kıymetler İhraç Farkı 1.600 alacak. Ödeme: 305 Çıkarılmış Bonolar ve Senetler 1.600 borç, 102 Bankalar 1.600 alacak.',
  'Altı aylık ihraç farkı 4.800; iki aylık payı 1.600.'),
 ('Dönem sonu işlemi yedi. Satın alınan hazine bonosuyla ilgili 4.000 lira faiz tahakkuk ettirilmiştir.',
  kayit([('181 Gelir Tahakkukları', '4.000')], [('642 Faiz Gelirleri', '4.000')])),
 ('Dönem sonu işlemi sekiz. Döneme ilişkin kurumlar vergisi 5.000 lira hesaplanmıştır.',
  kayit([('691 Dönem Kârı Vergi ve Diğer Yasal Yükümlülük Karşılıkları', '5.000')], [('370 Dönem Kârı Vergi ve Diğer Yasal Yükümlülük Karşılıkları', '5.000')])),
 ('Son soru. Bu işlemlerden sonra dönem kârı, vergi ve net kâr ne olur; bilanço toplamı kaç liradır?',
  'Net satışlar 75.000, satışların maliyeti 50.000, brüt satış kârı 25.000. Faaliyet kârı 20.000. Diğer olağan gelirler 38.000, diğer olağan giderler 22.800, finansman giderleri 3.400; olağan kâr 31.800. Olağandışı giderler 11.200; dönem kârı 20.600, vergi 5.000, dönem net kârı 15.600. Dönem sonu bilanço toplamı 601.000.',
  'Yedi A seçeneğinde 760 ve 780 hesapları yansıtma hesaplarıyla 631 ve 660 hesaplarına aktarılır, sonra gelir tablosu 690 Dönem Kârı veya Zararı hesabında kapanır.'),
]
yaz(M + 'cs-01-2025-3.txt', 'Çıkmış Sorular 2025-3 Klasik. Finansal Muhasebe', fm_giris, fm,
    'Finansal Muhasebe klasik sınavı bitti. Klasik sınavda hesap adı ile hesap kodunun birlikte yazılması gerektiğini unutma; yalnızca kod ya da yalnızca ad yazana puan verilmiyor.', bekle=12)

# ---------------- FİNANSAL TABLOLAR ----------------
fta_giris = ('İki bin yirmi beş yılı üçüncü dönem Finansal Tablolar ve Analizi klasik sınavı. İlk iki soru için verilen 2024 rakamları şunlar: Aktif toplamı 6.647.912, '
             'dönen varlıklar 4.233.000, hazır değerler 230.000, ticari alacaklar 2.058.000, stoklar 1.945.000, duran varlıklar 2.414.912, maddi duran varlıklar 1.962.712, maddi olmayan duran varlıklar 452.200. '
             'Kısa vadeli yabancı kaynaklar 3.777.200, uzun vadeli yabancı kaynaklar 1.022.080, özkaynaklar 1.848.632. Net satışlar 8.800.000, brüt satış kârı 2.023.520, dönem net kârı 237.432. '
             'Rakamları tek tek ezberlemene gerek yok; formülü ve hesabın mantığını dinle.')
fta = [
 ('Soru bir. 2024 için varlık devir hızını hesaplayınız.', 'Net satışlar 8.800.000 bölü varlık toplamı 6.647.912, yaklaşık 1,32.'),
 ('Nakit oranı hesaplayınız.', 'Hazır değerler artı menkul kıymetler 230.000 bölü kısa vadeli yabancı kaynaklar 3.777.200, yaklaşık 0,06.', 'Genel kabul gören ölçü 0,20 civarı olduğu için bu işletmenin nakit oranı düşüktür.'),
 ('Kaldıraç oranını hesaplayınız.', 'Yabancı kaynaklar toplamı, 3.777.200 artı 1.022.080, bölü pasif toplamı 6.647.912, yüzde 72,19.', 'Genel ölçü yüzde elli civarı; işletme ağırlıklı olarak borçla finanse ediliyor.'),
 ('Satışların kârlılığını hesaplayınız.', 'Brüt satış kârı 2.023.520 bölü net satışlar 8.800.000, yüzde 22,99.'),
 ('Varlıkların kârlılığını hesaplayınız.', 'Dönem net kârı 237.432 bölü varlık toplamı 6.647.912, yüzde 3,57.'),
 ('Soru iki. 31 Aralık 2024 bilançosunun varlık kalemlerini dikey yüzde yöntemiyle analiz ediniz.',
  'Formül: ilgili kalem bölü varlık toplamı, çarpı yüz. Dönen varlıklar yüzde 63,67; hazır değerler yüzde 3,46; ticari alacaklar yüzde 30,96; stoklar yüzde 29,26. Duran varlıklar yüzde 36,33; maddi duran varlıklar yüzde 29,52; maddi olmayan duran varlıklar yüzde 6,80. Toplam yüzde yüz.'),
 ('Soru üç. Ticari alım satım yapan bir firmada 2025 yılının ocak, şubat ve mart ayları için ticari alacak tahsil süresini hesaplayınız. Ticari alacaklar 31 Aralık 2024 2.500; ocak sonu 2.100, şubat sonu 2.150, mart sonu 2.300. Aylık net satışlar ocak 1.800, şubat 1.600, mart 1.900.',
  'Alacak devir hızı, net satışlar bölü ortalama ticari alacaklar: ocak 0,78, şubat 0,69, mart 0,79. Tahsil süresi, otuz gün bölü devir hızı: ocak 38,33 gün, şubat 43,59 gün, mart 37,89 gün.',
  'Dikkat: komisyon her ayın ortalamasını 31 Aralık bakiyesiyle o ay sonu bakiyesinin ortalaması olarak almış. Örneğin şubat için 2.500 artı 2.150 bölü iki.'),
 ('Aynı firma için ticari borç ödeme süresini hesaplayınız. Ticari borçlar 31 Aralık 3.200; ocak sonu 3.100, şubat sonu 3.100, mart sonu 3.150. Satılan ticari mal maliyeti ocak 1.300, şubat 1.250, mart 1.450.',
  'Borç devir hızı, satışların maliyeti bölü ortalama ticari borçlar: ocak 0,41, şubat 0,40, mart 0,46. Ödeme süresi: ocak 72,69 gün, şubat 75,60 gün, mart 65,69 gün.'),
 ('Ticari mal stok devir süresini hesaplayınız. Stoklar 31 Aralık 4.000; ocak sonu 4.500, şubat sonu 4.300, mart sonu 4.200.',
  'Stok devir hızı, satışların maliyeti bölü ortalama stok: ocak 0,31, şubat 0,30, mart 0,35. Stok devir süresi: ocak 98,08 gün, şubat 99,60 gün, mart 84,83 gün.'),
]
yaz(M + 'cs-02-2025-3.txt', 'Çıkmış Sorular 2025-3 Klasik. Finansal Tablolar ve Analizi', fta_giris, fta,
    'Finansal Tablolar klasik sınavı bitti. Klasik sınavda hesaplamanın nasıl yapıldığını göstermeyen, yalnızca sonucu yazan cevaplar değerlendirilmiyor; formülü mutlaka yaz.', bekle=12)

# ---------------- MALİYET ----------------
mal = [
 ('Soru bir. Muhasebe Sistemi Uygulama Genel Tebliğine göre ticaret işletmelerinin, hizmet üretim işletmelerinin ve mamul üretim işletmelerinin kullanacağı yedi kodlu hesapları ayrı ayrı yazınız.',
  'Ticaret işletmeleri: 750 Araştırma ve Geliştirme Giderleri, 760 Pazarlama Satış ve Dağıtım Giderleri, 770 Genel Yönetim Giderleri, 780 Finansman Giderleri. '
  'Hizmet işletmeleri: bunlara ek olarak 740 Hizmet Üretim Maliyeti. Mamul üreten işletmeler: 710 Direkt İlk Madde ve Malzeme Giderleri, 720 Direkt İşçilik Giderleri, 730 Genel Üretim Giderleri ile 750, 760, 770 ve 780.'),
 ('Soru iki. Fireli safha maliyeti uygulanan bir işletmede dönem sonu yarı mamulün eşdeğeri; ilk madde açısından 10.000, işçilik ve genel üretim gideri açısından 20.000 birim. Firenin eşdeğeri ilk madde açısından 1.000, işçilik ve genel üretim gideri açısından 500 birim. Birim maliyetler: ilk madde 100, işçilik 30, genel üretim gideri 20 lira. Yarı mamul stok maliyetini ve fire maliyetini bulunuz.',
  'Yarı mamul: ilk madde 10.000 çarpı 100, 1.000.000; işçilik 20.000 çarpı 30, 600.000; genel üretim gideri 20.000 çarpı 20, 400.000; toplam 2.000.000 lira. Fire: 1.000 çarpı 100, 100.000; 500 çarpı 30, 15.000; 500 çarpı 20, 10.000; toplam 125.000 lira.'),
 ('Soru üç a. Safha maliyeti uygulanan bir işletmede dönem başı yarı mamul 20.000 birim, dönemde üretime başlanan 500.000 birim, dönem sonu yarı mamul 50.000 birim. Dönemde tamamlanıp devrolan miktar kaçtır?',
  'Üretime giren miktar üretimden çıkan miktara eşittir: 20.000 artı 500.000, eşittir tamamlanan artı 50.000. Tamamlanıp devrolan 470.000 birim.'),
 ('Soru üç b. Dönemde üretimine başlanıp tamamlanan miktar kaçtır?', '470.000 eksi dönem başı yarı mamul 20.000, 450.000 birim.'),
 ('Soru üç c. Dönem başı yarı mamul ilk madde açısından %70, işçilik ve genel üretim gideri açısından %55 tamamlanmış; dönem sonu yarı mamul ise ilk madde açısından %20, işçilik ve genel üretim gideri açısından %40 tamamlanmış. Eşdeğer mamul birimleri tablosunu düzenleyiniz.',
  'Dönem başı yarı mamulün bu dönemde tamamlanan kısmı: ilk madde %30 ile 6.000, işçilik ve genel üretim %45 ile 9.000. Başlanıp tamamlanan 450.000. Dönem sonu yarı mamul: ilk madde 10.000, işçilik ve genel üretim 20.000. Toplam eşdeğer: ilk madde 466.000, işçilik 479.000, genel üretim 479.000 birim.',
  'Komisyon ilk giren ilk çıkar mantığıyla, dönem başı yarı mamulün yalnızca bu dönemde tamamlanan kısmını saymış.'),
 ('Soru üç d. Dönemin ilk madde gideri 20.970.000, direkt işçilik 7.185.000, genel üretim gideri 10.777.500 lira. Birim mamul maliyeti nedir?',
  'İlk madde 20.970.000 bölü 466.000, 45 lira. İşçilik 7.185.000 bölü 479.000, 15 lira. Genel üretim gideri 10.777.500 bölü 479.000, 22,5 lira. Birim maliyet 82,5 lira.'),
]
yaz(M + 'cs-03-2025-3.txt', 'Çıkmış Sorular 2025-3 Klasik. Maliyet Muhasebesi',
    'İki bin yirmi beş yılı üçüncü dönem Maliyet Muhasebesi klasik sınavı. Üç soru var: hesap planı, fireli safha maliyeti ve eşdeğer birim. Soruyu dinle, kağıtsız çözmeye çalış, sonra komisyonun cevabını dinle.',
    mal, 'Maliyet klasik sınavı bitti. Eşdeğer birim sorularında önce üretim miktar dengesini kur: giren eşittir çıkan.', bekle=14)

# ---------------- DENETİM ----------------
den = [
 ('Soru bir. Kamu Gözetimi Kurumu Bağımsız Denetim Standartlarına göre iç kontrol nedir, iç denetim nedir? Tanımlayınız ve aralarındaki temel farkı açıklayınız.',
  'İç kontrol; finansal raporlamanın güvenilirliği, faaliyetlerin etkililiği ve verimliliği ile mevzuata uygunluk açısından işletmenin amaçlarına ulaştığına dair makul güvence sağlamak için üst yönetimden sorumlu olanlar, yönetim ve diğer personel tarafından tasarlanan, uygulanan ve sürekliliği sağlanan sistemdir. '
  'Beş bileşeni vardır: kontrol ortamı, risk değerlendirme süreci, kontrol faaliyetleri, bilgi sistemi ve iletişim, izleme. '
  'İç denetim ise işletmenin kurumsal yönetim, risk yönetimi ve iç kontrol süreçlerini değerlendirmek ve iyileştirmek için tasarlanan bağımsız ve tarafsız bir güvence ve danışmanlık faaliyetidir. '
  'Temel fark: iç kontrol, üst yönetimin sorumluluğunda tüm personelce işletilen sistemin kendisidir ve her işletmede vardır; iç denetim bu sistemi denetleyen, üst yönetime bağlı bağımsız bir fonksiyondur ve her işletmede bulunmak zorunda değildir.',
  'Komisyonun örneği: Mahalle bakkalında da iç kontrol vardır ama iç denetçiye gerek yoktur; büyük bir süpermarkette ise iç kontrolleri denetleyecek iç denetçiye ihtiyaç duyulur.'),
 ('Soru iki. Bağımsız Denetim Standartları kapsamında önemlilik nedir, performans önemliliği nedir?',
  'Önemlilik: Eksiklik ve yanlışlıkların, tek başına veya toplu olarak, finansal tablo kullanıcılarının ekonomik kararlarını etkilemesi makul ölçüde bekleniyorsa bunlar önemlidir. '
  'Performans önemliliği: Toplulaştırma riskini, yani düzeltilmemiş ve tespit edilmemiş yanlışlıkların toplamının genel önemliliği aşma olasılığını, uygun düşük seviyeye indirmek için genel önemlilikten daha düşük belirlenen tutar veya tutarlardır.'),
 ('Soru üç. Bağımsız Denetim Yönetmeliğine göre şu ifadelerden hangileri tam olarak doğrudur? Bir: Denetim, kullanıcılara TFRS çerçevesinde güvence sağlayacak bir görüş oluşturmak amacıyla yapılır. İki: Denetim makul veya sınırlı güvence sağlar; sınırlı güvence açıkça belirtilmemişse makul güvence verecek şekilde yapılır; kapsam TDS çerçevesinde belirlenir. Üç: Denetim, TFRS çerçevesinde yeterli ve uygun kanıt toplanmasını kapsar. Dört: Denetimin unsurları; konusu, tarafları, kıstası, kanıtları ve denetim raporudur.',
  'İki ve dört numaralı ifadeler doğrudur. Bu d şıkkıdır.',
  'Bir ve üç numaralı ifadeler TFRS diyor; oysa denetim belirlenmiş bir kıstasa göre ve Türkiye Denetim Standartları çerçevesinde yapılır. TFRS raporlama standardıdır, denetim standardı değildir.'),
]
yaz(M + 'cs-04-2025-3.txt', 'Çıkmış Sorular 2025-3 Klasik. Muhasebe Denetimi',
    'İki bin yirmi beş yılı üçüncü dönem Muhasebe Denetimi klasik sınavı. Üç soru var: iç kontrol ile iç denetim, önemlilik ile performans önemliliği ve Bağımsız Denetim Yönetmeliği ifadeleri. Cevaplar uzun; tanımlardaki anahtar kelimelere dikkat et.',
    den, 'Denetim klasik sınavı bitti. Tanım sorularında anahtar kavramlar puan getirir: makul güvence, beş bileşen, toplulaştırma riski.', bekle=12)

# ---------------- SPK ----------------
spk = [
 ('Soru bir a. Sermaye Piyasası Kanununa göre halka arz nedir?', 'Sermaye piyasası araçlarının satın alınması için her türlü yoldan yapılan genel bir çağrı ve bu çağrı devamında gerçekleştirilen satıştır.'),
 ('Soru bir b. Halka arz eden kimdir?', 'Sahip olduğu sermaye piyasası araçlarını halka arz etmek üzere Kurula başvuruda bulunan gerçek veya tüzel kişilerdir.'),
 ('Soru bir c. Halka arzlarda ön talep toplama nedir?', 'Payların ilk halka arzında veya ikincil halka arzlarda, izahname Kurulca onaylanmadan önce belirli bir fiyat aralığından, yatırımcıların olası taleplerinin, talepte bulunanlar için yükümlülük ve bağlayıcılık doğurmaksızın yetkili kuruluşlarca toplanmasıdır.'),
 ('Soru bir ç. Halka arzlarda ek pay satışı nedir?', 'Toplanan kesin talebin satışa sunulan pay miktarından fazla olması halinde, fazla talebi karşılamak için azami nominal değeri önceden belirlenip kamuya duyurulan payların dağıtılacak toplam paylara eklenmesidir.'),
 ('Soru iki. Kripto varlık hizmet sağlayıcılarının kurucu ve ortaklarından aranan şartları maddeler halinde sayınız.',
  'Müflis olmamak, konkordato ilan etmemiş ve iflası ertelenmemiş olmak. Faaliyet izni iptal edilmiş finans kuruluşlarında yüzde on veya daha fazla paya ya da kontrole sahip olmamak. '
  'Zimmet, rüşvet, hırsızlık, dolandırıcılık, sahtecilik, güveni kötüye kullanma, suç gelirlerini aklama, terörün finansmanı, vergi kaçakçılığı gibi kanunda sayılan suçlardan hükümlü olmamak ve kasten işlenen bir suçtan beş yıl veya daha fazla hapis cezası almamış olmak. '
  'Kanunun yüz birinci maddesine göre işlem yasaklı olmamak. Gerekli mali güce, dürüstlüğe ve itibara sahip olmak. Faaliyet izni Kurulca iptal edilmiş kuruluşlarda bu iptalden sorumlu kişilerden olmamak. Son beş yıl içinde Kanunun yüz dördüncü maddesine göre idari para cezası almamış olmak.'),
 ('Soru üç. Sermaye Piyasası Kanununa göre güveni kötüye kullanma suçunun nitelikli halini oluşturan fiilleri sayınız.',
  'Bir: Yatırım kuruluşuna, fon kuruluna veya teminat sorumlularına tevdi edilen sermaye piyasası araçlarını, nakit ve diğer kıymetleri kendisinin veya başkasının menfaatine satmak, kullanmak, rehnetmek, gizlemek veya inkâr etmek. '
  'İki: İlişkili bir teşebbüs veya kişiyle emsallerinden bariz şekilde farklı fiyat ve bedellerle örtülü işlem yaparak halka açık ortaklığın kârını veya malvarlığını azaltmak. '
  'Üç: Halka açık ortaklıklar ve kolektif yatırım kuruluşlarıyla ilişkili kişiler arasında emsallere, piyasa teamüllerine ve ticari dürüstlüğe aykırı anlaşmalar veya işlem hacmi üreterek kârlarını veya malvarlıklarını azaltmak ya da artmasını engellemek.'),
]
yaz(M + 'cs-08-2025-3.txt', 'Çıkmış Sorular 2025-3 Klasik. Sermaye Piyasası Mevzuatı',
    'İki bin yirmi beş yılı üçüncü dönem Sermaye Piyasası Mevzuatı klasik sınavı. Kavram tanımları, kripto varlık hizmet sağlayıcıları ve güveni kötüye kullanma suçu soruldu.',
    spk, 'Sermaye Piyasası klasik sınavı bitti. Son dönemde kripto varlık düzenlemeleri de soruluyor; bu konuyu ayrıca tekrar et.', bekle=10)
print('5 dosya yazıldı')
