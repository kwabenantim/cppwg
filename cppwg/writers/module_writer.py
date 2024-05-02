"""Wrapper code writer for modules."""

import logging
import os
from typing import Dict, List

from cppwg.utils.constants import CPPWG_EXT, CPPWG_HEADER_COLLECTION_FILENAME
from cppwg.writers.class_writer import CppClassWrapperWriter
from cppwg.writers.free_function_writer import CppFreeFunctionWrapperWriter


class CppModuleWrapperWriter:
    """
    Class to automatically generates Python bindings for modules.

    A module is a collection of classes and free functions that are to be
    wrapped in Python. The module writer generates the main cpp file for the
    module, which contains the pybind11 module definition. Within the module
    definition, the module's free functions and classes are registered.

    Attributes
    ----------
    module_info : ModuleInfo
        The module information to generate Python bindings for
    wrapper_templates : Dict[str, str]
        String templates with placeholders for generating wrapper code
    wrapper_root : str
        The output directory for the generated wrapper code
    package_license : str
        The license to include in the generated wrapper code
    class_decls : List[pygccxml.declarations.class_t]
        A list of declarations of all classes to be wrapped in the module
    """

    def __init__(
        self,
        module_info: "ModuleInfo",  # noqa: F821
        wrapper_templates: Dict[str, str],
        wrapper_root: str,
        package_license: str = "",
    ):
        self.module_info: "ModuleInfo" = module_info  # noqa: F821
        self.wrapper_templates: Dict[str, str] = wrapper_templates
        self.wrapper_root: str = wrapper_root
        self.package_license: str = (
            package_license  # TODO: use this in the generated wrappers
        )

        # For convenience, store a list of declarations of all
        # classes to be wrapped in the module
        self.class_decls: List["class_t"] = []  # noqa: F821

        for class_info in self.module_info.class_info_collection:
            self.class_decls.extend(class_info.decls)

    def write_module_wrapper(self) -> None:
        """
        Generate the contents of the main cpp file for the module.

        The main cpp file is named `modulename.main.cpp`. This file contains the
        pybind11 module definition, within which the module's classes and free
        functions are registered.

        Example output:

        ```
        #include <pybind11/pybind11.h> #include "Foo.cppwg.hpp"

        PYBIND11_MODULE(_packagename_modulename, m) {
            register_Foo_class(m);
        }
        ```
        """
        # Add top level includes
        cpp_string = "#include <pybind11/pybind11.h>\n"

        if self.module_info.package_info.common_include_file:
            cpp_string += f'#include "{CPPWG_HEADER_COLLECTION_FILENAME}"\n'

        # Add outputs from running custom generator code
        if self.module_info.custom_generator:
            cpp_string += self.module_info.custom_generator.get_module_pre_code()

        # Add includes for class wrappers in the module
        for class_info in self.module_info.class_info_collection:
            for short_name in class_info.short_names:
                # Example: #include "Foo2_2.cppwg.hpp"
                cpp_string += f'#include "{short_name}.{CPPWG_EXT}.hpp"\n'

        # Format module name as _packagename_modulename
        full_module_name = (
            "_" + self.module_info.package_info.name + "_" + self.module_info.name
        )

        # Create the pybind11 module
        cpp_string += "\nnamespace py = pybind11;\n"
        cpp_string += f"\nPYBIND11_MODULE({full_module_name}, m)\n"
        cpp_string += "{\n"

        # Add free functions
        for free_function_info in self.module_info.free_function_info_collection:
            function_writer = CppFreeFunctionWrapperWriter(
                free_function_info, self.wrapper_templates
            )
            cpp_string += function_writer.generate_wrapper()

        # Add classes
        for class_info in self.module_info.class_info_collection:
            for short_name in class_info.short_names:
                # Example: register_Foo2_2_class(m);"
                cpp_string += f"    register_{short_name}_class(m);\n"

        # Add code from the module's custom generator
        if self.module_info.custom_generator:
            cpp_string += self.module_info.custom_generator.get_module_code()

        cpp_string += "}\n"  # End of the pybind11 module

        # Write to /path/to/wrapper_root/modulename/modulename.main.cpp
        module_dir = os.path.join(self.wrapper_root, self.module_info.name)
        if not os.path.isdir(module_dir):
            os.makedirs(module_dir)

        module_cpp_file = os.path.join(module_dir, self.module_info.name + ".main.cpp")

        with open(module_cpp_file, "w") as out_file:
            out_file.write(cpp_string)

    def write_class_wrappers(self) -> None:
        """Write wrappers for classes in the module."""
        logger = logging.getLogger()

        for class_info in self.module_info.class_info_collection:
            logger.info(f"Generating wrapper for class {class_info.name}")

            class_writer = CppClassWrapperWriter(
                class_info,
                self.wrapper_templates,
                self.class_decls,
            )

            # Write the class wrappers into /path/to/wrapper_root/modulename/
            module_dir = os.path.join(self.wrapper_root, self.module_info.name)
            class_writer.write(module_dir)

    def write(self) -> None:
        """Generate the module and class wrappers."""
        logger = logging.getLogger()

        logger.info(f"Generating wrappers for module {self.module_info.name}")

        self.write_module_wrapper()
        self.write_class_wrappers()
