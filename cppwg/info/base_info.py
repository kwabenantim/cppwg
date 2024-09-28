"""Generic information structure."""

import importlib.util
import logging
import os
import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import cppwg.templates.custom as cppwg_custom
from cppwg.utils.constants import CPPWG_SOURCEROOT_STRING


class BaseInfo(ABC):
    """
    A generic information structure for features.

    Features include packages, modules, classes, free functions, etc.
    Information structures are used to store information about the features.
    BaseInfo is the base information structure, and set up attributes that are
    common to all features.

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
            for key in [
                "arg_type_excludes",
                "calldef_excludes",
                "constructor_arg_type_excludes",
                "constructor_signature_excludes",
                "custom_generator",
                "excluded",
                "excluded_methods",
                "excluded_variables",
                "extra_code",
                "name_replacements",
                "pointer_call_policy",
                "prefix_code",
                "prefix_text",
                "reference_call_policy",
                "return_type_excludes",
                "smart_ptr_type",
                "source_includes",
                "source_root",
                "template_substitutions",
            ]:
                if key in info_config:
                    setattr(self, key, info_config[key])

        self.load_custom_generator()

    @property
    @abstractmethod
    def parent(self) -> Optional["BaseInfo"]:
        """
        Returns this object's parent node in the info tree hierarchy.

        This property is supplied by subclasses e.g. a ModuleInfo's parent
        is a PackageInfo, a ClassInfo's parent is a ModuleInfo etc.

        Returns
        -------
        Optional[BaseInfo]
            The parent node in the info tree hierarchy.
        """
        pass

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
        Get the attribute value from this object or one further up the info tree.

        Ascend the info tree hierarchy searching for the attribute and return
        the first value found for it.

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
        Get a list of attribute values from this object and others in the info tree.

        Ascend the info tree hierarchy searching for the attribute and return
        a list of all the values found for it.

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
