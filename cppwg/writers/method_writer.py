"""Wrapper code writer for C++ methods."""

import re
from typing import Dict

from pygccxml import declarations

from cppwg.writers.base_writer import CppBaseWrapperWriter


class CppMethodWrapperWriter(CppBaseWrapperWriter):
    """
    Manage addition of method wrapper code.

    Attributes
    ----------
    class_info : ClassInfo
        The class information for the class containing the method
    template_idx: int
        The index of the template in class_info
    method_decl : [pygccxml.declarations.member_function_t]
        The pygccxml declaration object for the method
    class_decl : [pygccxml.declarations.class_t]
        The class declaration for the class containing the method
    wrapper_templates : Dict[str, str]
        String templates with placeholders for generating wrapper code
    class_short_name : Optional[str]
        The short name of the class e.g. 'Foo2_2'
    template_params: Optional[List[str]]
        The template params for the class e.g. ['DIM_A', 'DIM_B']
    template_args: Optional[List[str]]
        The template args for the class e.g. ['2', '2']
    """

    def __init__(
        self,
        class_info: "CppClassInfo",  # noqa: F821
        template_idx: int,
        method_decl: "member_function_t",  # noqa: F821
        wrapper_templates: Dict[str, str],
    ) -> None:

        super(CppMethodWrapperWriter, self).__init__(wrapper_templates)

        self.class_info: "CppClassInfo" = class_info  # noqa: F821
        self.method_decl: "member_function_t" = method_decl  # noqa: F821
        self.class_decl: "class_t" = class_info.decls[template_idx]  # noqa: F821

        self.class_short_name = class_info.short_names[template_idx]
        if self.class_short_name is None:
            self.class_short_name = self.class_decl.name

        self.template_params = class_info.template_params

        self.template_args = None
        if class_info.template_arg_lists:
            self.template_args = class_info.template_arg_lists[template_idx]

    def exclusion_criteria(self) -> bool:
        """
        Check if the method should be excluded from the wrapper code.

        Returns
        -------
        bool
            True if the method should be excluded, False otherwise
        """
        # Exclude private methods without over-rides
        if self.method_decl.access_type == "private":
            return True

        # Exclude sub class (e.g. iterator) methods such as:
        #   class Foo {
        #     public:
        #       class FooIterator {
        if self.method_decl.parent != self.class_decl:
            return True

        # Check for excluded return types
        calldef_excludes = [
            x.replace(" ", "")
            for x in self.class_info.hierarchy_attribute_gather("calldef_excludes")
        ]

        return_type_excludes = [
            x.replace(" ", "")
            for x in self.class_info.hierarchy_attribute_gather("return_type_excludes")
        ]

        return_type = self.method_decl.return_type.decl_string.replace(" ", "")
        if return_type in calldef_excludes or return_type in return_type_excludes:
            return True

        # Check for excluded argument patterns
        for argument_type in self.method_decl.argument_types:
            # e.g. ::std::vector<unsigned int> const & -> ::std::vector<unsigned
            arg_type_short = argument_type.decl_string.split()[0].replace(" ", "")
            if arg_type_short in calldef_excludes:
                return True

            # e.g. ::std::vector<unsigned int> const & -> ::std::vector<unsignedint>const&
            arg_type_full = argument_type.decl_string.replace(" ", "")
            if arg_type_full in calldef_excludes:
                return True

        return False

    def generate_wrapper(self) -> str:
        """
        Generate the method wrapper code.

        Example output:
        .def("bar", (void(Foo::*)(double)) &Foo::bar, " ", py::arg("d") = 1.0)

        Returns
        -------
        str
            The method wrapper code.
        """
        # Skip excluded methods
        if self.exclusion_criteria():
            return ""

        # Pybind11 def type e.g. "_static" for def_static()
        def_adorn = ""
        if self.method_decl.has_static:
            def_adorn += "_static"

        # How to point to class
        if self.method_decl.has_static:
            self_ptr = "*"
        else:
            # e.g. Foo2_2::*
            self_ptr = self.class_short_name + "::*"

        # Const-ness
        const_adorn = ""
        if self.method_decl.has_const:
            const_adorn = " const "

        # Get the arg signature e.g. "int, bool"
        arg_types = [t.decl_string for t in self.method_decl.argument_types]
        arg_signature = ", ".join(arg_types)

        # Default args e.g. py::arg("d") = 1.0
        default_args = ""
        if not self.default_arg_exclusion_criteria():
            for arg in self.method_decl.arguments:
                default_args += f', py::arg("{arg.name}")'

                if arg.default_value is not None:
                    default_value = str(arg.default_value)

                    if self.template_params:
                        # Check for template params in default value
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

                    default_args += f" = {default_value}"

        # Call policy, e.g. "py::return_value_policy::reference"
        call_policy = ""
        if declarations.is_pointer(self.method_decl.return_type):
            ptr_policy = self.class_info.hierarchy_attribute("pointer_call_policy")
            if ptr_policy:
                call_policy = f", py::return_value_policy::{ptr_policy}"

        elif declarations.is_reference(self.method_decl.return_type):
            ref_policy = self.class_info.hierarchy_attribute("reference_call_policy")
            if ref_policy:
                call_policy = f", py::return_value_policy::{ref_policy}"

        method_dict = {
            "def_adorn": def_adorn,
            "method_name": self.method_decl.name,
            "return_type": self.method_decl.return_type.decl_string,
            "self_ptr": self_ptr,
            "arg_signature": arg_signature,
            "const_adorn": const_adorn,
            "class_short_name": self.class_short_name,
            "method_docs": '" "',
            "default_args": default_args,
            "call_policy": call_policy,
        }
        class_method_template = self.wrapper_templates["class_method"]
        wrapper_string = class_method_template.format(**method_dict)

        return wrapper_string

    def generate_virtual_override_wrapper(self) -> str:
        """
        Generate wrapper code for overriding virtual methods.

        Example output:
        ```
        void bar(double d) const override {
            PYBIND11_OVERRIDE_PURE(
                bar,
                Foo2_2,
                bar,
                d);
        }
        ```

        Returns
        -------
        str
            The virtual override wrapper code.
        """
        # Skip private methods
        if self.method_decl.access_type == "private":
            return ""

        # Get list of arguments and types
        arg_list = []
        arg_name_list = []

        for arg, arg_type in zip(
            self.method_decl.arguments, self.method_decl.argument_types
        ):
            arg_list.append(f"{arg_type.decl_string} {arg.name}")
            arg_name_list.append(f"        {arg.name}")

        arg_string = ", ".join(arg_list)  # e.g. "int a, bool b, double c"
        arg_name_string = ",\n".join(arg_name_list)  # e.g. "a,\n b,\n c"

        # Const-ness
        const_adorn = ""
        if self.method_decl.has_const:
            const_adorn = " const "

        # For pure virtual methods, use PYBIND11_OVERRIDE_PURE
        overload_adorn = ""
        if self.method_decl.virtuality == "pure virtual":
            overload_adorn = "_PURE"

        # Get the return type e.g. "void"
        return_string = self.method_decl.return_type.decl_string

        # Add the override code from the template
        override_dict = {
            "return_type": return_string,
            "method_name": self.method_decl.name,
            "arg_string": arg_string,
            "const_adorn": const_adorn,
            "overload_adorn": overload_adorn,
            "tidy_method_name": self.tidy_name(return_string),
            "short_class_name": self.class_short_name,
            "args_string": arg_name_string,
        }
        wrapper_string = self.wrapper_templates["method_virtual_override"].format(
            **override_dict
        )

        return wrapper_string
