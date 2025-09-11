from manim import *
from custom_classes import *
from MF_Tools import TransformByGlyphMap

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
    
class TwoTrains(Scene): # Done
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

        return 
    
class GalilainEquations(Scene): # Done
    def construct(self):
        x = MathTex('{{x\'}} = {{x}} - {{v}}{{t}}')
        t = MathTex('{{t\'}} = {{t}}')
        u = MathTex('{{u\'}} = {{u}} - {{v}}')
        equations = VGroup(x, t, u).arrange(DOWN, aligned_edge=LEFT).scale(1.2)

        prime_color = RED
        var_color = BLUE
        v_color = PURPLE

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
        self.play(Write(x), Write(t), Write(u))
        self.wait()
        return

class LightClockExplenation(Scene): # Done
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
        self.wait()
        clock1.start()
        self.wait(2)
        clock1.stop()

        clock2 = LightClock(self)
        clock2.objects.shift(UP)

        self.play(FadeOut(clock1.objects), FadeIn(clock2.objects))
        self.remove(*clock1.objects)
        self.wait()
        clock2.start()
        self.play(background.animate(run_time=4, rate_func=linear).shift(LEFT*10))
        clock2.stop()

        ct__brace = BraceBetweenPoints(clock2.case @ -0.9, clock2.case @ 0.9)
        ct__label = ct__brace.get_tex(r"c {{\Delta t_0}}")
        ct__label.set_color_by_tex(r"\Delta t_0", RED)

        self.add(ct__brace, ct__label)

        self.wait()

        self.remove(ct__brace, ct__label, *clock2.objects)

        clock3 = LightClock(self)
        clock3.objects.shift(UP + 5*LEFT)
        self.play(FadeIn(clock1.objects), FadeIn(clock3.objects))

        clock3.start()
        self.play(clock3.case.animate(run_time=1.5, rate_func=linear).shift(15/4*RIGHT))
        clock3.stop()

        path = TracedPath(clock3.ball.get_center, stroke_color=YELLOW, stroke_width=2)
        self.add(path)

        clock3.start()
        self.play(clock3.case.animate(run_time=1, rate_func=linear).shift(5/2*RIGHT))
        clock3.stop()

        path.clear_updaters()

        ct_brace = BraceBetweenPoints(path.get_end(), path.get_start())
        ct_label = ct_brace.get_tex(r"c {{\Delta t}}")
        ct_label.set_color_by_tex(r"\Delta t", BLUE)

        self.add(ct_brace, ct_label)

        self.wait()

        self.remove(path, ct_brace, ct_label, *clock3.objects)

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
        self.wait()

        return

