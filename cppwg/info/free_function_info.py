"""Free function information structure."""

from typing import Any, Dict, Optional

from cppwg.info.cpp_entity_info import CppEntityInfo


class CppFreeFunctionInfo(CppEntityInfo):
    """An information structure for individual free functions to be wrapped."""

    def __init__(
        self, name: str, free_function_config: Optional[Dict[str, Any]] = None
    ):
        super().__init__(name, free_function_config)

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
