from footwork import slvs
import footwork as fw

class Pad:
    sys = None
    workplane = None
    units = None

    def __init__(self, node_id, pin_number, x=None, y=None, width=None, height=None):
        self.id = node_id
        self.pin_number = pin_number
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def set_system(self, system, workplane, units):
        """Sets the system and workplane used by the constraints

        This method is called by the footprint class."""
        self.sys = system
        self.workplane = workplane
        self.units = units

    def build(self):
        """Constructs elements and constraints"""
        self.create_geometry()
        self.create_constraints()

    def create_geometry(self):
        """Adds points and lines to the equation system and the workplane.

        Points are arranged according with the quadrants of a coordinate system, like the follwoing diagram:

        ```
        2---1
        |  /|
        | c |
        |/  |
        3---4
        ```"""

        assert(self.sys != None and self.workplane != None and self.units != None)

        if self.x == None:
            _x = 1
        else:
            _x = self.x.m_as(fw.BASE_UNIT)

        if self.y == None:
            _y = 1
        else:
            _y = self.y.m_as(fw.BASE_UNIT)

        if self.width == None:
            _width = 1
        else:
            _width = self.width.m_as(fw.BASE_UNIT)

        if self.height == None:
            _height = 1
        else:
            _height = self.height.m_as(fw.BASE_UNIT)

        # Point 1
        p1x = self.sys.add_param(_x + _width/2)
        p1y = self.sys.add_param(_y + _height/2)
        self.point_1 = slvs.Point2d(self.workplane, p1x, p1y)

        # Point 2
        p2x = self.sys.add_param(_x - _width/2)
        p2y = self.sys.add_param(_y + _height/2)
        self.point_2 = slvs.Point2d(self.workplane, p2x, p2y)

        # Point 3
        p3x = self.sys.add_param(_x - _width/2)
        p3y = self.sys.add_param(_y - _height/2)
        self.point_3 = slvs.Point2d(self.workplane, p3x, p3y)

        # Point 4
        p4x = self.sys.add_param(_x + _width/2)
        p4y = self.sys.add_param(_y - _height/2)
        self.point_4 = slvs.Point2d(self.workplane, p4x, p4y)

        # Center point
        pcx = self.sys.add_param(_x)
        pcy = self.sys.add_param(_y)
        self.point_center = slvs.Point2d(self.workplane, pcx, pcy)

        # Line 1-2 (top)
        self.line_top = slvs.LineSegment2d(self.workplane, self.point_1, self.point_2)

        # Line 2-3 (left)
        self.line_left = slvs.LineSegment2d(self.workplane, self.point_2, self.point_3)

        # Line 3-4 (bottom)
        self.line_bottom = slvs.LineSegment2d(self.workplane, self.point_3, self.point_4)

        # Line 4-1 (right)
        self.line_right = slvs.LineSegment2d(self.workplane, self.point_4, self.point_1)

        # Line 1-3 (Diagonal)
        self.line_diagonal = slvs.LineSegment2d(self.workplane, self.point_1, self.point_3)

    def get_x(self):
        """Returns the x coordinate of the center point"""
        return self.units.Quantity(self.point_center.u().value, fw.BASE_UNIT)

    def get_y(self):
        """Returns the y coordinate of the center point"""
        return self.units.Quantity(self.point_center.v().value, fw.BASE_UNIT)

    def get_width(self):
        """Returns the width of the pad"""
        return self.units.Quantity(self.point_1.u().value - self.point_2.u().value, fw.BASE_UNIT)

    def get_height(self):
        """Returns the height of the pad"""
        return self.units.Quantity(self.point_1.v().value - self.point_4.v().value, fw.BASE_UNIT)

    def create_constraints(self):
        """Adds constraints to ensure shape of the pad."""

        # Horizontal and vertical constraints to ensure rectangularity
        slvs.Constraint.horizontal(self.workplane, self.line_top)
        slvs.Constraint.vertical(self.workplane, self.line_left)
        slvs.Constraint.horizontal(self.workplane, self.line_bottom)
        slvs.Constraint.vertical(self.workplane, self.line_right)

        # Fix the center point to be half-way on the diagonal
        slvs.Constraint.midpoint(self.workplane, self.point_center, self.line_diagonal)

    def __str__(self):

        return "Rectangular pad {pin_number} at <{x:+6.3f}, {y:+6.3f}> mm, w={width:6.3f} mm, h={height:6.3f} mm".format(
        **{
        'pin_number': self.pin_number,
        'x': self.get_x().m_as(self.units.millimeter),
        'y': self.get_y().m_as(self.units.millimeter),
        'width': self.get_width().m_as(self.units.millimeter),
        'height': self.get_height().m_as(self.units.millimeter)}
        )

    def kicad_footprint_form(self):
        """Returns a string representing the KiCAD footprint form."""

        return \
            f"(pad {self.pin_number} " \
            f"smd rect (at {self.get_x().m_as(self.units.millimeter)} " \
            f"{self.get_y().m_as(self.units.millimeter)}) " \
            f"(size {self.get_width().m_as(self.units.millimeter)} " \
            f"{self.get_height().m_as(self.units.millimeter)}) " \
            f"(layers F.Cu F.Paste F.Mask))"
