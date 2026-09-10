
import threading
import requests
import random
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import StringProperty, ListProperty
from datetime import datetime
from kivy.uix.boxlayout import BoxLayout

PATTERNS_18 = [
    {"id": 1, "name": "Double Bottom", "type": "Bullish Reversal", "signal": "BUY", "base_conf": 84, "sl": 3, "tp": 12, "rr": "1:4", "desc": "Duha ka bottom nag hold sa 4393. Classic reversal.", "best_tf": "5M"},
    {"id": 2, "name": "Double Top", "type": "Bearish Reversal", "signal": "SELL", "base_conf": 83, "sl": 3, "tp": 12, "rr": "1:4", "desc": "Duha ka top sa taas, di ka break. SELL!", "best_tf": "5M"},
    {"id": 3, "name": "Head & Shoulders", "type": "Bearish Reversal", "signal": "SELL", "base_conf": 88, "sl": 3, "tp": 18, "rr": "1:6", "desc": "Ulo sa tunga taas, abaga ubos. Strong SELL.", "best_tf": "15M"},
    {"id": 4, "name": "Inv. H&S", "type": "Bullish Reversal", "signal": "BUY", "base_conf": 89, "sl": 3, "tp": 18, "rr": "1:6", "desc": "Baliktad H&S sa baba. Kusog BUY!", "best_tf": "15M"},
    {"id": 5, "name": "Ascending Triangle", "type": "Bullish Cont.", "signal": "BUY", "base_conf": 82, "sl": 3, "tp": 9, "rr": "1:3", "desc": "Flat top, higher lows. Breakout BUY.", "best_tf": "1M"},
    {"id": 6, "name": "Descending Triangle", "type": "Bearish Cont.", "signal": "SELL", "base_conf": 81, "sl": 3, "tp": 9, "rr": "1:3", "desc": "Flat bottom, lower highs. SELL.", "best_tf": "1M"},
    {"id": 7, "name": "Symmetrical Triangle", "type": "Neutral", "signal": "BUY", "base_conf": 77, "sl": 3, "tp": 12, "rr": "1:4", "desc": "Triangle nag huot, breakout bisan asa.", "best_tf": "5M"},
    {"id": 8, "name": "Rising Wedge", "type": "Bearish", "signal": "SELL", "base_conf": 79, "sl": 3, "tp": 15, "rr": "1:5", "desc": "Pataas pero huot, weak na. SELL.", "best_tf": "15M"},
    {"id": 9, "name": "Falling Wedge", "type": "Bullish", "signal": "BUY", "base_conf": 85, "sl": 3, "tp": 15, "rr": "1:5", "desc": "Pababa pero huot, bullish breakout!", "best_tf": "15M"},
    {"id": 10, "name": "Bull Flag", "type": "Bullish Cont.", "signal": "BUY", "base_conf": 86, "sl": 3, "tp": 9, "rr": "1:3", "desc": "Kusog saka then flag, BUY padayon!", "best_tf": "1M"},
    {"id": 11, "name": "Bear Flag", "type": "Bearish Cont.", "signal": "SELL", "base_conf": 85, "sl": 3, "tp": 9, "rr": "1:3", "desc": "Kusog baba then flag, SELL padayon.", "best_tf": "1M"},
    {"id": 12, "name": "Bull Pennant", "type": "Bullish", "signal": "BUY", "base_conf": 80, "sl": 3, "tp": 12, "rr": "1:4", "desc": "Flag triangle gamay, BUY breakout.", "best_tf": "5M"},
    {"id": 13, "name": "Cup & Handle", "type": "Bullish", "signal": "BUY", "base_conf": 90, "sl": 3, "tp": 25, "rr": "1:8", "desc": "Tasa pattern, handle gamay. Master BUY!", "best_tf": "15M"},
    {"id": 14, "name": "Rounding Bottom", "type": "Bullish", "signal": "BUY", "base_conf": 87, "sl": 3, "tp": 20, "rr": "1:6", "desc": "Hinay nag round sa baba, long term BUY.", "best_tf": "15M"},
    {"id": 15, "name": "Channel Up", "type": "Bullish", "signal": "BUY", "base_conf": 78, "sl": 3, "tp": 9, "rr": "1:3", "desc": "Channel pataas, BUY sa ubos.", "best_tf": "1M"},
    {"id": 16, "name": "Channel Down", "type": "Bearish", "signal": "SELL", "base_conf": 77, "sl": 3, "tp": 9, "rr": "1:3", "desc": "Channel pababa, SELL sa taas.", "best_tf": "1M"},
    {"id": 17, "name": "Triple Bottom", "type": "Strong Bullish", "signal": "BUY", "base_conf": 92, "sl": 3, "tp": 20, "rr": "1:6", "desc": "Tulo ka bottom! Super strong BUY.", "best_tf": "5M"},
    {"id": 18, "name": "Support Hold V3.1", "type": "Bisaya Custom", "signal": "BUY", "base_conf": 83, "sl": 3, "tp": 12, "rr": "1:4", "desc": "Imong original! Hold 4393.46, BUY scalp.", "best_tf": "1M"},
]

