"""Module for defining common type hints used across modules."""

from typing import Any, Dict, Literal, Union

import pandas as pd

from pyfredapi.utils.enums import ReturnFormat

ApiKeyType = Union[str, None]
JsonType = Dict[str, Any]
JsonOrPdType = Union[Dict, pd.DataFrame]
ReturnFmtType = Union[Literal["json", "pandas"], ReturnFormat]
KwargsType = Dict[str, Union[int, str, None]]
