from footwork import slvs

class ConstructionLine:
    workplane = None

    line = None

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def set_system(self, system, workplane, units):
        """Sets the system and workplane used by the constraints

        This method is called by the footprint class."""
        self.workplane = workplane

    def build(self):
        """Constructs elements and constraints"""
        self.line = slvs.LineSegment2d(self.workplane, self.point1, self.point2)

    def kicad_footprint_form(self):
        return ""