class LorentzDerivation(Scene): # Done
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

        clock = LightClock(self)
        clock.objects.shift(UP+1.5625*RIGHT)
        clock.ball.move_to(clock.case @ 0.9)
        path = Line(clock.case @ -0.9 + 3.125 * LEFT, clock.case @ 0.9, stroke_color=YELLOW, stroke_width=2)
        path2 = Line(clock.case @ -0.9 + 3.125 * LEFT, clock.case @ -0.9, stroke_color=YELLOW, stroke_width=2)
        
        ct__brace = BraceBetweenPoints(clock.case @ -0.9, clock.case @ 0.9)
        ct__label = ct__brace.get_tex(r"c \Delta t_0")
        for i in [1,2,3]: ct__label[0][i].set_color(RED)
        
        ct_brace = BraceBetweenPoints(path.get_end(), path.get_start())
        ct_label = ct_brace.get_tex(r"c \Delta t")
        for i in [1,2]: ct_label[0][i].set_color(BLUE)

        vt_brace = BraceBetweenPoints(path2.get_start(), path2.get_end())
        vt_label = vt_brace.get_tex(r"v \Delta t",)
        for i in [1,2]: vt_label[0][i].set_color(BLUE)

        things_to_shift = VGroup(ct_brace, ct_label, vt_brace, vt_label, ct__brace, ct__label, *clock.objects, path, path2)
        self.add(things_to_shift)

        equation1 = MathTex(r"\left(c \Delta t\right)^2 = \left(v \Delta t\right)^2 + \left(c \Delta t_0\right)^2")
        equation2 = MathTex(r"c^2 \Delta t^2 = v^2 \Delta t^2 + c^2 \Delta t_0^2")
        equation3 = MathTex(r"c^2 \Delta t^2 - v^2 \Delta t^2 = c^2 \Delta t_0^2")
        equation4 = MathTex(r"\left(c^2 - v^2\right) \Delta t^2 = c^2 \Delta t_0^2")
        equation5 = MathTex(r"\frac{\left(c^2 - v^2\right)}{c^2} \Delta t^2 = \Delta t_0^2")
        equation6 = MathTex(r"\left(1 - \frac{v^2}{c^2}\right) \Delta t^2 = \Delta t_0^2")
        equation7 = MathTex(r"\sqrt{\left(1 - \frac{v^2}{c^2}\right) \Delta t^2} = \sqrt{\Delta t_0^2}")
        equation8 = MathTex(r"\sqrt{\left(1 - \frac{v^2}{c^2}\right)} \Delta t = \Delta t_0")
        equation9 = MathTex(r"\Delta t = \frac{1}{\sqrt{\left(1 - \frac{v^2}{c^2}\right)}}\Delta t_0")
        equation10 = MathTex(r"\Delta t = \gamma\Delta t_0")
        equations = Group(equation1, equation2, equation3, equation4, equation5, equation6, equation7, equation8, equation9, equation10)
        equations.shift(0.5*DOWN)
        for i in [2,3,9,10]: equation1[0][i].set_color(BLUE)
        for i in [2,3,8,9]: 
            equation2[0][i].set_color(BLUE)
            equation3[0][i].set_color(BLUE)
        for i in [7,8]: equation4[0][i].set_color(BLUE)
        for i in [10,11]: equation5[0][i].set_color(BLUE)
        for i in [9,10]: equation6[0][i].set_color(BLUE)
        for i in [11,12]: 
            equation7[0][i].set_color(BLUE)
            equation8[0][i].set_color(BLUE)
        for i in [0,1]: 
            equation9[0][i].set_color(BLUE)
            equation10[0][i].set_color(BLUE)

        for i in [-3,-4,-5]: equation1[0][i].set_color(RED)
        for i in [-1,-3,-4]: 
            equation2[0][i].set_color(RED)
            equation3[0][i].set_color(RED)
            equation4[0][i].set_color(RED)
            equation5[0][i].set_color(RED)
            equation6[0][i].set_color(RED)
            equation7[0][i].set_color(RED)
        for i in[-1,-2,-3]:
            equation8[0][i].set_color(RED)
            equation9[0][i].set_color(RED)
            equation10[0][i].set_color(RED)

        self.play(things_to_shift.animate.shift(UP))
        # Animate copies of each symbol into the equation
        self.play(
            TransformFromCopy(ct_label[0][:2], equation1[0][1:3]),
            TransformFromCopy(ct_label[0][2], equation1[0][3]),
            TransformFromCopy(vt_label[0][:2], equation1[0][8:10]),
            TransformFromCopy(vt_label[0][2], equation1[0][10]),
            TransformFromCopy(ct__label[0][:2], equation1[0][15:17]),
            TransformFromCopy(ct__label[0][2:], equation1[0][17:19]),
        )
        self.play(Write(equation1[0][0]), Write(equation1[0][4:6]), Write(equation1[0][7]), Write(equation1[0][11:13]), Write(equation1[0][14]), Write(equation1[0][19:21]))  # the "2"s
        self.play(Write(equation1[0][6]), Write(equation1[0][13]))  # "+" and "="
        self.play(
            TransformByGlyphMap(
                equation1, equation2,
                ([0,4,7,11,14,19],[]),
                ([5], [1,4]),
                ([12],[7,10]),
                ([20],[13,16]),
            )
        )
        self.play(
            TransformByGlyphMap(
                equation2, equation3,
                ([5,11],[11,5]),
            )
        )
        self.play(
            TransformByGlyphMap(
                equation3, equation4,
                ([],[0,6]),
                ([2,3,4],[7,8,9]),
                ([8,9,10],[7,8,9]),
            )          
        )
        self.play(
            TransformByGlyphMap(
                equation4, equation5,
                ([],[7]),
                ([11,12],[8,9])
            )
        )
        self.play(
            TransformByGlyphMap(
                equation5, equation6,
                ([3,6,8,9],[2,8,6,7]),
                ([1,2,8,9],[1])
            )
        )
        self.play(
            TransformByGlyphMap(
                equation6, equation7,
                ([],[0,1,15,16]),
            )
        )
        self.play(
            TransformByGlyphMap(
                equation7, equation8,
                ([13,15,16,19],[])
            )
        )
        self.play(
            TransformByGlyphMap(
                equation8, equation9,
                ([11,12,13],[0,1,2]),
                ([],[3,4])
            )
        )

        self.wait()

        lorentz_equation = MathTex(r"\gamma=\frac{1}{\sqrt{\left(1 - \frac{v^2}{c^2}\right)}}").shift(2.5*DOWN)
        
        self.play(
            Write(lorentz_equation[0][:2]),
            TransformFromCopy(equation9[0][3], lorentz_equation[0][2:]),
            TransformByGlyphMap(
                equation9, equation10,
                ([3,4,5,6,7,8,9,10,11,12,13,14,15],[3])
            )
        )

        self.wait()
        return

