from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.config import Config

from Youtuber import YTD

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class Mainwindow(RelativeLayout):

    text = StringProperty("")
    button_state = BooleanProperty(True)
    res_state = BooleanProperty(True)
    again_btn_state = BooleanProperty(True)

    video = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def not_a_url(self):
        error_message = Label(
            text="The given url is not an youtube url"
        )
        close_button = Button(
            text="close",
            size_hint=(1, 0.3)
        )
        url_error_popup = BoxLayout(orientation="vertical")
        url_error_popup.add_widget(error_message)
        url_error_popup.add_widget(close_button)
        url_error = Popup(
            title="[!] Not a youtube url",
            content=url_error_popup,
            size_hint=(0.4, 0.4)
        )
        close_button.bind(on_press=url_error.dismiss)
        return url_error

    def somthing_error(self):
        error_message = Label(
            text="Somthing went wrong"
        )
        close_button = Button(
            text="close",
            size_hint=(1, 0.3)
        )
        error_message_layout = BoxLayout(orientation="vertical")
        error_message_layout.add_widget(error_message)
        error_message_layout.add_widget(close_button)
        error_message_popup = Popup(
            title="ERROR",
            content=error_message_layout,
            auto_dismiss=True,
            size_hint=(0.4, 0.4)
        )
        close_button.bind(on_press=error_message_popup.dismiss)
        return error_message_popup

    def process_url(self, url, *args):
        try:
            self.video = YTD(url)
        except:
            error = self.somthing_error()
            self.text = ""
            error.open()

    def add_audio_video_btn(self, audio_btn, video_btn, *args):

        if self.video not in [None, ""]:
            audio_btn.text = audio_btn.value
            video_btn.text = video_btn.value
            audio_btn.disabled = False
            video_btn.disabled = False
            self.text = ""

    def add_title_thumb(self, *args):
        self.ids.title.text = self.video.get_title()
        url = self.video.get_thumb()
        self.ids.thumb.color = 1, 1, 1, 1
        self.ids.thumb.source = url

    def on_press_enter(self, url, audio_btn, video_btn):
        url = url.text
        if "https://youtu.be/" in url:
            self.text = "Loading...."
            Clock.schedule_once(partial(self.process_url, url), 1)
            Clock.schedule_once(partial(self.add_audio_video_btn, audio_btn, video_btn), 5)
            Clock.schedule_once(self.add_title_thumb, 1)
        else:
            url_error = self.not_a_url()
            url_error.open()

    def on_press_button(self, url, audio_btn, video_btn):
        url = self.ids.url_input.text
        if "https://youtu.be/" in url:
            self.text = "Loading...."
            Clock.schedule_once(partial(self.process_url, url), 1)
            Clock.schedule_once(partial(self.add_audio_video_btn, audio_btn, video_btn), 5)
            Clock.schedule_once(self.add_title_thumb, 1)
        else:
            url_error = self.not_a_url()
            url_error.open()

    def add_again_btn(self, again_btn, *args):
        self.text = "Downloaded"
        again_btn.text = again_btn.value
        again_btn.disabled = False
        again_btn.background_color = 1, 1, 1, 1

    def download_audio(self, again_btn):
        video = self.video
        try:
            self.text = "Downloading..."
            Clock.schedule_once(video.audio_download, 1)
        except:
            error = self.somthing_error()
            error.open()
        Clock.schedule_once(partial(self.add_again_btn, again_btn), 5)

    def download_video_button(self, *args):
        resolution_dic = self.video.available_res_video()
        for btn in args:
            if btn.value in resolution_dic.keys():
                btn.text = btn.value
                btn.disabled = False


    def download_video(self, button, again_btn):
        resolution = button.text
        video = self.video
        try:
            self.text = "Downloading..."
            Clock.schedule_once(partial(video.video_download, resolution), 1)
        except:
            error = self.somthing_error()
            error.open()
        Clock.schedule_once(partial(self.add_again_btn, again_btn), 5)

    def reset(self, *args):
        self.text = ""
        self.ids.title.text = ""
        self.ids.thumb.color = 0, 0, 0, 1
        for btn in args:
            btn.text = ""
            btn.disabled = True


class YoutuberApp(App):
    pass

YoutuberApp().run()