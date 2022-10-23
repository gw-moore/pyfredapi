"""This module provides functions to request data from the `FRED API Categories endpoints <https://fred.stlouisfed.org/docs/api/fred/#Categories>`_."""


from typing import Dict, Literal, Optional

from pydantic import BaseModel, Extra, PositiveInt

from ._base import _get_request
from .series import SeriesInfo
from .utils._common_type_hints import (
    ApiKeyType,
    JsonOrPdType,
    JsonType,
    KwargsType,
    ReturnFmtType,
)
from .utils._convert_to_pandas import _convert_to_pandas
from .utils.enums import ReturnFormat


class CategoryApiParameters(BaseModel):
    """Represents the parameters accepted by the FRED Category endpoints."""

    category_id: Optional[int] = None
    realtime_start: Optional[str] = None
    realtime_end: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[PositiveInt] = None
    order_by: Optional[
        Literal[
            "series_id",
            "title",
            "units",
            "frequency",
            "seasonal_adjustment",
            "realtime_start",
            "realtime_end",
            "last_updated",
            "observation_start",
            "observation_end",
            "popularity",
            "group_popularity",
        ]
    ] = None
    sort_order: Optional[Literal["acs", "desc"]] = None
    filter_variable: Optional[
        Literal["frequency", "units", "seasonal_adjustment"]
    ] = None
    filter_value: Optional[str] = None
    tag_names: Optional[str] = None
    exclude_tag_names: Optional[str] = None

    class Config:
        extra = Extra.allow


def get_category(
    category_id: Optional[int] = None, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get category by ID. https://fred.stlouisfed.org/docs/api/fred/category.html.

    Parameters
    ----------
    category_id : str | None
        Category id of interest.
    api_key : str | None
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs: Dict[str, str], optional
        Additional parameters to FRED API ``category/`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict
        Dictionary representing the json response.
    """
    params = CategoryApiParameters(category_id=category_id, **kwargs)
    return _get_request(
        api_key=api_key,
        endpoint="category",
        params=params.dict(exclude_none=True),
    )


def get_category_children(
    category_id: Optional[int] = None, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get category children by category ID. https://fred.stlouisfed.org/docs/api/fred/category_children.html.

    Parameters
    ----------
    category_id : str | None
        Category id of interest.
    api_key : str | None
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``category/children`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict
        Dictionary representing the json response.
    """
    params = CategoryApiParameters(category_id=category_id, **kwargs)
    return _get_request(
        endpoint="category/children",
        api_key=api_key,
        params=params.dict(exclude_none=True),
    )


def get_category_related(
    category_id: int, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get related categories by category ID. https://fred.stlouisfed.org/docs/api/fred/category_related.html.

    Parameters
    ----------
    category_id : str
        Category id of interest.
    api_key : str | None
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``category/children`` endpoint. Refer to the FRED documentation for a list of all possible parameters.


    Returns
    -------
    dict
        Dictionary representing the json response.
    """
    params = CategoryApiParameters(category_id=category_id, **kwargs)
    return _get_request(
        api_key=api_key,
        endpoint="category/related",
        params=params.dict(exclude_none=True),
    )


def get_category_series(
    category_id: int,
    api_key: ApiKeyType = None,
    **kwargs: KwargsType,
) -> Dict[str, SeriesInfo]:
    """Get the series info for each series in a category by category ID. https://fred.stlouisfed.org/docs/api/fred/category_series.html.

    Parameters
    ----------
    category_id : str
        Category id of interest.
    api_key : str | None
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``category/children`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict
        A dictionary where the keys are series ids and the values for SeriesInfo objects.
    """
    params = CategoryApiParameters(category_id=category_id, **kwargs)
    response = _get_request(
        api_key=api_key,
        endpoint="category/series",
        params=params.dict(exclude_none=True),
    )

    return {series["id"]: SeriesInfo(**series) for series in response["seriess"]}


def get_category_tags(
    category_id: Optional[int] = None,
    api_key: ApiKeyType = None,
    return_format: ReturnFmtType = "json",
    **kwargs: KwargsType,
) -> JsonOrPdType:
    """Get the FRED tags for a category by category ID. https://fred.stlouisfed.org/docs/api/fred/category_tags.html.

    Parameters
    ----------
    category_id : str | None
        Category id of interest.
    api_key : str | None
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    return_format : str | ReturnFormat
        Define how to return the response. Must be either 'json' or 'pandas'.
    **kwargs : dict, optional
        Additional parameters to FRED API ``category/children`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict | pd.DataFrame
        Either a dictionary representing the json response or a pandas dataframe.
    """
    return_format = ReturnFormat(return_format)

    params = CategoryApiParameters(category_id=category_id, **kwargs)
    response = _get_request(
        api_key=api_key,
        endpoint="category/tags",
        params=params.dict(exclude_none=True),
    )

    if return_format == ReturnFormat.pandas:
        return _convert_to_pandas(response["tags"])
    return response


def get_category_related_tags(
    category_id: Optional[int] = None,
    api_key: ApiKeyType = None,
    return_format: ReturnFmtType = "json",
    **kwargs: KwargsType,
) -> JsonOrPdType:
    """Get the related FRED tags for a category by category ID. https://fred.stlouisfed.org/docs/api/fred/category_related_tags.html.

    Parameters
    ----------
    category_id : str | None
        Category id of interest.
    api_key : str | None
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    return_format : str | ReturnFormat
        Define how to return the response. Must be either 'json' or 'pandas'.
    **kwargs : dict, optional
        Additional parameters to FRED API ``category/children`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict | pd.DataFrame
        Either a dictionary representing the json response or a pandas dataframe.
    """
    return_format = ReturnFormat(return_format)

    params = CategoryApiParameters(category_id=category_id, **kwargs)
    response = _get_request(
        api_key=api_key,
        endpoint="category/related_tags",
        params=params.dict(exclude_none=True),
    )

    if return_format == ReturnFormat.pandas:
        return _convert_to_pandas(response["tags"])
    return response