class LorentzFactorPlot(Scene): # Done
    def construct(self):
        #Axes
        axes = Axes(
            x_range=[0, 1.1, 0.1], # normalized v/c (cannot reach 1)
            y_range=[0, 29, 1],
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": np.arange(0, 1.1, 0.2), "decimal_number_config": {"num_decimal_places": 1}},
            y_axis_config={"numbers_to_include": np.arange(0, 29, 5)}
        )

        labels = axes.get_axis_labels(x_label="v/c", y_label="\\gamma")

        # Lorentz factor function
        lorentz_factor = lambda x: 1 / np.sqrt(1 - x**2)

        graph = axes.plot(lorentz_factor, x_range=[0, 0.999, 0.001], color=YELLOW)

        # Title
        title = Text("Lorentz Factor vs Speed", font_size=36).to_edge(UP)

        # Display everything
        self.play(Create(axes), Write(labels))
        self.play(Write(title))
        self.play(Create(graph))

        # Highlight divergence near v/c -> 1
        dot = Dot(color=RED).move_to(axes.c2p(0.999, lorentz_factor(0.999)))
        note = Text("Diverges as v → c", font_size=28, color=RED).next_to(dot, UP+LEFT)
        self.play(FadeIn(dot), Write(note))

        self.wait()

class LorentzEquations(Scene): # Done
    def construct(self):
        x = MathTex(r"x' = \gamma\left(x - vt\right)")
        t = MathTex(r"t' = \gamma\left(t - \frac{vx}{c^2}\right)")
        u = MathTex(r"u' = \frac{dx'}{dt'}")
        equations = VGroup(x, t, u).arrange(DOWN, aligned_edge=LEFT).scale(1.2)

        prime_color = RED
        var_color = BLUE
        v_color = PURPLE

        for i in [0,1]: 
            x[0][i].set_color(prime_color)
            t[0][i].set_color(prime_color)
        for i in [5,8]: 
            x[0][i].set_color(var_color)
            t[0][i].set_color(var_color)
        for i in [7]: 
            x[0][i].set_color(v_color)
            t[0][i].set_color(v_color)
        
        for i in [0,1,3,4,5,7,8,9]: u[0][i].set_color(prime_color)

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
        self.play(Write(x), Write(t), Write(u))
        self.wait()

        u1 = MathTex(r"u' = \frac{\gamma\left(dx - vdt\right)}{\gamma\left(dt - \frac{vdx}{c^2}\right)}")
        u2 = MathTex(r"u' = \frac{dx - vdt}{dt - \frac{v}{c^2}dx}")
        u3 = MathTex(r"u' = \frac{\frac{dx}{dt} - \frac{vdt}{dt}}{\frac{dt}{dt} - \frac{v}{c^2}\frac{dx}{dt}}")
        u4 = MathTex(r"u' = \frac{u - v}{1 - \frac{v}{c^2}u}")
        u5 = MathTex(r"u' = \frac{u - v}{1 - \frac{uv}{c^2}}")

        for i in [0,1]:
            u1[0][i].set_color(prime_color)
            u2[0][i].set_color(prime_color)
            u3[0][i].set_color(prime_color)
            u4[0][i].set_color(prime_color)
            u5[0][i].set_color(prime_color)
        
        for i in [5,6,9,10,15,16,19,20]:
            u1[0][i].set_color(var_color)
        for i in [8,18]:
            u1[0][i].set_color(v_color)

        for i in [3,4,7,8,10,11,17,18]:
            u2[0][i].set_color(var_color)
        for i in [6,13]:
            u2[0][i].set_color(v_color)

        for i in [3,4,5,6,7,10,11,12,13,14,16,17,18,19,20,26,27,28,29,30]:
            u3[0][i].set_color(var_color)
        for i in [9,22]:
            u3[0][i].set_color(v_color)

        for i in [3,13]:
            u4[0][i].set_color(var_color)
        for i in [5,9]:
            u4[0][i].set_color(v_color)

        for i in [3,9]:
            u5[0][i].set_color(var_color)
        for i in [5,10]:
            u5[0][i].set_color(v_color)

        Group(u1, u2, u3, u4, u5).scale(1.2).shift(u.get_center_of_mass() - u1.get_center_of_mass())

        self.play(
            ReplacementTransform(u[0][:3], u1[0][:3]),
            TransformFromCopy(x[0][3:5], u1[0][3:5]),
            TransformFromCopy(u[0][3], u1[0][5]),
            TransformFromCopy(x[0][5:8], u1[0][6:9]),
            ReplacementTransform(u[0][3], u1[0][9]),
            TransformFromCopy(x[0][8:], u1[0][10:12]),
            ReplacementTransform(u[0][6], u1[0][12]),
            TransformFromCopy(t[0][3:5], u1[0][13:15]),
            TransformFromCopy(u[0][7], u1[0][15]),
            TransformFromCopy(t[0][5:8], u1[0][16:19]),
            ReplacementTransform(u[0][7], u1[0][19]),
            TransformFromCopy(t[0][8:], u1[0][20:]),
            FadeOut(u[0][4:6], u[0][8:10])
        )

        self.play(
            TransformByGlyphMap(
                u1, u2,
                ([3,4,11,13,14,24],[]),
                ([19,20],[17,18])
            )
        )

        self.play(
            TransformByGlyphMap(
                u2, u3,
                ([],[5,6,7,12,13,14,18,19,20,28,29,30]),
            )
        )

        self.play(
            TransformByGlyphMap(
                u3, u4,
                ([3,4,5,6,7],[3]),
                ([10,11,12,13,14],[]),
                ([16,17,18,19,20],[7]),
                ([26,27,28,29,30],[13]),
            )
        )

        self.play(
            TransformByGlyphMap(
                u4, u5,
                ([13],[9])
            )
        )

        self.wait()
        return
