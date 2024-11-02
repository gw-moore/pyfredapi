"""Utilities module."""

from pydantic import BaseModel


def _convert_pydantic_model_to_frozenset(model: BaseModel) -> frozenset:
    return frozenset(model.model_dump(exclude_none=True).items())


def _convert_pydantic_model_to_dict(model: BaseModel) -> dict:
    return model.model_dump(exclude_none=True)
