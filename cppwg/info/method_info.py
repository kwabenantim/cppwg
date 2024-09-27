"""Method information structure."""

from typing import Optional

from cppwg.info.cpp_entity_info import CppEntityInfo


class CppMethodInfo(CppEntityInfo):
    """
    An information structure for individual methods to be wrapped.

    Attributes
    ----------
    class_info : CppClassInfo
        The class info object associated this method belongs to.
    """

    def __init__(self, name: str, _) -> None:

        super().__init__(name)

        self.class_info: Optional["CppClassInfo"] = None  # noqa: F821

    @property
    def owner(self) -> "CppClassInfo":  # noqa: F821
        """
        Returns the class info object that holds this method info object.
        """
        return self.class_info
