"""Free function information structure."""

from typing import Any, Dict, Optional

from cppwg.info.cpp_type_info import CppTypeInfo


class CppFreeFunctionInfo(CppTypeInfo):
    """An information structure for individual free functions to be wrapped."""

    def __init__(
        self, name: str, free_function_config: Optional[Dict[str, Any]] = None
    ):

        super().__init__(name, free_function_config)

    @property
    def parent(self) -> "ModuleInfo":  # noqa: F821
        """Returns the parent module info object."""
        return self.module_info

    def update_from_ns(self, source_ns: "namespace_t") -> None:  # noqa: F821
        """
        Update with information from the source namespace.

        Adds the free function declaration.

        Parameters
        ----------
        source_ns : pygccxml.declarations.namespace_t
            The source namespace
        """
        ff_decls = source_ns.free_functions(self.name, allow_empty=True)
        self.decls = [ff_decls[0]]
