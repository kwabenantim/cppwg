# Bring in everything from the shared module
from pyshapes._syntax import ClassDict
from pyshapes.primitives._pyshapes_primitives import *

Shape = ClassDict(
    "Shape",
    [
        (2,),
        (3,),
    ],
)
