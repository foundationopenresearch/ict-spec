# pylint: disable=no-member, no-name-in-module, import-error
"""ICT model."""

import logging
from functools import singledispatchmethod
from pathlib import Path
from typing import Optional, TypeVar

import yaml  # type: ignore
from polus.plugins import Plugin  # type: ignore
from polus.plugins._plugins.classes import _load_plugin  # type: ignore
from pydantic import model_validator

from ict.hardware import HardwareRequirements
from ict.io import IO
from ict.metadata import Metadata
from ict.tools import clt_dict
from ict.ui import UIItem
from ict.wipp_utils import (
    convert_wipp_hardware_to_ict,
    convert_wipp_io_to_ict,
    convert_wipp_metadata_to_ict,
    convert_wipp_ui_to_ict,
)

StrPath = TypeVar("StrPath", str, Path)

logger = logging.getLogger("ict")


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

    def to_clt(self, network_access: bool = False) -> dict:
        """Convert ICT to CWL CommandLineTool.


        Args:
            network_access: bool
                Default is `False`. If set to `True`, the
                requirements of the CLT will include
                `networkAccess`: `True`.

        Returns: `dict` representation of the CLT.
        """
        return clt_dict(self, network_access)

    @property
    def clt(self) -> dict:
        """Convenience property of object as CommandLineTool with no network access."""
        return clt_dict(self, network_access=False)

    def save_clt(self, cwl_path: StrPath, network_access: bool = False) -> Path:
        """Save the ICT as CommandLineTool to a file."""
        assert (
            str(cwl_path).rsplit(".", maxsplit=1)[-1] == "cwl"
        ), "Path must end in .cwl"
        with Path(cwl_path).open("w", encoding="utf-8") as file:
            yaml.dump(self.to_clt(network_access), file)
        return Path(cwl_path)

    def save_yaml(self, yaml_path: StrPath) -> Path:
        """Save the ICT as yaml to a file."""
        assert str(yaml_path).rsplit(".", maxsplit=1)[-1] in [
            "yaml",
            "yml",
        ], "Path must end in .yaml or .yml"
        with Path(yaml_path).open("w", encoding="utf-8") as file:
            yaml.dump(
                self.model_dump(mode="json", exclude_none=True, by_alias=True), file
            )
        return Path(yaml_path)

    def save_yml(self, yml_path: StrPath) -> Path:
        """Save the ICT as yaml to a file.

        Alias for `save_yaml`.
        """
        return self.save_yaml(yml_path)

    @singledispatchmethod
    @classmethod
    def from_wipp(cls, wipp: Plugin, **kwargs) -> "ICT":
        """Convert WIPP Plugin to ICT."""
        metadata = convert_wipp_metadata_to_ict(wipp, **kwargs)
        if wipp.resourceRequirements is not None:
            hardware = convert_wipp_hardware_to_ict(wipp.resourceRequirements)
        else:
            hardware = None
        inputs = [convert_wipp_io_to_ict(inp) for inp in wipp.inputs]
        outputs = [convert_wipp_io_to_ict(out) for out in wipp.outputs]
        ui = [convert_wipp_ui_to_ict(ui_, wipp.inputs) for ui_ in wipp.ui]
        return cls(
            **metadata.model_dump(),
            inputs=inputs,
            outputs=outputs,
            ui=ui,
            hardware=hardware,
        )

    @from_wipp.register(Path)  # type: ignore
    @classmethod
    def _(cls, wipp, **kwargs) -> "ICT":
        """Convert WIPP Plugin to ICT."""
        wipp_ = _load_plugin(wipp)
        return cls.from_wipp(wipp_, **kwargs)

    @from_wipp.register(str)  # type: ignore
    @classmethod
    def _(cls, wipp, **kwargs) -> "ICT":
        """Convert WIPP Plugin to ICT."""
        wipp_ = _load_plugin(wipp)
        return cls.from_wipp(wipp_, **kwargs)
