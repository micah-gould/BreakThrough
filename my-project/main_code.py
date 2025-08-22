from manim import *
from custom_classes import *
class Scene1(Scene):
    def construct(self):
        diagram2 = SpaceTimeGrid(self, 0)
        diagram2.show()
        self.wait(0.1)
        diagram2.change_speed(1)
        self.wait()