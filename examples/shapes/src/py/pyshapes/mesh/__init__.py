# Bring in everything from the shared module
from pyshapes._syntax import ClassDict
from pyshapes.mesh._pyshapes_mesh import *

AbstractMesh = ClassDict(
    {
        (2, 2): AbstractMesh_2_2,
        (3, 3): AbstractMesh_3_3,
    }
)

ConcreteMesh = ClassDict(
    {
        2: ConcreteMesh_2,
        3: ConcreteMesh_3,
    }
)