class ExplainRelitivisticDiagrams(Scene): # Done
    def construct(self):
        speed=0.3
        diagram = SpaceTimeGrid(self, speed=0)

        diagram.create(run_time=2, moving_object=False)
        self.wait()

        line = WorldLine(diagram, speed=speed)
        
        line.draw()
        self.wait()

        line.draw_angle()
        self.wait()

        label1 = MathTex(r"\theta = arctan\left(\frac{x}{ct}\right)")
        label2 = MathTex(r"\theta = arctan\left(\frac{vt}{ct}\right)")
        label3 = MathTex(r"\theta = arctan\left(\frac{v}{c}\right)")
        labels = Group(label1, label2, label3)
        labels.next_to(line.angle).shift(UP)

        self.play(Write(label1))
        self.play(
            TransformByGlyphMap(
                label1, label2,
                ([9],[9,10])
            )
        )
        self.play(
            TransformByGlyphMap(
                label2, label3,
                ([10,13],[])
            )
        )
        self.wait()

        t = MathTex(r"t' = \gamma\left(t - \frac{vx}{c^2}\right)")
        t1 = MathTex(r"0 = \gamma\left(t - \frac{vx}{c^2}\right)")
        t2 = MathTex(r"0 = t - \frac{vx}{c^2}")
        t3 = MathTex(r"t = \frac{vx}{c^2}")
        t4 = MathTex(r"\frac{ct}{x} = \frac{v}{c}")
        Group(t, t1, t2, t3, t4).shift(DR+RIGHT)

        self.play(Write(t))
        self.play(
            TransformByGlyphMap(
                t, t1,
                ([0,1],[0])
            )
        )
        self.play(
            TransformByGlyphMap(
                t1, t2,
                ([2,3,11],[])
            )
        )
        self.play(
            TransformByGlyphMap(
                t2, t3,
                ([0, 3],[]),
                ([2],[0])
            )
        )
        self.play(
            TransformByGlyphMap(
                t3, t4,
                ([6],[]),
                ([5],[0,7]),
                ([4],[2,6]),
                ([0,1,2,3],[1,4,5,3])
            )
        )
        self.wait()

        line2 = Line(diagram.grid @ (diagram.max_number - diagram.count, (diagram.max_number - diagram.count) * np.arctan(speed)), diagram.grid @ (0, 0), stroke_width=2, color=YELLOW)
        angle2 = Angle(diagram.grid.get_x_axis(), line2, quadrant=(1, -1), radius=np.linalg.norm(diagram.grid @ (0, 3 * diagram.count) - diagram.grid @ (0, 0)))
        self.play(Create(line2), Create(angle2))
        self.wait()

        self.play(FadeOut(*VGroup(line.line_head, line.angle, angle2, t4, label3)))

        diagram2 = SpaceTimeGrid(self, speed=speed)
        diagram2.show()

        self.play(FadeOut(*VGroup(line.line, line2)))
        self.wait()
        return
    
