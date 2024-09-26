"""Package information structure."""

import fnmatch
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from cppwg.input.base_info import BaseInfo
from cppwg.utils.constants import CPPWG_EXT


class PackageInfo(BaseInfo):
    """
    A structure to hold information about the package.

    Attributes
    ----------
    name : str
        The name of the package
    source_locations : List[str]
        A list of source locations for this package
    module_info_collection : List[ModuleInfo]
        A list of module info objects associated with this package
    source_root : str
        The root directory of the C++ source code
    source_hpp_patterns : List[str]
        A list of source file patterns to include
    source_hpp_files : List[str]
        A list of source file names to include
    common_include_file : bool
        Use a common include file for all source files
    exclude_default_args : bool
        Exclude default arguments from method wrappers.
    """

    def __init__(
        self,
        name: str,
        source_root: str,
        package_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Create a package info object from a package_config.

        The package_config is a dictionary of package configuration settings
        extracted from a yaml input file.

        Parameters
        ----------
        name : str
            The name of the package
        source_root : str
            The root directory of the C++ source code
        package_config : Dict[str, Any]
            A dictionary of package configuration settings
        """
        super().__init__(name)

        self.name: str = name
        self.source_locations: List[str] = None
        self.module_info_collection: List["ModuleInfo"] = []  # noqa: F821
        self.source_root: str = source_root
        self.source_hpp_patterns: List[str] = ["*.hpp"]
        self.source_hpp_files: List[str] = []
        self.common_include_file: bool = False
        self.exclude_default_args: bool = False

        if package_config:
            for key, value in package_config.items():
                setattr(self, key, value)

    @property
    def parent(self) -> None:
        """Returns None as this is the top level object in the hierarchy."""
        return None

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
        Update modules with information from the source headers.
        """
        for module_info in self.module_info_collection:
            module_info.update_from_source(self.source_hpp_files)

    def update_from_ns(self, source_ns: "namespace_t") -> None:  # noqa: F821
        """
        Update modules with information from the parsed source namespace.

        Parameters
        ----------
        source_ns : pygccxml.declarations.namespace_t
            The source namespace
        """
        for module_info in self.module_info_collection:
            module_info.update_from_ns(source_ns)
