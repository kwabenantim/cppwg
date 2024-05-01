"""Class information structure."""

from typing import Any, Dict, List, Optional

from cppwg.input.cpp_type_info import CppTypeInfo


class CppClassInfo(CppTypeInfo):
    """
    An information structure for individual C++ classes to be wrapped.

    Attributes
    ----------
    full_names : List[str]
        The C++ names of the class e.g. ["Foo<2,2>", "Foo<3,3>"]
    short_names : List[str]
        The Python names of the class e.g. ["Foo2_2", "Foo3_3"]
    """

    def __init__(self, name: str, class_config: Optional[Dict[str, Any]] = None):

        super(CppClassInfo, self).__init__(name, class_config)

        self.full_names: List[str] = None
        self.short_names: List[str] = None

    def update_short_names(self):
        """
        Get the Python name for the class e.g. Foo2_2.

        Return the name of the class as it will appear on the Python side. This
        collapses template arguments, separating them by underscores and removes
        special characters. The return type is a list, as a class can have
        multiple names if it is templated. For example, a class "Foo" with
        template arguments [[2, 2], [3, 3]] will have a short name list
        ["Foo2_2", "Foo3_3"].

        Returns
        -------
        List[str]
            The list of short names
        """
        # Handles untemplated classes
        if self.template_arg_lists is None:
            if self.name_override:
                self.short_names = [self.name_override]
            else:
                self.short_names = [self.name]
            return

        self.short_names = []

        # Table of special characters for removal
        rm_chars = {"<": None, ">": None, ",": None, " ": None}
        rm_table = str.maketrans(rm_chars)

        # Clean the type name
        type_name = self.name
        if self.name_override is not None:
            type_name = self.name_override

        # Do standard name replacements e.g. "unsigned int" -> "Unsigned"
        for name, replacement in self.name_replacements.items():
            type_name = type_name.replace(name, replacement)

        # Remove special characters
        type_name = type_name.translate(rm_table)

        # Capitalize the first letter e.g. "foo" -> "Foo"
        if len(type_name) > 1:
            type_name = type_name[0].capitalize() + type_name[1:]

        # Create a string of template args separated by "_" e.g. 2_2
        for template_arg_list in self.template_arg_lists:
            # Example template_arg_list : [2, 2]

            template_string = ""
            for idx, arg in enumerate(template_arg_list):

                # Do standard name replacements
                arg_str = str(arg)
                for name, replacement in self.name_replacements.items():
                    arg_str = arg_str.replace(name, replacement)

                # Remove special characters
                arg_str = arg_str.translate(rm_table)

                # Capitalize the first letter
                if len(arg_str) > 1:
                    arg_str = arg_str[0].capitalize() + arg_str[1:]

                # Add "_" between template arguments
                template_string += arg_str
                if idx < len(template_arg_list) - 1:
                    template_string += "_"

            self.short_names.append(type_name + template_string)

    def update_full_names(self):
        """
        Get the C++ name for the class e.g. Foo<2,2>.

        Return the name (declaration) of the class as it appears on the C++
        side. The return type is a list, as a class can have multiple names
        (declarations) if it is templated. For example, a class "Foo" with
        template arguments [[2, 2], [3, 3]] will have a full name list
        ["Foo<2,2 >", "Foo<3,3 >"].

        Returns
        -------
        List[str]
            The list of full names
        """
        # Handles untemplated classes
        if self.template_arg_lists is None:
            self.full_names = [self.name]
            return

        self.full_names = []
        for template_arg_list in self.template_arg_lists:
            # Create template string from arg list e.g. [2, 2] -> "<2,2 >"
            template_string = ",".join([str(arg) for arg in template_arg_list])
            template_string = "<" + template_string + " >"

            # Join full name e.g. "Foo<2,2 >"
            self.full_names.append(self.name + template_string)

    @property
    def parent(self) -> "ModuleInfo":  # noqa: F821
        """Returns the parent module info object."""
        return self.module_info
