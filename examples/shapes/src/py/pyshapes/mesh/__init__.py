# Bring in everything from the shared module
from pyshapes._syntax import TemplateClassDict
from pyshapes.mesh._pyshapes_mesh import *

AbstractMesh = TemplateClassDict(
    {
        (2, 2): AbstractMesh_2_2,
        (3, 3): AbstractMesh_3_3,
    }
)

ConcreteMesh = TemplateClassDict(
    {
        2: ConcreteMesh_2,
        3: ConcreteMesh_3,
    }
)
