# Çıkarılan çıkmış soruları (json) sesli okunacak ders metinlerine (metin/cs-*.txt) çevirir.
# Şıklar okunmaz: soru → düşünme süresi → cevap.
import json, re, sys
from collections import defaultdict

BIR = ['', 'bir', 'iki', 'üç', 'dört', 'beş', 'altı', 'yedi', 'sekiz', 'dokuz']
ON = ['', 'on', 'yirmi', 'otuz', 'kırk', 'elli', 'altmış', 'yetmiş', 'seksen', 'doksan']
def uc(n):
    y, r = divmod(n, 100); o, b = divmod(r, 10)
    s = []
    if y: s.append('yüz' if y == 1 else BIR[y] + ' yüz')
    if o: s.append(ON[o])
    if b: s.append(BIR[b])
    return ' '.join(s)
def sayi(n):
    if n == 0: return 'sıfır'
    parts = []
    for v, ad in ((10**12, 'trilyon'), (10**9, 'milyar'), (10**6, 'milyon'), (1000, 'bin')):
        q, n = divmod(n, v)
        if q: parts.append('bin' if (v == 1000 and q == 1) else uc(q) + ' ' + ad)
    if n: parts.append(uc(n))
    return ' '.join(parts)
def ondalik(d):
    lead = len(d) - len(d.lstrip('0'))
    rest = d.lstrip('0')
    return ' '.join(['sıfır'] * lead + ([sayi(int(rest))] if rest else []))

def sayilari_yaz(t):
    def f(m):
        s = m.group(0)
        tam, _, ond = s.partition(',')
        n = int(tam.replace('.', ''))
        ond = ond.rstrip('0')
        return sayi(n) + (' virgül ' + ondalik(ond) if ond else '')
    return re.sub(r'\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?', f, t)

SIRA = {'bir': 'birinci', 'iki': 'ikinci', 'üç': 'üçüncü', 'dört': 'dördüncü', 'beş': 'beşinci', 'altı': 'altıncı', 'yedi': 'yedinci',
        'sekiz': 'sekizinci', 'dokuz': 'dokuzuncu', 'on': 'onuncu', 'yirmi': 'yirminci', 'otuz': 'otuzuncu', 'kırk': 'kırkıncı',
        'elli': 'ellinci', 'altmış': 'altmışıncı', 'yetmiş': 'yetmişinci', 'seksen': 'sekseninci', 'doksan': 'doksanıncı', 'yüz': 'yüzüncü', 'bin': 'bininci'}
def sira(n):
    w = sayi(n).split(' '); w[-1] = SIRA.get(w[-1], w[-1]); return ' '.join(w)
def ek_uyum(e):
    return e.translate(str.maketrans('eiöü', 'aıou'))

KISA = {
    'KDV': 'kadeve', 'KGK': 'Kamu Gözetimi Kurumu', 'GÜG': 'genel üretim giderleri', 'TMS': 'te me se', 'TFRS': 'te fe re se',
    'DİMM': 'direkt ilk madde ve malzeme', 'DİS': 'direkt işçilik', 'BDS': 'Bağımsız Denetim Standartları', 'TÜRMOB': 'Türmob',
    'SGK': 'Sosyal Güvenlik Kurumu', 'TL': 'lira', 'KAYİK': 'kamu yararını ilgilendiren kuruluş', 'BDY': 'Bağımsız Denetim Yönetmeliği',
    'TDS': 'Türkiye Denetim Standartları', 'SPK': 'Sermaye Piyasası Kurulu', 'VUK': 'Vergi Usul Kanunu', 'TTK': 'Türk Ticaret Kanunu',
    'TBK': 'Türk Borçlar Kanunu', 'ÖTV': 'özel tüketim vergisi', 'BOBİ': 'bobi', 'FRS': 'ef re se', 'KAP': 'Kamuyu Aydınlatma Platformu',
    'MKK': 'Merkezi Kayıt Kuruluşu', 'GVK': 'Gelir Vergisi Kanunu', 'KVK': 'Kurumlar Vergisi Kanunu', 'İİK': 'İcra ve İflas Kanunu',
}
ROMA = {'I': 'bir', 'II': 'iki', 'III': 'üç', 'IV': 'dört', 'V': 'beş', 'VI': 'altı', 'VII': 'yedi', 'VIII': 'sekiz'}

def tr_kucuk(w):
    return w.replace('I', 'ı').replace('İ', 'i').lower()

