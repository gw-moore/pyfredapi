"""Module for defining common type hints used across modules."""

from __future__ import annotations


from typing import Any, Dict, Literal, Union
from pyfredapi.utils.enums import ReturnFormat
from pandas import DataFrame as PdDataFrame

try:
    from polars import DataFrame as PlDataFrame
except ImportError:
    PlDataFrame: "pl.DataFrame" = any 


ApiKeyType = Union[str, None]
JsonType = Dict[str, Any]
ReturnTypes = Union[Dict, PdDataFrame, PlDataFrame]
ReturnFormats = Union[Literal["json", "pandas", "polars"], ReturnFormat]
KwargsType = Dict[str, Union[int, str, None]]