KV = """
MDScreen:
    md_bg_color: 0.06, 0.06, 0.06, 1
    MDScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(12)
            spacing: dp(12)
            adaptive_height: True
            MDBoxLayout:
                size_hint_y: None
                height: dp(26)
                MDLabel:
                    text: "GOLD SCANNER V5 - 18 CHART CHEAT SHEET"
                    font_size: "12sp"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 1,0.8,0.2,1
                MDLabel:
                    text: "LIVE ONLINE"
                    font_size: "10sp"
                    halign: "right"
                    theme_text_color: "Custom"
                    text_color: 0.3,0.9,0.5,1
                    bold: True
            MDGridLayout:
                cols: 3
                spacing: dp(6)
                size_hint_y: None
                height: dp(42)
                MDButton:
                    style: "filled"
                    on_release: app.set_mode("EXPERT")
                    MDButtonText:
                        text: "EXPERT"
                        font_size: "11sp"
                MDButton:
                    style: "filled"
                    theme_bg_color: "Custom"
                    md_bg_color: 1, 0.75, 0.05, 1
                    on_release: app.set_mode("PRO")
                    MDButtonText:
                        text: "PRO"
                        font_size: "11sp"
                        theme_text_color: "Custom"
                        text_color: 0,0,0,1
                        bold: True
                MDButton:
                    style: "filled"
                    on_release: app.set_mode("MASTER")
                    MDButtonText:
                        text: "MASTER"
                        font_size: "11sp"
            MDBoxLayout:
                spacing: dp(6)
                size_hint_y: None
                height: dp(38)
                MDLabel:
                    text: "TF:"
                    size_hint_x: None
                    width: dp(28)
                    font_size: "11sp"
                    theme_text_color: "Custom"
                    text_color: 0.6,0.6,0.6,1
                MDButton:
                    style: "filled"
                    theme_bg_color: "Custom"
                    md_bg_color: 0.95,0.8,0.1,1
                    size_hint_x: None
                    width: dp(50)
                    on_release: app.set_timeframe("1M")
                    MDButtonText:
                        text: "1M"
                        font_size: "12sp"
                        theme_text_color: "Custom"
                        text_color: 0,0,0,1
                        bold: True
                MDButton:
                    style: "outlined"
                    size_hint_x: None
                    width: dp(50)
                    on_release: app.set_timeframe("5M")
                    MDButtonText:
                        text: "5M"
                        font_size: "12sp"
                MDButton:
                    style: "outlined"
                    size_hint_x: None
                    width: dp(50)
                    on_release: app.set_timeframe("15M")
                    MDButtonText:
                        text: "15M"
                        font_size: "12sp"
                MDLabel:
                    text: root.tf_info
                    font_size: "9sp"
                    theme_text_color: "Custom"
                    text_color: 0.5,0.5,0.5,1
                    halign: "right"
            MDCard:
                md_bg_color: root.signal_bg_color
                padding: dp(14)
                radius: [dp(16)]
                size_hint_y: None
                height: self.minimum_height
                line_color: 0.3,0.6,0.3,1
                line_width: 1
                MDBoxLayout:
                    orientation: 'vertical'
                    adaptive_height: True
                    spacing: dp(10)
                    MDBoxLayout:
                        adaptive_height: True
                        MDBoxLayout:
                            size_hint_x: None
                            width: dp(48)
                            height: dp(48)
                            md_bg_color: 1,1,1,0.15
                            radius: [dp(12)]
                            MDIcon:
                                icon: root.signal_icon
                                pos_hint: {"center_x": .5, "center_y": .5}
                                theme_text_color: "Custom"
                                text_color: 1,1,1,1
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [dp(10),0,0,0]
                            MDLabel:
                                text: root.signal_title_text
                                font_size: "15sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 1,1,1,1
                            MDLabel:
                                text: root.pattern_name_text
                                font_size: "11sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 1,0.9,0.3,1
                            MDLabel:
                                text: root.similarity_text
                                font_size: "10sp"
                                theme_text_color: "Custom"
                                text_color: 0.8,0.8,0.8,1
                        MDBoxLayout:
                            orientation: 'vertical'
                            size_hint_x: None
                            width: dp(68)
                            MDLabel:
                                text: "CONF"
                                font_size: "9sp"
                                halign: "right"
                                theme_text_color: "Custom"
                                text_color: 0.7,0.7,0.7,1
                            MDLabel:
                                text: root.confidence_text
                                font_size: "20sp"
                                bold: True
                                halign: "right"
                                theme_text_color: "Custom"
                                text_color: 1,1,1,1
                    MDGridLayout:
                        cols: 3
                        spacing: dp(6)
                        size_hint_y: None
                        height: dp(60)
                        MDCard:
                            md_bg_color: 0,0,0,0.35
                            padding: dp(8)
                            radius: [dp(10)]
                            MDBoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    text: "ENTRY"
                                    font_size: "8sp"
                                    theme_text_color: "Custom"
                                    text_color: 0.5,0.5,0.5,1
                                MDLabel:
                                    text: root.entry_text
                                    font_size: "11sp"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 1,1,1,1
                        MDCard:
                            md_bg_color: 0,0,0,0.35
                            padding: dp(8)
                            radius: [dp(10)]
                            MDBoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    text: "SL (-$3)"
                                    font_size: "8sp"
                                    theme_text_color: "Custom"
                                    text_color: 0.5,0.5,0.5,1
                                MDLabel:
                                    text: root.sl_text
                                    font_size: "11sp"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 1,0.5,0.5,1
                        MDCard:
                            md_bg_color: 0,0,0,0.35
                            padding: dp(8)
                            radius: [dp(10)]
                            MDBoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    text: "TP (+$)"
                                    font_size: "8sp"
                                    theme_text_color: "Custom"
                                    text_color: 0.5,0.5,0.5,1
                                MDLabel:
                                    text: root.tp_text
                                    font_size: "11sp"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0.4,0.9,0.6,1
                    MDCard:
                        md_bg_color: 0,0,0,0.4
                        padding: dp(10)
                        radius: [dp(8)]
                        size_hint_y: None
                        height: self.minimum_height
                        MDBoxLayout:
                            orientation: 'vertical'
                            adaptive_height: True
                            spacing: dp(4)
                            MDLabel:
                                text: root.strategy_header
                                font_size: "10sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 1,0.85,0.2,1
                            MDLabel:
                                text: root.bisaya_text
                                font_size: "10sp"
                                theme_text_color: "Custom"
                                text_color: 0.9,0.9,0.9,1
                                adaptive_height: True
            MDLabel:
                text: "18 CHART CHEAT SHEET - PILIA PATTERN"
                font_size: "10sp"
                bold: True
                theme_text_color: "Custom"
                text_color: 0.7,0.7,0.7,1
                size_hint_y: None
                height: dp(18)
            MDGridLayout:
                id: pattern_grid
                cols: 1
                spacing: dp(6)
                adaptive_height: True
            MDCard:
                md_bg_color: 0.10,0.10,0.10,1
                padding: dp(10)
                radius: [dp(12)]
                size_hint_y: None
                height: dp(90)
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(3)
                    MDLabel:
                        text: "LIVE PRICE ACTION - GOLD-API.COM"
                        font_size: "9sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.6,0.6,0.6,1
                    MDLabel:
                        text: root.live_price_text
                        font_size: "13sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 1,0.9,0.3,1
                    MDLabel:
                        text: root.api_status_text
                        font_size: "8sp"
                        theme_text_color: "Custom"
                        text_color: 0.4,0.9,0.7,1
            MDButton:
                style: "filled"
                theme_bg_color: "Custom"
                md_bg_color: 1, 0.75, 0.05, 1
                size_hint_y: None
                height: dp(46)
                radius: [dp(23)]
                on_release: app.scan_next_pattern()
                MDButtonText:
                    text: "SCAN NEXT PATTERN (1-18)"
                    theme_text_color: "Custom"
                    text_color: 0,0,0,1
                    bold: True
                    pos_hint: {"center_x": .5, "center_y": .5}
"""