def seslendir(t):
    t = t.replace('’', "'").replace('‘', "'")
    t = re.sub(r"₺'([a-zçğıöşü]+)", lambda m: 'lira' + ek_uyum(m.group(1)), t)
    t = t.replace('₺', ' lira')
    t = re.sub(r'%\s*(\d+(?:,\d+)?)', r'yüzde \1', t)
    t = re.sub(r'(\d+(?:,\d+)?)\s*%', r'yüzde \1', t)
    # Roma rakamlı madde başları ve "I ve III" gibi cevaplar
    t = re.sub(r'(?<![A-Za-zÇĞİÖŞÜçğıöşü])(VIII|VII|VI|IV|V|III|II|I)(?=\.\s|\s*,|\s+ve\s|\s*$|\s*\))', lambda m: ROMA[m.group(1)].capitalize() if m.end() < len(t) and t[m.end():m.end()+1] == '.' else ROMA[m.group(1)], t)
    def kisa_ek(m):
        ac, ek = KISA[m.group(1)], m.group(2)
        if ac.endswith('u'):
            for pat, rep in (('^n[ıiuü]n$', 'nun'), ('^[yn]?[ae]$', 'na'), ('^[dt][ae]$', 'nda'), ('^[dt][ae]n$', 'ndan'), ('^[cç][ae]$', 'nca')):
                if re.match(pat, ek): return ac + rep
        return ac + ek
    t = re.sub(r"\b([A-ZÇĞİÖŞÜ]{2,})'([a-zçğıöşü]+)", lambda m: kisa_ek(m) if m.group(1) in KISA else m.group(0), t)
    t = re.sub(r'\b([A-ZÇĞİÖŞÜ]{2,})\b', lambda m: KISA.get(m.group(1), m.group(1) if len(m.group(1)) > 4 and m.group(1) not in ('XYZ',) else ' '.join(m.group(1))), t)
    t = re.sub(r'\b([A-ZÇĞİÖŞÜ]{5,})\b', lambda m: tr_kucuk(m.group(1)), t)
    t = re.sub(r"(\d)'([a-zçğıöşü]+)", r'\1\2', t)
    t = re.sub(r'(?<![\d.,])(\d{1,3})\.\s(?=[a-zçğıöşü])', lambda m: sira(int(m.group(1))) + ' ', t)
    t = sayilari_yaz(t)
    t = re.sub(r"(\w)'(\w)", r'\1\2', t)
    t = t.replace('/', ' bölü ').replace('&', ' ve ')
    t = re.sub(r'\s+', ' ', t).strip()
    return t

YANLIS = re.compile(r'(yanlış|değildir|yer almaz|olamaz|bulunmaz|söylenemez|yoktur)\b[^.?]*\?\s*$', re.I)

def main(src, outdir):
    Q = json.load(open(src))
    grup = defaultdict(list)
    for q in Q: grup[(q['sinav'], q['ders'])].append(q)
    ANAHTAR = {'Finansal Muhasebe': '01', 'Finansal Tablolar ve Analizi': '02', 'Maliyet Muhasebesi': '03', 'Muhasebe Denetimi': '04',
               'Vergi Mevzuatı': '05', 'Hukuk': '06', 'Meslek Hukuku': '07', 'Sermaye Piyasası Mevzuatı': '08'}
    for (sinav, ders), qs in sorted(grup.items()):
        yil, donem = sinav.split('-')
        dn = 'birinci' if donem == '1' else 'ikinci'
        L = [f'BAŞLIK: Çıkmış Sorular {sinav}. {ders}', '',
             f'İki bin yirmi altı yılı {dn} dönem yeterlilik sınavının {ders} soruları. Bu bölümde {sayi(len(qs))} gerçek sınav sorusu var. Şıkları okumayacağım: önce soruyu duyacaksın, zil çalınca düşün, ikinci zilden sonra doğru cevabı dinle.', '']
        for q in qs:
            soru, cevap = seslendir(q['soru']), seslendir(q['cevap'])
            if re.search(r'kaç\s*₺', q['soru']) and re.fullmatch(r'[\d.,\s]+', q['cevap'].strip()): cevap += ' lira'
            elif (mm := re.search(r'kaç\s+(iş günü|ay|gün|yıl|saat|hafta|kişi|aylık|günlük|yıllık)', q['soru'])) and re.fullmatch(r'[\d\s]+', q['cevap'].strip()): cevap += ' ' + mm.group(1)
            elif re.search(r'yüzde kaç|% kaç|kaç %', q['soru']) and re.fullmatch(r'[\d.,\s%]+', q['cevap'].strip()) and 'yüzde' not in cevap: cevap = 'yüzde ' + cevap
            hesap = len(re.findall(r'\d', q['soru'])) > 12
            bekle = 14 if hesap else 8
            yanlis = bool(YANLIS.search(q['soru']))
            onek = 'Cevap, yani yanlış olan ifade: ' if yanlis else ('Doğru kayıt: ' if q.get('kayit') else 'Cevap: ')
            L += ['[[bip]]', f'Soru {sayi(q["no"])}. {soru}', '', 'Düşün.', f'[[{bekle}]]', '[[bip]]', onek + cevap.rstrip('.') + '.', '', '[[1]]', '']
        L += [f'{ders} çıkmış soruları bitti. Takıldığın soruların konusunu, ilgili ders bölümünden tekrar dinle.', '']
        fn = f'{outdir}/cs-{ANAHTAR[ders]}-{yil}-{donem}.txt'
        open(fn, 'w').write('\n'.join(L))
    print(len(grup), 'dosya yazıldı')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
