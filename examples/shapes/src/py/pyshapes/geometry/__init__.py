# Bring in everything from the shared module
from pyshapes._syntax import ClassDict
from pyshapes.geometry._pyshapes_geometry import *

Point = ClassDict(
    {
        2: Point_2,
        3: Point_3,
    }
)
