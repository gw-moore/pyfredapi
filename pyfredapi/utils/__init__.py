"""Utilities module."""

from frozendict import frozendict
from pydantic import BaseModel

from ._convert_to_pandas import _convert_to_pandas


def _convert_pydantic_model_to_frozen_dict(model: BaseModel) -> frozendict:
    return frozendict(model.model_dump(exclude_none=True))
