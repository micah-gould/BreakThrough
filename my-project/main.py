from manim import *

class SpaceTimeGrid:
    def __init__(self, scene, v):
        # Create the coordinate system
        self.scene = scene
        self.speed = v
        self.angle = np.arctan(self.speed)

        self.scale = 25

        grid = Axes(
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
        x_label.next_to(grid.x_axis, RIGHT).shift(DOWN * 0.5 + LEFT)
        ct_label.next_to(grid.y_axis, UP).shift(DOWN * 0.5 + LEFT)

        x__line = Arrow(
            start=grid.coords_to_point(-self.scale, -self.speed * self.scale), 
            end=grid.coords_to_point(self.scale, self.speed * self.scale),
            color=YELLOW,
            stroke_width = 32 / self.scale)
        
        x__label = Text("Space (x')", font_size=36).move_to(grid.coords_to_point(self.scale, self.speed * (self.scale + 1)))

        x__ticks = VGroup()
        x__labels = VGroup()

        for i in range(int((-self.scale + 1) * (1 - self.speed**2)**(1/2)), int(self.scale * (1 - self.speed**2)**(1/2)), 2):
            new_cord = (i / (1 - self.speed**2)**(1/2))
            tick = Line(
                start=grid.coords_to_point(new_cord - self.speed * 0.25,  self.speed * new_cord + 0.25),
                end=grid.coords_to_point(new_cord + self.speed * 0.25,  self.speed * new_cord - 0.25),
                color=WHITE,
                stroke_width=32 / self.scale,
            )
            if (np.abs(i) > 2):
                label = Text(str(i), font_size=30, color=YELLOW)
                label.move_to(grid.coords_to_point(new_cord + self.speed * 0.5 * np.sign(i),  self.speed * new_cord -  0.5 * np.sign(i)))
                x__labels.add(label)
            x__ticks.add(tick)


        ct__line = Arrow(
            start=grid.coords_to_point(-self.speed * self.scale, -self.scale), 
            end=grid.coords_to_point(self.speed * self.scale, self.scale),
            color=YELLOW,
            stroke_width = 32 / self.scale)
        
        ct__label = Text("Time (ct')", font_size=36).move_to(grid.coords_to_point(self.speed * (self.scale + 3), self.scale - 1))

        ct__ticks = VGroup()
        ct__labels = VGroup()

        for i in range(int((-self.scale + 1) * (1 - self.speed**2)**(1/2)), int(self.scale * (1 - self.speed**2)**(1/2)), 2):
            new_cord = (i / (1 - self.speed**2)**(1/2))
            tick = Line(
                start=grid.coords_to_point(self.speed * new_cord - 0.25,  new_cord + self.speed * 0.25),
                end=grid.coords_to_point(self.speed * new_cord + 0.25,  new_cord - self.speed * 0.25),
                color=WHITE,
                stroke_width=32 / self.scale,
            )
            if (np.abs(i) > 2):
                label = Text(str(i), font_size=30, color=YELLOW)
                label.move_to(grid.coords_to_point(self.speed * new_cord - 0.5 * np.sign(i),  new_cord + self.speed * 0.5 * np.sign(i)))
                ct__labels.add(label)
            ct__ticks.add(tick)

        # Group all elements
        self.everything = VGroup(grid, x_label, ct_label, x__line, x__label, *x__ticks, *x__labels, ct__line, ct__label, *ct__ticks, *ct__labels)
        self.everything.scale(.1)
        self.everything.move_to(ORIGIN)

        # Add everything to the scene
        self.scene.add(self.everything)
    
    def remove(self):
        self.scene.clear()

    def plot(self, x, ct):
        # Create the point
        point = Dot(self.everything[0].coords_to_point(x, ct), color=RED, radius=0.015)
        self.scene.add(point)
        # self.scene.play(Create(point))
        # self.scene.wait(0.5)

        # Create the lines
        line1 = Line(self.everything[0].coords_to_point(x, ct), self.everything[0].coords_to_point(x, 0), color=RED, stroke_width=0.5)
        line2 = Line(self.everything[0].coords_to_point(x, ct), self.everything[0].coords_to_point(0, ct), color=RED, stroke_width=0.5)
        self.scene.add(line1, line2)
        # self.scene.play(Create(line1), Create(line2))
        # self.scene.wait(0.5)

class Scene1(Scene):
    def construct(self):
        diagram = SpaceTimeGrid(self, .6)
        # self.wait(0.5)
        diagram.plot(5, 3)
        diagram.plot(3, 5)
        # self.wait(0.5)
        # self.play(FadeOut(diagram.everything))
        # self.wait(0.5)
        # diagram.remove()
