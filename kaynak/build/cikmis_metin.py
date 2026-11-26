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
    SEK = {'nin': 'nin', 'nın': 'nin', 'ye': 'ne', 'ya': 'ne', 'de': 'nde', 'da': 'nde', 'deki': 'ndeki', 'den': 'nden', 'dan': 'nden', 'i': 'ni'}
    t = re.sub(r"A\.\s?Ş\.(?:'([a-zçğıöşü]+))?", lambda m: 'Anonim Şirketi' + SEK.get(m.group(1), m.group(1) or '')[0:0] if not m.group(1) else 'Anonim Şirketi' + SEK.get(m.group(1), m.group(1)), t)
    t = re.sub(r"Ltd\.\s?Şti(?:\.?'?([a-zçğıöşü]+)|\.)?", lambda m: 'Limited Şirketi' + ({'nin': 'nin'}.get(m.group(1), m.group(1) or '')), t)
    # boşluk doldurma işaretleri, (i)/(ii) numaraları, (%) ve +/- işaretleri
    RN = {'i': 'bir', 'ii': 'iki', 'iii': 'üç', 'iv': 'dört', 'v': 'beş'}
    t = re.sub(r'\((i{1,3}|iv|v)\)\s*(?:-{2,}|_{2,})', lambda m: ' boşluk ' + RN[m.group(1)] + ' ', t)
    t = re.sub(r'-{2,}|_{2,}', ' boşluk ', t)
    t = re.sub(r'\((i{1,3}|iv|v)\)', lambda m: '(' + RN[m.group(1)] + ')', t)
    t = re.sub(r'\(\s*%\s*\)', '', t)
    t = re.sub(r'%\s*(?=[a-zçğıöşü])', 'yüzde ', t)
    t = re.sub(r'([Ff]azla)\s*\(\+\)', r'\1', t); t = re.sub(r'([Ee]ksik)\s*\(-\)', r'\1', t)
    t = t.replace('(+)', ' artı ').replace('(-)', ' eksi ').replace('+', ' artı ')
    t = re.sub(r'(?<=[a-zçğıöşü]) - (?=[A-ZÇĞİÖŞÜ])', ' eksi ', t)
    t = re.sub(r'(?<=\w)\(', ' (', t)
    t = re.sub(r'%\s*(\d+(?:,\d+)?)', r'yüzde \1', t)
    t = re.sub(r'(\d+(?:,\d+)?)\s*%', r'yüzde \1', t)
    # Roma rakamlı madde başları ve "I ve III" gibi cevaplar
    t = re.sub(r'(?<![A-Za-zÇĞİÖŞÜçğıöşü])(VIII|VII|VI|IV|V|III|II|I)(?=\.\s|\s*,|\s+ve\s|\s*$|\s*\))', lambda m: ('İ' + ROMA[m.group(1)][1:] if ROMA[m.group(1)][0] == 'i' else ROMA[m.group(1)].capitalize()) if m.end() < len(t) and t[m.end():m.end()+1] == '.' else ROMA[m.group(1)], t)
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
    AY = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
    t = re.sub(r'\b(\d{1,2})[./](\d{1,2})[./](\d{4})\b', lambda m: f'{int(m.group(1))} {AY[int(m.group(2)) - 1]} {m.group(3)}' if 1 <= int(m.group(2)) <= 12 else m.group(0), t)
    t = re.sub(r'\b(\d{4})\s*/\s*(?=[A-ZÇĞİÖŞÜ][a-zçğıöşü])', r'\1 ', t)  # 2025/Aralık
    t = re.sub(r'\s*/\s*kg(\w*)', r' kilogram başına\1', t)
    t = re.sub(r'\bkg\b', 'kilogram', t)
    t = re.sub(r'(\d+)\s*/\s*([a-zA-ZçÇ])\b', r'\1 \2', t)  # 4/a -> dört a
    t = re.sub(r'hangisi\s*/\s*hangileri', 'hangisi ya da hangileri', t)
    t = re.sub(r'(?<![\w\d])-\s?(?=\d)', 'eksi ', t)
    t = sayilari_yaz(t)
    t = re.sub(r"(\w)'(\w)", r'\1\2', t)
    t = t.replace('/', ' bölü ').replace('&', ' ve ')
    t = re.sub(r'\s+', ' ', t).strip()
    return t

