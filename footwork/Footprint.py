from footwork import slvs

class Footprint:

    def __init__(self, name):
        self.name = name
        self.description = None
        self.nodes = {}
        self.system = None
        self.workplane = None
        self.origin = None

    def add_node(self, node):
        node.set_system(system=self.system, workplane=self.workplane)
        node.build()

        self.nodes[node.id] = node

    def setup_system(self):
        # Setup equation system
        self.system = slvs.System()
        g1 = slvs.groupNum(1)
        self.system.default_group = g1

        # Origin point zero
        p0 = self.system.add_param(0)
        p1 = self.system.add_param(0)
        p2 = self.system.add_param(0)
        Point0 = slvs.Point3d(p0, p1, p2)

        # Create normal vector
        # Quaternion represents a plane through the origin
        qw, qx, qy, qz = slvs.Slvs_MakeQuaternion(*[1, 0, 0], *[0, 1, 0])
        p3 = self.system.add_param(qw)
        p4 = self.system.add_param(qx)
        p5 = self.system.add_param(qy)
        p6 = self.system.add_param(qz)
        Normal1 = slvs.Normal3d(p3, p4, p5, p6)

        # Create workplane (a plane to draw 2D points on), defined by the origin
        # point and the normal vector
        self.workplane = slvs.Workplane(Point0, Normal1)

        # Setup the origin point
        self.origin = slvs.Point2d(self.workplane, p0, p1)
        slvs.Constraint.on(self.workplane, Point0, self.origin)
        

    def solve(self):
        # The solver can now be set to work
        self.system.calculateFaileds = 1
        self.system.solve()
        result = self.system.result

        if result == slvs.SLVS_RESULT_OKAY:
            print("OK")
        else:
            print("solve failed: problematic constraints are:")
            print(self.system.faileds)
            for e in range(self.system.faileds):
                print(self.system.failed)
            if result == slvs.SLVS_RESULT_INCONSISTENT:
                print("system inconsistent")
            else:
                print("system nonconvergent")
