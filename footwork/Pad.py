from footwork.slvs import *

class Pad:
    def __init__(self, sys, wp, x=1, y=1, width=1, height=1):
        self.sys = sys
        self.workplane = wp
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.create_points_and_lines()
        self.create_constraints()

    def create_points_and_lines(self):
        """Adds points and lines to the equation system and the workplane.

        Points are arranged according with the quadrants of a coordinate system, like the follwoing diagram:

        ```
        2---1
        |  /|
        | c |
        |/  |
        3---4
        ```"""

        # Point 1
        p1x = self.sys.add_param(self.x + self.width/2)
        p1y = self.sys.add_param(self.y + self.height/2)
        self.point1 = Point2d(self.workplane, p1x, p1y)

        # Point 2
        p2x = self.sys.add_param(self.x - self.width/2)
        p2y = self.sys.add_param(self.y + self.height/2)
        self.point2 = Point2d(self.workplane, p2x, p2y)

        # Point 3
        p3x = self.sys.add_param(self.x - self.width/2)
        p3y = self.sys.add_param(self.y - self.height/2)
        self.point3 = Point2d(self.workplane, p3x, p3y)

        # Point 4
        p4x = self.sys.add_param(self.x + self.width/2)
        p4y = self.sys.add_param(self.y - self.height/2)
        self.point4 = Point2d(self.workplane, p4x, p4y)

        # Center point
        pcx = self.sys.add_param(self.x)
        pcy = self.sys.add_param(self.y)
        self.point_center = Point2d(self.workplane, pcx, pcy)

        # Line 1-2 (top)
        self.line_top = LineSegment2d(self.workplane, self.point1, self.point2)

        # Line 2-3 (left)
        self.line_left = LineSegment2d(self.workplane, self.point2, self.point3)

        # Line 3-4 (bottom)
        self.line_bottom = LineSegment2d(self.workplane, self.point3, self.point4)

        # Line 4-1 (right)
        self.line_right = LineSegment2d(self.workplane, self.point4, self.point1)

        # Line 1-3 (Diagonal)
        self.line_diagonal = LineSegment2d(self.workplane, self.point1, self.point3)

    def create_constraints(self):
        """Adds constraints to ensure shape of the pad."""

        # Horizontal and vertical constraints to ensure rectangularity
        Constraint.horizontal(self.workplane, self.line_top)
        Constraint.vertical(self.workplane, self.line_left)
        Constraint.horizontal(self.workplane, self.line_bottom)
        Constraint.vertical(self.workplane, self.line_right)

        # Fix the center point to be half-way on the diagonal
        Constraint.midpoint(self.workplane, self.point_center, self.line_diagonal)

    def __str__(self):
        return "Rectangular pad at <{x:+6.3f}, {y:+6.3f}>, w={width:6.3f}, h={height:6.3f}".format(
        **{'x': self.point_center.u().value,
        'y': self.point_center.v().value,
        'width': self.point1.u().value - self.point2.u().value,
        'height': self.point1.v().value - self.point4.v().value}
        )

        