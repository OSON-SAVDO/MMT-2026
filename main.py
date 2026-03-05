from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.metrics import dp

# МАЪЛУМОТИ АСОСӢ (Ин ҷоро барои обновить кардан таҳрир кунед)
DATA = {
    "uni": "РӮЙХАТИ ДОНИШГОҲҲО:\n\n1. ДМТ (Душанбе)\n2. ДТТ (Хуҷанд)\n3. ДТМТ (Донишгоҳи Тиббӣ)",
    "coll": "РӮЙХАТИ КОЛЛЕҶҲО:\n\n1. Коллеҷи Тиббии Душанбе\n2. Коллеҷи Техникии Душанбе",
    "cl_1": "КЛАСТЕРИ 1: ТАБИӢ ВА ТЕХНИКӢ\n\nИхтисосҳо:\n1-400101 - ТИ\n1-310303 - Математика",
    "cl_2": "КЛАСТЕРИ 2: ИҚТИСОД ВА ГЕОГРАФИЯ\n\nИхтисосҳо:\n1-250103 - Иқтисод\n1-260202 - Менеҷмент",
    "cl_3": "КЛАСТЕРИ 3: ФИЛОЛОГИЯ ВА ПЕДАГОГИКА\n\nИхтисосҳо:\n1-020301 - Забони тоҷикӣ",
    "cl_4": "КЛАСТЕРИ 4: ҶОМЕАШИНОСӢ ВА ҲУҚУҚ\n\nИхтисосҳо:\n1-240102 - Ҳуқуқшиносӣ",
    "cl_5": "КЛАСТЕРИ 5: ТИББ ВА БИОЛОГИЯ\n\nИхтисосҳо:\n1-790101 - Кори табобатӣ",
    "tests": "ТЕСТҲОИ НАВ (Версияи 1.0):\n\nСаволи 1: Пойтахти Тоҷикистон кадом шаҳр аст?\nА) Душанбе\nБ) Хуҷанд",
    "ans": "ҶАВОБҲОИ ТЕСТҲО:\n\n1. Ҷавоби дуруст: А) Душанбе"
}

CL_COLORS = {
    1: (0.1, 0.5, 0.8, 1), 2: (0.1, 0.7, 0.3, 1), 3: (0.8, 0.5, 0.1, 1),
    4: (0.5, 0.2, 0.7, 1), 5: (0.8, 0.1, 0.1, 1)
}

class ClickableLabel(ButtonBehavior, Label):
    pass

class HomeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        l = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(8))
        title = ClickableLabel(text="ММТ 2026", font_size='28sp', bold=True, color=(0.1, 0.5, 0.8, 1), size_hint_y=0.15)
        title.bind(on_release=self.ask_password)
        l.add_widget(title)

        btns = [
            ("ДОНИШГОҲҲО", 'uni'), ("КОЛЛЕҶҲО", 'coll'), 
            ("КЛАСТЕРҲО (ИХТИСОС)", 'clast_menu'), ("ҲИСОБИ БАЛ", 'calc'),
            ("ТЕСТҲО", 'tests'), ("ҶАВОБҲО", 'ans')
        ]
        for text, key in btns:
            btn = Button(text=text, size_hint_y=None, height=dp(50), background_color=(0.12, 0.45, 0.7, 1), background_normal='')
            if key == 'clast_menu': btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'clast_menu'))
            elif key == 'calc': btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'calc'))
            else: btn.bind(on_release=lambda x, k=key, t=text: self.go_info(k, t))
            l.add_widget(btn)
        self.add_widget(l)

    def go_info(self, key, title):
        self.manager.get_screen('info').setup(title, key)
        self.manager.current = 'info'

    def ask_password(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.pw = TextInput(hint_text="Парол (7777)", password=True, multiline=False, size_hint_y=None, height=dp(45))
        content.add_widget(self.pw)
        btn = Button(text="ВОРУД", size_hint_y=None, height=dp(45))
        popup = Popup(title='Админ', content=content, size_hint=(0.8, 0.4))
        btn.bind(on_release=lambda x: self.check_pw(popup))
        content.add_widget(btn)
        popup.open()

    def check_pw(self, p):
        if self.pw.text == "7777": p.dismiss(); self.manager.current = 'admin'
        else: self.pw.hint_text = "ХАТО!"

class ClusterMenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        l = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        l.add_widget(Label(text="ИНТИХОБИ КЛАСТЕР", font_size='18sp', bold=True, color=(0,0,0,1)))
        for i in range(1, 6):
            btn = Button(text=f"КЛАСТЕРИ {i}", size_hint_y=None, height=dp(50), background_color=CL_COLORS[i], background_normal='')
            btn.bind(on_release=lambda x, n=i: self.go(n))
            l.add_widget(btn)
        l.add_widget(Button(text="БОЗГАШТ", height=dp(45), size_hint_y=None, on_release=lambda x: setattr(self.manager, 'current', 'home')))
        self.add_widget(l)
    def go(self, n):
        self.manager.get_screen('info').setup(f"КЛАСТЕРИ {n}", f"cl_{n}", CL_COLORS[n])
        self.manager.current = 'info'

class CalcScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        l = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))
        l.add_widget(Label(text="ҲИСОБИ БАЛ", font_size='22sp', bold=True, color=(0.1, 0.4, 0.7, 1)))
        self.val = TextInput(hint_text="Балли ибтидоӣ", multiline=False, input_type='number', height=dp(60), size_hint_y=None, font_size='20sp')
        l.add_widget(self.val)
        self.res = Label(text="Натиҷа: 0", font_size='24sp', bold=True, color=(0, 0.6, 0, 1))
        l.add_widget(self.res)
        btn = Button(text="ҲИСОБ", size_hint_y=None, height=dp(60), background_color=(0.1, 0.6, 0.2, 1), background_normal='')
        btn.bind(on_release=self.do_calc)
        l.add_widget(btn)
        l.add_widget(Button(text="БОЗГАШТ", height=dp(50), size_hint_y=None, on_release=lambda x: setattr(self.manager, 'current', 'home')))
        self.add_widget(l)
    def do_calc(self, x):
        if self.val.text.isdigit(): self.res.text = f"Балли шкалавӣ: ~{int(self.val.text) * 4}"
        else: self.res.text = "Рақам нависед!"

