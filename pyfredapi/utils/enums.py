"""The enum module contains enum definitions."""

from enum import Enum


class ReturnFormat(str, Enum):
    """Defines how to format the data returned from the FRED endpoint."""

    pandas = "pandas"
    polars = "polars"
    json = "json"
