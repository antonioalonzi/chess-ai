import os

from sound import Sound
from theme import Theme


class Config:
    def __init__(self):
        self.themes = []
        self.add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.move_sound = Sound(os.path.join('../assets/sounds/move.wav'))
        self.capture_sound = Sound(os.path.join('../assets/sounds/capture.wav'))

    def change_theme(self):
        self.idx = (self.idx + 1) % len(self.themes)
        self.theme = self.themes[self.idx]

    def add_themes(self):
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), (200, 100, 100), (200, 70, 70))
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), (200, 100, 100), (200, 70, 70))
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), (200, 100, 100), (200, 70, 70))
        self.themes = [green, brown, blue]
