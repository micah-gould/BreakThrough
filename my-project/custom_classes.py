from manim import *

class SpaceTimeGrid:
    def __init__(self, scene, speed=0, max_number=24, count=2):
        # Create the coordinate system
        self.scene = scene
        self.speed = ValueTracker(speed)

        self.max_number = max_number
        self.count = count
        self.scale_factor = 0.3

        self.grid = Axes(
            x_range=[-self.max_number, self.max_number, self.count],
            y_range=[-self.max_number, self.max_number, self.count],
            x_length=24,  # Enlarged so it looks good after scaling
            y_length=24,
            axis_config={"include_numbers": True, "stroke_width": 4 / 3},
        ).scale(self.scale_factor).move_to(ORIGIN)

        # Label the axes
        self.x_label = Text("Space (x)", font_size=36).scale(self.scale_factor)  # Larger to compensate for scaling
        self.ct_label = Text("Time (ct)", font_size=36).scale(self.scale_factor)

        # Position the labels
        self.x_label.next_to(self.grid @ (self.max_number, self.max_number / 12), UP).shift(DOWN * (self.scale_factor + 0.1))
        self.ct_label.next_to(self.grid @ (self.max_number / 12, self.max_number), RIGHT).shift(LEFT * (self.scale_factor + 0.1))
        
        def make_number_line(flip=1):

            angle = np.arctan(self.speed.get_value()) if flip == -1 else PI/2 - np.arctan(self.speed.get_value())
            speed = self.speed.get_value()

            if speed == 0: return VMobject()

            if abs(speed) <= 0.99:
                nl = NumberLine(
                    x_range=[-self.max_number * (1 - speed**2)**(1/2), self.max_number * (1 - speed**2)**(1/2), self.count],
                    length=np.linalg.norm(self.grid @ (-self.max_number, -speed * self.max_number) - self.grid @ (self.max_number, speed * self.max_number)) / self.scale_factor,
                    include_numbers=True,
                    include_tip=True,
                    exclude_origin_tick=True,
                    numbers_to_exclude=list(range(-(self.count), self.count + 1)),
                    color=YELLOW,
                    stroke_width = 4 / 3
                )

                tangent = nl @ (1) - nl @ (0)
                tangent /= np.linalg.norm(tangent)
                normal = rotate_vector(tangent, PI / 2) * flip
                for mob in nl.numbers:
                    num = mob.number
                    base_point = nl @ (num)
                    mob.move_to((base_point + self.scale_factor * normal) if num > 0 else (base_point - self.scale_factor * normal))
                    mob.rotate(-angle, about_point=mob.get_center())
            else:
                nl = NumberLine(
                    x_range=[-1, 1, 1],
                    length=np.linalg.norm(self.grid @ (-self.max_number, -self.max_number) - self.grid @ (self.max_number, self.max_number)) / self.scale_factor,
                    include_numbers=False,
                    include_tip=True,
                    exclude_origin_tick=True,
                    color=YELLOW,
                    stroke_width = 4 / 3
                )
            nl.rotate(angle, about_point=ORIGIN).scale(self.scale_factor).shift(self.grid @ (0, 0) - nl @ (0))
            return nl

        self.x__line = always_redraw(lambda: make_number_line(1))
        
        self.x__label = always_redraw(lambda: Text("Space (x')" if self.speed.get_value() != 0 else "", font_size=36).move_to(self.grid @ (self.max_number, (self.speed.get_value() + 1/24) * self.max_number)).scale(self.scale_factor))

        self.ct__line = always_redraw(lambda: make_number_line(-1))
        
        self.ct__label = always_redraw(lambda: Text("Time (ct')" if self.speed.get_value() != 0 else "", font_size=36).move_to(self.grid @ ((self.speed.get_value() + 1/8) * self.max_number, self.max_number * 47/48)).scale(self.scale_factor))

        self.moveing_object = VGroup(self.x__line, self.ct__line, self.x__label, self.ct__label)
        self.observer = VGroup(self.grid, self.x_label, self.ct_label)
        self.everything = VGroup(*self.observer, *self.moveing_object)
    
    def show(self, observer=True, moving_object=True):
        self.scene.add(self.observer if observer else VGroup(), self.moveing_object if moving_object else VGroup())

    def create(self, observer=True, moving_object=True, **kwargs):
        self.scene.play(Create(self.observer if observer else VGroup()), Create(self.moveing_object if moving_object else VGroup()), **kwargs)

    def remove(self):
        self.scene.clear()
    
    def prime_to_cords(self, x, ct):
        # Convert the coordinates to the new system
        new_x = (x / (1 - self.speed.get_value()**2)**(1/2))
        new_ct = (ct / (1 - self.speed.get_value()**2)**(1/2))
        return tuple(map(lambda x, y: x + y, (new_x, self.speed.get_value() * new_x), (self.speed.get_value() * new_ct, new_ct)))
        # Return the new coordinates
    
    def change_speed(self, new_speed, **kwargs):
        self.scene.play(self.speed.animate(**kwargs).set_value(new_speed))

    def set_speed(self, new_speed):
        self.speed.set_value(new_speed)
        self.scene.play(self.speed.animate(run_time=1/60).set_value(new_speed))

