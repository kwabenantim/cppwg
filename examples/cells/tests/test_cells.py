import unittest
import sys

import petsc4py
import vtk
from pycells import PetscUtils, Scene


class TestCells(unittest.TestCase):

    def testVtkCaster(self):
        scene = Scene[2]()
        renderer = scene.GetRenderer()
        self.assertIsInstance(renderer, vtk.vtkRenderingOpenGL2Python.vtkOpenGLRenderer)

    def testPetscCaster(self):
        petsc4py.init(sys.argv)
        vec = PetscUtils.CreateVec(10)
        self.assertIsInstance(vec, petsc4py.PETSc.Vec)


if __name__ == "__main__":
    unittest.main()
