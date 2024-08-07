import cv2
import numpy as np
from typing import Callable

from kivy.uix.image import Image
from kivy.uix.camera import Camera
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

from kivy.clock import Clock
from kivy.utils import platform

from kivy.graphics.texture import Texture
from kivy.properties import (
    NumericProperty, ObjectProperty, 
    ListProperty
)

from kivy.lang import Builder

def standard_filter(frame: np.ndarray) -> np.ndarray:
    # Translate the texture
    frame_np = cv2.flip(frame, -1)
    frame_np = cv2.cvtColor(frame_np, cv2.COLOR_RGB2RGBA)
    return frame_np

class Filterable(Widget):
    filters: list[Callable[[np.ndarray], np.ndarray]] = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _apply_filter(self, frame: np.ndarray):
        new_frame = frame
        for myfilter in self.filters:
            new_frame = myfilter(new_frame)
        return new_frame

    def add_filter(self, filter: Callable[[np.ndarray], np.ndarray]):
        self.filters.append(filter)

class KivyCvCamera(Camera, Filterable):
    FPS = NumericProperty(1/60)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.play = True
        self._frame: np.ndarray = None
        Clock.schedule_once(self._update_frame, self.FPS)

    def _update_frame(self, dt=-1):
        if self.texture:
            frame_data = self.texture.pixels
            width = self.texture.width
            height = self.texture.height
            frame_np = np.frombuffer(frame_data, dtype=np.uint8).reshape((height, width, 4))
            if platform == "android":
                frame_np = np.flipud(frame_np)
            self._frame = self._apply_filter(frame_np)
        Clock.schedule_once(self._update_frame, self.FPS)

    def on_texture(self, instance, value):
        value = value.flip_horizontal()
        return super().on_texture(instance, value)

    def get_frame(self) -> np.ndarray:
        return self._frame

class ImageReceiver(Image, Filterable):
    FPS = NumericProperty(1/60)

    def __init__(
            self, 
            filters: list[Callable[[np.ndarray], np.ndarray]]=[], 
            **kwargs
    ):
        super().__init__(**kwargs)
        self._frame = None
        self.filters = filters
        Clock.schedule_once(self._update_frame, self.FPS)

    def _create_texture(self, frame: np.ndarray):
        buf = frame.tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgba')
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

    def _update_frame(self, dt=-1):
        if self._frame is not None:
            new_frame = self._apply_filter(self._frame)
            self.texture = self._create_texture(new_frame)
        Clock.schedule_once(self._update_frame, self.FPS)

    def set_frame(self, frame: np.ndarray):
        self._frame = frame

Builder.load_string('''
<KivyCvCameraSet>:
    orientation: 'vertical'
    image: image
    camera: camera
    img_filters: []
    cam_filters: []

    KivyCvCamera:
        id: camera
        size_hint: None, None
        size: 0, 0
        play: True
        filters: root.cam_filters

    ImageReceiver:
        id: image
        filters: root.img_filters
''')

class KivyCvCameraSet(BoxLayout):
    image: ImageReceiver = ObjectProperty()
    camera: KivyCvCamera = ObjectProperty()
    cam_filters: list[Callable[[np.ndarray], np.ndarray]] = ListProperty()
    img_filters: list[Callable[[np.ndarray], np.ndarray]] = ListProperty()

    def __init__(
            self, 
            img_filters: list[Callable[[np.ndarray], np.ndarray]]=[], 
            cam_filters: list[Callable[[np.ndarray], np.ndarray]]=[], 
            **kwargs
        ):
        super().__init__(**kwargs)
        self.img_filters = img_filters
        self.cam_filters = cam_filters
        Clock.schedule_interval(
            lambda dt: 
            self.ids.image.set_frame(
                self.ids.camera.get_frame()
        ), 1/60)
        Clock.schedule_once(self._apply_filter, 1)

    def _apply_filter(self, dt=-1):
        self.image.filters = self.img_filters
        self.camera.filters = self.cam_filters

    def add_filter(self, comp: Filterable, filter: Callable[[np.ndarray], np.ndarray]):
        comp.add_filter(filter)

if __name__ == "__main__":
    from kivy.app import App

    class TestCamera(App):
        def build(self):
            return KivyCvCameraSet(cam_filters=[standard_filter])

    TestCamera().run()