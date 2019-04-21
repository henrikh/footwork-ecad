import footwork as fw

footprint = fw.Footprint("footprint-alignment")
mm = footprint.units.millimeter

### An example of a footprint with very non-trivial aligment

# Four pads are defined. The widths are all equal, but the heights are
# defined by their alignment.

# 2-----1  2-----1
# |     |  |     |
# |  1  |  |  2  |  2-----1  2-----1
# |     |  |     |  |  3  |  |  4  |
# |     |  3-----4  3-----4  |     |
# 3-----4                    3-----4

pad1 = fw.Pad("1", pin_number=1, x=-10*mm)
pad2 = fw.Pad("2", pin_number=2, x=10*mm)
pad3 = fw.Pad("3", pin_number=3, x=20*mm)
pad4 = fw.Pad("4", pin_number=4, x=30*mm)

footprint.add_node(pad1)
footprint.add_node(pad2)
footprint.add_node(pad3)
footprint.add_node(pad4)

# All widths are equal
fw.Constraint.distance(footprint, 50*mm, pad1.line_top)
fw.Constraint.equal(footprint, pad1.line_top, pad2.line_top)
fw.Constraint.equal(footprint, pad1.line_top, pad3.line_top)
fw.Constraint.equal(footprint, pad1.line_top, pad4.line_top)

# The aligment contraints are set
fw.Constraint.on(footprint, pad2.line_top.a(), pad1.line_top)
fw.Constraint.on(footprint, pad3.line_bottom.a(), pad2.line_bottom)
fw.Constraint.on(footprint, pad4.line_top.a(), pad3.line_top)
fw.Constraint.on(footprint, pad4.line_bottom.a(), pad1.line_bottom)

# A few of the heights are defined
fw.Constraint.distance(footprint, 60*mm, pad1.line_right)
fw.Constraint.distance(footprint, 50*mm, pad2.line_right)
fw.Constraint.distance(footprint, 40*mm, pad4.line_right)

construction_line_1_2 = fw.ConstructionLine(pad1.point_1, pad2.point_2)
footprint.add_node(construction_line_1_2)
construction_line_2_3 = fw.ConstructionLine(pad2.point_4, pad3.point_3)
footprint.add_node(construction_line_2_3)
construction_line_3_4 = fw.ConstructionLine(pad3.point_1, pad4.point_2)
footprint.add_node(construction_line_3_4)

fw.Constraint.equal(footprint, construction_line_1_2.line, construction_line_2_3.line)
fw.Constraint.equal(footprint, construction_line_2_3.line, construction_line_3_4.line)

# A construction line is added to fix the pad in space. This construction line
# goes diagonally across the footprint and the midpoint is fixed to the (0,0)
# coordinate. The length of line fixes the distance between the pads.
construction_line = fw.ConstructionLine(pad1.point_2, pad4.point_4)
footprint.add_node(construction_line)
fw.Constraint.midpoint(footprint, footprint.origin, construction_line.line)
fw.Constraint.distance(footprint, 260*mm, construction_line.line)

footprint.solve()

print(footprint.kicad_footprint_form())