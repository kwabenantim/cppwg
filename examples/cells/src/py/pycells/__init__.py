"""Main pycells module."""

from ._pycells_all import (
    Cell,
    MeshFactory_PottsMesh_2,
    MeshFactory_PottsMesh_3,
    Node_2,
    Node_3,
    PetscUtils,
    PottsMesh_2,
    PottsMesh_3,
    Scene_2,
    Scene_3,
)
from ._syntax import TemplateClassDict

MeshFactory = TemplateClassDict(
    {
        ("PottsMesh", "2"): MeshFactory_PottsMesh_2,
        ("PottsMesh", "3"): MeshFactory_PottsMesh_3,
    }
)

Node = TemplateClassDict(
    {
        ("2",): Node_2,
        ("3",): Node_3,
    }
)

PottsMesh = TemplateClassDict(
    {
        ("2",): PottsMesh_2,
        ("3",): PottsMesh_3,
    }
)

Scene = TemplateClassDict(
    {
        ("2",): Scene_2,
        ("3",): Scene_3,
    }
)

__all__ = [
    "Cell",
    "MeshFactory",
    "Node",
    "PetscUtils",
    "PottsMesh",
    "Scene",
]
