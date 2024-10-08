# Bring in everything from the shared module
from pyshapes._syntax import TemplateClassDict
from pyshapes.primitives._pyshapes_primitives import *

Shape = TemplateClassDict(
    {
        2: Shape_2,
        3: Shape_3,
    }
)
