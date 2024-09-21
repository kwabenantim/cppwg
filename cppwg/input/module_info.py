"""Module information structure."""

import os
from functools import cmp_to_key
from typing import Any, Dict, List, Optional

from cppwg.input.base_info import BaseInfo


class ModuleInfo(BaseInfo):
    """
    A structure to hold information for individual modules.

    Attributes
    ----------
    package_info : PackageInfo
        The package info parent object associated with this module
    source_locations : List[str]
        A list of source locations for this module
    class_info_collection : List[CppClassInfo]
        A list of class info objects associated with this module
    free_function_info_collection : List[CppFreeFunctionInfo]
        A list of free function info objects associated with this module
    variable_info_collection : List[CppFreeFunctionInfo]
        A list of variable info objects associated with this module
    use_all_classes : bool
        Use all classes in the module
    use_all_free_functions : bool
        Use all free functions in the module
    use_all_variables : bool
        Use all variables in the module
    """

    def __init__(self, name: str, module_config: Optional[Dict[str, Any]] = None):

        super(ModuleInfo, self).__init__(name)

        self.package_info: Optional["PackageInfo"] = None  # noqa: F821
        self.source_locations: List[str] = None
        self.class_info_collection: List["CppClassInfo"] = []  # noqa: F821
        self.free_function_info_collection: List["CppFreeFunctionInfo"] = []  # fmt: skip # noqa: F821
        self.variable_info_collection: List["CppFreeFunctionInfo"] = []  # noqa: F821
        self.use_all_classes: bool = False
        self.use_all_free_functions: bool = False
        self.use_all_variables: bool = False

        if module_config:
            for key, value in module_config.items():
                setattr(self, key, value)

    @property
    def parent(self) -> "PackageInfo":  # noqa: F821
        """Returns the parent package info object."""
        return self.package_info

    def is_decl_in_source_path(self, decl: "declaration_t") -> bool:  # noqa: F821
        """
        Check if the declaration is associated with a file in the specified source paths.

        Parameters
        ----------
        decl : declaration_t
            The declaration to check

        Returns
        -------
        bool
            True if the declaration is associated with a file in a specified source path
        """
        if self.source_locations is None:
            return True

        for source_location in self.source_locations:
            full_path = os.path.join(self.package_info.source_root, source_location)
            if full_path in decl.location.file_name:
                return True

        return False

    def sort_classes(self) -> None:
        """Sort the class info collection in inheritance order."""

        def compare(class_info_0: "ClassInfo", class_info_1: "ClassInfo"):
            # Sort classes with no declarations to the bottom
            if class_info_0.decls == class_info_1.decls:
                return 0
            if class_info_0.decls is None:
                return 1
            if class_info_1.decls is None:
                return -1

            # Get the base classes for each class
            bases_0 = [
                base.related_class for decl in class_info_0.decls for base in decl.bases
            ]
            bases_1 = [
                base.related_class for decl in class_info_1.decls for base in decl.bases
            ]

            # 1 if class_0 is a child of class_1
            child_0 = int(any(base in class_info_1.decls for base in bases_0))

            # 1 if class_1 is a child of class 0
            child_1 = int(any(base in class_info_0.decls for base in bases_1))

            return child_0 - child_1

        self.class_info_collection.sort(key=lambda x: x.name)
        self.class_info_collection.sort(key=cmp_to_key(compare))
