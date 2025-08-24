from manim import *

def round_up_to_even(n):
    return int(np.ceil(n / 2.0)) * 2

def round_down_to_even(n):
    return int(np.floor(n / 2.0)) * 2

class SpaceTimeGrid:
    def __init__(self, scene, v):
        # Create the coordinate system
        self.scene = scene
        self.speed = ValueTracker(v)

        self.max_number = 24
        self.count = 2
        self.scale_factor = 0.3

        self.grid = Axes(
            x_range=[-self.max_number, self.max_number, self.count],
            y_range=[-self.max_number, self.max_number, self.count],
            x_length=self.max_number,  # Enlarged so it looks good after scaling
            y_length=self.max_number,
            axis_config={"include_numbers": True, "stroke_width": 32 / self.max_number},
        ).scale(self.scale_factor).move_to(ORIGIN)

        # Label the axes
        x_label = Text("Space (x)", font_size=36).scale(self.scale_factor)  # Larger to compensate for scaling
        ct_label = Text("Time (ct)", font_size=36).scale(self.scale_factor)

        # Position the labels
        x_label.next_to(self.grid @ (self.max_number, self.count), UP).shift(DOWN * (self.scale_factor + 0.1))
        ct_label.next_to(self.grid @ (self.count, self.max_number), RIGHT).shift(LEFT * (self.scale_factor + 0.1))
        
        def make_number_line(flip=1):

            angle = np.arctan(self.speed.get_value()) if flip == -1 else PI/2 - np.arctan(self.speed.get_value())
            speed = self.speed.get_value()

            if abs(speed) <= 0.99:
                nl = NumberLine(
                    x_range=[round_up_to_even(-self.max_number * (1 - speed**2)**(1/2)), round_down_to_even(self.max_number * (1 - speed**2)**(1/2)), 2],
                    length=np.linalg.norm(self.grid @ (-self.max_number, -speed * self.max_number) - self.grid @ (self.max_number, speed * self.max_number)) / self.scale_factor,
                    include_numbers=True,
                    include_tip=True,
                    exclude_origin_tick=True,
                    numbers_to_exclude=list(range(-3, 4)),
                    color=YELLOW,
                    stroke_width = 32 / self.max_number
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
                    stroke_width = 32 / self.max_number
                )
            nl.rotate(angle, about_point=ORIGIN).scale(self.scale_factor).shift(self.grid @ (0, 0) - nl @ (0))
            return nl

        self.x__line = always_redraw(lambda: make_number_line(1))
        
        x__label = always_redraw(lambda: Text("Space (x')", font_size=36).move_to(self.grid @ (self.max_number, self.speed.get_value() * self.max_number + 1)).scale(self.scale_factor))

        self.ct__line = always_redraw(lambda: make_number_line(-1))
        
        ct__label = always_redraw(lambda: Text("Time (ct')", font_size=36).move_to(self.grid @ (self.speed.get_value() * self.max_number + 3, self.max_number - 0.5)).scale(self.scale_factor))

        # Group all elements
        self.everything = VGroup(self.grid, x_label, ct_label, self.x__line, x__label, self.ct__line, ct__label)

        return
    
    def show(self):
        self.scene.add(self.everything)
        return

    def create(self):
        self.scene.play(Create(*self.everything))
        return

    def remove(self):
        self.scene.clear()
        return
    
    def prime_to_cords(self, x, ct):
        # Convert the coordinates to the new system
        new_x = (x / (1 - self.speed.get_value()**2)**(1/2))
        new_ct = (ct / (1 - self.speed.get_value()**2)**(1/2))
        return tuple(map(lambda x, y: x + y, (new_x, self.speed.get_value() * new_x), (self.speed.get_value() * new_ct, new_ct)))
        # Return the new coordinates
    
    def change_speed(self, new_speed, **kwargs):
        self.scene.play(self.speed.animate(**kwargs).set_value(new_speed))
        return

