from manim import *
from custom_classes import *

class ExplainTheDiagram(Scene): # DONE
    def construct(self):
        first_train_x = NumberLine(x_range=[-1, 1, 1], length=4, color=BLUE, exclude_origin_tick=True, tip_shape=StealthTip, include_tip=True).shift(UP)

        self.play(GrowFromPoint(first_train_x, first_train_x.get_center()))
        self.wait()

        me = Dot(first_train_x @ (0), color=YELLOW, z_index=1000)

        self.play(Create(me))
        self.wait()

        self.play(me.animate.move_to(first_train_x @ (1)), rate_func=wiggle, run_time=2)
        self.wait()
        
        first_train_t = NumberLine(x_range=[0, 2, 2], length=4, color=BLUE, include_tip=True, exclude_origin_tick=True, z_index=-1).rotate(90*DEGREES, about_point=ORIGIN).shift(first_train_x @ (-1) - ORIGIN)

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
        return
    
class TwoTrains(Scene):
    def construct(self):
        first_train_x = NumberLine(x_range=[-1, 1, 1], length=4, color=BLUE, exclude_origin_tick=True, z_index=100, tip_shape=StealthTip, include_tip=True).shift(UP)
        first_train_t = NumberLine(x_range=[0, 2, 2], length=4, color=BLUE, include_tip=True, exclude_origin_tick=True, z_index=-1).rotate(90*DEGREES, about_point=ORIGIN).shift(first_train_x @ (-1) - ORIGIN)
        first_train_x.shift(first_train_t @ (0) - first_train_x @ (-1))

        self.add(first_train_x, first_train_t)
        
        line_head = Dot(first_train_x @ (-1), color=YELLOW, z_index=1000)
        line = always_redraw(lambda: Line(line_head.get_center(), first_train_x @ (-1), color=YELLOW, z_index=-2, stroke_width=2))
        self.play(Create(line_head), Create(line))
        self.wait()

        self.play(line_head.animate.shift((first_train_x @ (0) - first_train_x @ (-1)) + (first_train_t @ (np.sqrt(3)) - first_train_t @ (0))), run_time=2)
        self.wait()

        second_train_t = NumberLine(x_range=[0, 2, 2], length=4, color=YELLOW, include_tip=True, exclude_origin_tick=True, z_index=-2).rotate(60*DEGREES, about_point=ORIGIN)
        second_train_t.shift(first_train_x @ (-1) - second_train_t @ (0))

        self.play(FadeIn(second_train_t), FadeOut(line), FadeOut(line_head))
        self.wait()

        second_train_x = NumberLine(x_range=[-1, 1, 1], length=4, color=YELLOW, exclude_origin_tick=True, z_index=-1, tip_shape=StealthTip, include_tip=True).rotate(-30*DEGREES, about_point=ORIGIN)
        second_train_x.shift(first_train_x @ (-1) - second_train_x @ (-1))

        self.play(Create(second_train_x))
        self.wait()

        return 

class Testing(Scene):
    def construct(self):
        return