class InfoScreen(Screen):
    def setup(self, title, key, color=(0.1, 0.5, 0.8, 1)):
        self.title_label.text = title
        self.title_label.color = color
        self.content_label.text = DATA.get(key, "Маълумот нест")
    def __init__(self, **kw):
        super().__init__(**kw)
        l = BoxLayout(orientation='vertical', padding=dp(15))
        self.title_label = Label(text="", font_size='22sp', bold=True, size_hint_y=None, height=dp(60))
        l.add_widget(self.title_label)
        sc = ScrollView()
        self.content_label = Label(text="", size_hint_y=None, halign='left', font_size='18sp', color=(0,0,0,1))
        self.content_label.bind(size=self._s)
        sc.add_widget(self.content_label)
        l.add_widget(sc)
        l.add_widget(Button(text="БОЗГАШТ", height=dp(50), size_hint_y=None, on_release=lambda x: setattr(self.manager, 'current', 'home')))
        self.add_widget(l)
    def _s(self, *a):
        self.content_label.text_size = (self.content_label.width, None)
        self.content_label.height = self.content_label.texture_size[1]

class AdminScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        l = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        l.add_widget(Label(text="ТАҲРИР (Танҳо барои шумо)", color=(0,0,0,1), size_hint_y=None, height=dp(30)))
        self.et = TextInput(font_size='18sp', multiline=True, keyboard_suggestions=True)
        l.add_widget(self.et)
        sc = ScrollView(size_hint_y=None, height=dp(60))
        box = BoxLayout(size_hint_x=None, width=dp(900), spacing=dp(5))
        for k in DATA.keys():
            btn = Button(text=k.upper(), size_hint_x=None, width=dp(90), on_release=lambda x, key=k: self.load(key))
            box.add_widget(btn)
        sc.add_widget(box)
        l.add_widget(sc)
        l.add_widget(Button(text="ЗАХИРА (Дар телефон)", height=dp(55), background_color=(0,0.7,0,1), on_release=self.save))
        l.add_widget(Button(text="БОЗГАШТ", height=dp(45), on_release=lambda x: setattr(self.manager, 'current', 'home')))
        self.add_widget(l)
    def load(self, k): self.cur = k; self.et.text = DATA[k]
    def save(self, x): 
        if hasattr(self, 'cur'): DATA[self.cur] = self.et.text
        self.manager.current = 'home'

class MMTApp(App):
    def build(self):
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        Window.softinput_mode = "below_target"
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ClusterMenuScreen(name='clast_menu'))
        sm.add_widget(CalcScreen(name='calc'))
        sm.add_widget(InfoScreen(name='info'))
        sm.add_widget(AdminScreen(name='admin'))
        return sm

if __name__ == "__main__":
    MMTApp().run()
