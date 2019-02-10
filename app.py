# adapted from https://github.com/KmolYuan/python-solvespace/blob/master/example/PyDemo.py

from footwork.slvs import *
from footwork.Pad import Pad

sys = System()
g1 = groupNum(1)
sys.default_group = g1

# origin Point zero
p0 = sys.add_param(0)
p1 = sys.add_param(0)
p2 = sys.add_param(0)
Point0 = Point3d(p0, p1, p2)

# create normal vector
# quaternion represents a plane through the origin
qw, qx, qy, qz = Slvs_MakeQuaternion(*[1, 0, 0], *[0, 1, 0])
p3 = sys.add_param(qw)
p4 = sys.add_param(qx)
p5 = sys.add_param(qy)
p6 = sys.add_param(qz)
Normal1 = Normal3d(p3, p4, p5, p6)

# create workplane (a plane to draw 2D points on), defined by
# the origin point and the normal vector
Workplane1 = Workplane(Point0, Normal1)

origin = Point2d(Workplane1, p0, p1)
Constraint.on(Workplane1, Point0, origin)

### Example of creating and constraining a single pad

# Pad -- The pad is created in an equation system and a workplane
pad1 = Pad(sys, Workplane1, x=-10)
pad2 = Pad(sys, Workplane1)

# The width and height of the pad is constrained
Constraint.distance(40, Workplane1, pad1.line_right.a(), pad1.line_right.b())
Constraint.distance(50, Workplane1, pad1.line_top.a(), pad1.line_top.b())

Constraint.equal(Workplane1, pad1.line_right, pad2.line_right)
Constraint.equal(Workplane1, pad1.line_top, pad2.line_top)

# We then fix the distance between the two pads' closest edges
Constraint.distance(20, Workplane1, pad1.point1, pad2.point2)

# A construction line is added to fix the pad in space. This construction line
# goes between the center of the two pads. The line is fixed to be horizontal
# and the origin is at the midpoint.
construction_line = LineSegment2d(Workplane1, pad1.point_center, pad2.point_center)
Constraint.horizontal(Workplane1, construction_line)
Constraint.midpoint(Workplane1, origin, construction_line)

# The solver can now be set to work
sys.calculateFaileds = 1
sys.solve()
result = sys.result

if result == SLVS_RESULT_OKAY:
    print("OK")
else:
    print("solve failed: problematic constraints are:")
    print(sys.faileds)
    for e in range(sys.faileds):
        print(sys.failed)
    if result == SLVS_RESULT_INCONSISTENT:
        print("system inconsistent")
    else:
        print("system nonconvergent")

print(pad1.to_string())
print(pad2.to_string())

print("{} DOF".format(sys.dof))
