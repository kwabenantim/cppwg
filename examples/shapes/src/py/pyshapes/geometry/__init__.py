# Bring in everything from the shared module
from pyshapes._syntax import TemplateClassDict
from pyshapes.geometry._pyshapes_geometry import *

Point = TemplateClassDict(
    {
        2: Point_2,
        3: Point_3,
    }
)
