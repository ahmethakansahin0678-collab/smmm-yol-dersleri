# TÜRMOB-TESMER yeterlilik soru kitapçıklarından (PDF) soru metni + kırmızıyla işaretli doğru cevabı çıkarır.
# Kullanım: python3 -I cikmis_cikar.py <pdf_klasoru> <cikti.json>
import sys, re, json, glob, os
import pdfplumber

KIRMIZI = (1.0, 0.0, 0.0)
DERS = {
    'finansal-muhasebe': 'Finansal Muhasebe', 'finansal-tablolar-analizi': 'Finansal Tablolar ve Analizi',
    'maliyet-muhasebesi': 'Maliyet Muhasebesi', 'muhasebe-denetimi': 'Muhasebe Denetimi',
    'vergi-mevzuati': 'Vergi Mevzuatı', 'hukuk': 'Hukuk', 'meslek-hukuku': 'Meslek Hukuku', 'spk-mevzuati': 'Sermaye Piyasası Mevzuatı'}
SECENEK = re.compile(r'^([A-E])\)\s*')

def kirmizi_mi(w):
    c = w.get('non_stroking_color')
    try: return tuple(round(float(x), 2) for x in c) == KIRMIZI
    except Exception: return False

def satirlar(page):
    W, H = page.width, page.height
    words = page.extract_words(extra_attrs=['non_stroking_color', 'fontname'], x_tolerance=1.5, y_tolerance=2, keep_blank_chars=False)
    out = []
    for col in (0, 1):
        ws = [w for w in words if (w['x0'] < W / 2) == (col == 0) and 45 < w['top'] < H - 40]
        ws.sort(key=lambda w: (round(w['top']), w['x0']))
        lines = []
        for w in ws:
            if lines and abs(w['top'] - lines[-1]['top']) < 3: lines[-1]['w'].append(w)
            else: lines.append({'top': w['top'], 'w': [w]})
        for L in lines:
            L['w'].sort(key=lambda w: w['x0'])
            out.append(L['w'])
    return out


SAYI = re.compile(r'^[\d.]+(,\d+)?$')
def kayit_oku(lines):
    """Yevmiye kaydı tablosunu satır satır [hesap, tutar, taraf] listesine çevirir."""
    rows = []
    for ws in lines:
        ws = [w for w in ws if not re.fullmatch(r'[A-E]\)', w['text'])]
        if not ws: continue
        nums = [w for w in ws if SAYI.match(w['text']) and not re.fullmatch(r'\d{3}', w['text'])]
        acc = [w for w in ws if w not in nums]
        if not acc and nums and rows and rows[-1][1] is None:
            rows[-1][1] = nums[-1]; continue
        if not acc: continue
        rows.append([acc, nums[-1] if nums else None])
    if not rows: return None
    xs = sorted(r[1]['x0'] for r in rows if r[1])
    ax = min(r[0][0]['x0'] for r in rows)
    out = []
    for acc, num in rows:
        taraf = None
        if num and xs and xs[-1] - xs[0] > 20: taraf = 'alacak' if num['x0'] > (xs[0] + xs[-1]) / 2 else 'borç'
        elif acc[0]['x0'] > ax + 8: taraf = 'alacak'
        else: taraf = 'borç'
        out.append({'hesap': ' '.join(w['text'] for w in acc), 'tutar': num['text'] if num else '', 'taraf': taraf})
    return out
def tr_baslik(t):
    t = t.replace('I', 'ı').replace('İ', 'i').lower()
    return ' '.join((w[0].replace('i', 'İ').upper() if w[0] == 'i' else w[0].upper()) + w[1:] if w else w for w in t.split(' '))
def kayit_metin(k):
    return ' '.join(f"{tr_baslik(r['hesap'])}, {r['tutar']} {r['taraf']}." if r['tutar'] else f"{tr_baslik(r['hesap'])}." for r in k)

def cikar(pdf_path):
    pdf = pdfplumber.open(pdf_path)
    sorular = {}; cur = None; seen = set()
    for page in pdf.pages:
        for ws in satirlar(page):
            text = ' '.join(w['text'] for w in ws).strip()
            if not text or text in ('TEST BİTTİ.', 'A', 'B') or text.startswith('Diğer sayfaya') or text.startswith('TÜRMOB-TESMER'): continue
            m = re.match(r'^(\d{1,2})\.\s*(.*)$', text)
            bold0 = 'Bold' in ws[0]['fontname']
            if m and bold0 and int(m.group(1)) not in seen and int(m.group(1)) <= max(seen, default=0) + 4 and not re.match(r'^ve\s', m.group(2)):
                n = int(m.group(1)); seen.add(n)
                cur = {'no': n, 'soru': [m.group(2)] if m.group(2) else [], 'secenek': False, 'cevap': [], 'opts': {}}
                sorular[n] = cur; continue
            if cur is None: continue
            red = [w['text'] for w in ws if kirmizi_mi(w)]
            om = SECENEK.match(text)
            if om or cur['secenek']:
                cur['secenek'] = True
                if om: cur['harf'] = om.group(1); cur['opts'].setdefault(cur['harf'], [])
                if cur.get('harf'): cur['opts'][cur['harf']].append(ws)
                if red:
                    rt = ' '.join(red).strip()
                    if re.fullmatch(r'[A-E]\)', rt): cur['kirmizi_harf'] = rt[0]
                    else: cur['cevap'].append(rt)
                continue
            if red: cur['cevap'].append(' '.join(red))
            cur['soru'].append(text)
    sonuc = []
    for n in sorted(sorular):
        q = sorular[n]
        soru = re.sub(r'\s+', ' ', ' '.join(q['soru'])).strip()
        cev = re.sub(r'\s+', ' ', ' '.join(q['cevap'])).strip()
        cev = SECENEK.sub('', cev)
        kayit = None
        if not cev and q.get('kirmizi_harf'):
            kayit = kayit_oku(q['opts'].get(q['kirmizi_harf'], []))
            cev = kayit_metin(kayit) if kayit else ''
        sonuc.append({'no': n, 'soru': soru, 'cevap': cev, 'kayit': kayit})
    return sonuc

if __name__ == '__main__':
    klasor, cikti = sys.argv[1], sys.argv[2]
    hepsi = []
    for f in sorted(glob.glob(klasor + '/*.pdf')):
        b = os.path.basename(f)
        if 'cevapsiz' in b: continue
        m = re.match(r'YETERLILIK_(\d{4})_(\d)_(.+)\.pdf', b)
        sinav, ders = f'{m.group(1)}-{m.group(2)}', DERS[m.group(3)]
        qs = cikar(f)
        eksik = [q['no'] for q in qs if not q['cevap']]
        print(f'{sinav} {ders}: {len(qs)} soru, cevapsız: {eksik}, numaralar: {qs[0]["no"] if qs else "-"}..{qs[-1]["no"] if qs else "-"}')
        for q in qs: q.update(sinav=sinav, ders=ders)
        hepsi += qs
    json.dump(hepsi, open(cikti, 'w'), ensure_ascii=False, indent=1)
    print('toplam', len(hepsi))
