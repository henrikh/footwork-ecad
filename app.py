# Adapted from
#  - https://github.com/KmolYuan/python-solvespace/blob/master/example/PyDemo.py
#  - Work by Sean

from slvs import *

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


# Square

# Definitions of points
p7 = sys.add_param(0)
p8 = sys.add_param(0)
Point1 = Point2d(Workplane1, p7, p8)

p9 = sys.add_param(10)
p10 = sys.add_param(0)
Point2 = Point2d(Workplane1, p9, p10)

p11 = sys.add_param(10)
p12 = sys.add_param(0)
Point3 = Point2d(Workplane1, p11, p12)

p13 = sys.add_param(10)
p14 = sys.add_param(10)
Point4 = Point2d(Workplane1, p13, p14)

p15 = sys.add_param(10)
p16 = sys.add_param(10)
Point5 = Point2d(Workplane1, p15, p16)

p17 = sys.add_param(0)
p18 = sys.add_param(10)
Point6 = Point2d(Workplane1, p17, p18)

p19 = sys.add_param(0)
p20 = sys.add_param(10)
Point7 = Point2d(Workplane1, p19, p20)

p21 = sys.add_param(0)
p22 = sys.add_param(0)
Point8 = Point2d(Workplane1, p21, p22)

Line1 = LineSegment2d(Workplane1, Point1, Point2)
Line2 = LineSegment2d(Workplane1, Point3, Point4)
Line3 = LineSegment2d(Workplane1, Point5, Point6)
Line4 = LineSegment2d(Workplane1, Point7, Point8)

# Constrain edges of lines so the end-points are coincident
Constraint.on(Workplane1, Point1, Point8)
Constraint.on(Workplane1, Point2, Point3)
Constraint.on(Workplane1, Point4, Point5)
Constraint.on(Workplane1, Point6, Point7)

# Constrain level
Constraint.vertical(Workplane1, Line2)
Constraint.vertical(Workplane1, Line4)
Constraint.horizontal(Workplane1, Line1)
Constraint.horizontal(Workplane1, Line3)

# Constrain dimensions
Constraint.distance(100, Workplane1, Point1, Point2)
Constraint.equal(Workplane1, Line1, Line2)

# Constraint position
Constraint.distance(0, Workplane1, Point0, Point1)

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

print(Point1.u().value, Point1.v().value)
print(Point2.u().value, Point2.v().value)
print(Point3.u().value, Point3.v().value)
print(Point4.u().value, Point4.v().value)
print(Point5.u().value, Point5.v().value)
print(Point6.u().value, Point6.v().value)
print(Point7.u().value, Point7.v().value)
print(Point8.u().value, Point8.v().value)

print("{} DOF".format(sys.dof))
