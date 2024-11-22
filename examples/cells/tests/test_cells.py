import sys
import unittest

import petsc4py
import vtk
from pycells import Node, PetscUtils, Scene


class TestCells(unittest.TestCase):
    def testVtkCaster(self):
        scene = Scene[2]()
        renderer = scene.GetRenderer()
        self.assertIsNotNone(renderer)

    def testPetscCaster(self):
        petsc4py.init(sys.argv)
        vec = PetscUtils.CreateVec(10)
        self.assertIsNotNone(vec)

    def testUblasCaster(self):
        node = Node[2]()
        self.assertEqual(list(node.GetLocation()), [0, 0])
        node.Translate([1, 1])
        self.assertEqual(list(node.GetLocation()), [1, 1])


if __name__ == "__main__":
    unittest.main()