# Tabloya dayanan (tablosu metne gelmeyen) Finansal Tablolar sorularına cevaptan sonra formül hatırlatması
FORMUL = [
    (r'net işletme sermayesi', 'net işletme sermayesi, dönen varlıklardan kısa vadeli yabancı kaynakların çıkarılmasıyla bulunur. Eksi çıkması, kısa vadeli borçların dönen varlıklardan fazla olduğunu gösterir'),
    (r'brüt işletme sermayesi', 'brüt işletme sermayesi, dönen varlıkların toplamıdır'),
    (r'cari oran', 'cari oran, dönen varlıkların kısa vadeli yabancı kaynaklara bölümüdür'),
    (r'likidite oranı', 'likidite oranı, dönen varlıklardan stoklar düşüldükten sonra kalan tutarın kısa vadeli yabancı kaynaklara bölümüdür'),
    (r'stok devir hızı', 'stok devir hızı, satışların maliyetinin ortalama stoka bölümüdür. Ortalama stok, dönem başı ve dönem sonu stokların toplamının yarısıdır'),
    (r'devir süresi', 'stok devir süresi, dönemdeki gün sayısının stok devir hızına bölümüdür. Devir hızı, satışların maliyetinin ya da ilgili stok için kullanılan tutarın ortalama stoka bölümüdür. Yıl için üç yüz altmış, bir çeyrek için doksan gün kullanılır'),
    (r'tahsilat süresi', 'alacak tahsil süresi, dönemdeki gün sayısının alacak devir hızına bölümüdür. Alacak devir hızı, net satışların ortalama ticari alacaklara bölümüdür'),
    (r'borç ödeme süresi', 'borç ödeme süresi, dönemdeki gün sayısının borç devir hızına bölümüdür. Borç devir hızı, satışların maliyetinin ya da alışların ortalama ticari borçlara bölümüdür'),
    (r'brüt satışların kârlılığı|satışların kârlılığı', 'satışların kârlılığı, brüt satış kârının net satışlara bölünüp yüzle çarpılmasıyla bulunur'),
    (r'faaliyet kârlılığı', 'faaliyet kârlılığı, faaliyet kârının net satışlara bölünüp yüzle çarpılmasıyla bulunur'),
    (r'varlıkların kârlılığı', 'varlıkların kârlılığı, net kârın toplam varlıklara bölünüp yüzle çarpılmasıyla bulunur'),
    (r'brüt satışların dikey', 'gelir tablosunun dikey analizinde temel net satışlardır. Bu yüzden brüt satışların dikey yüzdesi yüzün üzerinde çıkar'),
    (r'dikey', 'dikey yüzde, kalemin temel tutara bölünüp yüzle çarpılmasıdır. Bilançoda temel aktif ya da pasif toplamı, gelir tablosunda net satışlardır'),
    (r'eğilim|trend', 'trend yüzdesi, ilgili yılın tutarının baz yıl tutarına bölünüp yüzle çarpılmasıdır'),
    (r'değişim yüzde', 'değişim yüzdesi, cari yıl ile önceki yıl arasındaki farkın önceki yıla bölünüp yüzle çarpılmasıdır'),
    (r'satışlardan sağlanan nakit', 'satışlardan nakit girişi, net satışlara dönem başı ticari alacakların eklenip dönem sonu ticari alacakların çıkarılmasıyla bulunur'),
]

# Seçenekler arasından seçim isteyen sorularda şıklar okunur (sayısal ve öncül kombinasyonlu şıklar hariç)
def sik_oku(q):
    if q.get('kayit') or len(q.get('secenekler', {})) < 2: return False
    if not re.search(r'hangi|aşağıdaki|neden|nedir|nasıl|nelerdir|ne yapmalıdır|ne zaman', q['soru'], re.I): return False
    v = list(q['secenekler'].values())
    if all(len(re.findall(r'[A-Za-zÇĞİÖŞÜçğıöşü]{4,}', x)) == 0 for x in v): return False   # sayısal şıklar
    if all(re.fullmatch(r'(Yalnız\s+)?[IVX]+(\s*(,|ve)\s*[IVX]+)*', x.strip()) for x in v): return False  # öncüller soruda
    return sum(map(len, v)) < 2000

def dogrudan(t):
    """Test sorusunu şıksız, doğrudan soru biçimine çevirir: 'Aşağıdakilerden hangisi X değildir?' -> 'X olmayan nedir?'"""
    # boşluk doldurma: son cümleyi kısa bir soruya çevir
    bm = re.search(r'(?<=[."”?])\s*[^."”]*(?:boş bırakılan|boşlu[kğ]|tamamlayan)[^."”]*aşağıdakilerden\s+hangi[^.?]*\?\s*$', t, re.I)
    if bm:
        cogul = re.search(r'boşluklar|yerlere|kısımlar|sırasıyla', bm.group(0), re.I) or len(re.findall(r'-{2,}|_{2,}', t)) >= 2
        return t[:bm.start()].rstrip() + (' Boşluklara sırasıyla ne gelir?' if cogul else ' Boşluğa ne gelir?')
    if re.search(r'hangileri|Yalnız|yukarıdaki', t, re.I): return t
    t = re.sub(r'(ifadelerden|yorumlardan)\s+(?=(?:yanlış|doğru|hangisi))', '', t)
    t = re.sub(r'seçeneklerde belirtilenlerden\s+', '', t)
    t = re.sub(r'aşağıda yapılan\s+', '', t)
    t = re.sub(r'^Aşağıda verilen\s+', '', t)
    t = re.sub(r'[Aa]şağıdaki(?:lerden)?\s+(?:([\wçğıöşüÇĞİÖŞÜ]+?(?:lardan|lerden|ların|lerin)?)\s+)?(?=hangi)', lambda m: (m.group(1) + ' ') if m.group(1) else '', t)
    t = re.sub(r'[Aa]şağıdaki\s+', '', t)
    SON = [(r'biri değildir', 'biri olmayan nedir'), (r'birisi olarak sayılmamıştır', 'biri olarak sayılmayan nedir'), (r'sayılmamıştır', 'sayılmayan nedir'),
           (r'değildir', 'olmayan nedir'), (r'girmez', 'girmeyen nedir'), (r'yer almaz', 'yer almayan nedir'), (r'kullanılmaz', 'kullanılmayan nedir'),
           (r'yanlıştır', 'yanlış olan ifade nedir'), (r'doğrudur', 'doğru olan ifade nedir'), (r'tabidir', 'tabi olan nedir')]
    m = re.search(r'\bhangisi\s+((?:(?!hangisi).)*?)\s*(' + '|'.join(a for a, _ in SON) + r')\s*\?(\s*\(.*\))?\s*$', t)
    if m:
        bitis = dict(SON)[m.group(2)]
        t = t[:m.start()] + (m.group(1) + ' ' if m.group(1) else '') + bitis + '?' + (m.group(3) or '')
    t = re.sub(r'\s+', ' ', t).strip()
    return t[0].upper() + t[1:] if t else t

