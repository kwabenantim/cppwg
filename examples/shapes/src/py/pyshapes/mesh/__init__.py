# Bring in everything from the shared module
from pyshapes._syntax import ClassDict
from pyshapes.mesh._pyshapes_mesh import *

AbstractMesh = ClassDict(
    "AbstractMesh",
    [
        (2, 2),
        (3, 3),
    ],
)
ConcreteMesh = ClassDict(
    "ConcreteMesh",
    [
        (2,),
        (3,),
    ],
)
