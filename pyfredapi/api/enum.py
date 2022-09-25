from enum import Enum


class ReturnFormat(str, Enum):
    """Defines how to format the data returned from the FRED endpoint."""

    pandas = "pandas"
    json = "json"
