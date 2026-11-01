from kivy.config import Config
Config.set("kivy", "keyboard_mode", "system")

import json, os, calendar
from datetime import datetime, date
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

BG   = (0.05, 0.07, 0.12, 1)
CARD = (0.11, 0.14, 0.21, 1)
CHI  = (0.16, 0.20, 0.29, 1)
TXT  = (0.96, 0.97, 0.99, 1)
MUT  = (0.55, 0.62, 0.72, 1)
PUR  = (0.55, 0.36, 0.96, 1)
CYN  = (0.02, 0.71, 0.83, 1)
GRN  = (0.06, 0.72, 0.51, 1)
RED  = (0.94, 0.27, 0.42, 1)
YEL  = (0.98, 0.75, 0.14, 1)
DRK  = (0.05, 0.05, 0.10, 1)

FILE = "butce_veri.json"
LANG_FILE = "butce_dil.json"
Window.clearcolor = BG
Window.softinput_mode = 'below_target'

islemler = []
dil_ayar = "tr"

DIL = {
    'tr': {
        'toplam': 'TOPLAM BAKİYE',
        'gelir': 'Gelir', 'gider': 'Gider',
        'ekle': 'EKLE', 'liste': 'LİSTE', 'takvim': 'TAKVİM',
        'yeni_islem': 'YENİ İŞLEM EKLE',
        'tur': 'Tür', 'tutar': 'Tutar', 'kategori': 'Kategori',
        'ne': 'Ne?', 'kaydet': 'KAYDET', 'sil': 'Sil', 'diger': 'Diğer',
        'market': 'Market', 'kira': 'Kira', 'fatura': 'Fatura',
        'maas': 'Maaş', 'ek_gelir': 'Ek Gelir',
        'islem_gecmisi': 'İŞLEM GEÇMİŞİ',
        'henuz_islem_yok': 'Henüz işlem yok.',
        'ozel_hint': 'Örn: Kahve, Hediye...',
        'gecerli_tutar': '❌ Geçerli bir tutar girin!',
        'eklendi': '✅ {} / {:.2f} TL eklendi',
        'aylar': ['', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'],
        'gunler': ['Pt', 'Sa', 'Ça', 'Pe', 'Cu', 'Ct', 'Pa'],
        'dil_btn': 'EN',
    },
    'en': {
        'toplam': 'TOTAL BALANCE',
        'gelir': 'Income', 'gider': 'Expense',
        'ekle': 'ADD', 'liste': 'LIST', 'takvim': 'CALENDAR',
        'yeni_islem': 'ADD NEW TRANSACTION',
        'tur': 'Type', 'tutar': 'Amount', 'kategori': 'Category',
        'ne': 'What?', 'kaydet': 'SAVE', 'sil': 'Delete', 'diger': 'Other',
        'market': 'Market', 'kira': 'Rent', 'fatura': 'Bill',
        'maas': 'Salary', 'ek_gelir': 'Extra Income',
        'islem_gecmisi': 'TRANSACTION HISTORY',
        'henuz_islem_yok': 'No transactions yet.',
        'ozel_hint': 'e.g.: Coffee, Gift...',
        'gecerli_tutar': '❌ Enter a valid amount!',
        'eklendi': '✅ {} / {:.2f} TL added',
        'aylar': ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        'gunler': ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'],
        'dil_btn': 'BG',
    },
    'bg': {
        'toplam': 'ОБЩО САЛДО',
        'gelir': 'Приход', 'gider': 'Разход',
        'ekle': 'ДОБАВИ', 'liste': 'СПИСЪК', 'takvim': 'КАЛЕНДАР',
        'yeni_islem': 'НОВА ТРАНЗАКЦИЯ',
        'tur': 'Тип', 'tutar': 'Сума', 'kategori': 'Категория',
        'ne': 'Какво?', 'kaydet': 'ЗАПАЗИ', 'sil': 'Изтрий', 'diger': 'Друго',
        'market': 'Пазар', 'kira': 'Наем', 'fatura': 'Сметка',
        'maas': 'Заплата', 'ek_gelir': 'Доп. доход',
        'islem_gecmisi': 'ИСТОРИЯ НА ТРАНЗАКЦИИТЕ',
        'henuz_islem_yok': 'Все още няма транзакции.',
        'ozel_hint': 'Напр.: Кафе, Подарък...',
        'gecerli_tutar': '❌ Въведете валидна сума!',
        'eklendi': '✅ {} / {:.2f} TL добавено',
        'aylar': ['', 'Януари', 'Февруари', 'Март', 'Април', 'Май', 'Юни', 'Юли', 'Август', 'Септември', 'Октомври', 'Ноември', 'Декември'],
        'gunler': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'],
        'dil_btn': 'TR',
    }
}

KAT_KEYLER = ('market', 'kira', 'fatura', 'maas', 'ek_gelir', 'diger')

def dil(k):
    return DIL.get(dil_ayar, DIL['tr']).get(k, k)

def dil_yukle():
    global dil_ayar
    if os.path.exists(LANG_FILE):
        try:
            with open(LANG_FILE) as f:
                dil_ayar = json.load(f).get('lang', 'tr')
        except:
            dil_ayar = 'tr'

def dil_kaydet():
    with open(LANG_FILE, 'w') as f:
        json.dump({'lang': dil_ayar}, f)

def tur_canonical(t):
    t = str(t).lower()
    return 'gelir' if t in ('gelir', 'income', 'приход') else 'gider'

def kat_canonical(k):
    kl = str(k).lower()
    for key in KAT_KEYLER:
        for lang in DIL:
            if kl == DIL[lang][key].lower():
                return key
    return k

def kat_display(kv):
    if kv in KAT_KEYLER:
        return dil(kv)
    kvl = str(kv).lower()
    for key in KAT_KEYLER:
        for lang in DIL:
            if kvl == DIL[lang][key].lower():
                return dil(key)
    return kv

def yukle():
    if os.path.exists(FILE):
        try:
            with open(FILE, encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def kaydet(v):
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(v, f, ensure_ascii=False)


class Kart(BoxLayout):
    def __init__(self, r=20, bg=CARD, **kw):
        super().__init__(**kw)
        with self.canvas.before:
            self._c = Color(*bg)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[r])
        self.bind(pos=self._u, size=self._u)
    def _u(self, *a):
        self._rect.pos = self.pos
        self._rect.size = self.size

class Buton(Button):
    def __init__(self, r=16, bg=PUR, tc=TXT, **kw):
        super().__init__(**kw)
        self.background_normal = ''
        self.background_active = ''
        self.background_color = (0, 0, 0, 0)
        self.color = tc
        self.bold = True
        self.font_size = '15sp'
        with self.canvas.before:
            self._c = Color(*bg)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[r])
        self.bind(pos=self._u, size=self._u)
    def _u(self, *a):
        self._rect.pos = self.pos
        self._rect.size = self.size
    def renk(self, bg, tc=None):
        self._c.rgba = bg
        if tc: self.color = tc

