from manim import *

#TODO: FIXME: have the grid hidden when speed is 0, and appear when speed is nonzero
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

        return
    
    def show(self, observer=True, moving_object=True):
        self.scene.add(self.observer if observer else VGroup(), self.moveing_object if moving_object else VGroup())
        return

    def create(self, observer=True, moving_object=True, **kwargs):
        self.scene.play(Create(self.oberser if observer else VGroup()), Create(self.moveing_object if moving_object else VGroup()), **kwargs)
        return

    def remove(self):
        self.scene.clear()
        return
    
    def prime_to_cords(self, x, ct):
        # Convert the coordinates to the new system
        new_x = (x / (1 - self.speed.get_value()**2)**(1/2))
        new_ct = (ct / (1 - self.speed.get_value()**2)**(1/2))
        a = tuple(map(lambda x, y: x + y, (new_x, self.speed.get_value() * new_x), (self.speed.get_value() * new_ct, new_ct)))
        return a
        # Return the new coordinates
    
    def change_speed(self, new_speed, **kwargs):
        self.scene.play(self.speed.animate(**kwargs).set_value(new_speed))
        return
    
    def set_speed(self, new_speed):
        self.speed.set_value(new_speed)
        self.scene.play(self.speed.animate(run_time=1/60).set_value(new_speed))
        return

class Location:
    def __init__(self, diagram, x, ct):
        self.x = ValueTracker(x)
        self.ct = ValueTracker(ct)
        self.diagram = diagram
        self.everything = VGroup()
        return
    
    def _x(self, x, ct): 
        a = (x - self.diagram.speed.get_value() * ct) / (1 - self.diagram.speed.get_value()**2)**(1/2)
        return a
    def _ct(self, x, ct): 
        a = (ct - self.diagram.speed.get_value() * x) / (1 - self.diagram.speed.get_value()**2)**(1/2)
        return a

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
        return

    def plot_point(self, **kwargs):
        # Create the point
        point = always_redraw(
            lambda: Dot(self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), color=RED, radius=0.04)
        )
        self.everything.add(point)
        self.diagram.scene.play(Create(point), **kwargs)
        self.diagram.scene.wait(0.1)
        return

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
        return

    def get_prime_coords(self):
        return (self._x(self.x.get_value(), self.ct.get_value()), self._ct(self.x.get_value(), self.ct.get_value()))
    
    def create(self, **kwargs):
        self.plot_lines(**kwargs)
        self.plot_point(**kwargs)
        self.plot__lines(**kwargs)
        return 

    def remove(self):
        self.diagram.scene.remove(*self.everything)
        return
    
    def move_to(self, x, ct, **kwargs):
        self.diagram.scene.play(self.x.animate(**kwargs).set_value(x), self.ct.animate(**kwargs).set_value(ct))
        return

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
        return

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
        return

    def plot_point(self, **kwargs):
        # Create the point
        point = always_redraw(
            lambda: Dot(self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), color=RED, radius=0.04)
        )
        self.everything.add(point)
        self.diagram.scene.play(Create(point), **kwargs)
        self.diagram.scene.wait(0.1)
        return

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
        return

    def get_coords(self):
        return (self.x.get_value(), self.ct.get_value())
    
    def create(self, **kwargs):
        self.plot__lines(**kwargs)
        self.plot_point(**kwargs)
        self.plot_lines(**kwargs)
        return

    def remove(self):  
        self.diagram.scene.remove(*self.everything)
        return
    
    def move_to(self, x, ct, **kwargs):
        self.diagram.scene.play(self._x.animate(**kwargs).set_value(x), self._ct.animate(**kwargs).set_value(ct))
        return