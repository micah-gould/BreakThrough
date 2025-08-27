from manim import *
from custom_classes import *

# TODO: Add subtitles later

class ExplainTheDiagram(Scene):
    def construct(self):
        first_train_x = NumberLine(x_range=[-1, 1, 1], length=4, color=BLUE, exclude_origin_tick=True, tip_shape=StealthTip, include_tip=True).shift(UP)

        self.play(GrowFromPoint(first_train_x, first_train_x.get_center()))
        self.wait()

        me = Dot(first_train_x @ (0), color=YELLOW, z_index=1000)

        self.play(Create(me))
        self.wait()

        self.play(me.animate.move_to(first_train_x @ (1)), rate_func=wiggle, run_time=2)
        self.wait()
        
        first_train_t = NumberLine(x_range=[0, 2, 2], length=4, color=MAROON_A, include_tip=True, exclude_origin_tick=True, z_index=-1).rotate(90*DEGREES, about_point=ORIGIN).shift(first_train_x @ (-1) - ORIGIN)

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
                1.9*np.sin(2*PI*t/3.5),  # x wiggle
                t,                # y upward
                0
            ]),
            t_range=[0, 3.5],  # duration of motion
        ).shift(first_train_x @ (0))

        # Animate the dot along the path
        self.play(MoveAlongPath(me, path), run_time=2, rate_func=linear)
        self.wait()

        self.play(FadeOut(me))
        return
    
class TwoTrains(Scene):
    def construct(self):
        first_train_x = NumberLine(x_range=[-1, 1, 1], length=4, color=BLUE, exclude_origin_tick=True, z_index=100, tip_shape=StealthTip, include_tip=True).shift(UP)
        first_train_t = NumberLine(x_range=[0, 2, 2], length=4, color=MAROON_A, include_tip=True, exclude_origin_tick=True, z_index=-1).rotate(90*DEGREES, about_point=ORIGIN).shift(first_train_x @ (-1) - ORIGIN)
        first_train_x.shift(first_train_t @ (0) - first_train_x @ (-1))

        self.add(first_train_x, first_train_t)
        
        line_head = Dot(first_train_x @ (-1), color=MAROON_B, z_index=1000)
        line = always_redraw(lambda: Line(line_head.get_center(), first_train_x @ (-1), color=MAROON_B, z_index=-2, stroke_width=2))
        self.play(Create(line_head), Create(line))
        self.wait()

        self.play(line_head.animate.shift((first_train_x @ (2/np.sqrt(3) - 1) - first_train_x @ (-1)) + (first_train_t @ (2) - first_train_t @ (0))), run_time=2)
        self.wait()

        second_train_t = NumberLine(x_range=[0, 2, 2], length=8/np.sqrt(3), color=MAROON_B, include_tip=True, exclude_origin_tick=True, z_index=-2).rotate(60*DEGREES, about_point=ORIGIN)
        second_train_t.shift(first_train_x @ (-1) - second_train_t @ (0))

        self.play(FadeIn(second_train_t), FadeOut(line), FadeOut(line_head))
        self.wait()

        second_train_x = NumberLine(x_range=[-1, 1, 1], length=4, color=YELLOW, exclude_origin_tick=True, z_index=101, tip_shape=StealthTip, include_tip=True)
        second_train_x.shift(first_train_x @ (-1) - second_train_x @ (-1)).set_opacity(0.5 )

        self.play(Create(second_train_x))
        self.wait()

        def showTrainMovmement():
            temp = first_train_x.copy()
            self.play(temp.animate().shift(first_train_t @ (2) - first_train_x @ (-1)))
            self.wait()

            temp2 = second_train_x.copy().set_opacity(1)
            self.play(temp2.animate().shift(second_train_t @ (2) - second_train_x @ (-1)))
            self.wait()
        
            self.play(FadeOut(temp), FadeOut(temp2))
            self.wait()

        showTrainMovmement()

        temp = first_train_t.copy().set_length(8/np.sqrt(3))
        temp2 = second_train_t.copy().set_length(4)
        self.play(first_train_t.animate.set_length(8/np.sqrt(3)).shift(first_train_x @ (-1) - temp @ (0)).rotate(30*DEGREES, about_point=first_train_x @ (-1)), second_train_t.animate.set_length(4).shift(second_train_x @ (-1) - temp2 @ (0)).rotate(30*DEGREES, about_point=second_train_x @ (-1)))
        self.wait()

        showTrainMovmement()

        # TODO: add more?

        return 

class Testing(Scene):
    def construct(self):
        return