def formul_notu(soru):
    for pat, txt in FORMUL:
        if re.search(pat, soru, re.I): return 'Bu soru sınavda bir tabloya dayanıyordu, tabloyu burada okuyamıyorum. Formülü hatırla: ' + txt + '.'
    return ''

YANLIS = re.compile(r'(yanlış(?:tır|lardır)?|değildir|yer almaz|olamaz|bulunmaz|söylenemez|yoktur)\b[^.?]*\?\s*$', re.I)

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
             f'İki bin yirmi altı yılı {dn} dönem yeterlilik sınavının {ders} soruları. Bu bölümde {sayi(len(qs))} gerçek sınav sorusu var. Şıkları okumayacağım; test soruları doğrudan soru olarak sorulacak. Önce soruyu duyacaksın, sonra düşünme süresi, zilden sonra doğru cevabı dinle.', '']
        for q in qs:
            soru, cevap = seslendir(dogrudan(q['soru'])), seslendir(q['cevap'])
            if re.search(r'kaç\s*₺', q['soru']) and re.fullmatch(r'-?[\d.,\s]+', q['cevap'].strip()): cevap += ' lira'
            elif (mm := re.search(r'kaç\s+(iş günü|ay|gün|yıl|saat|hafta|kişi|aylık|günlük|yıllık)', q['soru'])) and re.fullmatch(r'[\d\s]+(,0+)?', q['cevap'].strip()): cevap += ' ' + mm.group(1)
            elif re.search(r'yüzde kaç|% kaç|kaç %|yüzdesi|yüzde \(%\)|\(%\)', q['soru'][-70:]) and re.fullmatch(r'-?[\d.,\s%]+', q['cevap'].strip()) and 'yüzde' not in cevap: cevap = ('eksi yüzde ' + cevap[5:]) if cevap.startswith('eksi ') else 'yüzde ' + cevap
            if '₺' in q['soru'] and re.fullmatch(r'-?\d{1,3}(\.\d{3})+', q['cevap'].strip()) and not cevap.endswith('lira'): cevap += ' lira'
            hesap = len(re.findall(r'\d', q['soru'])) > 12
            bekle = 14 if hesap else 8
            yanlis = bool(YANLIS.search(q['soru']))
            onek = (('Cevap, yani yanlış olan ifadeler: ' if re.search(r'hangileri', q['soru']) else 'Cevap, yani yanlış olan ifade: ') if re.search(r'yanlış', q['soru'][-80:]) else 'Cevap, yani bunlardan biri olmayan: ') if yanlis else ('Doğru kayıt: ' if q.get('kayit') else 'Cevap: ')
            not_ = formul_notu(q['soru']) if ders == 'Finansal Tablolar ve Analizi' and len(q['soru']) < 170 else ''
            siklar = []
            if dogrudan(q['soru']) != q['soru'] and not q.get('kayit'): onek = 'Cevap: '
            if False and sik_oku(q):  # kullanıcı isteği: şık okunmaz, soru doğrudan sorulur
                siklar = ['Şıklar.', ''] + sum([[f'{h}, {seslendir(v).rstrip(".")}.', ''] for h, v in sorted(q['secenekler'].items())], [])
                bekle += 4
                if q.get('dogru'): onek = onek[:-2] + f', {q["dogru"]} şıkkı: ' if onek.endswith(': ') else onek
            L += ['[[bip]]', f'Soru {sayi(q["no"])}. {soru}', ''] + siklar + ['Düşün.', f'[[{bekle}]]', '[[bip]]', onek + cevap.rstrip('.') + '.'] + ([not_] if not_ else []) + ['', '[[1]]', '']
        L += [f'{ders} çıkmış soruları bitti. Takıldığın soruların konusunu, ilgili ders bölümünden tekrar dinle.', '']
        fn = f'{outdir}/cs-{ANAHTAR[ders]}-{yil}-{donem}.txt'
        open(fn, 'w').write('\n'.join(L))
    print(len(grup), 'dosya yazıldı')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
