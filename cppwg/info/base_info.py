"""Generic information structure."""

import importlib.util
import logging
import os
import sys
from typing import Any, Dict, List, Optional

import cppwg.templates.custom as cppwg_custom
from cppwg.utils.constants import CPPWG_SOURCEROOT_STRING


class BaseInfo:
    """
    A generic information structure for features.

    Features include packages, modules, classes, free functions, etc.
    Information structures are used to store information about the features. The
    information structures for each feature type inherit from BaseInfo, which
    sets a number of default attributes common to all features.

    Attributes
    ----------
    arg_type_excludes : List[str]
        List of exclude patterns for arg types in methods.
    calldef_excludes : List[str]
        Do not include calldefs matching these patterns.
    constructor_arg_type_excludes : List[str]
        List of exclude patterns for arg types in constructors.
    constructor_signature_excludes : List[List[str]]
        List of exclude patterns for constructor signatures.
    custom_generator : str
        A custom generator for the feature.
    excluded: bool
        Exclude this feature.
    excluded_methods : List[str]
        Do not include these methods.
    excluded_variables : List[str]
        Do not include these variables.
    extra_code : List[str]
        Any extra wrapper code for the feature.
    name : str
        The name of the package, module, class etc. represented by this object.
    name_replacements : Dict[str, str]
        A dictionary of name replacements e.g. {"double":"Double"}
    pointer_call_policy : str
        The default pointer call policy.
    prefix_code : List[str]
        Any wrapper code that precedes the feature.
    prefix_text : str
        Text to add at the top of all wrappers.
    reference_call_policy : str
        The default reference call policy.
    return_type_excludes : List[str]
        List of exclude patterns for return types.
    smart_ptr_type : str
        Handle classes with this smart pointer type.
    source_includes : List[str]
        A list of source files to be included with the feature.
    source_root : str
        The root directory of the C++ source code.
    template_substitutions : Dict[str, List[Any]]
        A list of template substitution sequences.

    custom_generator_instance : cppwg_custom.Custom
        An instance of the custom generator class.
    """

    def __init__(self, name: str, info_config: Optional[Dict[str, Any]] = None) -> None:
        """
        Create a base info object from a config dict.

        Parameters
        ----------
        name : str
            The name of the package, module, class, etc. represented by this object.
        info_config : Dict[str, Any]
            A dictionary of configuration settings
        """
        self.name: str = name

        # Paths
        self.source_includes: List[str] = []
        self.source_root: str = ""

        # Exclusions
        self.arg_type_excludes: List[str] = []
        self.calldef_excludes: List[str] = []
        self.constructor_arg_type_excludes: List[str] = []
        self.constructor_signature_excludes: List[List[str]] = []
        self.excluded: bool = False
        self.excluded_methods: List[str] = []
        self.excluded_variables: List[str] = []
        self.return_type_excludes: List[str] = []

        # Pointers
        self.pointer_call_policy: str = ""
        self.reference_call_policy: str = ""
        self.smart_ptr_type: str = ""

        # Substitutions
        self.template_substitutions: Dict[str, List[Any]] = []
        self.name_replacements: Dict[str, str] = {
            "double": "Double",
            "unsigned int": "Unsigned",
            "Unsigned int": "Unsigned",
            "unsigned": "Unsigned",
            "double": "Double",
            "std::vector": "Vector",
            "std::pair": "Pair",
            "std::map": "Map",
            "std::string": "String",
            "boost::shared_ptr": "SharedPtr",
            "*": "Ptr",
            "c_vector": "CVector",
            "std::set": "Set",
        }

        # Custom Code
        self.extra_code: List[str] = []
        self.prefix_code: List[str] = []
        self.prefix_text: str = ""
        self.custom_generator: str = ""

        self.custom_generator_instance: cppwg_custom.Custom = None

        if info_config:
            # Paths
            self.source_includes = info_config.get(
                "source_includes", self.source_includes
            )
            self.source_root = info_config.get("source_root", self.source_root)

            # Exclusions
            self.arg_type_excludes = info_config.get(
                "arg_type_excludes", self.arg_type_excludes
            )
            self.calldef_excludes = info_config.get(
                "calldef_excludes", self.calldef_excludes
            )
            self.constructor_arg_type_excludes = info_config.get(
                "constructor_arg_type_excludes", self.constructor_arg_type_excludes
            )
            self.constructor_signature_excludes = info_config.get(
                "constructor_signature_excludes", self.constructor_signature_excludes
            )
            self.excluded = info_config.get("excluded", self.excluded)
            self.excluded_methods = info_config.get(
                "excluded_methods", self.excluded_methods
            )
            self.excluded_variables = info_config.get(
                "excluded_variables", self.excluded_variables
            )
            self.return_type_excludes = info_config.get(
                "return_type_excludes", self.return_type_excludes
            )

            # Pointers
            self.pointer_call_policy = info_config.get(
                "pointer_call_policy", self.pointer_call_policy
            )
            self.reference_call_policy = info_config.get(
                "reference_call_policy", self.reference_call_policy
            )
            self.smart_ptr_type = info_config.get("smart_ptr_type", self.smart_ptr_type)

            # Substitutions
            self.template_substitutions = info_config.get(
                "template_substitutions", self.template_substitutions
            )
            self.name_replacements = info_config.get(
                "name_replacements", self.name_replacements
            )

            # Custom Code
            self.extra_code = info_config.get("extra_code", self.extra_code)
            self.prefix_code = info_config.get("prefix_code", self.prefix_code)
            self.prefix_text = info_config.get("prefix_text", self.prefix_text)
            self.custom_generator = info_config.get(
                "custom_generator", self.custom_generator
            )

        self.load_custom_generator()

    @property
    def parent(self) -> Optional["BaseInfo"]:
        """
        Get this object's parent.

        Return the parent object of the feature in the hierarchy. This is
        overriden in subclasses e.g. ModuleInfo returns a PackageInfo, ClassInfo
        returns a ModuleInfo, etc.

        Returns
        -------
        Optional[BaseInfo]
            The parent object.
        """
        return None

    def load_custom_generator(self) -> None:
        """
        Check if a custom generator is specified and load it.
        """
        if not self.custom_generator:
            return

        logger = logging.getLogger()

        # Replace the `CPPWG_SOURCEROOT` placeholder in the custom generator
        # path if needed. For example, a custom generator might be specified
        # as `custom_generator: CPPWG_SOURCEROOT/path/to/CustomGenerator.py`
        filepath = self.custom_generator.replace(
            CPPWG_SOURCEROOT_STRING, self.source_root
        )
        filepath = os.path.abspath(filepath)

        # Verify that the custom generator file exists
        if not os.path.isfile(filepath):
            logger.error(
                f"Could not find specified custom generator for {self.name}: {filepath}"
            )
            raise FileNotFoundError()

        logger.info(f"Custom generator for {self.name}: {filepath}")

        # Load the custom generator as a module
        module_name = os.path.splitext(filepath)[0]  # /path/to/CustomGenerator
        class_name = os.path.basename(module_name)  # CustomGenerator

        spec = importlib.util.spec_from_file_location(module_name, filepath)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Get the custom generator class from the loaded module.
        # Note: The custom generator class name must match the filename.
        CustomGeneratorClass: cppwg_custom.Custom = getattr(module, class_name)

        # Instantiate the custom generator from the provided class
        self.custom_generator_instance = CustomGeneratorClass()

    def hierarchy_attribute(self, attribute_name: str) -> Any:
        """
        Get the attribute value from this object or the one that owns this.

        Search higher level objects recursively and return the first
        value found for the attribute.

        Parameters
        ----------
        attribute_name : str
            The attribute name to search for.

        Returns
        -------
        Any
            The attribute value, or None if not found.
        """
        value = getattr(self, attribute_name, None)
        if value:
            return value

        if self.parent is None:
            # Reached the top of the hierarchy (i.e. PackageInfo)
            return None

        return self.parent.hierarchy_attribute(attribute_name)

    def hierarchy_attribute_gather(self, attribute_name: str) -> List[Any]:
        """
        Get a list of attribute values from this object or the one that owns it.

        Search higher level objects recursively, gathering attribute values
        into a list wherever the attribute is found.

        Parameters
        ----------
        attribute_name : str
            The attribute name to search for.

        Returns
        -------
        List[Any]
            The list of attribute values.
        """
        value_list: List[Any] = []

        value = getattr(self, attribute_name, None)
        if value:
            value_list.append(value)

        if self.parent is None:
            # Reached the top of the hierarchy (i.e. PackageInfo)
            return value_list

        value_list.extend(self.parent.hierarchy_attribute_gather(attribute_name))
        return value_list
