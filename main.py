from kivy.config import Config
Config.set("kivy", "keyboard_mode", "system")

import json, os
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

# --- PAKET TAKİP TASARIM RENKLERİ ---
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
Window.clearcolor = BG
Window.softinput_mode = 'below_target'

islemler = []

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

# --- TASARIM SINIFLARI ---
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
        self.font_size = '16sp'
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
        self.font_size = '20sp'
        self.padding = [15, 10, 15, 10]
        self.multiline = False

class ButceApp(App):
    def build(self):
        global FILE, islemler
        self.title = 'Bütçe Yönetim'
        self.data_dir = self.user_data_dir
        FILE = os.path.join(self.data_dir, "butce_veri.json")
        islemler = yukle()

        self.root = BoxLayout(orientation='vertical', padding=[14, 14, 14, 10], spacing=10)

        # --- ÜST BAKİYE KARTI ---
        self.ust = Kart(r=26, orientation='vertical', size_hint_y=0.25, padding=[15, 15, 15, 15], spacing=2)
        self.ust.add_widget(Label(text='TOPLAM BAKİYE', font_size='13sp', color=MUT, bold=True, size_hint_y=0.2))
        self.bakiye_label = Label(text='0.00 TL', font_size='45sp', bold=True, color=YEL, size_hint_y=0.6)
        self.ust.add_widget(self.bakiye_label)
        self.detay_label = Label(text='', font_size='13sp', color=MUT, bold=True, size_hint_y=0.2)
        self.ust.add_widget(self.detay_label)
        self.root.add_widget(self.ust)

        self.ic = BoxLayout(orientation='vertical', spacing=10)
        self.root.add_widget(self.ic)

        # --- ALT MENÜ ---
        a = BoxLayout(size_hint_y=0.1, spacing=8)
        self.b_ekle = Buton(text='EKLE', bg=PUR, r=22)
        self.b_liste = Buton(text='LİSTE', bg=CARD, tc=MUT, r=22)
        self.b_ekle.bind(on_press=lambda x: self.sp())
        self.b_liste.bind(on_press=lambda x: self.sl())
        a.add_widget(self.b_ekle)
        a.add_widget(self.b_liste)
        self.root.add_widget(a)

        self.guncelle()
        self.sp()
        return self.root

    def guncelle(self):
        gelir = sum(i['tutar'] for i in islemler if i['tur'] == 'Gelir')
        gider = sum(i['tutar'] for i in islemler if i['tur'] == 'Gider')
        bakiye = gelir - gider
        renk = GRN if bakiye >= 0 else RED
        self.bakiye_label.text = '%.2f TL' % bakiye
        self.bakiye_label.color = renk
        self.detay_label.text = 'Gelir: %.2f | Gider: %.2f' % (gelir, gider)

    def rs(self, ak):
        self.b_ekle.renk(CARD, MUT)
        self.b_liste.renk(CARD, MUT)
        if ak == 'e': self.b_ekle.renk(PUR, TXT)
        elif ak == 'l': self.b_liste.renk(CYN, DRK)

    def tz(self):
        self.ic.clear_widgets()

    def sp(self):
        self.rs('e')
        self.tz()
        self.ic.add_widget(Label(text='YENİ İŞLEM EKLE', font_size='18sp', bold=True, color=TXT, size_hint_y=0.06))
        
        # Tür Seçimi
        k1 = Kart(r=20, orientation='horizontal', size_hint_y=0.15, padding=[15, 10, 15, 10], spacing=10)
        k1.add_widget(Label(text='Tür', font_size='15sp', color=MUT, size_hint_x=0.3, bold=True))
        self.spinner_tur = Spinner(text='Gider', values=('Gelir', 'Gider'), background_normal='', background_color=CHI, color=TXT, font_size='18sp')
        k1.add_widget(self.spinner_tur)
        self.ic.add_widget(k1)

        # Tutar
        k2 = Kart(r=20, orientation='horizontal', size_hint_y=0.15, padding=[15, 10, 15, 10], spacing=10)
        k2.add_widget(Label(text='Tutar', font_size='15sp', color=MUT, size_hint_x=0.3, bold=True))
        self.inp_tutar = In(input_type='number', hint_text='0.00')
        k2.add_widget(self.inp_tutar)
        self.ic.add_widget(k2)

        # Kategori
        k3 = Kart(r=20, orientation='horizontal', size_hint_y=0.15, padding=[15, 10, 15, 10], spacing=10)
        k3.add_widget(Label(text='Kategori', font_size='15sp', color=MUT, size_hint_x=0.3, bold=True))
        self.spinner_kat = Spinner(text='Market', values=('Market', 'Kira', 'Fatura', 'Maaş', 'Ek Gelir', 'Diğer'), background_normal='', background_color=CHI, color=TXT, font_size='18sp')
        k3.add_widget(self.spinner_kat)
        self.ic.add_widget(k3)

        kb = Buton(text='KAYDET', bg=GRN, tc=DRK, r=20, size_hint_y=0.15, font_size='20sp')
        kb.bind(on_press=self.kaydet)
        self.ic.add_widget(kb)

        self.mesaj = Label(text='', font_size='14sp', color=GRN, bold=True, size_hint_y=0.1)
        self.ic.add_widget(self.mesaj)

    def kaydet(self, inst):
        try:
            tutar = float(self.inp_tutar.text.replace(',', '.'))
            if tutar <= 0: raise ValueError
        except:
            self.mesaj.text = 'Geçerli bir tutar girin!'
            self.mesaj.color = RED
            return
        
        islem = {
            "tur": self.spinner_tur.text,
            "tutar": tutar,
            "kategori": self.spinner_kat.text,
            "tarih": datetime.now().strftime("%d-%m-%Y %H:%M")
        }
        islemler.append(islem)
        kaydet(islemler)
        self.guncelle()
        self.mesaj.text = 'İşlem başarıyla eklendi!'
        self.mesaj.color = GRN
        self.inp_tutar.text = ''

    def sl(self):
        self.rs('l')
        self.tz()
        self.ic.add_widget(Label(text='İŞLEM GEÇMİŞİ', font_size='18sp', bold=True, color=TXT, size_hint_y=0.06))
        
        if not islemler:
            self.ic.add_widget(Label(text='Henüz işlem yok.', color=MUT))
            return

        sc = ScrollView()
        bx = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8, padding=[4,4,4,4])
        bx.bind(minimum_height=bx.setter('height'))

        for i, islem in enumerate(reversed(islemler)):
            idx = len(islemler) - 1 - i
            renk = GRN if islem['tur'] == 'Gelir' else RED
            isaret = '+' if islem['tur'] == 'Gelir' else '-'
            
            k = Kart(r=14, bg=CHI, orientation='horizontal', size_hint_y=None, height=55, padding=[10, 5, 10, 5])
            lbl = Label(text=f"{isaret} {islem['kategori']}\n[color=aaaaaa]{islem['tarih']}[/color]", font_size='13sp', halign='left', valign='middle', markup=True, color=renk)
            lbl.bind(size=lbl.setter('text_size'))
            
            tutar = Label(text=f"{islem['tutar']:.2f} TL", font_size='15sp', bold=True, color=renk, size_hint_x=0.4)
            btn = Buton(text='Sil', bg=RED, r=8, size_hint_x=0.15, font_size='12sp')
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
            self.sl() # Listeyi yenile

if __name__ == '__main__':
    ButceApp().run()
