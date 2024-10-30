import unittest

import vtk
from pycells import Scene_2


class TestCells(unittest.TestCase):

    def testVtkCaster(self):
        scene = Scene_2()
        renderer = scene.GetRenderer()
        self.assertIsNotNone(renderer)


if __name__ == "__main__":
    unittest.main()
