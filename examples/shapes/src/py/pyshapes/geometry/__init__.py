# Bring in everything from the shared module
from pyshapes._syntax import ClassDict
from pyshapes.geometry._pyshapes_geometry import *

Point = ClassDict(
    "Point",
    [
        (2,),
        (3,),
    ],
)
