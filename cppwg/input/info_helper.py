"""Helper utilities for info structures."""

import logging
import os
from typing import Any, Dict, List

from cppwg.input.base_info import BaseInfo
from cppwg.input.class_info import CppClassInfo
from cppwg.input.module_info import ModuleInfo
from cppwg.utils import utils


class CppInfoHelper:
    """
    Adds information extracted from C++ source code to info objects.

    Helper class that attempts to automatically fill in extra feature
    information based on simple analysis of the source tree.

    __________
    Attributes
    __________
    module_info : ModuleInfo
        The module info object that this helper is working with.
    class_dict : dict
        A dictionary of class info objects keyed by class name.
    """

    def __init__(self, module_info: ModuleInfo):

        self.module_info: ModuleInfo = module_info

        # For convenience, collect class info in a dict keyed by name
        self.class_dict: Dict[str, CppClassInfo] = {
            class_info.name: class_info
            for class_info in module_info.class_info_collection
        }

    def extract_templates_from_source(self, feature_info: BaseInfo) -> None:
        """
        Get template args from the source file associated with an info object.

        __________
        Parameters
        __________
        feature_info : BaseInfo
            The feature info object to expand.
        """
        logger = logging.getLogger()

        if not isinstance(feature_info, CppClassInfo):
            logger.error(f"Unsupported feature type: {type(feature_info)}")
            raise TypeError()

        # Skip if there are pre-defined template args
        if feature_info.template_arg_lists:
            return

        # Skip if there is no source file
        source_path = feature_info.source_file_full_path
        if not source_path:
            return

        if not os.path.isfile(source_path):
            logger.error(f"Could not find source file: {source_path}")
            raise FileNotFoundError()

        # Get list of template substitutions from this feature and its parents
        # e.g. {"signature":"<unsigned DIM_A,unsigned DIM_B>","replacement":[[2,2], [3,3]]}
        template_substitutions: List[Dict[str, Any]] = (
            feature_info.hierarchy_attribute_gather("template_substitutions")
        )

        # Skip if there are no template substitutions
        if len(template_substitutions) == 0:
            return

        source = utils.read_source_file(
            source_path,
            strip_comments=True,
            strip_preprocessor=True,
            strip_whitespace=True,
        )

        # Search for template signatures in the source file
        for template_substitution in template_substitutions:
            # Signature e.g. <unsigned DIM_A,unsigned DIM_B>
            signature = template_substitution["signature"].strip()

            class_list = utils.find_classes_in_source(
                source,
                class_name=feature_info.name,
                template_signature=signature,
            )

            if class_list:
                # Replacement e.g. [[2,2], [3,3]]
                replacement = template_substitution["replacement"]

                feature_info.template_arg_lists = replacement
                feature_info.template_signature = signature

                # Extract ["DIM_A", "DIM_B"] from "<unsigned DIM_A,unsigned DIM_B=DIM_A>"
                template_params = []
                for tp in signature.split(","):
                    template_params.append(
                        tp.strip()
                        .replace("<", "")
                        .replace(">", "")
                        .split(" ")[1]
                        .split("=")[0]
                        .strip()
                    )
                feature_info.template_params = template_params
                break
