import unittest
import footwork as fw
import random

class TestSum(unittest.TestCase):

    def test_two_pad_footprint(self):
        footprint = fw.Footprint("test")

        footprint.set_up_system()

        Workplane1 = footprint.workplane

        ### Example of creating and constraining a simple two-pad footprint

        # Pads -- The pads are created in an equation system and a workplane
        pad1 = fw.Pad("1", pin_number=1, x=-10)
        pad2 = fw.Pad("2", pin_number=2)

        footprint.add_node(pad1)
        footprint.add_node(pad2)

        # The width and height of the pad is constrained
        fw.Constraint.distance(40, Workplane1, pad1.line_right.a(), pad1.line_right.b())
        fw.Constraint.distance(50, Workplane1, pad1.line_top.a(), pad1.line_top.b())

        fw.Constraint.equal(Workplane1, pad1.line_right, pad2.line_right)
        fw.Constraint.equal(Workplane1, pad1.line_top, pad2.line_top)

        # We then fix the distance between the two pads' closest edges
        desired_distance = random.randint(0, 100)
        fw.Constraint.distance(desired_distance, Workplane1, pad1.point1, pad2.point2)

        # A construction line is added to fix the pad in space. This construction line
        # goes between the center of the two pads. The line is fixed to be horizontal
        # and the origin is at the midpoint.
        construction_line = fw.LineSegment2d(Workplane1, pad1.point_center, pad2.point_center)
        fw.Constraint.horizontal(Workplane1, construction_line)
        fw.Constraint.midpoint(Workplane1, footprint.origin, construction_line)

        footprint.solve()

        distance = abs(pad1.point1.u().value - pad2.point2.u().value)

        self.assertEqual(round(distance, 10), desired_distance)

        self.assertEqual(round(pad1.get_height(), 10), 40)
        self.assertEqual(round(pad1.get_width(), 10), 50)
        self.assertEqual(round(pad2.get_height(), 10), 40)
        self.assertEqual(round(pad2.get_width(), 10), 50)

        print(pad1)
        print(footprint.kicad_footprint_form())

    def test_footprint_alignment(self):
        footprint = fw.Footprint("footprint-alignment")

        footprint.set_up_system()

        Workplane1 = footprint.workplane

        ### An example of a footprint with very non-trivial aligment

        # Four pads are defined. The widths are all equal, but the heights are
        # defined by their alignment.

        # 2-----1  2-----1
        # |     |  |     |
        # |  1  |  |  2  |  2-----1  2-----1
        # |     |  |     |  |  3  |  |  4  |
        # |     |  3-----4  3-----4  |     |
        # 3-----4                    3-----4

        pad1 = fw.Pad("1", pin_number=1, x=-10)
        pad2 = fw.Pad("2", pin_number=2, x=10)
        pad3 = fw.Pad("3", pin_number=3, x=20)
        pad4 = fw.Pad("4", pin_number=4, x=30)

        footprint.add_node(pad1)
        footprint.add_node(pad2)
        footprint.add_node(pad3)
        footprint.add_node(pad4)

        # All widths are equal
        fw.Constraint.distance(50, Workplane1, pad1.line_top.a(), pad1.line_top.b())
        fw.Constraint.equal(Workplane1, pad1.line_top, pad2.line_top)
        fw.Constraint.equal(Workplane1, pad1.line_top, pad3.line_top)
        fw.Constraint.equal(Workplane1, pad1.line_top, pad4.line_top)

        # The aligment contraints are set
        fw.Constraint.on(Workplane1, pad2.line_top.a(), pad1.line_top)
        fw.Constraint.on(Workplane1, pad3.line_bottom.a(), pad2.line_bottom)
        fw.Constraint.on(Workplane1, pad4.line_top.a(), pad3.line_top)
        fw.Constraint.on(Workplane1, pad4.line_bottom.a(), pad1.line_bottom)

        # A few of the heights are defined
        fw.Constraint.distance(60, Workplane1, pad1.line_right.a(), pad1.line_right.b())
        fw.Constraint.distance(50, Workplane1, pad2.line_right.a(), pad2.line_right.b())
        fw.Constraint.distance(40, Workplane1, pad4.line_right.a(), pad4.line_right.b())

        construction_line_1_2 = fw.LineSegment2d(Workplane1, pad1.point1, pad2.point2)
        construction_line_2_3 = fw.LineSegment2d(Workplane1, pad2.point4, pad3.point3)
        construction_line_3_4 = fw.LineSegment2d(Workplane1, pad3.point1, pad4.point2)
        fw.Constraint.equal(Workplane1, construction_line_1_2, construction_line_2_3)
        fw.Constraint.equal(Workplane1, construction_line_2_3, construction_line_3_4)

        # A construction line is added to fix the pad in space. This construction line
        # goes diagonally across the footprint and the midpoint is fixed to the (0,0)
        # coordinate. The length of line fixes the distance between the pads.
        construction_line = fw.LineSegment2d(Workplane1, pad1.point2, pad4.point4)
        fw.Constraint.midpoint(Workplane1, footprint.origin, construction_line)
        fw.Constraint.distance(260, Workplane1, pad1.point2, pad4.point4)

        footprint.solve()

        self.assertEqual(round(pad1.get_width(), 10), 50)
        self.assertEqual(round(pad2.get_width(), 10), 50)
        self.assertEqual(round(pad3.get_width(), 10), 50)
        self.assertEqual(round(pad4.get_width(), 10), 50)

        print(footprint.kicad_footprint_form())

if __name__ == '__main__':
    unittest.main()