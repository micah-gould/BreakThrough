from manim import *
from custom_classes import *
class Scene1(Scene):
    def construct(self):
        diagram = SpaceTimeGrid(scene=self, speed=0.8, max_number=9, count=1)
        diagram.show()
        location = Location(diagram=diagram, x=3, ct=3)
        location.create()
        location2 = PrimeLocation(diagram=diagram, x=2, ct=2)
        location2.create()
        print(diagram.x__line.x_range, location.diagram.x__line.x_range)
        print(diagram.speed.get_value(), location.diagram.speed.get_value())
        diagram.change_speed(new_speed=0.2, run_time=1)
        print(diagram.x__line.x_range, location.diagram.x__line.x_range)
        print(diagram.speed.get_value(), location.diagram.speed.get_value())
        self.wait()
        return

class Testing(Scene):
    def construct(self):
        return