class RelitivisticDiagrams(Scene): # Done
    def construct(self):
        diagram = SpaceTimeGrid(self, speed=0.3)
        diagram.show()

        def resolve(a, *args):
            if isinstance(a, ValueTracker):
                return a.get_value()
            elif callable(a):
                return a(*args)
            else:
                return a   # plain value
        
        get_row = lambda dot, name: [
                MathTex(name), 
                Text(f"({resolve(dot.x):.2f},").set_color(dot.point.color).scale(0.7),
                Text(f"{resolve(dot.ct):.2f})").set_color(dot.point.color).scale(0.7),
                Text(f"({resolve(dot._x, resolve(dot.x), resolve(dot.ct)):.2f},").set_color(dot.point.color).scale(0.7),
                Text(f"{resolve(dot._ct, resolve(dot.x), resolve(dot.ct)):.2f})").set_color(dot.point.color).scale(0.7),
            ]
        
        A = Location(diagram, x=10, ct=10, name="A")
        B = PrimeLocation(diagram, x=10, ct=10, name="B")

        # Dynamic table generator
        def make_table():
            headers = [MathTex(""), MathTex("(x,"), MathTex("ct)"), MathTex("(x',"), MathTex("ct')")]
            A_row = get_row(A, A.name)
            B_row = get_row(B, B.name)
            table = VGroup(*headers, *A_row, *B_row)
            table.arrange_in_grid(rows=3, cols=5, buff=0.4, cell_alignment=RIGHT)
            table.scale(0.5)
            table.to_corner(UR)
            return table

        # Single always_redraw for the entire table
        dynamic_table = always_redraw(make_table)

        A.create(run_time=1/3)
        B.create(run_time=1/3)

        speed_text = always_redraw(lambda: Text(f"v = {diagram.speed.get_value():.2f}c").next_to(dynamic_table, DOWN).scale(0.7))

        self.add(dynamic_table, speed_text)

        self.wait()

        A.move_to(13, 17)
        B.move_to(8, 5)
        diagram.change_speed(0.6)

        self.wait()
        return
