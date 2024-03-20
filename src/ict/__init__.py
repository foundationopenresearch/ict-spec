"""ICT Python API."""

from pathlib import Path

from ict.model import ICT
from ict.validate import validate

with Path(__file__).with_name("VERSION").open(
    "r",
    encoding="utf-8",
) as version_file:
    VERSION = version_file.read().strip()

__all__ = ["ICT", "validate", "VERSION"]
__version__ = VERSION