class Location:
    def __init__(self, diagram, x, ct):
        self.x = ValueTracker(x)
        self.ct = ValueTracker(ct)
        self.diagram = diagram
        self.everything = VGroup()
    
    _x = lambda self, x, ct: ((x - self.diagram.speed.get_value() * ct) / (1 - self.diagram.speed.get_value()**2)**0.5)
    _ct = lambda self, x, ct: ((ct - self.diagram.speed.get_value() * x) / (1 - self.diagram.speed.get_value()**2)**0.5)

    def plot_lines(self, **kwargs):
        # Create the lines
        x_line = always_redraw(
            lambda: Line(self.diagram.grid @ (self.x.get_value(), 0), self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), stroke_width=1)
        )
        ct_line = always_redraw(
            lambda: Line(self.diagram.grid @ (0, self.ct.get_value()), self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), stroke_width=1)
        )
        self.everything.add(x_line, ct_line)
        self.diagram.scene.play(Create(x_line), Create(ct_line), **kwargs)
        self.diagram.scene.wait(0.1)

    def plot_point(self, **kwargs):
        # Create the point
        point = always_redraw(
            lambda: Dot(self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), color=RED, radius=0.04)
        )
        self.everything.add(point)
        self.diagram.scene.play(Create(point), **kwargs)
        self.diagram.scene.wait(0.1)

    def plot__lines(self, **kwargs):
        # Create the lines 
        x__line = always_redraw(
            lambda: Line(self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), self.diagram.grid @ self.diagram.prime_to_cords(self._x(self.x.get_value(), self.ct.get_value()), 0), color=YELLOW, stroke_width=0.5)
        )
        ct__line = always_redraw(
            lambda: Line(self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), self.diagram.grid @ self.diagram.prime_to_cords(0, self._ct(self.x.get_value(), self.ct.get_value())), color=YELLOW, stroke_width=0.5)
        )
        self.everything.add(x__line, ct__line)
        self.diagram.scene.play(Create(x__line), Create(ct__line), **kwargs)
        self.diagram.scene.wait(0.1)

    get_prime_coords = lambda self: (self._x(self.x.get_value(), self.ct.get_value()), self._ct(self.x.get_value(), self.ct.get_value()))
    
    def create(self, **kwargs):
        self.plot_lines(**kwargs)
        self.plot_point(**kwargs)
        self.plot__lines(**kwargs)

    def remove(self):
        self.diagram.scene.remove(*self.everything)
        
    
    def move_to(self, x, ct, **kwargs):
        self.diagram.scene.play(self.x.animate(**kwargs).set_value(x), self.ct.animate(**kwargs).set_value(ct))

