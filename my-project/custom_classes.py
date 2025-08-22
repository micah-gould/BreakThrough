from manim import *

#TODO: Figure out why it jumps around when the speed is changed


def round_up_to_even(n):
    return int(np.ceil(n / 2.0)) * 2

def round_down_to_even(n):
    return int(np.floor(n / 2.0)) * 2

class SpaceTimeGrid:
    def __init__(self, scene, v):
        # Create the coordinate system
        self.scene = scene
        self.speed = ValueTracker(v)

        self.scale = 24
        self.count = 2

        self.grid = Axes(
            x_range=[-self.scale, self.scale, self.count],
            y_range=[-self.scale, self.scale, self.count],
            x_length=self.scale,  # Enlarged so it looks good after scaling
            y_length=self.scale,
            axis_config={"include_numbers": True, "stroke_width": 32 / self.scale},
        )

        # Label the axes
        x_label = Text("Space (x)", font_size=36)  # Larger to compensate for scaling
        ct_label = Text("Time (ct)", font_size=36)

        # Position the labels
        x_label.next_to(self.grid.x_axis, RIGHT).shift(DOWN * 0.5 + LEFT)
        ct_label.next_to(self.grid.y_axis, UP).shift(DOWN * 0.5 + LEFT)
        
        def make_number_line(flip=1):

            angle = np.arctan(self.speed.get_value()) if flip == -1 else PI/2 - np.arctan(self.speed.get_value())

            nl = NumberLine(
                x_range=[round_up_to_even(-self.scale * (1 - self.speed.get_value()**2)**(1/2)), round_down_to_even(self.scale * (1 - self.speed.get_value()**2)**(1/2)), 2],
                length=np.linalg.norm(self.grid.coords_to_point(-self.scale, -self.speed.get_value() * self.scale) - self.grid.coords_to_point(self.scale, self.speed.get_value() * self.scale)),
                include_numbers=True,
                include_tip=True,
                exclude_origin_tick=True,
                numbers_to_exclude=list(range(-3, 4)),
                color=YELLOW,
                stroke_width = 32 / self.scale
            ).rotate(angle, about_point=ORIGIN)

            tangent = nl.number_to_point(1) - nl.number_to_point(0)
            tangent /= np.linalg.norm(tangent)
            normal = rotate_vector(tangent, PI / 2) * flip
            for mob in nl.numbers:
                num = mob.number
                base_point = nl.number_to_point(num)
                mob.move_to((base_point + 0.3 * normal) if num > 0 else (base_point - 0.3 * normal))
                mob.rotate(-angle, about_point=mob.get_center())

            # Adjust the position of the tip
            return nl

        x__line = always_redraw(lambda: make_number_line(1))
        
        x__label = always_redraw(lambda: Text("Space (x')", font_size=36).move_to(self.grid.coords_to_point(self.scale, self.speed.get_value() * self.scale + 0.5)))

        ct__line = always_redraw(lambda: make_number_line(-1))
        
        ct__label = always_redraw(lambda: Text("Time (ct')", font_size=36).move_to(self.grid.coords_to_point(self.speed.get_value() * self.scale + 2, self.scale - 1)))

        # Group all elements
        self.everything = VGroup(self.grid, x_label, ct_label, x__line, x__label, ct__line, ct__label)
        self.everything.scale(.3)
        # self.everything.move_to(ORIGIN)
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
    
    def change_speed(self, new_speed):
        self.scene.play(self.speed.animate.set_value(new_speed))
        return

class Location:
    def __init__(self, diagram, x, ct):
        self.x = x
        self.ct = ct
        self.diagram = diagram
        self._x = (x - diagram.speed * ct) / (1 - diagram.speed**2)**(1/2)
        self._ct = (ct - diagram.speed * x) / (1 - diagram.speed**2)**(1/2)
        self.everything = VGroup()
        return

    def plot_lines(self):
        # Create the lines
        x_line = Line(self.diagram.grid.coords_to_point(self.x, 0), self.diagram.grid.coords_to_point(self.x, self.ct), stroke_width=1)
        ct_line = Line(self.diagram.grid.coords_to_point(0, self.ct), self.diagram.grid.coords_to_point(self.x, self.ct), stroke_width=1)
        self.everything.add(x_line, ct_line)
        self.diagram.scene.play(Create(x_line), Create(ct_line))
        self.diagram.scene.wait(0.1)
        return

    def plot_point(self):
        # Create the point
        point = Dot(self.diagram.grid.coords_to_point(self.x, self.ct), color=RED, radius=0.04)
        self.everything.add(point)
        self.diagram.scene.play(Create(point))
        self.diagram.scene.wait(0.1)
        return

    def plot__lines(self):
        # Create the lines 
        x__line = Line(self.diagram.grid.coords_to_point(self.x, self.ct), self.diagram.grid.coords_to_point(*self.diagram.prime_to_cords(self._x, 0)), color=YELLOW, stroke_width=0.5)
        ct__line = Line(self.diagram.grid.coords_to_point(self.x, self.ct), self.diagram.grid.coords_to_point(*self.diagram.prime_to_cords(0, self._ct)), color=YELLOW, stroke_width=0.5)
        self.everything.add(x__line, ct__line)
        self.diagram.scene.play(Create(x__line), Create(ct__line))
        self.diagram.scene.wait(0.1)
        return

    def get_prime_coords(self):
        return (self._x, self._ct)
    
    def create(self):
        self.plot_lines()
        self.plot_point()
        self.plot__lines()
        return 

    def remove(self):
        self.diagram.scene.remove(*self.everything)
        return
        

class PrimeLocation:
    def __init__(self, diagram, x, ct):
        self._x = x
        self._ct = ct   
        self.diagram = diagram
        (self.x, self.ct) = diagram.prime_to_cords(x, ct)
        self.everything = VGroup()
        return

    def plot__lines(self):
        # Create the lines
        x__line = Line(self.diagram.grid.coords_to_point(*self.diagram.prime_to_cords(self._x, 0)), self.diagram.grid.coords_to_point(self.x, self.ct), color=YELLOW, stroke_width=0.5)
        ct__line = Line(self.diagram.grid.coords_to_point(*self.diagram.prime_to_cords(0, self._ct)), self.diagram.grid.coords_to_point(self.x, self.ct), color=YELLOW, stroke_width=0.5)
        self.everything.add(x__line, ct__line)
        self.diagram.scene.play(Create(x__line), Create(ct__line))
        self.diagram.scene.wait(0.1)
        return

    def plot_point(self):
        # Create the point
        point = Dot(self.diagram.grid.coords_to_point(self.x, self.ct), color=RED, radius=0.04)
        self.everything.add(point)
        self.diagram.scene.play(Create(point))
        self.diagram.scene.wait(0.1)
        return

    def plot_lines(self):
        # Create the lines
        x_line = Line(self.diagram.grid.coords_to_point(self.x, self.ct), self.diagram.grid.coords_to_point(self.x, 0), stroke_width=1)
        ct_line = Line(self.diagram.grid.coords_to_point(self.x, self.ct), self.diagram.grid.coords_to_point(0, self.ct), stroke_width=1)
        self.everything.add(x_line, ct_line)
        self.diagram.scene.play(Create(x_line), Create(ct_line))
        self.diagram.scene.wait(0.1)
        return

    def get_coords(self):
        return (self.x, self.ct)
    
    def create(self):
        self.plot__lines()
        self.plot_point()
        self.plot_lines()
        return

    def remove(self):  
        self.diagram.scene.remove(*self.everything)
        return