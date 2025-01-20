"""Module for defining common type hints used across modules."""

from __future__ import annotations

from typing import Any, Dict, Literal, Union

from pandas import DataFrame as PdDataFrame

from pyfredapi.utils.enums import ReturnFormat

try:
    from polars import DataFrame as PlDataFrame
except ImportError:
    PlDataFrame: Any  # type: ignore


ApiKeyType = Union[str, None]
JsonType = Dict[str, Any]
ReturnTypes = Union[Dict, PdDataFrame, PlDataFrame]
ReturnFormats = Union[Literal["json", "pandas", "polars"], ReturnFormat]
KwargsType = Dict[str, Union[int, str, None]]
