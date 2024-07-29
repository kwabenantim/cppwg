import unittest

import pyshapes.geometry
import pyshapes.mesh
import pyshapes.primitives


class TestClasses(unittest.TestCase):

    def testGeometry(self):

        p0 = pyshapes.geometry.Point2()
        self.assertTrue(p0.GetLocation() == [0.0, 0.0])

        p1 = pyshapes.geometry.Point2(5.0, 0.0)
        self.assertTrue(p1.GetLocation() == [5.0, 0.0])

        p2 = pyshapes.geometry.Point2(5.0, 5.0)
        self.assertTrue(p2.GetLocation() == [5.0, 5.0])

        p3 = pyshapes.geometry.Point2(0.0, 5.0)
        self.assertTrue(p3.GetLocation() == [0.0, 5.0])

        points = [p1, p2, p3]

        triangle = pyshapes.primitives.Shape2()
        triangle.SetVertices(points)
        self.assertTrue(len(triangle.rGetVertices()) == 3)

        rectangle = pyshapes.primitives.Rectangle(5.0, 10.0)
        self.assertTrue(len(rectangle.rGetVertices()) == 4)

        rectangle = pyshapes.primitives.Rectangle([p0, p1, p2, p3])
        self.assertTrue(rectangle.rGetVertices() == [p0, p1, p2, p3])

        cuboid = pyshapes.primitives.Cuboid(5.0, 10.0, 20.0)
        self.assertTrue(len(cuboid.rGetVertices()) == 8)

    def testMesh(self):

        cmesh = pyshapes.mesh.ConcreteMesh2()
        self.assertTrue(cmesh.GetIndex() == 0)

        cmesh.SetIndex(1)
        self.assertTrue(cmesh.GetIndex() == 1)


if __name__ == "__main__":
    unittest.main()
