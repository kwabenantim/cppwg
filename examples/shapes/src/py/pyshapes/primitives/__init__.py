# Bring in everything from the shared module
from pyshapes._syntax import ClassDict
from pyshapes.primitives._pyshapes_primitives import *

Shape = ClassDict(
    {
        2: Shape_2,
        3: Shape_3,
    }
)
