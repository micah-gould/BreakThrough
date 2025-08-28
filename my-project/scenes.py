from manim import *
from custom_classes import *

# TODO: Add subtitles later

class ExplainTheDiagram(Scene): # Done
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
    
class GalilainEquations(Scene): # Done
    def construct(self):
        x = MathTex('{{x\'}} = {{x}} - {{v}}{{t}}')
        t = MathTex('{{t\'}} = {{t}}')
        v = MathTex('{{u\'}} = {{u}} - {{v}}')
        equations = VGroup(x, t, v).arrange(DOWN, aligned_edge=LEFT).scale(1.2)

        prime_color = PURPLE
        var_color = BLUE
        v_color = RED

        for eq in equations:
            for sym in ["x", "t", "u"]:
                eq.set_color_by_tex(sym, var_color)

            eq.set_color_by_tex("'", prime_color)

            eq.set_color_by_tex("v", v_color)

        legend_left = VGroup(
            MathTex("x, t, u").set_color(var_color),
            MathTex("v").set_color(v_color),
            MathTex("x', t', u'").set_color(prime_color),
        )

        legend_right = VGroup(
            Tex("variables in the observer frame (position, time, velocity)"),
            Tex("relative velocity between frames"),
            Tex("variables in the moving frame (position, time, velocity)"),
        )

        legend = VGroup(
            VGroup(legend_left[0], legend_right[0]).arrange(RIGHT, buff=0.3, aligned_edge=DOWN),
            VGroup(legend_left[1], legend_right[1]).arrange(RIGHT, buff=0.3, aligned_edge=DOWN),
            VGroup(legend_left[2], legend_right[2]).arrange(RIGHT, buff=0.3, aligned_edge=DOWN),
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.8)

        legend.to_edge(UP)
        equations.next_to(legend, DOWN, buff=1)

        self.play(FadeIn(legend, shift=DOWN))
        self.play(Write(x), Write(t), Write(v))
        self.wait()
        return

class LightClockExplenation(Scene):
    def construct(self):
        clock1 = LightClock(self)

        clock1.start()

        # TODO: Finish

        return

class ExplainRelitivisticDiagrams(Scene):
    def construct(self):
        diagram = SpaceTimeGrid(self, speed=0)

        diagram.create(run_time=2)
        self.wait()

        line = WorldLine(diagram, speed=0.2)
        
        line.draw()
        self.wait()

        line.draw_angle()
        self.wait()

        return