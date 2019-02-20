from footwork import *

footprint = Footprint("test")

footprint.setup_system()

sys = footprint.system
Workplane1 = footprint.workplane

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
Constraint.midpoint(Workplane1, footprint.origin, construction_line)

footprint.solve()

print(pad1.to_string())
print(pad2.to_string())

print("{} DOF".format(footprint.system.dof))
