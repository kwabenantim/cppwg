"""Package information structure."""

import fnmatch
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from cppwg.info.base_info import BaseInfo
from cppwg.utils.constants import CPPWG_EXT


class PackageInfo(BaseInfo):
    """
    A structure to hold information about the package.

    Attributes
    ----------
    common_include_file : bool
        Use a common include file for all source files
    exclude_default_args : bool
        Exclude default arguments from method wrappers.
    name : str
        The name of the package
    source_hpp_patterns : List[str]
        A list of source file patterns to include

    module_collection : List[ModuleInfo]
        A list of module info objects associated with this package
    source_hpp_files : List[str]
        A list of source file names to include
    """

    def __init__(
        self, name: str, package_config: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Create a package info object from a package_config dict.

        Parameters
        ----------
        name : str
            The name of the package
        package_config : Dict[str, Any]
            A dictionary of package configuration settings
        """
        super().__init__(name, package_config)

        self.common_include_file: bool = False
        self.exclude_default_args: bool = False
        self.source_hpp_patterns: List[str] = ["*.hpp"]

        self.module_collection: List["ModuleInfo"] = []  # noqa: F821
        self.source_hpp_files: List[str] = []

        if package_config:
            self.common_include_file = package_config.get(
                "common_include_file", self.common_include_file
            )
            self.exclude_default_args = package_config.get(
                "exclude_default_args", self.exclude_default_args
            )
            self.source_hpp_patterns = package_config.get(
                "source_hpp_patterns", self.source_hpp_patterns
            )

    @property
    def parent(self) -> None:
        """
        Returns None, as this is the top level of the info tree hierarchy.
        """
        return None

    def add_module(self, module_info: "ModuleInfo") -> None:  # noqa: F821
        """
        Add a module info object to the package.

        Parameters
        ----------
        module_info : ModuleInfo
            The module info object to add
        """
        self.module_collection.append(module_info)
        module_info.parent = self

    def init(self, restricted_paths: List[str]) -> None:
        """
        Initialise - collect header files and update info.

        Parameters
        ----------
        restricted_paths : List[str]
            A list of restricted paths to skip when collecting header files.
        """
        self.collect_source_headers(restricted_paths)
        self.update_from_source()

    def collect_source_headers(self, restricted_paths: List[str]) -> None:
        """
        Collect header files from the source root.

        Walk through the source root and add any files matching the provided
        source file patterns e.g. "*.hpp".

        Parameters
        ----------
        restricted_paths : List[str]
            A list of restricted paths to skip when collecting header files.
        """
        logger = logging.getLogger()

        for root, _, filenames in os.walk(self.source_root, followlinks=True):
            for pattern in self.source_hpp_patterns:
                for filename in fnmatch.filter(filenames, pattern):
                    filepath = os.path.abspath(os.path.join(root, filename))

                    # Skip files in restricted paths
                    for restricted_path in restricted_paths:
                        if Path(restricted_path) in Path(filepath).parents:
                            continue

                    # Skip files with the extensions like .cppwg.hpp
                    suffix = os.path.splitext(os.path.splitext(filename)[0])[1]
                    if suffix == CPPWG_EXT:
                        continue

                    self.source_hpp_files.append(filepath)

        # Check if any source files were found
        if not self.source_hpp_files:
            logger.error(f"No header files found in source root: {self.source_root}")
            raise FileNotFoundError()

        # Sort by filename
        self.source_hpp_files.sort(key=lambda x: os.path.basename(x))

    def update_from_source(self) -> None:
        """
        Update with data from the source headers.
        """
        for module_info in self.module_collection:
            module_info.update_from_source(self.source_hpp_files)

    def update_from_ns(self, source_ns: "namespace_t") -> None:  # noqa: F821
        """
        Update modules with information from the parsed source namespace.

        Parameters
        ----------
        source_ns : pygccxml.declarations.namespace_t
            The source namespace
        """
        for module_info in self.module_collection:
            module_info.update_from_ns(source_ns)
