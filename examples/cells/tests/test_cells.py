import sys
import unittest

import petsc4py
import vtk
from pycells import PetscUtils, Scene


class TestCells(unittest.TestCase):

    def testVtkCaster(self):
        scene = Scene[2]()
        renderer = scene.GetRenderer()
        self.assertIsNotNone(renderer)

    def testPetscCaster(self):
        petsc4py.init(sys.argv)
        vec = PetscUtils.CreateVec(10)
        self.assertIsNotNone(vec)


if __name__ == "__main__":
    unittest.main()