class PrimeLocation:
    def __init__(self, diagram, x, ct):
        self._x = ValueTracker(x)
        self._ct = ValueTracker(ct)   
        self.diagram = diagram
        self.x = ValueTracker()
        self.ct = ValueTracker()

        def update_outputs(_):
            _x = self._x.get_value()
            _ct = self._ct.get_value()
            (x, ct) = self.diagram.prime_to_cords(_x, _ct)
            self.x.set_value(x)
            self.ct.set_value(ct)

        dummy = Mobject()
        dummy.add_updater(update_outputs)
        self.diagram.scene.add(dummy)
        
        self.everything = VGroup()

    def plot__lines(self, **kwargs):
        # Create the lines
        x__line = always_redraw(
            lambda: Line(self.diagram.grid @ self.diagram.prime_to_cords(self._x.get_value(), 0), self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), color=YELLOW, stroke_width=0.5)
        )
        ct__line = always_redraw(
            lambda: Line(self.diagram.grid @ self.diagram.prime_to_cords(0, self._ct.get_value()), self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), color=YELLOW, stroke_width=0.5)
        )
        self.everything.add(x__line, ct__line)
        self.diagram.scene.play(Create(x__line), Create(ct__line), **kwargs)
        self.diagram.scene.wait(0.1)

    def plot_point(self, **kwargs):
        # Create the point
        point = always_redraw(
            lambda: Dot(self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), color=RED, radius=0.04)
        )
        self.everything.add(point)
        self.diagram.scene.play(Create(point), **kwargs)
        self.diagram.scene.wait(0.1)

    def plot_lines(self, **kwargs):
        # Create the lines
        x_line = always_redraw(
            lambda: Line(self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), self.diagram.grid @ (self.x.get_value(), 0), stroke_width=1)
        )
        ct_line = always_redraw(
            lambda: Line(self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), self.diagram.grid @ (0, self.ct.get_value()), stroke_width=1)
        )
        self.everything.add(x_line, ct_line)
        self.diagram.scene.play(Create(x_line), Create(ct_line), **kwargs)
        self.diagram.scene.wait(0.1)

    get_coords = lambda self: (self.x.get_value(), self.ct.get_value())
    
    def create(self, **kwargs):
        self.plot__lines(**kwargs)
        self.plot_point(**kwargs)
        self.plot_lines(**kwargs)

    def remove(self):  
        self.diagram.scene.remove(*self.everything)

    def move_to(self, x, ct, **kwargs):
        self.diagram.scene.play(self._x.animate(**kwargs).set_value(x), self._ct.animate(**kwargs).set_value(ct))

class WorldLine:
    def __init__(self, diagarm, speed=1, color=YELLOW):
        self.diagram = diagarm
        self.speed = speed
        self.color = color
        self.angle = np.arctan(speed)

    def draw(self):
        self.line_head = Dot(self.diagram.grid @ (0, 0), color=self.color).scale(0.5)
        self.line = always_redraw(lambda: Line(self.line_head.get_center(), self.diagram.grid @ (0, 0), color=self.color, stroke_width=2)).scale(0.5)
        
        self.diagram.scene.play(Create(self.line_head), Create(self.line))
        self.wait()
        self.diagram.scene.play(self.line_head.animate.move_to(self.diagram.grid @ ((self.diagram.max_number - self.diagram.count) * self.angle, self.diagram.max_number - self.diagram.count)))

    def draw_angle(self):
        self.angle = Angle(self.diagram.grid.get_y_axis(), self.line, quadrant=(1, -1), radius=np.linalg.norm(self.diagram.grid @ (0, 3 * self.diagram.count) - self.diagram.grid @ (0, 0)), other_angle=True)
        self.diagram.scene.play(Create(self.angle))

class LightClock:
    def __init__(self, scene):
        self.scene = scene
        self.case = NumberLine(x_range=[-1, 1, 1], exclude_origin_tick=True, length=1).rotate(90*DEGREES, about_point=ORIGIN)
        self.ball = Dot(radius=np.linalg.norm(self.case @ (0) - self.case @ (0.1)), color=TEAL_A)
        self.ball.start_direction = 1 # 1 is up
        self.objects = VGroup(self.case, self.ball)

    def create(self):
        self.scene.play(Create(self.case))
        self.scene.play(GrowFromCenter(self.ball))

    def start(self):
        self.ball.start_time = self.scene.time
        self.ball.start_pos = self.case.p2n(self.ball.get_center())
        self.ball.add_updater(self.linear_bounce_updater)

    def linear_bounce_updater(self, mob, dt):
            t = self.scene.time - mob.start_time
            period = 2     # total time for left -> right -> left
            offset = mob.start_pos + 1 if mob.start_direction == 1 else 3 - mob.start_pos
            frac = ((t + period * offset / 4) % period) / period
            if frac < 0.5:
                x = -0.9 + 3.6 * frac
                mob.end_direction = 1
            else:
                x = 0.9 - 3.6 * (frac - 0.5)
                mob.end_direction = -1
            mob.move_to(self.case @ x)

    def stop(self):
        self.ball.remove_updater(self.linear_bounce_updater)
        self.ball.start_direction = self.ball.end_direction
