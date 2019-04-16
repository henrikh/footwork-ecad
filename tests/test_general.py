import unittest
import footwork as fw
import random

class TestSum(unittest.TestCase):

    def test_two_pad_footprint(self):
        footprint = fw.Footprint("test")

        footprint.setup_system()

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
        print(pad1.kicad_footprint_form())

if __name__ == '__main__':
    unittest.main()