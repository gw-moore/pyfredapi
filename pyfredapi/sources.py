"""The sources module provides functions to request data from the `FRED API Sources endpoints. <https://fred.stlouisfed.org/docs/api/fred/#Sources>`_.

The FRED database contains many sources of data. The sources module provides functions to query the FRED database for information about the available sources.
"""

from typing import Literal, Optional

from frozendict import frozendict
from pydantic import BaseModel, Extra, PositiveInt

from ._base import _get_request
from .utils._common_type_hints import ApiKeyType, JsonType, KwargsType


class SourceApiParameters(BaseModel):
    """Represents the parameters accepted by the FRED Sources endpoints."""

    source_id: Optional[PositiveInt] = None
    realtime_start: Optional[str] = None
    realtime_end: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[PositiveInt] = None
    order_by: Optional[
        Literal["source_id", "name", "realtime_start", "realtime_end"]
    ] = None
    sort_order: Optional[Literal["asc", "desc"]] = None

    class Config:
        extra = Extra.allow


def get_sources(api_key: ApiKeyType = None, **kwargs: KwargsType) -> JsonType:
    """Get all sources of economic data. https://fred.stlouisfed.org/docs/api/fred/sources.html.

    Parameters
    ----------
    api_key : str | None
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``sources/`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    Dictionary representing the Json response
    """
    params = SourceApiParameters(**kwargs)
    return _get_request(
        endpoint="sources",
        api_key=api_key,
        params=frozendict(params.dict(exclude_none=True)),
    )


def get_source(
    source_id: int, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get a source of economic data. https://fred.stlouisfed.org/docs/api/fred/source.html.

    Parameters
    ----------
    source_id : int
        Source id of interest.
    api_key : str | None
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``source/`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    Dictionary representing the Json response
    """
    params = SourceApiParameters(source_id=source_id, **kwargs)
    return _get_request(
        endpoint="source",
        api_key=api_key,
        params=frozendict(params.dict(exclude_none=True)),
    )


def get_source_release(
    source_id: int, api_key: ApiKeyType = None, **kwargs: KwargsType
):
    """Get the releases for a source. https://fred.stlouisfed.org/docs/api/fred/source.html.

    Parameters
    ----------
    source_id : int
        Source id of interest.
    api_key : str | None
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``source/releases`` endpoint.
        Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    Dictionary representing the Json response
    """
    params = SourceApiParameters(source_id=source_id, **kwargs)
    return _get_request(
        endpoint="source/releases",
        api_key=api_key,
        params=frozendict(params.dict(exclude_none=True)),
    )
