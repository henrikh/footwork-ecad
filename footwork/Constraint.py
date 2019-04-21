from footwork import slvs
import footwork as fw

def distance(footprint, distance, *args):
    if len(args) == 1 \
        and isinstance(args[0], slvs.LineSegment2d):
        return slvs.Constraint.distance(distance.m_as(fw.BASE_UNIT), footprint.workplane,
            args[0].a(), args[0].b())

    elif len(args) == 2 \
        and isinstance(args[0], slvs.Point2d) \
        and isinstance(args[1], slvs.Point2d):
        return slvs.Constraint.distance(distance.m_as(fw.BASE_UNIT), footprint.workplane,
            args[0], args[1])

def equal(footprint, line1, line2):
    return slvs.Constraint.equal(footprint.workplane, line1, line2)

def horizontal(footprint, line):
    return slvs.Constraint.horizontal(footprint.workplane, line)

def midpoint(footprint, a, b):
    if isinstance(a, slvs.Point2d):
        return slvs.Constraint.midpoint(footprint.workplane, a, b)
    else:
        return slvs.Constraint.midpoint(footprint.workplane, b, a)

def on(footprint, a, b):
    if isinstance(a, slvs.Point2d):
        return slvs.Constraint.on(footprint.workplane, a, b)
    else:
        return slvs.Constraint.on(footprint.workplane, b, a)
