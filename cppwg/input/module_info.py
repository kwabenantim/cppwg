"""Module information structure."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from cppwg.input.base_info import BaseInfo
from cppwg.input.class_info import CppClassInfo
from cppwg.input.free_function_info import CppFreeFunctionInfo


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

        super().__init__(name)

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
        """
        Returns the associated package info object.
        """
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
            if Path(full_path) in Path(decl.location.file_name).parents:
                return True

        return False

    def sort_classes(self) -> None:
        """
        Sort the class info collection in order of dependence.
        """
        cache = dict()

        def compare(a: CppClassInfo, b: CppClassInfo) -> int:
            """
            Compare two class info objects for dependence order.

            Parameters
            ----------
            a : CppClassInfo
            b : CppClassInfo

            Returns
            -------
            int
                -1 if a comes before b (b depends on a)
                 0 if there is no dependence
                 1 if a comes after b (a depends on b)
            """
            order = cache.get((a, b), None)
            if order is not None:
                return order

            a_req_b = a.requires(b)
            b_req_a = b.requires(a)
            if a.is_child_of(b) or (a_req_b and not b_req_a):
                # a comes after b (ignore cyclic dependencies)
                cache[(a, b)] = 1
                cache[(b, a)] = -1
                return 1
            elif b.is_child_of(a) or (b_req_a and not a_req_b):
                # a comes before b (ignore cyclic dependencies)
                cache[(a, b)] = -1
                cache[(b, a)] = 1
                return -1

            # Order doesn't matter
            cache[(a, b)] = 0
            cache[(b, a)] = 0
            return 0

        self.class_info_collection.sort(key=lambda x: x.source_file_full_path)

        i = 0
        n = len(self.class_info_collection)
        while i < n - 1:
            cls_i = self.class_info_collection[i]
            ii = i  # Tracks destination of cls_i
            j_pos = []  # Tracks positions of cls_i's dependents

            for j in range(i + 1, n):
                cls_j = self.class_info_collection[j]
                order = compare(cls_i, cls_j)
                if order == 1:
                    # Position cls_i after all classes it depends on
                    ii = j
                elif order == -1:
                    # Collect positions of cls_i's dependents
                    j_pos.append(j)

            if ii <= i:
                i += 1
                continue  # No change in position

            # Move cls_i into new position ii
            cls_i = self.class_info_collection.pop(i)
            self.class_info_collection.insert(ii, cls_i)

            # Move dependents into positions after ii
            for idx, j in enumerate(j_pos):
                if j > ii:
                    break  # Rest of dependents are already positioned after ii
                cls_j = self.class_info_collection.pop(j - 1 - idx)
                self.class_info_collection.insert(ii + idx, cls_j)

    def update_from_ns(self, source_ns: "namespace_t") -> None:  # noqa: F821
        """
        Update module with information from the source namespace.

        Parameters
        ----------
        source_ns : pygccxml.declarations.namespace_t
            The source namespace
        """
        # Add discovered classes: if `use_all_classes` is True, this module
        # has no class info objects. Use class declarations from the
        # source namespace to create class info objects.
        if self.use_all_classes:
            class_decls = source_ns.classes(allow_empty=True)
            for class_decl in class_decls:
                if self.is_decl_in_source_path(class_decl):
                    class_info = CppClassInfo(class_decl.name)
                    class_info.update_names()
                    class_info.module_info = self
                    self.class_info_collection.append(class_info)

        # Update classes with information from source namespace.
        for class_info in self.class_info_collection:
            class_info.update_from_ns(source_ns)

        # Sort classes by dependence
        self.sort_classes()

        # Add discovered free functions: if `use_all_free_functions` is True,
        # this module has no free function info objects. Use free function
        # decls from the source namespace to create free function info objects.
        if self.use_all_free_functions:
            free_functions = source_ns.free_functions(allow_empty=True)
            for free_function in free_functions:
                if self.is_decl_in_source_path(free_function):
                    ff_info = CppFreeFunctionInfo(free_function.name)
                    ff_info.module_info = self
                    self.free_function_info_collection.append(ff_info)

        # Update free functions with information from source namespace.
        for ff_info in self.free_function_info_collection:
            ff_info.update_from_ns(source_ns)

    def update_from_source(self, source_file_paths: List[str]) -> None:
        """
        Update module with information from the source headers.

        Parameters
        ----------
        source_files : List[str]
            A list of source file paths.
        """
        for class_info in self.class_info_collection:
            class_info.update_from_source(source_file_paths)
