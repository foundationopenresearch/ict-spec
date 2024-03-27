"""ICT model."""

from pathlib import Path
from typing import Optional, TypeVar, Union

import yaml
from pydantic import Field, model_validator
from typing_extensions import Annotated

from ict.hardware import HardwareRequirements
from ict.io import IO
from ict.metadata import Metadata
from ict.tools import clt_dict, ict_dict
from ict.ui import (
    UICheckbox,
    UIColor,
    UIDatetime,
    UIFile,
    UIMultiselect,
    UINumber,
    UIPath,
    UISelect,
    UIText,
)

StrPath = TypeVar("StrPath", str, Path)
UIItem = Annotated[
    Union[
        UIText,
        UINumber,
        UICheckbox,
        UISelect,
        UIMultiselect,
        UIColor,
        UIDatetime,
        UIPath,
        UIFile,
    ],
    Field(discriminator="ui_type"),
]


class ICT(Metadata):
    """ICT object."""

    inputs: list[IO]
    outputs: list[IO]
    ui: list[UIItem]
    hardware: Optional[HardwareRequirements] = None

    @model_validator(mode="after")
    def validate_ui(self) -> "ICT":
        """Validate that the ui matches the inputs and outputs."""
        io_dict = {"inputs": [], "outputs": []}  # type: ignore
        ui_keys = [ui.key.root.split(".") for ui in self.ui]
        for ui_ in ui_keys:
            io_dict[ui_[0]].append(ui_[1])
        input_names = [io.name for io in self.inputs]
        output_names = [io.name for io in self.outputs]
        inp_bool = [x in input_names for x in io_dict["inputs"]]
        out_bool = [x in output_names for x in io_dict["outputs"]]

        if not all(inp_bool):
            raise ValueError(
                f"The ui keys must match the inputs and outputs keys. Unmatched: inputs.{set(io_dict['inputs'])-set(input_names)}"
            )
        if not all(out_bool):
            raise ValueError(
                f"The ui keys must match the inputs and outputs keys. Unmatched: outputs.{set(io_dict['outputs'])-set(output_names)}"
            )
        return self

    @property
    def clt(self) -> dict:
        """CWL CommandLineTool from an ICT object."""
        return clt_dict(self)
    
    @property
    def ict(self) -> dict:
        """ICT yaml from an ICT object."""
        return ict_dict(self)

    def save_clt(self, cwl_path: StrPath) -> Path:
        """Save the ICT as CommandLineTool to a file."""
        assert (
            str(cwl_path).rsplit(".", maxsplit=1)[-1] == "cwl"
        ), "Path must end in .cwl"
        with Path(cwl_path).open("w", encoding="utf-8") as file:
            yaml.dump(self.clt, file)
        return Path(cwl_path)

    def save_ict(self, ict_path: StrPath) -> Path:
        """Save the ICT as YAML to a file. Useful for when converting CLT->ICT"""
        assert (
            str(ict_path).rsplit(".", maxsplit=1)[-1] in ["yml", "yaml"]
        ), "Path must end in .yml or .yaml"
        with Path(ict_path).open("w", encoding="utf-8") as file:
            yaml.dump(self.ict, file)
        return Path(ict_path)
