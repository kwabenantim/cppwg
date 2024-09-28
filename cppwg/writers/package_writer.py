"""Wrapper code writer for the package."""

from typing import Dict

from cppwg.writers.module_writer import CppModuleWrapperWriter


class CppPackageWrapperWriter:
    """
    Class to generates Python bindings for all modules in the package.

    Attributes
    ----------
    package_info : PackageInfo
        The package information to generate Python bindings for
    wrapper_templates : Dict[str, str]
        String templates with placeholders for generating wrapper code
    wrapper_root : str
        The output directory for the generated wrapper code
    """

    def __init__(
        self,
        package_info: "PackageInfo",  # noqa: F821
        wrapper_templates: Dict[str, str],
        wrapper_root: str,
    ):
        self.package_info = package_info
        self.wrapper_templates = wrapper_templates
        self.wrapper_root = wrapper_root

    def write(self) -> None:
        """
        Write all the wrappers required for the package.
        """
        for module_info in self.package_info.module_collection:
            module_writer = CppModuleWrapperWriter(
                module_info,
                self.wrapper_templates,
                self.wrapper_root,
            )
            module_writer.write()
