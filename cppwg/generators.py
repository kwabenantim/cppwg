"""Contains the main interface for generating Python wrappers."""

import fnmatch
import logging
import os
import re
import subprocess
import uuid
from pathlib import Path
from typing import List, Optional

import pygccxml
from pygccxml.declarations.runtime_errors import declaration_not_found_t

from cppwg.input.class_info import CppClassInfo
from cppwg.input.free_function_info import CppFreeFunctionInfo
from cppwg.input.info_helper import CppInfoHelper
from cppwg.input.package_info import PackageInfo
from cppwg.parsers.package_info_parser import PackageInfoParser
from cppwg.parsers.source_parser import CppSourceParser
from cppwg.templates import pybind11_default as wrapper_templates
from cppwg.utils import utils
from cppwg.utils.constants import (
    CPPWG_DEFAULT_WRAPPER_DIR,
    CPPWG_EXT,
    CPPWG_HEADER_COLLECTION_FILENAME,
)
from cppwg.writers.header_collection_writer import CppHeaderCollectionWriter
from cppwg.writers.module_writer import CppModuleWrapperWriter


class CppWrapperGenerator:
    """
    Main class for generating C++ wrappers.

    Attributes
    ----------
    source_root : str
        The root directory of the C++ source code
    source_includes : List[str]
        The list of source include paths
    wrapper_root : str
        The output directory for the wrapper code
    castxml_binary : str
        The path to the castxml binary
    castxml_cflags : str
        Optional cflags to be passed to castxml e.g. "-std=c++17"
    package_info_path : str
        The path to the package info yaml config file; defaults to "package_info.yaml"
    source_ns : pygccxml.declarations.namespace_t
        The namespace containing C++ declarations parsed from the source tree
    package_info : PackageInfo
        A data structure containing the information parsed from package_info_path
    """

    def __init__(
        self,
        source_root: str,
        source_includes: Optional[List[str]] = None,
        wrapper_root: Optional[str] = None,
        castxml_binary: Optional[str] = None,
        package_info_path: Optional[str] = None,
        castxml_cflags: Optional[str] = None,
    ):
        logger = logging.getLogger()

        # Check that castxml_binary exists and is executable
        self.castxml_binary: str = ""

        if castxml_binary:
            if os.path.isfile(castxml_binary) and os.access(castxml_binary, os.X_OK):
                self.castxml_binary = castxml_binary
            else:
                logger.warning(
                    "Could not find specified castxml binary. Searching on path."
                )

        # Search for castxml_binary
        if not self.castxml_binary:
            path_to_castxml, _ = pygccxml.utils.find_xml_generator(name="castxml")

            if path_to_castxml:
                self.castxml_binary = path_to_castxml
                logger.info(f"Found castxml binary: {self.castxml_binary}")
            else:
                logger.error("Could not find a castxml binary.")
                raise FileNotFoundError()

        # Check castxml and pygccxml versions
        castxml_version: str = (
            subprocess.check_output([self.castxml_binary, "--version"])
            .decode("ascii")
            .strip()
        )
        castxml_version = re.search(
            r"castxml version \d+\.\d+\.\d+", castxml_version
        ).group(0)
        logger.info(castxml_version)
        logger.info(f"pygccxml version {pygccxml.__version__}")

        # Sanitize castxml_cflags
        self.castxml_cflags: str = ""
        if castxml_cflags:
            self.castxml_cflags = castxml_cflags

        # Sanitize source_root
        self.source_root: str = os.path.abspath(source_root)
        if not os.path.isdir(self.source_root):
            logger.error(f"Could not find source root directory: {source_root}")
            raise FileNotFoundError()

        # Sanitize wrapper_root
        self.wrapper_root: str = ""

        if wrapper_root:
            self.wrapper_root = os.path.abspath(wrapper_root)

        else:
            wrapper_dirname = CPPWG_DEFAULT_WRAPPER_DIR + "_" + uuid.uuid4().hex[:8]
            self.wrapper_root = os.path.join(self.source_root, wrapper_dirname)
            logger.info(f"Wrapper root not specified - using {self.wrapper_root}")

        if not os.path.isdir(self.wrapper_root):
            # Create the wrapper root directory if it doesn't exist
            logger.info(f"Creating wrapper root directory: {self.wrapper_root}")
            os.makedirs(self.wrapper_root)

        # Sanitize source_includes
        self.source_includes: List[str]  # type hinting
        if source_includes:
            self.source_includes = [
                os.path.abspath(include_path) for include_path in source_includes
            ]

            for include_path in self.source_includes:
                if not os.path.isdir(include_path):
                    logger.warning(
                        f"Could not find source include directory: {include_path}"
                    )
        else:
            self.source_includes = [self.source_root]

        # Sanitize package_info_path
        self.package_info_path: Optional[str] = None
        if package_info_path:
            # If a package info config file is specified, check that it exists
            self.package_info_path = os.path.abspath(package_info_path)
            if not os.path.isfile(package_info_path):
                logger.error(f"Could not find package info file: {package_info_path}")
                raise FileNotFoundError()
        else:
            # If no package info config file has been supplied, check the default
            default_package_info_file = os.path.join(os.getcwd(), "package_info.yaml")
            if os.path.isfile(default_package_info_file):
                self.package_info_path = default_package_info_file
                logger.info(
                    f"Package info file not specified - using {default_package_info_file}"
                )
            else:
                logger.warning("No package info file found - using default settings.")

        # Initialize remaining attributes
        self.source_ns: Optional[pygccxml.declarations.namespace_t] = None

        self.package_info: Optional[PackageInfo] = None

        self.header_collection_filepath: str = os.path.join(
            self.wrapper_root, CPPWG_HEADER_COLLECTION_FILENAME
        )

    def collect_source_hpp_files(self) -> None:
        """
        Collect *.hpp files from the source root.

        Walk through the source root and add any files matching the provided
        patterns e.g. "*.hpp". Skip the wrapper root and wrappers to
        avoid pollution.
        """
        for root, _, filenames in os.walk(self.source_root, followlinks=True):
            for pattern in self.package_info.source_hpp_patterns:
                for filename in fnmatch.filter(filenames, pattern):
                    filepath = os.path.abspath(os.path.join(root, filename))

                    # Skip files in wrapper root dir
                    if Path(self.wrapper_root) in Path(filepath).parents:
                        continue

                    # Skip files with the extensions like .cppwg.hpp
                    suffix = os.path.splitext(os.path.splitext(filename)[0])[1]
                    if suffix == CPPWG_EXT:
                        continue

                    self.package_info.source_hpp_files.append(filepath)

        # Check if any source files were found
        if not self.package_info.source_hpp_files:
            logging.error(f"No header files found in source root: {self.source_root}")
            raise FileNotFoundError()

    def extract_templates_from_source(self) -> None:
        """Extract template arguments for each class from the associated source file."""
        for module_info in self.package_info.module_info_collection:
            info_helper = CppInfoHelper(module_info)
            for class_info in module_info.class_info_collection:
                # Skip excluded classes
                if class_info.excluded:
                    continue
                info_helper.extract_templates_from_source(class_info)
                class_info.update_names()

    def log_unknown_classes(self) -> None:
        """Get unwrapped classes."""
        all_class_decls = self.source_ns.classes(allow_empty=True)

        seen_class_names = set()
        for module_info in self.package_info.module_info_collection:
            for class_info in module_info.class_info_collection:
                seen_class_names.add(class_info.name)
                if class_info.decls:
                    seen_class_names.update(decl.name for decl in class_info.decls)

        for decl in all_class_decls:
            if (
                Path(self.source_root) in Path(decl.location.file_name).parents
                and decl.name not in seen_class_names
            ):
                seen_class_names.add(decl.name)
                seen_class_names.add(decl.name.split("<")[0].strip())
                logging.info(
                    f"Unknown class {decl.name} from {decl.location.file_name}:{decl.location.line}"
                )

        # Check for uninstantiated class templates not parsed by pygccxml
        for hpp_file_path in self.package_info.source_hpp_files:

            class_list = utils.find_classes_in_source_file(hpp_file_path)

            for _, class_name, _ in class_list:
                if class_name not in seen_class_names:
                    seen_class_names.add(class_name)
                    logging.info(f"Unknown class {class_name} from {hpp_file_path}")

    def map_classes_to_hpp_files(self) -> None:
        """
        Map each class to a header file.

        Attempt to map source file paths to each class, assuming the containing
        file name is the class name.
        """
        for module_info in self.package_info.module_info_collection:
            for class_info in module_info.class_info_collection:
                # Skip excluded classes
                if class_info.excluded:
                    continue
                for hpp_file_path in self.package_info.source_hpp_files:
                    hpp_file_name = os.path.basename(hpp_file_path)
                    if class_info.name == os.path.splitext(hpp_file_name)[0]:
                        class_info.source_file_full_path = hpp_file_path
                        if class_info.source_file is None:
                            class_info.source_file = hpp_file_name

    def parse_header_collection(self) -> None:
        """
        Parse the hpp files to collect C++ declarations.

        Parse the headers with pygccxml and castxml to populate the source
        namespace with C++ declarations collected from the source tree.
        """
        source_parser = CppSourceParser(
            self.source_root,
            self.header_collection_filepath,
            self.castxml_binary,
            self.source_includes,
            self.castxml_cflags,
        )
        self.source_ns = source_parser.parse()

    def parse_package_info(self) -> None:
        """Parse the package info file to create a PackageInfo object."""
        if self.package_info_path:
            # If a package info file exists, parse it to create a PackageInfo object
            info_parser = PackageInfoParser(self.package_info_path, self.source_root)
            self.package_info = info_parser.parse()

        else:
            # If no package info file exists, create a PackageInfo object with default settings
            self.package_info = PackageInfo("cppwg_package", self.source_root)

    def add_discovered_classes(self) -> None:
        """
        Add discovered classes.

        Add class info objects for classes discovered by pygccxml from
        parsing the C++ source code. This is run for modules which set
        `use_all_classes` to True. No class info objects were created for
        those modules while parsing the package info yaml file.
        """
        for module_info in self.package_info.module_info_collection:
            if module_info.use_all_classes:
                class_decls = self.source_ns.classes(allow_empty=True)

                for class_decl in class_decls:
                    if module_info.is_decl_in_source_path(class_decl):
                        class_info = CppClassInfo(class_decl.name)
                        class_info.update_names()
                        class_info.module_info = module_info
                        module_info.class_info_collection.append(class_info)

    def add_class_decls(self) -> None:
        """
        Add declarations to class info objects.

        Update all class info objects with their corresponding
        declarations found by pygccxml in the C++ source code.
        """
        for module_info in self.package_info.module_info_collection:
            for class_info in module_info.class_info_collection:
                # Skip excluded classes
                if class_info.excluded:
                    continue

                class_info.decls: List["class_t"] = []  # noqa: F821

                for class_cpp_name in class_info.cpp_names:
                    decl_name = class_cpp_name.replace(" ", "")  # e.g. Foo<2,2>

                    try:
                        class_decl = self.source_ns.class_(decl_name)

                    except declaration_not_found_t as e1:
                        if (
                            class_info.template_signature is None
                            or "=" not in class_info.template_signature
                        ):
                            logging.error(
                                f"Could not find declaration for class {decl_name}"
                            )
                            raise e1

                        # If class has default args, try to compress the template signature
                        logging.warning(
                            f"Could not find declaration for class {decl_name}: trying for a partial match."
                        )

                        # Try to find the class without default template args
                        # e.g. for template <int A, int B=A> class Foo {};
                        # Look for Foo<2> instead of Foo<2,2>
                        pos = 0
                        for i, s in enumerate(class_info.template_signature.split(",")):
                            if "=" in s:
                                pos = i
                                break

                        decl_name = ",".join(decl_name.split(",")[0:pos]) + " >"

                        try:
                            class_decl = self.source_ns.class_(decl_name)

                        except declaration_not_found_t as e2:
                            logging.error(
                                f"Could not find declaration for class {decl_name}"
                            )
                            raise e2

                        logging.info(f"Found {decl_name}")

                    class_info.decls.append(class_decl)

    def add_discovered_free_functions(self) -> None:
        """
        Add discovered free function.

        Add free function info objects discovered by pygccxml from
        parsing the C++ source code. This is run for modules which set
        `use_all_free_functions` to True. No free function info objects were
        created for those modules while parsing the package info yaml file.
        """
        for module_info in self.package_info.module_info_collection:
            if module_info.use_all_free_functions:
                free_functions = self.source_ns.free_functions(allow_empty=True)

                for free_function in free_functions:
                    if module_info.is_decl_in_source_path(free_function):
                        ff_info = CppFreeFunctionInfo(free_function.name)
                        ff_info.module_info = module_info
                        module_info.free_function_info_collection.append(ff_info)

    def add_free_function_decls(self) -> None:
        """
        Add declarations to free function info objects.

        Update all free function info objects with their corresponding
        declarations found by pygccxml in the C++ source code.
        """
        for module_info in self.package_info.module_info_collection:
            for ff_info in module_info.free_function_info_collection:
                decls = self.source_ns.free_functions(ff_info.name, allow_empty=True)
                ff_info.decls = [decls[0]]

    def write_header_collection(self) -> None:
        """Write the header collection to file."""
        header_collection_writer = CppHeaderCollectionWriter(
            self.package_info,
            self.wrapper_root,
            self.header_collection_filepath,
        )
        header_collection_writer.write()

    def write_wrappers(self) -> None:
        """Write all the wrappers required for the package."""
        for module_info in self.package_info.module_info_collection:
            module_writer = CppModuleWrapperWriter(
                module_info,
                wrapper_templates.template_collection,
                self.wrapper_root,
            )
            module_writer.write()

    def generate_wrapper(self) -> None:
        """Parse input yaml and C++ source to generate Python wrappers."""
        # Parse the input yaml for package, module, and class information
        self.parse_package_info()

        # Search for header files in the source root
        self.collect_source_hpp_files()

        # Map each class to a header file
        self.map_classes_to_hpp_files()

        # Attempt to extract templates for each class from the source files
        self.extract_templates_from_source()

        # Write the header collection to file
        self.write_header_collection()

        # Parse the headers with pygccxml and castxml
        self.parse_header_collection()

        # Add discovered classes from the parsed code
        self.add_discovered_classes()

        # Add declarations to class info objects
        self.add_class_decls()

        # Add discovered free functions from the parsed code
        self.add_discovered_free_functions()

        # Add declarations to free function info objects
        self.add_free_function_decls()

        # Log list of unknown classes in the source root
        self.log_unknown_classes()

        # Write all the wrappers required
        self.write_wrappers()
