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
        background = NumberPlane(
            x_range=[-100, 100, 1], 
            y_range=[-100, 100, 1], 
            background_line_style={
                "stroke_color": PURPLE_A,
                "stroke_width": 2,
            },
            faded_line_style={
                "stroke_color": PURPLE_A,
                "stroke_width": 1,
            },
            faded_line_ratio=3,
            axis_config={"color": PURPLE_A},
            stroke_width=2).set_opacity(0.5)
        self.add(background)

        ORIGIN = background @ (0, 0)
        UP = background @ (0, 1) - ORIGIN
        DOWN = background @ (0, -1) - ORIGIN
        LEFT = background @ (-1, 0) - ORIGIN
        RIGHT = background @ (1, 0) - ORIGIN

        clock1 = LightClock(self)
        clock1.objects.shift(DOWN)

        clock1.create()
        # self.wait()
        # clock1.start()
        # self.wait(2)
        # clock1.stop()

        # clock2 = LightClock(self)
        # clock2.objects.shift(UP)

        # self.play(FadeOut(clock1.objects), FadeIn(clock2.objects))
        # self.remove(*clock1.objects)
        # self.wait()
        # clock2.start()
        # self.play(background.animate(run_time=4, rate_func=linear).shift(LEFT*10))
        # clock2.stop()

        # ct__brace = BraceBetweenPoints(clock2.case @ -0.9, clock2.case @ 0.9)
        # ct__label = ct__brace.get_tex(r"{{c}} \Delta t_0")
        # ct__label.set_color_by_tex(r"\Delta t_0", RED)

        # self.add(ct__brace, ct__label)

        # self.wait()

        # self.remove(ct__brace, ct__label, *clock2.objects)

        # clock3 = LightClock(self)
        # clock3.objects.shift(UP + 5*LEFT)
        # self.play(FadeIn(clock1.objects), FadeIn(clock3.objects))

        # clock3.start()
        # self.play(clock3.case.animate(run_time=1.5, rate_func=linear).shift(15/4*RIGHT))
        # clock3.stop()

        # path = TracedPath(clock3.ball.get_center, stroke_color=YELLOW, stroke_width=2)
        # self.add(path)

        # clock3.start()
        # self.play(clock3.case.animate(run_time=1, rate_func=linear).shift(5/2*RIGHT))
        # clock3.stop()

        # path.clear_updaters()

        # ct_brace = BraceBetweenPoints(path.get_end(), path.get_start())
        # ct_label = ct_brace.get_tex(r"{{c}} \Delta t")
        # ct_label.set_color_by_tex(r"\Delta t", BLUE)

        # self.add(ct_brace, ct_label)

        # self.wait()

        # self.remove(path, ct_brace, ct_label, *clock3.objects)

        clock4 = LightClock(self)
        clock4.objects.shift(UP + 6.25*LEFT)
        self.play(FadeIn(clock4.objects))

        clock1.start()
        clock4.start(0.8)
        self.play(clock4.case.animate(run_time=1.875, rate_func=linear).shift(4.6875*RIGHT))
        clock4.stop()

        path2 = TracedPath(clock4.ball.get_center, stroke_color=YELLOW, stroke_width=2)
        path3 = TracedPath(lambda: clock4.case @ -0.9, stroke_color=YELLOW, stroke_width=2)
        self.add(path2, path3)

        clock4.start(0.8)
        self.play(clock4.case.animate(run_time=1.25, rate_func=linear).shift(3.125*RIGHT))
        clock4.stop()
        clock1.stop()

        path2.clear_updaters()
        path3.clear_updaters()

        ct__brace2 = BraceBetweenPoints(clock4.case @ -0.9, clock4.case @ 0.9)
        ct__label2 = ct__brace2.get_tex(r"c {{\Delta t_0}}")
        ct__label2.set_color_by_tex(r"\Delta t_0", RED)
        
        ct_brace2 = BraceBetweenPoints(path2.get_end(), path2.get_start())
        ct_label2 = ct_brace2.get_tex(r"c {{\Delta t}}")
        ct_label2.set_color_by_tex(r"\Delta t", BLUE)

        vt_brace = BraceBetweenPoints(path3.get_start(), path3.get_end())
        vt_label = vt_brace.get_tex(r"v {{\Delta t}}",)
        vt_label.set_color_by_tex(r"\Delta t", BLUE)

        self.add(ct_brace2, ct_label2, vt_brace, vt_label, ct__brace2, ct__label2)
        self.remove(*clock1.objects)

        equation1 = MathTex(r"({{c}} {{\Delta t}}){{^2}}", "=", r"({{v}} {{\Delta t}}){{^2}}", "+", r"({{c}} {{\Delta t_0}}){{^2}}")
        equation2 = MathTex(r"{{c}}^2 {{\Delta t}}^2", "=", r"{{v}}^2 {{\Delta t}}^2", "+", r"{{c}}^2 {{\Delta t_0}}^2")
        equation3 = MathTex(r"c^2 {{\Delta t}}^2", "-", r"v^2 {{\Delta t}}^2", "=", r"c^2 {{\Delta t_0}}^2")
        equation4 = MathTex(r"\left({{c^2}} - {{v^2}}\right) {{\Delta t}}^2", "=", r"c^2 {{\Delta t_0}}^2")
        equation5 = MathTex(r"\frac{\left(c^2 - v^2\right)}{c^2} {{\Delta t}}^2", "=", r"{{\Delta t_0}}^2")
        equation6 = MathTex(r"\left(1 - \frac{v^2}{c^2}\right) {{\Delta t}}^2", "=", r"{{\Delta t_0}}^2")
        equation7 = MathTex(r"\sqrt{\left(1 - \frac{v^2}{c^2}\right) {{\Delta t}}^2}", "=", r"\sqrt{{{\Delta t_0}}^2}")
        equation8 = MathTex(r"\sqrt{\left(1 - \frac{v^2}{c^2}\right)} {{\Delta t}}", "=", r"{{\Delta t_0}}")
        equations = Group(equation1, equation2, equation3, equation4, equation5, equation6, equation7, equation8)
        for eq in equations: eq.set_color_by_tex(r"\Delta t", BLUE)
        for eq in equations: eq.set_color_by_tex(r"\Delta t_0", RED)
        equations.scale(1.5).shift(DOWN)

        # Animate copies of each symbol into the equation
        self.play(
            TransformFromCopy(ct_label2, equation1[1:4]),  # "a" into "a" of "a^2"
            TransformFromCopy(vt_label, equation1[8:11]),  # "b" into "b" of "b^2"
            TransformFromCopy(ct__label2, equation1[15:18]),  # "c" into "c" of "c^2"
        )
        self.play(Write(equation1[0]), Write(equation1[4:6]), Write(equation1[7]), Write(equation1[11:13]), Write(equation1[14]), Write(equation1[18:20]))  # the "2"s
        self.play(Write(equation1[6]), Write(equation1[13]))  # "+" and "="
        # TODO: FIXME: manually correct animations
        self.play(
            FadeOut(equation1[0]),
            ReplacementTransform(equation1[1], equation2[0]),
            TransformFromCopy(equation1[5], equation2[1]),
            ReplacementTransform(equation1[2:4], equation2[2]),
            FadeOut(equation1[4]),
            ReplacementTransform(equation1[5:7], equation2[3:5]),
            FadeOut(equation1[7]),
            ReplacementTransform(equation1[8], equation2[5]),
            TransformFromCopy(equation1[12], equation2[6]),
            ReplacementTransform(equation1[9:11], equation2[7]),
            FadeOut(equation1[11]),
            ReplacementTransform(equation1[12:14], equation2[8:10]),
            FadeOut(equation1[14]),
            ReplacementTransform(equation1[15], equation2[10]),
            TransformFromCopy(equation1[19], equation2[11]),
            ReplacementTransform(equation1[16:18], equation2[12]),
            FadeOut(equation1[18]),
            ReplacementTransform(equation1[19], equation2[13]),
        )
        self.play(TransformMatchingTex(equation2, equation3))
        self.play(
            FadeIn(equation4[0]),
            ReplacementTransform(equation3[0], equation4[1]),
            FadeOut(equation3[1:3]),
            ReplacementTransform(equation3[3:5], equation4[2:4]),
            FadeIn(equation4[4]),
            ReplacementTransform(equation3[5:], equation4[5:]),
        )
        self.play(
            ReplacementTransform(equation4[0:5], equation5[0][0:7]),
            ReplacementTransform(equation4[8], equation5[0][8:10], arc_angle=-30*DEGREES),
            ReplacementTransform(equation4[5:8], equation5[1:4]),
            ReplacementTransform(equation4[9:], equation5[4:]),
        )
        self.play(TransformMatchingTex(equation5, equation6))
        self.play(TransformMatchingTex(equation6, equation7))
        self.play(TransformMatchingTex(equation7, equation8))

        self.wait()

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
