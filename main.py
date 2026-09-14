import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
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
            # यह महत्वपूर्ण है: कोड ephe फ़ोल्डर की तलाश करेगा
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

        grid.add_widget(Label(text="City (e.g. Jodhpur):"))
        self.city_input = TextInput(text="Jodhpur", multiline=False)
        grid.add_widget(self.city_input)

        self.add_widget(grid)

        # Buttons
        btn_auto = Button(text="Run Automatic BTR (Live Transit)", size_hint_y=0.15, background_color=(0.2, 0.6, 1, 1))
        btn_auto.bind(on_press=self.run_auto_btr)
        self.add_widget(btn_auto)

        btn_manual = Button(text="Run Manual BTR (Custom)", size_hint_y=0.15, background_color=(1, 0.5, 0, 1))
        btn_manual.bind(on_press=self.run_manual_btr)
        self.add_widget(btn_manual)

        # Output Label
        self.result_label = Label(text="Enter details and select a mode.", size_hint_y=0.3, halign="center")
        self.add_widget(self.result_label)

    def get_coordinates(self, city_name):
        """Geopy का उपयोग करके शहर का Lat/Lon निकालना"""
        geolocator = Nominatim(user_agent="kp_btr_app")
        try:
            location = geolocator.geocode(city_name)
            if location:
                return location.latitude, location.longitude
            return None, None
        except:
            return None, None

    def run_auto_btr(self, instance):
        self.result_label.text = "Fetching coordinates and Live Transit..."
        city = self.city_input.text
        lat, lon = self.get_coordinates(city)
        
        if not lat or not lon:
            self.result_label.text = f"Error: Could not find coordinates for {city}.\nCheck internet or spelling."
            return

        # Live Time for Ruling Planets
        now = datetime.now()
        jd_now = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60.0)
        moon_pos_now, _ = swe.calc_ut(jd_now, swe.MOON, flags=swe.FLG_SIDEREAL)
        
        # Birth Time Lagna Calculation
        try:
            dob = self.dob_input.text.split('/')
            tob = self.tob_input.text.split(':')
            d, m, y = int(dob[0]), int(dob[1]), int(dob[2])
            h, mnt, s = int(tob[0]), int(tob[1]), int(tob[2])
            
            birth_time_dec = h + mnt/60.0 + s/3600.0
            jd_birth = swe.julday(y, m, d, birth_time_dec)
            
            cusps, ascmc = swe.houses_ex(jd_birth, lat, lon, b'P', flags=swe.FLG_SIDEREAL)
            birth_lagna = ascmc[0]

            self.result_label.text = (
                f"--- AUTOMATIC BTR RESULT ---\n"
                f"City: {city} (Lat: {lat:.2f}, Lon: {lon:.2f})\n"
                f"Unrectified Lagna Degree: {birth_lagna:.4f}\n"
                f"Live Moon (Transit): {moon_pos_now[0]:.4f}\n"
                f"Status: Ready for Sub-lord adjustment."
            )
        except Exception as e:
            self.result_label.text = f"Error in date/time format.\nUse DD/MM/YYYY and HH:MM:SS"

    def run_manual_btr(self, instance):
        self.result_label.text = "Manual Mode active.\n(Here you can implement a second screen\nto select your own Ruling Planets.)"

class KPApp(App):
    def build(self):
        return KPBTRApp()

if __name__ == '__main__':
    KPApp().run()