class In(TextInput):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.background_normal = ''
        self.background_active = ''
        self.background_color = CHI
        self.foreground_color = TXT
        self.cursor_color = PUR
        self.hint_text_color = MUT
        self.font_size = '18sp'
        self.padding = [15, 10, 15, 10]
        self.multiline = False


class ButceApp(App):
    def build(self):
        global FILE, islemler
        self.title = 'Bütçe Yönetim'
        self.data_dir = self.user_data_dir
        FILE = os.path.join(self.data_dir, "butce_veri.json")
        islemler = yukle()
        dil_yukle()
        self.aktif_tab = 'e'
        self.root = BoxLayout(orientation='vertical', padding=[14, 14, 14, 10], spacing=10)
        self.olustur()
        return self.root

    def olustur(self):
        self.root.clear_widgets()

        self.ust = Kart(r=26, orientation='vertical', size_hint_y=0.22, padding=[15, 10, 15, 10], spacing=2)
        ust_satir = BoxLayout(orientation='horizontal', size_hint_y=0.25)
        ust_satir.add_widget(Label(text=dil('toplam'), font_size='13sp', color=MUT, bold=True))
        self.dil_btn = Buton(text=dil('dil_btn'), bg=CHI, tc=CYN, r=10, font_size='12sp', size_hint_x=0.2)
        self.dil_btn.bind(on_press=self.dil_degistir)
        ust_satir.add_widget(self.dil_btn)
        self.ust.add_widget(ust_satir)
        self.bakiye_label = Label(text='0.00 TL', font_size='45sp', bold=True, color=YEL, size_hint_y=0.6)
        self.ust.add_widget(self.bakiye_label)
        self.detay_label = Label(text='', font_size='13sp', color=MUT, bold=True, size_hint_y=0.2)
        self.ust.add_widget(self.detay_label)
        self.root.add_widget(self.ust)

        self.ic = BoxLayout(orientation='vertical', spacing=10)
        self.root.add_widget(self.ic)

        a = BoxLayout(size_hint_y=0.1, spacing=6)
        self.b_ekle = Buton(text=dil('ekle'), bg=PUR, r=22, font_size='14sp')
        self.b_liste = Buton(text=dil('liste'), bg=CARD, tc=MUT, r=22, font_size='14sp')
        self.b_takvim = Buton(text=dil('takvim'), bg=CARD, tc=MUT, r=22, font_size='14sp')
        self.b_ekle.bind(on_press=lambda x: self.sp())
        self.b_liste.bind(on_press=lambda x: self.sl())
        self.b_takvim.bind(on_press=lambda x: self.st())
        a.add_widget(self.b_ekle)
        a.add_widget(self.b_liste)
        a.add_widget(self.b_takvim)
        self.root.add_widget(a)

        self.guncelle()
        if self.aktif_tab == 'e': self.sp()
        elif self.aktif_tab == 'l': self.sl()
        elif self.aktif_tab == 't': self.st()

    def dil_degistir(self, inst):
        global dil_ayar
        dil_ayar = {'tr': 'en', 'en': 'bg', 'bg': 'tr'}[dil_ayar]
        dil_kaydet()
        self.olustur()

    def guncelle(self):
        gelir = sum(i['tutar'] for i in islemler if tur_canonical(i['tur']) == 'gelir')
        gider = sum(i['tutar'] for i in islemler if tur_canonical(i['tur']) == 'gider')
        bakiye = gelir - gider
        renk = GRN if bakiye >= 0 else RED
        self.bakiye_label.text = '%.2f TL' % bakiye
        self.bakiye_label.color = renk
        self.detay_label.text = '%s: %.2f | %s: %.2f' % (dil('gelir'), gelir, dil('gider'), gider)

    def rs(self, ak):
        self.b_ekle.renk(CARD, MUT)
        self.b_liste.renk(CARD, MUT)
        self.b_takvim.renk(CARD, MUT)
        if ak == 'e': self.b_ekle.renk(PUR, TXT)
        elif ak == 'l': self.b_liste.renk(CYN, DRK)
        elif ak == 't': self.b_takvim.renk(GRN, DRK)

    def tz(self):
        self.ic.clear_widgets()

    def sp(self):
        self.aktif_tab = 'e'
        self.rs('e')
        self.tz()
        self.ic.add_widget(Label(text=dil('yeni_islem'), font_size='18sp', bold=True, color=TXT, size_hint_y=0.06))

        k1 = Kart(r=20, orientation='horizontal', size_hint_y=0.12, padding=[15, 8, 15, 8], spacing=10)
        k1.add_widget(Label(text=dil('tur'), font_size='15sp', color=MUT, size_hint_x=0.3, bold=True))
        self.spinner_tur = Spinner(text=dil('gider'), values=(dil('gelir'), dil('gider')),
                                   background_normal='', background_color=CHI, color=TXT, font_size='18sp')
        k1.add_widget(self.spinner_tur)
        self.ic.add_widget(k1)

        k2 = Kart(r=20, orientation='horizontal', size_hint_y=0.12, padding=[15, 8, 15, 8], spacing=10)
        k2.add_widget(Label(text=dil('tutar'), font_size='15sp', color=MUT, size_hint_x=0.3, bold=True))
        self.inp_tutar = In(input_type='number', hint_text='0.00')
        k2.add_widget(self.inp_tutar)
        self.ic.add_widget(k2)

        k3 = Kart(r=20, orientation='horizontal', size_hint_y=0.12, padding=[15, 8, 15, 8], spacing=10)
        k3.add_widget(Label(text=dil('kategori'), font_size='15sp', color=MUT, size_hint_x=0.3, bold=True))
        self.spinner_kat = Spinner(
            text=dil('market'),
            values=(dil('market'), dil('kira'), dil('fatura'), dil('maas'), dil('ek_gelir'), dil('diger')),
            background_normal='', background_color=CHI, color=TXT, font_size='15sp')
        self.spinner_kat.bind(text=self.on_kategori_change)
        k3.add_widget(self.spinner_kat)
        self.ic.add_widget(k3)

        self.custom_kat_kart = Kart(r=20, orientation='horizontal', size_hint_y=None, height=0,
                                    padding=[15, 8, 15, 8], spacing=10, opacity=0, disabled=True)
        self.custom_kat_kart.add_widget(Label(text=dil('ne'), font_size='15sp', color=YEL, size_hint_x=0.3, bold=True))
        self.custom_kat_input = In(hint_text=dil('ozel_hint'))
        self.custom_kat_kart.add_widget(self.custom_kat_input)
        self.ic.add_widget(self.custom_kat_kart)

        kb = Buton(text=dil('kaydet'), bg=GRN, tc=DRK, r=20, size_hint_y=0.14, font_size='20sp')
        kb.bind(on_press=self.kaydet)
        self.ic.add_widget(kb)

        self.mesaj = Label(text='', font_size='14sp', color=GRN, bold=True, size_hint_y=0.1)
        self.ic.add_widget(self.mesaj)

    def on_kategori_change(self, spinner, text):
        if text == dil('diger'):
            self.custom_kat_kart.height = 60
            self.custom_kat_kart.opacity = 1
            self.custom_kat_kart.disabled = False
        else:
            self.custom_kat_kart.height = 0
            self.custom_kat_kart.opacity = 0
            self.custom_kat_kart.disabled = True
            if hasattr(self, 'custom_kat_input'):
                self.custom_kat_input.text = ''

    def kaydet(self, inst):
        try:
            tutar = float(self.inp_tutar.text.replace(',', '.'))
            if tutar <= 0: raise ValueError
        except:
            self.mesaj.text = dil('gecerli_tutar')
            self.mesaj.color = RED
            return

        tur = tur_canonical(self.spinner_tur.text)
        secilen = self.spinner_kat.text
        if secilen == dil('diger'):
            ozel = self.custom_kat_input.text.strip()
            kategori = ozel if ozel else 'diger'
        else:
            kategori = kat_canonical(secilen)

        islem = {
            "tur": tur,
            "tutar": tutar,
            "kategori": kategori,
            "tarih": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        islemler.append(islem)
        kaydet(islemler)
        self.guncelle()
        self.mesaj.text = dil('eklendi').format(kat_display(kategori), tutar)
        self.mesaj.color = GRN
        self.inp_tutar.text = ''
        self.custom_kat_input.text = ''

    def sl(self):
        self.aktif_tab = 'l'
        self.rs('l')
        self.tz()
        self.ic.add_widget(Label(text=dil('islem_gecmisi'), font_size='18sp', bold=True, color=TXT, size_hint_y=0.06))

        if not islemler:
            self.ic.add_widget(Label(text=dil('henuz_islem_yok'), color=MUT))
            return

        sc = ScrollView()
        bx = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8, padding=[4, 4, 4, 4])
        bx.bind(minimum_height=bx.setter('height'))

        for i, islem in enumerate(reversed(islemler)):
            idx = len(islemler) - 1 - i
            ct = tur_canonical(islem['tur'])
            renk = GRN if ct == 'gelir' else RED
            isaret = '+' if ct == 'gelir' else '-'
            k = Kart(r=14, bg=CHI, orientation='horizontal', size_hint_y=None, height=55, padding=[10, 5, 10, 5])
            lbl = Label(text=f"{isaret} {kat_display(islem['kategori'])}\n[color=aaaaaa]{islem['tarih']}[/color]",
                        font_size='13sp', halign='left', valign='middle', markup=True, color=renk)
            lbl.bind(size=lbl.setter('text_size'))
            tutar = Label(text=f"{islem['tutar']:.2f} TL", font_size='15sp', bold=True, color=renk, size_hint_x=0.35)
            btn = Buton(text=dil('sil'), bg=RED, r=8, size_hint_x=0.18, font_size='11sp')
            btn.bind(on_press=lambda x, j=idx: self.sil(j))
            k.add_widget(lbl)
            k.add_widget(tutar)
            k.add_widget(btn)
            bx.add_widget(k)

        sc.add_widget(bx)
        self.ic.add_widget(sc)

    def sil(self, idx):
        if 0 <= idx < len(islemler):
            del islemler[idx]
            kaydet(islemler)
            self.guncelle()
            self.sl()

    def st(self):
        self.aktif_tab = 't'
        self.rs('t')
        self.tz()
        b = date.today()
        y, mo = b.year, b.month
        AYLAR = dil('aylar')
        self.ic.add_widget(Label(text='%s %d' % (AYLAR[mo], y), font_size='22sp', bold=True, color=TXT, size_hint_y=0.06))

        gunluk = {}
        for islem in islemler:
            gun = islem['tarih'][:10]
            if tur_canonical(islem['tur']) == 'gelir':
                gunluk[gun] = gunluk.get(gun, 0) + islem['tutar']
            else:
                gunluk[gun] = gunluk.get(gun, 0) - islem['tutar']

        kart = Kart(r=20, padding=[8, 10, 8, 10], size_hint_y=0.85)
        g = GridLayout(cols=7, spacing=4)
        for x in dil('gunler'):
            g.add_widget(Label(text=x, bold=True, font_size='12sp', color=MUT))
        c = calendar.Calendar(firstweekday=0)
        for hf in c.monthdayscalendar(y, mo):
            for gn in hf:
                if gn == 0:
                    g.add_widget(Widget())
                else:
                    gs = '%04d-%02d-%02d' % (y, mo, gn)
                    d = gunluk.get(gs, None)
                    if d is None:
                        rn, yt, al = CHI, MUT, '-'
                    elif d > 0:
                        rn, yt, al = GRN, DRK, '+%.0f' % d
                    elif d < 0:
                        rn, yt, al = RED, TXT, '%.0f' % d
                    else:
                        rn, yt, al = YEL, DRK, '0'
                    h = Kart(r=12, bg=rn, orientation='vertical', padding=[2, 4, 2, 4], spacing=0)
                    h.add_widget(Label(text=str(gn), font_size='14sp', bold=True, color=yt))
                    h.add_widget(Label(text=al, font_size='10sp', color=yt))
                    g.add_widget(h)
        kart.add_widget(g)
        self.ic.add_widget(kart)

if __name__ == '__main__':
    ButceApp().run()
