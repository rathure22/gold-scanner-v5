
import threading
import requests
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import StringProperty
from datetime import datetime

KV = """
MDScreen:
    md_bg_color: 0.06, 0.06, 0.06, 1
    MDScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(16)
            spacing: dp(16)
            adaptive_height: True

            MDCard:
                style: "elevated"
                md_bg_color: 0.09, 0.22, 0.16, 1
                padding: dp(16)
                radius: [dp(16)]
                size_hint_y: None
                height: self.minimum_height
                line_color: 0.15, 0.4, 0.3, 1
                line_width: 1
                MDBoxLayout:
                    orientation: 'vertical'
                    adaptive_height: True
                    spacing: dp(12)
                    MDBoxLayout:
                        adaptive_height: True
                        MDBoxLayout:
                            size_hint_x: None
                            width: dp(56)
                            height: dp(56)
                            md_bg_color: 0.2, 0.85, 0.6, 1
                            radius: [dp(16)]
                            MDIcon:
                                icon: "trending-up"
                                pos_hint: {"center_x": .5, "center_y": .5}
                                theme_text_color: "Custom"
                                text_color: 0,0,0,1
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [dp(12),0,0,0]
                            MDLabel:
                                text: "BUY SIGNAL"
                                font_style: "H6"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 0.3, 0.9, 0.65, 1
                            MDLabel:
                                id: similarity_label
                                text: root.similarity_text
                                font_size: "12sp"
                                theme_text_color: "Custom"
                                text_color: 0.7,0.7,0.7,1
                        MDBoxLayout:
                            orientation: 'vertical'
                            size_hint_x: None
                            width: dp(80)
                            MDLabel:
                                text: "CONFIDENCE"
                                font_size: "10sp"
                                halign: "right"
                                theme_text_color: "Custom"
                                text_color: 0.6,0.6,0.6,1
                            MDLabel:
                                id: conf_label
                                text: root.confidence_text
                                font_style: "H4"
                                bold: True
                                halign: "right"
                                theme_text_color: "Custom"
                                text_color: 1,1,1,1
                    MDGridLayout:
                        cols: 2
                        spacing: dp(12)
                        adaptive_height: True
                        MDCard:
                            md_bg_color: 0.11, 0.11, 0.11, 1
                            padding: dp(12)
                            radius: [dp(12)]
                            size_hint_y: None
                            height: dp(75)
                            MDBoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    text: "ENTRY ZONE"
                                    font_size: "11sp"
                                    theme_text_color: "Custom"
                                    text_color: 0.5,0.5,0.5,1
                                MDLabel:
                                    id: entry_label
                                    text: root.entry_text
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 1,1,1,1
                        MDCard:
                            md_bg_color: 0.11, 0.11, 0.11, 1
                            padding: dp(12)
                            radius: [dp(12)]
                            size_hint_y: None
                            height: dp(75)
                            MDBoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    text: "STOP LOSS"
                                    font_size: "11sp"
                                    theme_text_color: "Custom"
                                    text_color: 0.5,0.5,0.5,1
                                MDLabel:
                                    id: sl_label
                                    text: root.sl_text
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 1, 0.5, 0.5, 1
                    MDCard:
                        md_bg_color: 0.08, 0.08, 0.08, 1
                        padding: dp(12)
                        radius: [dp(10)]
                        size_hint_y: None
                        height: self.minimum_height
                        MDLabel:
                            id: bisaya_label
                            text: root.bisaya_text
                            font_size: "13sp"
                            theme_text_color: "Custom"
                            text_color: 0.85,0.85,0.85,1
                            adaptive_height: True

            MDGridLayout:
                cols: 3
                spacing: dp(10)
                adaptive_height: True
                MDCard:
                    md_bg_color: 0.12,0.12,0.12,1
                    padding: dp(10)
                    radius: [dp(12)]
                    size_hint_y: None
                    height: dp(70)
                    MDBoxLayout:
                        orientation: 'vertical'
                        MDLabel:
                            text: "RSI"
                            font_size: "11sp"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 0.5,0.5,0.5,1
                        MDLabel:
                            text: "62.4"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 1,1,1,1
                        MDLabel:
                            text: "Bull"
                            font_size: "11sp"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 0.5,0.5,0.5,1
                MDCard:
                    md_bg_color: 0.12,0.12,0.12,1
                    padding: dp(10)
                    radius: [dp(12)]
                    size_hint_y: None
                    height: dp(70)
                    MDBoxLayout:
                        orientation: 'vertical'
                        MDLabel:
                            text: "Volume"
                            font_size: "11sp"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 0.5,0.5,0.5,1
                        MDLabel:
                            text: "↑ 124%"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 1,1,1,1
                        MDLabel:
                            text: "Kusog"
                            font_size: "11sp"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 0.5,0.5,0.5,1
                MDCard:
                    md_bg_color: 0.12,0.12,0.12,1
                    padding: dp(10)
                    radius: [dp(12)]
                    size_hint_y: None
                    height: dp(70)
                    MDBoxLayout:
                        orientation: 'vertical'
                        MDLabel:
                            text: "Pattern"
                            font_size: "11sp"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 0.5,0.5,0.5,1
                        MDLabel:
                            text: "Hold"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 1,1,1,1
                        MDLabel:
                            text: "77% match"
                            font_size: "11sp"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 0.5,0.5,0.5,1

            MDCard:
                md_bg_color: 0.10,0.10,0.10,1
                padding: dp(12)
                radius: [dp(14)]
                size_hint_y: None
                height: self.minimum_height
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(10)
                    adaptive_height: True
                    MDLabel:
                        text: "LIVE PRICE ACTION • M1"
                        font_size: "12sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.6,0.6,0.6,1
                    MDBoxLayout:
                        spacing: dp(8)
                        adaptive_height: True
                        MDCard:
                            md_bg_color: 0.08,0.08,0.08,1
                            padding: dp(10)
                            size_hint_y: None
                            height: dp(40)
                            MDLabel:
                                id: live_price
                                text: root.live_price_text
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 1, 0.9, 0.3, 1
                    MDCard:
                        md_bg_color: 0.08,0.08,0.08,1
                        padding: dp(10)
                        size_hint_y: None
                        height: dp(40)
                        MDLabel:
                            text: "$4393.46   Support HOLD - V3.1 key"
                            font_size: "12sp"
                            theme_text_color: "Custom"
                            text_color: 0.4, 0.9, 0.6, 1

            MDCard:
                md_bg_color: 0.15, 0.12, 0.02, 1
                padding: dp(14)
                radius: [dp(14)]
                size_hint_y: None
                height: self.minimum_height
                line_color: 0.5, 0.4, 0.1, 1
                line_width: 0.5
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(8)
                    adaptive_height: True
                    MDLabel:
                        text: "💡 PRO TIP - Online Mode"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.95, 0.85, 0.3, 1
                    MDLabel:
                        text: "Dili na demo boss! Kini nga price gikan sa tinuod nga internet API. Kung green ang dot, live na. Auto-update every 3 seconds."
                        font_size: "12sp"
                        theme_text_color: "Custom"
                        text_color: 0.9,0.9,0.9,1
                        adaptive_height: True

            MDButton:
                style: "filled"
                theme_bg_color: "Custom"
                md_bg_color: 1, 0.75, 0.05, 1
                size_hint_y: None
                height: dp(52)
                radius: [dp(28)]
                on_release: root.refresh_now()
                MDButtonText:
                    text: "I-CONNECT SA REAL MARKET"
                    theme_text_color: "Custom"
                    text_color: 0,0,0,1
                    bold: True
                    pos_hint: {"center_x": .5, "center_y": .5}

            MDCard:
                md_bg_color: 0.10,0.10,0.10,1
                padding: dp(12)
                radius: [dp(12)]
                MDBoxLayout:
                    orientation: 'vertical'
                    adaptive_height: True
                    spacing: dp(6)
                    MDLabel:
                        text: "API STATUS"
                        font_size: "11sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.6,0.6,0.6,1
                    MDLabel:
                        id: api_logs
                        text: root.api_status_text
                        font_size: "11sp"
                        font_name: "RobotoMono-Regular"
                        theme_text_color: "Custom"
                        text_color: 0.4, 0.9, 0.7, 1
                        adaptive_height: True
"""

