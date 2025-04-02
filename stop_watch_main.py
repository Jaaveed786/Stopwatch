from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import NumericProperty

Window.size = (400, 400)

KV = '''
BoxLayout:
    orientation: "vertical"
    spacing: 20
    padding: 20
    md_bg_color: [0, 0, 0, 1]  # Black background

    Label:
        id: lb
        text: "[size=40][color=#FFFFFF]00 : 00 : 00[/color][/size]"  # White text
        markup: True
        canvas.before:
            Color:
                rgba: 0, 0, 0, 1  # Black background
            Rectangle:
                pos: self.pos
                size: self.size

    MDRaisedButton:
        id: bt
        text: "START"
        on_press: app.toggle_clock()
        size_hint_y: None
        height: 50
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1  # White text
        md_bg_color: 0, 0.5, 0, 1  # Green button

    MDRaisedButton:
        id: bt_re
        text: "RESET"
        on_press: app.reset()
        size_hint_y: None
        height: 50
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1  # White text
        md_bg_color: 0.8, 0, 0, 1  # Red button
'''


class MainApp(MDApp):
    running = False
    seconds = NumericProperty(0.0)  # Observable property
    clock_event = None

    def build(self):
        return Builder.load_string(KV)

    def update_time(self, dt):
        self.seconds += dt
        # No need to update label here - will be handled by property binding

    def on_seconds(self, instance, value):
        """Automatically called when seconds value changes"""
        minutes, seconds = divmod(value, 60)
        hundredths = int((seconds - int(seconds)) * 100)
        self.root.ids.lb.text = f"[size=40][color=#FFFFFF]{int(minutes):02} : {int(seconds):02} : {hundredths:02}[/color][/size]"

    def toggle_clock(self):
        self.running = not self.running
        self.root.ids.bt.text = "STOP" if self.running else "START"
        self.root.ids.bt_re.disabled = self.running

        if self.running:
            self.clock_event = Clock.schedule_interval(self.update_time, 0.01)
        else:
            self.clock_event.cancel()

    def reset(self):
        self.seconds = 0.0
        if self.running:
            self.toggle_clock()

    def on_stop(self):
        if self.clock_event:
            self.clock_event.cancel()


if __name__ == '__main__':
    MainApp().run()