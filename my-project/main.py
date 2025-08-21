from manim import *

def round_up_to_even(n):
    return int(np.ceil(n / 2.0)) * 2

def round_down_to_even(n):
    return int(np.floor(n / 2.0)) * 2
class SpaceTimeGrid:
    def __init__(self, scene, v):
        # Create the coordinate system
        self.scene = scene
        self.speed = v

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

        x__line = Arrow(
            start=self.grid.coords_to_point(-self.scale, -self.speed * self.scale), 
            end=self.grid.coords_to_point(self.scale, self.speed * self.scale),
            color=YELLOW,
            stroke_width = 32 / self.scale)
        
        x__label = Text("Space (x')", font_size=36).move_to(self.grid.coords_to_point(self.scale, self.speed * self.scale + 0.5))

        x__ticks = VGroup()
        x__labels = VGroup()

        for i in range(round_up_to_even(-self.scale * (1 - self.speed**2)**(1/2)), round_down_to_even(self.scale * (1 - self.speed**2)**(1/2)), 2):
            new_cord = (i / (1 - self.speed**2)**(1/2))
            tick = Line(
                start=self.grid.coords_to_point(new_cord - self.speed * 0.25,  self.speed * new_cord + 0.25),
                end=self.grid.coords_to_point(new_cord + self.speed * 0.25,  self.speed * new_cord - 0.25),
                color=WHITE,
                stroke_width=32 / self.scale,
            )
            if (np.abs(i) > 2):
                label = Text(str(i), font_size=30, color=YELLOW)
                label.move_to(self.grid.coords_to_point(new_cord + self.speed * 0.5 * np.sign(i),  self.speed * new_cord -  0.5 * np.sign(i)))
                x__labels.add(label)
            x__ticks.add(tick)


        ct__line = Arrow(
            start=self.grid.coords_to_point(-self.speed * self.scale, -self.scale), 
            end=self.grid.coords_to_point(self.speed * self.scale, self.scale),
            color=YELLOW,
            stroke_width = 32 / self.scale)
        
        ct__label = Text("Time (ct')", font_size=36).move_to(self.grid.coords_to_point(self.speed * self.scale + 2, self.scale - 1))

        ct__ticks = VGroup()
        ct__labels = VGroup()

        for i in range(round_up_to_even(-self.scale * (1 - self.speed**2)**(1/2)), round_down_to_even(self.scale * (1 - self.speed**2)**(1/2)), 2):
            new_cord = (i / (1 - self.speed**2)**(1/2))
            tick = Line(
                start=self.grid.coords_to_point(self.speed * new_cord - 0.25,  new_cord + self.speed * 0.25),
                end=self.grid.coords_to_point(self.speed * new_cord + 0.25,  new_cord - self.speed * 0.25),
                color=WHITE,
                stroke_width=32 / self.scale,
            )
            if (np.abs(i) > 2):
                label = Text(str(i), font_size=30, color=YELLOW)
                label.move_to(self.grid.coords_to_point(self.speed * new_cord - 0.5 * np.sign(i),  new_cord + self.speed * 0.5 * np.sign(i)))
                ct__labels.add(label)
            ct__ticks.add(tick)

        # Group all elements
        self.everything = VGroup(self.grid, x_label, ct_label, x__line, x__label, *x__ticks, *x__labels, ct__line, ct__label, *ct__ticks, *ct__labels)
        self.everything.scale(.3)
        self.everything.move_to(ORIGIN)
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
        new_x = (x / (1 - self.speed**2)**(1/2))
        new_ct = (ct / (1 - self.speed**2)**(1/2))
        return tuple(map(lambda x, y: x + y, (new_x, self.speed * new_x), (self.speed * new_ct, new_ct)))
        # Return the new coordinates
    
    def change_speed(self, new_speed):
        self.show()
        new_diagram = SpaceTimeGrid(self.scene, new_speed)
        new_things = list(new_diagram.everything)[3:]
        old_things = list(self.everything)[3:]

        difference = (len(new_things) - len(old_things)) // 4
        keep_length = min((len(old_things) - 10) // 4, (len(new_things) - 10) // 4)

        if difference > 0:
            first_half, second_half = self.split_in_half(new_things)
        elif difference < 0:
            difference = -difference
            first_half, second_half = self.split_in_half(old_things)
        else:
            first_half, second_half = [], []

        if difference != 0:
            first_half, second_half = self.prune_halves(first_half, second_half, difference, keep_length)

            if len(new_things) > len(old_things):
                new_things = first_half + second_half
            else:
                old_things = first_half + second_half

        new_text, new_things = self.extract_text(new_things, keep_length)
        old_text, old_things = self.extract_text(old_things, keep_length)
        remove = [item for item in old_things if item not in new_things]
        add = [item for item in new_things if item not in old_things]


        angle = np.arctan(self.speed) - np.arctan(new_speed)

        self.scene.play(TransformMatchingShapes(VGroup(*old_text), VGroup(*new_text), path=angle), Transform(VGroup(*old_things), VGroup(*new_things)))
        self.remove()
        new_diagram.show()
        return
    
    def split_in_half(self, seq):
        """Split a sequence into two halves."""
        mid = len(seq) // 2
        return seq[:mid], seq[mid:]

    def prune_halves(self, first_half, second_half, difference, keep_length):
        """Apply deletions to both halves."""
        for half in (first_half, second_half):
            del half[2 : 2 + difference // 2]
            del half[keep_length + 5 : keep_length + 5 + difference]
            del half[-(difference // 2) :]
        return first_half, second_half

    def extract_text(self,things, keep_length):
        """Extract text elements while modifying the list in place."""
        first_half, second_half = self.split_in_half(things)
        text_first = [first_half.pop(1)] + [
            first_half.pop(keep_length + 4) for _ in range(keep_length)
        ]
        text_second = [second_half.pop(1)] + [
            second_half.pop(keep_length + 4) for _ in range(keep_length)
        ]
        return text_first + text_second, first_half + second_half

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
    
class alwaysUprightMathTex(MathTex):
    def __init__(self, *tex_strings, arg_separator = " ", substrings_to_isolate = None, tex_to_color_map = None, tex_environment = "align*", **kwargs):
        super().__init__(*tex_strings, arg_separator=arg_separator, substrings_to_isolate=substrings_to_isolate, tex_to_color_map=tex_to_color_map, tex_environment=tex_environment, **kwargs)
        self.submobjects.append(Line([-0.1,0,0],[+0.1,0,0],stroke_width=0))
        self.add_updater(self.updater, call_updater=True)

    def updater(self, mobj):
        self.rotate(-self.submobjects[-1].get_angle())


class Scene1(Scene):
    def construct(self):
        diagram2 = SpaceTimeGrid(self, .3)
        self.wait(0.1)
        diagram2.change_speed(0.9)
        self.wait()

class SlantedNumberLine(Scene):
    def construct(self):
        a = ValueTracker(40)
        sc = ValueTracker(10)

        # Create the tip label once
        tip_label = Text("Space (x)", font_size=36)

        def make_number_line():
            nl = NumberLine(
                x_range=[-sc.get_value(), sc.get_value() + 1, 2],
                length=10,
                include_numbers=True,
                include_tip=True,
                exclude_origin_tick=True,
                numbers_to_exclude=[0],
            ).set_color(YELLOW).rotate(a.get_value() * DEGREES, about_point=ORIGIN)

            # Vector along the line
            tangent = nl.number_to_point(1) - nl.number_to_point(0)
            tangent /= np.linalg.norm(tangent)
            normal = rotate_vector(tangent, PI/2)

            # Adjust numbers
            for mob in nl.numbers:
                num = mob.number
                base_point = nl.number_to_point(num)
                if num > 0:
                    mob.move_to(base_point + 0.3 * normal)
                elif num < 0:
                    mob.move_to(base_point - 0.3 * normal)
                mob.rotate(-a.get_value() * DEGREES, about_point=mob.get_center())

            # Update tip label position (like a number)
            tip_pos = nl.get_tip().get_center()
            tip_label.move_to(tip_pos + 0.3 * normal)

            return nl

        nl = always_redraw(make_number_line)
        self.add(nl, tip_label)

        self.wait()
        self.play(
            a.animate.set_value(5),
            sc.animate.set_value(4)
        )
        self.wait()
