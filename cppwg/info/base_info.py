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
    custom_generator : str, optional
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
    pointer_call_policy : str, optional
        The default pointer call policy.
    prefix_code : List[str]
        Any wrapper code that precedes the feature.
    prefix_text : str, optional
        Text to add at the top of all wrappers.
    reference_call_policy : str, optional
        The default reference call policy.
    return_type_excludes : List[str]
        List of exclude patterns for return types.
    smart_ptr_type : str, optional
        Handle classes with this smart pointer type.
    source_includes : List[str]
        A list of source files to be included with the feature.
    template_substitutions : Dict[str, List[Any]]
        A list of template substitution sequences.
    """

    def __init__(self, name):
        self.name: str = name

        # Paths
        self.source_includes: List[str] = []
        self.source_root: str = None

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
        self.pointer_call_policy: Optional[str] = None
        self.reference_call_policy: Optional[str] = None
        self.smart_ptr_type: Optional[str] = None

        # Custom Code
        self.extra_code: List[str] = []
        self.prefix_code: List[str] = []
        self.custom_generator: Optional[str] = None

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
        # string if needed. For example, a custom generator might be specified
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

        # Replace the `info.custom_generator` string with a new object created
        # from the provided custom generator class
        self.custom_generator = CustomGeneratorClass()

    def hierarchy_attribute(self, attribute_name: str) -> Any:
        """
        Get the attribute value from this object or one of its parents.

        For the supplied attribute, iterate through parent objects until a non-None
        value is found. If the top level parent (i.e. package) attribute is
        None, return None.

        Parameters
        ----------
        attribute_name : str
            The attribute name to search for.

        Returns
        -------
        Any
            The attribute value.
        """
        if hasattr(self, attribute_name) and getattr(self, attribute_name) is not None:
            return getattr(self, attribute_name)

        if hasattr(self, "parent") and self.parent is not None:
            return self.parent.hierarchy_attribute(attribute_name)

        return None

    def hierarchy_attribute_gather(self, attribute_name: str) -> List[Any]:
        """
        Get a list of attribute values from this object and its parents.

        For the supplied attribute, iterate through parent objects gathering list entries.

        Parameters
        ----------
        attribute_name : str
            The attribute name to search for.

        Returns
        -------
        List[Any]
            The list of attribute values.
        """
        att_list: List[Any] = []

        if hasattr(self, attribute_name) and getattr(self, attribute_name) is not None:
            att_list.extend(getattr(self, attribute_name))

        if hasattr(self, "parent") and self.parent is not None:
            att_list.extend(self.parent.hierarchy_attribute_gather(attribute_name))

        return att_list
