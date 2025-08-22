from manim import *
from custom_classes import *
class Scene1(Scene):
    def construct(self):
        diagram2 = SpaceTimeGrid(self, 1)
        diagram2.show()
        self.wait()
        diagram2.change_speed(0.5, run_time=4)
        self.wait()

class Testing(Scene):
    def construct(self):
        return