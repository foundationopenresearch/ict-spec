"""IO objects for ICT."""

import enum
import re
from typing import Optional, Union

from pydantic import BaseModel, Field

# dict used to map an ICT I/O
# type to a CWL I/O type
CWL_IO_DICT: dict[str, str] = {
    "string": "string",
    "number": "double",
    "array": "string",
    "boolean": "boolean",
    # TODO: File vs Directory?
}


class TypesEnum(str, enum.Enum):
    """Types enum for ICT IO."""

    STRING = "string"
    NUMBER = "number"
    ARRAY = "array"
    BOOLEAN = "boolean"
    PATH = "path"


# def _get_cwl_type(io_name: str, io_type: str) -> str:
def _get_cwl_type(io_type: str) -> str:
    """Return the CWL type from the ICT IO type."""
    if io_type == "path":
        # NOTE: for now, default to directory
        # this needs to be addressed
        # path could be File or Directory
        return "Directory"
        # if bool(re.search("dir", io_name, re.I)):
        #     return "Directory"
        # return "File"
    return CWL_IO_DICT[io_type]


class IO(BaseModel):
    """IO BaseModel."""

    name: str = Field(
        description="Unique input or output name for this plugin, case-sensitive match to corresponding variable expected by tool.",
        examples=["thresholdtype"],
    )
    io_type: TypesEnum = Field(
        ...,
        alias="type",
        description="Defines the parameter passed to the ICT tool based on broad categories of basic types.",
        examples=["string"],
    )
    description: Optional[str] = Field(
        None,
        description="Short text description of expected value for field.",
        examples=["Algorithm type for thresholding"],
    )
    required: bool = Field(
        description="Boolean (true/false) value indicating whether this "
        + "field needs an associated value.",
        examples=["true"],
    )
    io_format: Union[list[str], dict] = Field(
        ...,
        alias="format",
        description="Defines the actual value(s) that the input/output parameter"
        + "represents using an ontology schema.",
    )  # TODO ontology

    @property
    def _is_optional(self):
        """Return '?' if optional."""
        return "" if self.required else "?"

    def _input_to_cwl(self):
        """Convert inputs to CWL."""
        cwl_dict_ = {
            "inputBinding": {"prefix": f"--{self.name}"},
            # "type": f"{_get_cwl_type(self.name, self.io_type)}{self._is_optional}",
            "type": f"{_get_cwl_type(self.io_type)}{self._is_optional}",
        }
        return cwl_dict_

    def _output_to_cwl(self):
        """Convert outputs to CWL."""
        if self.name == "outDir":
            cwl_dict_ = {
                "outputBinding": {"glob": "$(inputs.outDir.basename)"},
                "type": "Directory",
            }
            return cwl_dict_
        return NotImplementedError
