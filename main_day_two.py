class MakeItGrain(Scene):
    def construct(self):
        rect = Rectangle(fill_color=BLUE, fill_opacity=.5) # width = 4, height = 2
        self.play(Write(rect))
        self.wait()
        
        grain_size_value_float = 2**-4

        grain_size = Text("Grain Size").scale(.8).to_corner(UR).to_edge(RIGHT, buff=1)
        grain_size_value = DecimalNumber(grain_size_value_float).next_to(grain_size, DOWN)
        number_of_grains = Text("Number of Grains").scale(.8).next_to(grain_size_value, DOWN)
        number_of_grains_value = Integer().next_to(number_of_grains, DOWN).add_updater(lambda m, dt: m.set_value(int(8/grain_size_value.get_value()**2)))

        self.play(Write(grain_size), Write(grain_size_value), Write(number_of_grains), Write(number_of_grains_value))

        number_of_squares = ValueTracker(8/grain_size_value.get_value()**2)
        number_of_circles = number_of_squares

        circle_radius = math.sqrt(8/number_of_circles.get_value())/2
        number_of_horizontal_arranged_circles = 4/(2*circle_radius)
        number_of_vertical_arranged_circles = 2/(2*circle_radius)

        circles = Group(
                    *[VGroup(
                        *[Circle(radius = circle_radius, color=BLUE, fill_opacity=.5)
                            for _ in range(int(number_of_horizontal_arranged_circles))
                                ]).arrange(RIGHT, buff=0) 
                            for _ in range(int(number_of_vertical_arranged_circles))
                                ]).arrange(DOWN, buff=0)

        squares = Group(
                    *[VGroup(
                        *[Square(side_length=circle_radius*2, color=BLACK, fill_color=BLACK, fill_opacity=1)
                            for _ in range(int(number_of_horizontal_arranged_circles))
                                ]).arrange(RIGHT, buff=0) 
                            for _ in range(int(number_of_vertical_arranged_circles))
                                ]).arrange(DOWN, buff=0)
        
        clone_circles = circles.copy().next_to(rect, UP)
        clone_circles.shuffle()
        clone_circles_shuffled = Group(*[VGroup() for _ in clone_circles])
        groups_already_shuffled = []

        for right_arranged_circles in clone_circles:
            right_arranged_circles.shuffle()
            for circle in right_arranged_circles:
                circle_has_already_been_added = False
                while not circle_has_already_been_added:
                    v_group_selected = random.choice(clone_circles_shuffled)
                    if v_group_selected not in groups_already_shuffled:
                        if len(v_group_selected) < len(right_arranged_circles):
                            v_group_selected.add(circle)
                            circle_has_already_been_added = True
                        else:
                            groups_already_shuffled.append(v_group_selected)

        clone_circles_shuffled.scale_to_fit_width(config.frame_width).move_to(ORIGIN)
        animations = []
        for right_arranged_circles, clone_right_arranged_circles in zip(circles, clone_circles_shuffled):
            for circle, clone_circle in zip(right_arranged_circles, clone_right_arranged_circles):
                animations.append(Transform(circle, clone_circle))
        
        self.play(FadeIn(circles))
        
        v = int(number_of_circles.get_value())
        time_offsets = numpy.linspace(0, 5, v)
        for time_offset in time_offsets:
            self.add_sound('sounds/1.wav', time_offset)

        self.play(
            AnimationGroup(*[FadeIn(square) for squares_right_arranged in squares for square in squares_right_arranged], lag_ratio=5/number_of_circles.get_value()),
            AnimationGroup(*animations, lag_ratio=5/number_of_circles.get_value()), 
            )
        self.wait()

        time_offsets = numpy.linspace(0, 1, v)
        for time_offset in time_offsets:
            self.add_sound('sounds/2.wav', time_offset)
        self.play(circles.animate.scale_to_fit_width(rect.width), AnimationGroup(*[FadeOut(square) for squares_right_arranged in squares for square in squares_right_arranged], lag_ratio=1/number_of_circles.get_value()))
        self.play(FadeOut(circles))
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob is not rect])
        self.play(Unwrite(rect))
        self.wait()
        
