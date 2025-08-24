from manim import *
from custom_classes import *
class Scene1(Scene):
    def construct(self):
        diagram = SpaceTimeGrid(scene=self, speed=0, max_number=9, count=1)
        diagram.show()
        location = Location(diagram=diagram, x=0, ct=0)
        location.create()
        location.move_to(x=3, ct=5)
        diagram.change_speed(new_speed=0.6)
        self.wait()
        return

class Testing(Scene):
    def construct(self):
        return