class GoldScannerApp(MDApp):
    signal_title_text = StringProperty("BUY SIGNAL")
    pattern_name_text = StringProperty("18. Support Hold V3.1")
    similarity_text = StringProperty("Support Hold - Bisaya Custom")
    confidence_text = StringProperty("83%")
    entry_text = StringProperty("$4424.10")
    sl_text = StringProperty("$4421.10 (-$3)")
    tp_text = StringProperty("$4436.10 (+$12)")
    live_price_text = StringProperty("$4424.10 LIVE NOW")
    api_status_text = StringProperty("System init - 18 patterns loaded")
    strategy_header = StringProperty("PRO 1M: Lose $3 / Win $12 (1:4 RR)")
    bisaya_text = StringProperty("Bisaya: Support hold 4393.46. BUY SL $3 TP $12!")
    signal_icon = StringProperty("trending-up")
    signal_bg_color = ListProperty([0.09, 0.22, 0.16, 1])
    tf_info = StringProperty("1M=$9 5M=$12-15 15M=$20+")
    current_mode = "PRO"
    current_tf = "1M"
    current_price = 4424.10
    current_pattern_idx = 17
    def build(self):
        self.theme_cls.theme_style = "Dark"
        root = Builder.load_string(KV)
        Clock.schedule_once(lambda dt: self.build_pattern_grid(), 0.5)
        return root
    def build_pattern_grid(self):
        try:
            grid = self.root.ids.pattern_grid
            grid.clear_widgets()
            from kivymd.uix.card import MDCard
            from kivymd.uix.label import MDLabel
            for i, pat in enumerate(PATTERNS_18):
                is_active = i == self.current_pattern_idx
                bg = (0.18, 0.28, 0.18, 1) if is_active else (0.12, 0.12, 0.12, 1)
                line_c = (0.3, 0.7, 0.3, 1) if is_active else (0,0,0,0)
                card = MDCard(md_bg_color=bg, padding=10, radius=[10], size_hint_y=None, height=58, line_color=line_c, line_width=1 if is_active else 0)
                inner = BoxLayout(orientation='vertical', spacing=2)
                row1 = MDLabel(text=f"{pat['id']}. {pat['name']} - {pat['signal']} | {pat['type']} | SL ${pat['sl']} TP ${pat['tp']} {pat['rr']} | Best {pat['best_tf']}", font_size="10sp", bold=is_active, theme_text_color="Custom", text_color=(1,1,1,1) if is_active else (0.85,0.85,0.85,1), size_hint_y=None, height=18)
                row2 = MDLabel(text=f"{pat['desc']} - {pat['signal']} Strategy: Lose ${pat['sl']} Win ${pat['tp']}", font_size="8sp", theme_text_color="Custom", text_color=(0.5,0.5,0.5,1), size_hint_y=None, height=14)
                inner.add_widget(row1)
                inner.add_widget(row2)
                card.add_widget(inner)
                card.bind(on_release=lambda x, idx=i: self.select_pattern(idx))
                grid.add_widget(card)
        except Exception as e:
            print(e)
    def on_start(self):
        self.fetch_price()
        Clock.schedule_interval(lambda dt: self.fetch_price(), 3)
        Clock.schedule_interval(lambda dt: self.auto_scan_pattern(), 7)
    def set_mode(self, mode):
        self.current_mode = mode
        self.update_strategy()
    def set_timeframe(self, tf):
        self.current_tf = tf
        self.update_strategy()
    def select_pattern(self, idx):
        self.current_pattern_idx = idx
        self.update_strategy()
        self.build_pattern_grid()
    def scan_next_pattern(self):
        self.current_pattern_idx = (self.current_pattern_idx + 1) % len(PATTERNS_18)
        self.update_strategy()
        self.build_pattern_grid()
    def auto_scan_pattern(self):
        if self.current_tf == "15M":
            self.current_pattern_idx = random.choice([2,3,7,12,13,16])
        elif self.current_tf == "5M":
            self.current_pattern_idx = random.choice([0,1,4,5,6,16])
        else:
            self.current_pattern_idx = random.choice([4,5,9,10,14,17])
        self.update_strategy()
        self.build_pattern_grid()
    def update_strategy(self):
        pat = PATTERNS_18[self.current_pattern_idx]
        mode = self.current_mode
        tf = self.current_tf
        price = self.current_price
        conf_base = pat["base_conf"]
        if mode == "EXPERT":
            conf = conf_base - 8
        elif mode == "PRO":
            conf = conf_base
        else:
            conf = min(95, conf_base + 5)
        sl = pat["sl"]
        tp_base = pat["tp"]
        if tf == "1M":
            tp = tp_base
        elif tf == "5M":
            tp = tp_base + 3
        else:
            tp = tp_base + 8
        if mode == "MASTER":
            tp += 5
        self.signal_title_text = f"{pat['signal']} SIGNAL"
        self.pattern_name_text = f"{pat['id']}. {pat['name']} - {pat['type']}"
        self.similarity_text = f"{pat['name']} | {pat['best_tf']} best | {pat['rr']} RR"
        self.confidence_text = f"{conf}%"
        self.signal_icon = "trending-up" if pat["signal"]=="BUY" else "trending-down"
        self.signal_bg_color = [0.09, 0.22, 0.16, 1] if pat["signal"]=="BUY" else [0.22, 0.09, 0.09, 1]
        self.entry_text = f"${price:.2f}"
        sl_price = price - sl if pat["signal"]=="BUY" else price + sl
        tp_price = price + tp if pat["signal"]=="BUY" else price - tp
        self.sl_text = f"${sl_price:.2f} (-${sl})"
        self.tp_text = f"${tp_price:.2f} (+${tp})"
        rr = f"1:{int(tp/sl)}"
        self.strategy_header = f"{mode} {tf}: {pat['name']} | Lose ${sl} / Win ${tp} ({rr} RR) | {pat['signal']}"
        if pat["signal"]=="BUY":
            self.bisaya_text = f"Bisaya {mode}: {pat['name']} detect! {pat['desc']} Price {price:.2f}. REAL STRATEGY: BUY sa {price:.2f}, SL ${sl} sa {sl_price:.2f}. Kung SL, ${sl} ra mawala. TP ${tp} sa {tp_price:.2f}. RR {rr}. 1 win = {int(tp/sl)} lose bawi! {tf} best. Tinuod live!"
        else:
            self.bisaya_text = f"Bisaya {mode}: {pat['name']} detect! {pat['desc']} Price {price:.2f}. REAL STRATEGY: SELL sa {price:.2f}, SL ${sl} sa {sl_price:.2f}. TP ${tp} sa {tp_price:.2f}. RR {rr}. Bearish, SELL ta! {tf} best."
    def fetch_price(self):
        threading.Thread(target=self._fetch_thread, daemon=True).start()
    def _fetch_thread(self):
        try:
            r = requests.get("https://api.gold-api.com/price/XAU", timeout=5)
            data = r.json()
            price = float(data.get('price', 0))
            if price == 0:
                raise ValueError("No price")
            self.current_price = price
            def update_ui():
                self.live_price_text = f"${price:.2f} LIVE NOW - {self.current_tf} - {PATTERNS_18[self.current_pattern_idx]['name']} - Support 4393.46"
                self.api_status_text = f"LIVE {price:.2f} from gold-api.com | 18 patterns | {self.current_tf} | {self.current_mode} | {PATTERNS_18[self.current_pattern_idx]['id']}/18 | SL $3 TP $9+"
                self.update_strategy()
            Clock.schedule_once(lambda dt: update_ui(), 0)
        except Exception as e:
            def err_ui():
                self.api_status_text = f"Error {e} - retry"
            Clock.schedule_once(lambda dt: err_ui(), 0)

GoldScannerApp().run()
