from manim import *
from custom_classes import *
class Scene1(Scene):
    def construct(self):
        diagram2 = SpaceTimeGrid(self, 1)
        diagram2.show()
        self.wait()
        diagram2.change_speed(0)
        self.wait()

class Testing(Scene):
    def construct(self):
        grid = Axes(
            x_range=[-24, 24, 2],
            y_range=[-24, 24, 2],
            x_length=24,  # Enlarged so it looks good after scaling
            y_length=24,
            axis_config={"include_numbers": True, "stroke_width": 32 / 24},
        ).scale(0.3).move_to(ORIGIN)

        a = ValueTracker(10)
        b = ValueTracker(0)

        def draw_number_line():
            nl = NumberLine(
                    x_range=[-a.get_value(), a.get_value(), 2],
                    length=10,
                    include_numbers=True,
                    include_tip=True,
                    exclude_origin_tick=True,
                    numbers_to_exclude=list(range(-3, 4)),
                    color=YELLOW,
                    stroke_width = 32 / 24
                ).rotate(b.get_value(), about_point=ORIGIN).scale(0.3).move_to(ORIGIN)

            tangent = nl.number_to_point(1) - nl.number_to_point(0)
            tangent /= np.linalg.norm(tangent)
            normal = rotate_vector(tangent, PI / 2)
            for mob in nl.numbers:
                num = mob.number
                base_point = nl.number_to_point(num)
                mob.move_to((base_point + 0.09 * normal) if num > 0 else (base_point - 0.09 * normal))
                mob.rotate(-b.get_value(), about_point=mob.get_center())

            return nl

        nl = always_redraw(draw_number_line) 

        self.add(grid)
        self.add(nl)

        self.wait()
        self.play(a.animate.set_value(20), b.animate.set_value(PI / 4), run_time=2)
        self.wait()