import swisseph as swe
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

class KPBTRApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        
        # Swiss Ephemeris Setup
        try:
            swe.set_ephe_path('./ephe')
            swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
        except Exception as e:
            pass

        # Title
        self.add_widget(Label(text="KP BTR Astrology App", font_size='24sp', size_hint_y=0.1))

        # Input Grid
        grid = GridLayout(cols=2, size_hint_y=0.4, spacing=5)
        
        grid.add_widget(Label(text="Date (DD/MM/YYYY):"))
        self.dob_input = TextInput(text="30/06/1983", multiline=False)
        grid.add_widget(self.dob_input)

        grid.add_widget(Label(text="Time (HH:MM:SS):"))
        self.tob_input = TextInput(text="01:16:00", multiline=False)
        grid.add_widget(self.tob_input)

        grid.add_widget(Label(text="Latitude (e.g. 26.24):"))
        self.lat_input = TextInput(text="26.2389", multiline=False)
        grid.add_widget(self.lat_input)

        grid.add_widget(Label(text="Longitude (e.g. 73.02):"))
        self.lon_input = TextInput(text="73.0243", multiline=False)
        grid.add_widget(self.lon_input)

        self.add_widget(grid)

        # Buttons
        btn_run = Button(text="Run KP BTR Calculation", size_hint_y=0.15, background_color=(0.2, 0.6, 1, 1))
        btn_run.bind(on_press=self.run_btr_calc)
        self.add_widget(btn_run)

        # Output Label
        self.result_label = Label(text="Enter details and press calculate.", size_hint_y=0.35, halign="center")
        self.add_widget(self.result_label)

    def run_btr_calc(self, instance):
        try:
            lat = float(self.lat_input.text)
            lon = float(self.lon_input.text)
            
            dob = self.dob_input.text.split('/')
            tob = self.tob_input.text.split(':')
            d, m, y = int(dob[0]), int(dob[1]), int(dob[2])
            h, mnt, s = int(tob[0]), int(tob[1]), int(tob[2])
            
            birth_time_dec = h + mnt/60.0 + s/3600.0
            jd_birth = swe.julday(y, m, d, birth_time_dec)
            
            # Calculate Lagna
            cusps, ascmc = swe.houses_ex(jd_birth, lat, lon, b'P', flags=swe.FLG_SIDEREAL)
            birth_lagna = ascmc[0]

            # Live Transit Moon
            now = datetime.now()
            jd_now = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60.0)
            moon_pos_now, _ = swe.calc_ut(jd_now, swe.MOON, flags=swe.FLG_SIDEREAL)

            self.result_label.text = (
                f"--- KP BTR SUCCESS ---\n"
                f"Lagna Degree: {birth_lagna:.4f}°\n"
                f"Live Moon Degree: {moon_pos_now[0]:.4f}°\n"
                f"Status: Calculation Complete!"
            )
        except Exception as e:
            self.result_label.text = f"Calculation Error:\n{str(e)}"

class KPApp(App):
    def build(self):
        return KPBTRApp()

if __name__ == '__main__':
    KPApp().run()