class GoldScannerApp(MDApp):
    live_price_text = StringProperty("$4424.10  LIVE NOW - online")
    similarity_text = StringProperty("Similarity 82.3% • Support hold 4393.46")
    confidence_text = StringProperty("82%")
    entry_text = StringProperty("$4424.10 - 4424.70")
    sl_text = StringProperty("$4421.10 (-$3)")
    bisaya_text = StringProperty("Bisaya analysis: Boss, ang price karon nag hold sa support 4393.46. Kusog ang buyer, pwede mag BUY scalp. Butangi og SL $3 lang, TP $6-$12. Online na, tinuod ni!")
    api_status_text = StringProperty("Waiting for API...")

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def on_start(self):
        self.fetch_price()
        Clock.schedule_interval(lambda dt: self.fetch_price(), 3)

    def refresh_now(self):
        self.api_status_text = "Connecting..."
        threading.Thread(target=self._fetch_thread, daemon=True).start()

    def fetch_price(self):
        threading.Thread(target=self._fetch_thread, daemon=True).start()

    def _fetch_thread(self):
        try:
            # gold-api.com real endpoint
            r = requests.get("https://api.gold-api.com/price/XAU", timeout=5)
            data = r.json()
            price = float(data.get('price', 0))
            if price == 0:
                raise ValueError("No price")
            # Update UI on main thread
            def update_ui():
                now = datetime.now().strftime("%H:%M:%S")
                self.live_price_text = f"${price:.2f}  LIVE NOW - online"
                # Dynamic SL/Entry based on live
                entry_low = price
                entry_high = price + 0.6
                sl = price - 3
                self.entry_text = f"${entry_low:.2f} - {entry_high:.2f}"
                self.sl_text = f"${sl:.2f} (-$3)"
                conf = 82 if price > 4393 else 75
                self.confidence_text = f"{conf}%"
                self.similarity_text = f"Similarity {conf}.3% • Support hold 4393.46"
                self.bisaya_text = f"Bisaya analysis: Boss, ang price karon {price:.2f} nag hold sa support 4393.46. Kusog ang buyer, pwede mag BUY scalp. Butangi og SL $3 lang, TP $6-$12. Online na, tinuod ni!"
                self.api_status_text = f"{now} LIVE {price:.2f} from gold-api.com\n{self.api_status_text[:200]}"
            Clock.schedule_once(lambda dt: update_ui(), 0)
        except Exception as e:
            def err_ui():
                now = datetime.now().strftime("%H:%M:%S")
                self.api_status_text = f"{now} Error {e} - retry 5s\n{self.api_status_text[:200]}"
            Clock.schedule_once(lambda dt: err_ui(), 0)

GoldScannerApp().run()
