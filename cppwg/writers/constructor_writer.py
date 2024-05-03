"""Wrapper code writer for C++ class constructors."""

import re
from typing import Dict

from pygccxml import declarations

from cppwg.writers.base_writer import CppBaseWrapperWriter


class CppConstructorWrapperWriter(CppBaseWrapperWriter):
    """
    Manage addition of constructor wrapper code.

    Attributes
    ----------
    class_info : ClassInfo
        The class information for the class containing the constructor
    template_idx: int
        The index of the template in class_info
    ctor_decl : pygccxml.declarations.constructor_t
        The pygccxml declaration object for the constructor
    class_decl : pygccxml.declarations.class_t
        The class declaration for the class containing the constructor
    wrapper_templates : Dict[str, str]
        String templates with placeholders for generating wrapper code
    class_py_name : Optional[str]
        The Python name of the class e.g. 'Foo2_2'
    template_params: Optional[List[str]]
        The template params for the class e.g. ['DIM_A', 'DIM_B']
    template_args: Optional[List[str]]
        The template args for the class e.g. ['2', '2']
    """

    def __init__(
        self,
        class_info: "CppClassInfo",  # noqa: F821
        template_idx: int,
        ctor_decl: "constructor_t",  # noqa: F821
        wrapper_templates: Dict[str, str],
    ) -> None:

        super(CppConstructorWrapperWriter, self).__init__(wrapper_templates)

        self.class_info: "CppClassInfo" = class_info  # noqa: F821
        self.ctor_decl: "constructor_t" = ctor_decl  # noqa: F821
        self.class_decl: "class_t" = class_info.decls[template_idx]  # noqa: F821

        self.class_py_name = class_info.py_names[template_idx]
        if self.class_py_name is None:
            self.class_py_name = self.class_decl.name

        self.template_params = class_info.template_params

        self.template_args = None
        if class_info.template_arg_lists:
            self.template_args = class_info.template_arg_lists[template_idx]

    def exclude(self) -> bool:
        """
        Check if the constructor should be excluded from the wrapper code.

        Returns
        -------
        bool
            True if the constructor should be excluded, False otherwise
        """
        # Exclude constructors for classes with private pure virtual methods
        if any(
            mf.virtuality == "pure virtual" and mf.access_type == "private"
            for mf in self.class_decl.member_functions(allow_empty=True)
        ):
            return True

        # Exclude constructors for abstract classes inheriting from abstract bases
        if self.class_decl.is_abstract and len(self.class_decl.recursive_bases) > 0:
            if any(
                base.related_class.is_abstract
                for base in self.class_decl.recursive_bases
            ):
                return True

        # Exclude sub class (e.g. iterator) constructors such as:
        #   class Foo {
        #     public:
        #       class FooIterator {
        if self.ctor_decl.parent != self.class_decl:
            return True

        # Exclude default copy constructors e.g. Foo::Foo(Foo const & foo)
        if (
            declarations.is_copy_constructor(self.ctor_decl)
            and self.ctor_decl.is_artificial
        ):
            return True

        # Check for excluded argument patterns
        calldef_excludes = [
            x.replace(" ", "")
            for x in self.class_info.hierarchy_attribute_gather("calldef_excludes")
        ]

        ctor_arg_type_excludes = [
            x.replace(" ", "")
            for x in self.class_info.hierarchy_attribute_gather(
                "constructor_arg_type_excludes"
            )
        ]

        for arg_type in self.ctor_decl.argument_types:
            # e.g. ::std::vector<unsigned int> const & -> ::std::vector<unsignedint>const&
            arg_type_str = arg_type.decl_string.replace(" ", "")

            # Exclude constructors with "iterator" in args
            if "iterator" in arg_type_str.lower():
                return True

            # Exclude constructors with args matching calldef_excludes
            if arg_type_str in calldef_excludes:
                return True

            # Exclude constructurs with args matching constructor_arg_type_excludes
            for excluded_type in ctor_arg_type_excludes:
                if excluded_type in arg_type_str:
                    return True

        return False

    def generate_wrapper(self) -> str:
        """
        Generate the constructor wrapper code.

        Example output:
        .def(py::init<int, bool >(), py::arg("i") = 1, py::arg("b") = false)

        Returns
        -------
        str
            The constructor wrapper code.
        """
        # Skip excluded constructors
        if self.exclude():
            return ""

        # Get the arg signature e.g. "int, bool"
        wrapper_string = "        .def(py::init<"

        arg_types = [t.decl_string for t in self.ctor_decl.argument_types]
        wrapper_string += ", ".join(arg_types)

        wrapper_string += " >()"

        # Keyword args with default values e.g. py::arg("i") = 1
        keyword_args = ""
        for arg in self.ctor_decl.arguments:
            keyword_args += f', py::arg("{arg.name}")'

            if not (
                arg.default_value is None
                or self.class_info.hierarchy_attribute("exclude_default_args")
            ):
                default_value = str(arg.default_value)

                # Check for template params in default value
                if self.template_params:
                    for param, val in zip(self.template_params, self.template_args):
                        if param in default_value:
                            # Replace e.g. Foo::DIM_A -> 2
                            default_value = re.sub(
                                f"\\b{self.class_info.name}::{param}\\b",
                                str(val),
                                default_value,
                            )

                            # Replace e.g. <DIM_A> -> <2>
                            default_value = re.sub(
                                f"\\b{param}\\b", f"{val}", default_value
                            )

                keyword_args += f" = {default_value}"

        wrapper_string += keyword_args + ")\n"

        return wrapper_string
