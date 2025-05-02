from manim import *

class SpaceTimeGrid:
    def __init__(self, scene, v):
        # Create the coordinate system
        self.scene = scene
        self.speed = v
        self.angle = np.arctan(self.speed)

        self.scale = 24

        self.grid = Axes(
            x_range=[-self.scale, self.scale, 2],
            y_range=[-self.scale, self.scale, 2],
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
        
        x__label = Text("Space (x')", font_size=36).move_to(self.grid.coords_to_point(self.scale, self.speed * (self.scale + 1)))

        x__ticks = VGroup()
        x__labels = VGroup()

        for i in range(int((-self.scale + 1) * (1 - self.speed**2)**(1/2)), int(self.scale * (1 - self.speed**2)**(1/2)), 2):
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
        
        ct__label = Text("Time (ct')", font_size=36).move_to(self.grid.coords_to_point(self.speed * (self.scale + 3), self.scale - 1))

        ct__ticks = VGroup()
        ct__labels = VGroup()

        for i in range(int((-self.scale + 1) * (1 - self.speed**2)**(1/2)), int(self.scale * (1 - self.speed**2)**(1/2)), 2):
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
        self.scene.play(Create(self.everything))
        return

    def remove(self):
        self.scene.clear()
        return

    def plot(self, x, ct):
        # Create the lines
        x_line = Line(self.grid.coords_to_point(x, 0), self.grid.coords_to_point(x, ct), stroke_width=1)
        ct_line = Line(self.grid.coords_to_point(0, ct), self.grid.coords_to_point(x, ct), stroke_width=1)
        self.scene.add(x_line, ct_line)
        self.everything.add(x_line, ct_line)
        self.scene.play(Create(x_line), Create(ct_line))
        self.scene.wait(0.1)

        # Create the point
        point = Dot(self.grid.coords_to_point(x, ct), color=RED, radius=0.04)
        self.scene.add(point)
        self.everything.add(point)
        self.scene.play(Create(point))
        self.scene.wait(0.1)

        # Create the lines 
        new_x = (x - self.speed * ct) / (1 - self.speed**2)**(1/2)
        new_ct = (ct - self.speed * x) / (1 - self.speed**2)**(1/2)
        x__line = Line(self.grid.coords_to_point(x, ct), self.grid.coords_to_point(self.prime_to_cords(new_x, 0)), color=YELLOW, stroke_width=0.5)
        ct__line = Line(self.grid.coords_to_point(x, ct), self.grid.coords_to_point(self.prime_to_cords(0, new_ct)), color=YELLOW, stroke_width=0.5)
        self.scene.add(x__line, ct__line)
        self.everything.add(x__line, ct__line)
        self.scene.play(Create(x__line), Create(ct__line))
        self.scene.wait(0.1)

        return [new_x, new_ct]
    
    def prime_to_cords(self, x, ct): #TODO: fix this math to find the coordinate of a primed point
        # Convert the coordinates to the new system
        new_x = (x + self.speed * ct) * (1 - self.speed**2)**(1/2)
        new_ct = (ct + self.speed * x) * (1 - self.speed**2)**(1/2)
        return [new_x, new_ct]

class Scene1(Scene):
    def construct(self):
        diagram = SpaceTimeGrid(self, .6)
        diagram.show()
        self.wait(0.1)
        [x1, y1] = diagram.plot(5, 3)
        [x2, y2] = diagram.plot(3, 5)
        [x3, y3] = diagram.plot(4, 4)
        print(f"({x1}, {y1})")
        print(f"({x2}, {y2})")
        print(f"({x3}, {y3})")
        self.wait(0.1)
        self.play(FadeOut(diagram.everything))
        diagram.remove()
        self.wait(0.1)
        diagram2 = SpaceTimeGrid(self, .8)
        diagram2.create()
        self.wait(0.1)