class Location:
    def __init__(self, diagram, x, ct):
        self.x = ValueTracker(x)
        self.ct = ValueTracker(ct)
        self.diagram = diagram
        self.everything = VGroup()
        return
    
    def _x(self, x, ct): return (x - self.diagram.speed.get_value() * ct) / (1 - self.diagram.speed.get_value()**2)**(1/2)
    def _ct(self, x, ct): return (ct - self.diagram.speed.get_value() * x) / (1 - self.diagram.speed.get_value()**2)**(1/2)

    def plot_lines(self):
        # Create the lines
        x_line = always_redraw(
            lambda: Line(self.diagram.grid @ (self.x.get_value(), 0), self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), stroke_width=1)
        )
        ct_line = always_redraw(
            lambda: Line(self.diagram.grid @ (0, self.ct.get_value()), self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), stroke_width=1)
        )
        self.everything.add(x_line, ct_line)
        self.diagram.scene.play(Create(x_line), Create(ct_line))
        self.diagram.scene.wait(0.1)
        return

    def plot_point(self):
        # Create the point
        point = always_redraw(
            lambda: Dot(self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), color=RED, radius=0.04)
        )
        self.everything.add(point)
        self.diagram.scene.play(Create(point))
        self.diagram.scene.wait(0.1)
        return

    def plot__lines(self):
        # Create the lines 
        x__line = always_redraw(
            lambda: Line(self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), self.diagram.grid @ self.diagram.prime_to_cords(self._x(self.x.get_value(), self.ct.get_value()), 0), color=YELLOW, stroke_width=0.5)
        )
        ct__line = always_redraw(
            lambda: Line(self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), self.diagram.grid @ self.diagram.prime_to_cords(0, self._ct(self.x.get_value(), self.ct.get_value())), color=YELLOW, stroke_width=0.5)
        )
        self.everything.add(x__line, ct__line)
        self.diagram.scene.play(Create(x__line), Create(ct__line))
        self.diagram.scene.wait(0.1)
        return

    def get_prime_coords(self):
        return (self._x(self.x.get_value(), self.ct.get_value()), self._ct(self.x.get_value(), self.ct.get_value()))
    
    def create(self):
        self.plot_lines()
        self.plot_point()
        self.plot__lines()
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
        (temp_x, temp_ct) = diagram.prime_to_cords(x, ct)
        self.x, self.ct = ValueTracker(temp_x), ValueTracker(temp_ct)
        self.everything = VGroup()
        return

    def plot__lines(self):
        # Create the lines
        x__line = always_redraw(
            lambda: Line(self.diagram.grid @ self.diagram.prime_to_cords(self._x.get_value(), 0), self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), color=YELLOW, stroke_width=0.5)
        )
        ct__line = always_redraw(
            lambda: Line(self.diagram.grid @ self.diagram.prime_to_cords(0, self._ct.get_value()), self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), color=YELLOW, stroke_width=0.5)
        )
        self.everything.add(x__line, ct__line)
        self.diagram.scene.play(Create(x__line), Create(ct__line))
        self.diagram.scene.wait(0.1)
        return

    def plot_point(self):
        # Create the point
        point = always_redraw(
            lambda: Dot(self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), color=RED, radius=0.04)
        )
        self.everything.add(point)
        self.diagram.scene.play(Create(point))
        self.diagram.scene.wait(0.1)
        return

    def plot_lines(self):
        # Create the lines
        x_line = always_redraw(
            lambda: Line(self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), self.diagram.grid @ (self.x.get_value(), 0), stroke_width=1)
        )
        ct_line = always_redraw(
            lambda: Line(self.diagram.grid @ (self.x.get_value(), self.ct.get_value()), self.diagram.grid @ (0, self.ct.get_value()), stroke_width=1)
        )
        self.everything.add(x_line, ct_line)
        self.diagram.scene.play(Create(x_line), Create(ct_line))
        self.diagram.scene.wait(0.1)
        return

    def get_coords(self):
        return (self.x.get_value(), self.ct.get_value())
    
    def create(self):
        self.plot__lines()
        self.plot_point()
        self.plot_lines()
        return

    def remove(self):  
        self.diagram.scene.remove(*self.everything)
        return
    
    def move_to(self, x, ct, **kwargs):
        (temp_x, temp_ct) = self.diagram.prime_to_cords(x, ct)
        self.diagram.scene.play(self._x.animate(**kwargs).set_value(x), self._ct.animate(**kwargs).set_value(ct), self.x.animate(**kwargs).set_value(temp_x), self.ct.animate(**kwargs).set_value(temp_ct))
        return