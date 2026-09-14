import swisseph as swe
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class KPBTRApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        # GitHub Actions में ऐप बनने के बाद ephe फ़ोल्डर का पाथ
        swe.set_ephe_path('./ephe') 
        swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
        
        self.result_label = Label(text="KP BTR App Ready!\nManual & Auto Modes Available.", halign="center")
        self.add_widget(self.result_label)
        
        # Auto Mode Button
        btn_auto = Button(text="Run Automatic BTR (Live Gocher)", size_hint=(1, 0.2))
        btn_auto.bind(on_press=self.run_auto_btr)
        self.add_widget(btn_auto)

        # Manual Mode Button
        btn_manual = Button(text="Run Manual BTR (Custom RPs)", size_hint=(1, 0.2))
        btn_manual.bind(on_press=self.run_manual_btr)
        self.add_widget(btn_manual)

    def run_auto_btr(self, instance):
        # यहाँ आपका BTR_Algorithm.py वाला लॉजिक आएगा
        now = datetime.now()
        jd = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60.0)
        moon_pos, _ = swe.calc_ut(jd, swe.MOON, flags=swe.FLG_SIDEREAL)
        
        self.result_label.text = f"Auto Mode Run!\nLive Moon Degree: {moon_pos[0]:.2f}\nBTR Rectification processing..."

    def run_manual_btr(self, instance):
        self.result_label.text = "Manual Mode Selected.\nEnter your RPs to rectify."

class MyApp(App):
    def build(self):
        return KPBTRApp()

if __name__ == '__main__':
    MyApp().run()
