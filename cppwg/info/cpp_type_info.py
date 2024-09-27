"""C++ type information structure."""

from typing import Any, Dict, List, Optional

from cppwg.info.base_info import BaseInfo


class CppTypeInfo(BaseInfo):
    """
    An information structure for C++ types including classes, free functions etc.

    Attributes
    ----------
    name_override : str
        The name override specified in config e.g. "CustomFoo" -> "Foo"
    source_file : str
        The source file containing the type
    source_file_path : str
        The full path to the source file containing the type

    module_info : ModuleInfo
        The module info parent object associated with this type

    decls : pygccxml.declarations.declaration_t
        The pygccxml declarations associated with this type, one per template arg if templated
    template_arg_lists : List[List[Any]]
        List of template replacement arguments e.g. [[2, 2], [3, 3]]
    template_params : List[str]
        List of template parameters e.g. ["DIM_A", "DIM_B"]
    template_signature : str
        The template signature of the type e.g. "<unsigned DIM_A, unsigned DIM_B = DIM_A>"
    """

    def __init__(self, name: str, type_config: Optional[Dict[str, Any]] = None):

        super().__init__(name, type_config)

        self.name_override: str = ""
        self.source_file: str = ""
        self.source_file_path: str = ""

        self.module_info: Optional["ModuleInfo"] = None  # noqa: F821

        self.decls: List["declaration_t"] = []  # noqa: F821
        self.template_arg_lists: List[List[Any]] = []
        self.template_params: List[str] = []
        self.template_signature: str = ""

        if type_config:
            self.name_override = type_config.get("name_override", self.name_override)
            self.source_file = type_config.get("source_file", self.source_file)
            self.source_file_path = type_config.get(
                "source_file_path", self.source_file_path
            )

    def set_module(self, module_info: "ModuleInfo") -> None:  # noqa: F821
        """
        Set the associated module info object.
        """
        self.module_info = module_info
