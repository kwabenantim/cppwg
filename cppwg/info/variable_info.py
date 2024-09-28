"""Variable information structure."""

from typing import Any, Dict, Optional

from cppwg.info.cpp_entity_info import CppEntityInfo


class CppVariableInfo(CppEntityInfo):
    """An information structure for individual variables to be wrapped."""

    def __init__(self, name: str, variable_config: Optional[Dict[str, Any]] = None):

        super().__init__(name, variable_config)
