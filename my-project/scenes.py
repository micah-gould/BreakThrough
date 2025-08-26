from manim import *
from custom_classes import *

class TwoTrains(Scene):
    def construct(self):
        first_train_x = NumberLine(x_range=[-1, 1, 1], length=6, color=BLUE, exclude_origin_tick=True)

        self.play(GrowFromPoint(first_train_x, first_train_x.get_center()))
        self.wait()

        me = Dot(first_train_x @ (0), color=YELLOW, z_index=1000)

        self.play(Create(me))
        self.wait()

        self.play(me.animate.move_to(first_train_x @ (1)), rate_func=wiggle, run_time=2)
        self.wait()
        
        first_train_t = NumberLine(x_range=[0, 2, 2], length=6, color=YELLOW_A, include_tip=True, exclude_origin_tick=True, z_index=-1).rotate(90*DEGREES, about_point=ORIGIN).shift(first_train_x @ (-1) - ORIGIN)

        distance = first_train_t @ (0) - first_train_x @ (-1)
        # Animate outward from the middle
        self.play(
            GrowFromPoint(first_train_t, first_train_t.get_center()),
            first_train_x.animate.shift(distance),
            me.animate.shift(distance),
            lag_ratio=0,
        )
        self.wait()

        path = ParametricFunction(
            lambda t: np.array([
                2.75*np.sin(2*PI*t/5),  # x wiggle
                t,                # y upward
                0
            ]),
            t_range=[0, 5],  # duration of motion
        ).shift(first_train_x @ (0))

        # Animate the dot along the path
        self.play(MoveAlongPath(me, path), run_time=2, rate_func=linear)
        self.wait()

        self.play(FadeOut(me))
        self.wait()

        line_head = Dot(first_train_x @ (-1), color=YELLOW, z_index=1000)
        line = always_redraw(lambda: Line(line_head.get_center(), first_train_x @ (-1), color=YELLOW, z_index=999))
        self.play(Create(line_head), Create(line))
        self.wait()

        self.play(line_head.animate.shift((first_train_x @ (0) - first_train_x @ (-1)) + (first_train_t @ (1.8) - first_train_t @ (0))), run_time=2)
        self.wait()

        return


class Testing(Scene):
    def construct(self):
        return