"""The `series` module provides functions to request data from the [FRED API Sources endpoints](https://fred.stlouisfed.org/docs/api/fred/#Series)."""

import webbrowser
from typing import List, Literal, Optional

import pandas as pd
from pydantic import BaseModel, ConfigDict, PositiveInt

from ._base import _get_request
from .utils import _convert_pydantic_model_to_dict, _convert_pydantic_model_to_frozenset
from .utils._common_type_hints import (
    ApiKeyType,
    JsonOrPdType,
    JsonType,
    KwargsType,
    ReturnFmtType,
)
from .utils._convert_to_pandas import _convert_to_pandas
from .utils.enums import ReturnFormat

_earliest_realtime_start: str = "1776-07-04"
_latest_realtime_end: str = "9999-12-31"


class SeriesApiParameters(BaseModel):
    """Represents the parameters accepted by the FRED Series endpoints."""

    model_config = ConfigDict(extra="allow")

    series_id: Optional[str] = None
    realtime_start: Optional[str] = None
    realtime_end: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[PositiveInt] = None
    sort_order: Optional[Literal["acs", "desc"]] = None
    observation_start: Optional[str] = None
    observation_end: Optional[str] = None
    units: Optional[
        Literal[
            "lin",
            "chg",
            "ch1",
            "pch",
            "pc1",
            "pca",
            "cch",
            "cca",
            "log",
        ]
    ] = None
    frequency: Optional[
        Literal[
            "d",
            "w",
            "bw",
            "m",
            "q",
            "sa",
            "a",
            "wef",
            "weth",
            "wew",
            "wetu",
            "wem",
            "wesu",
            "wesa",
            "bwew",
            "bwem",
        ]
    ] = None
    aggregation_method: Optional[Literal["avg", "sum", "eop"]] = None
    output_type: Optional[Literal["1", "2", "3", "4", 1, 2, 3, 4]] = None
    vintage_dates: Optional[str] = None


class SeriesSearchParameters(BaseModel):
    """Represents the parameters accepted by the FRED Series Search endpoints."""

    model_config = ConfigDict(extra="allow")

    search_text: Optional[str] = None
    search_type: Optional[Literal["full_text", "series_id"]] = None
    realtime_start: Optional[str] = None
    realtime_end: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[PositiveInt] = None
    order_by: Optional[
        Literal[
            "search_rank",
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
    sort_order: Optional[Literal["asc", "desc"]] = None
    filter_variable: Optional[Literal["frequency", "units", "seasonal_adjustment"]] = (
        None
    )
    filter_value: Optional[str] = None
    tag_names: Optional[str] = None
    exclude_tag_names: Optional[str] = None


class SeriesInfo(BaseModel):
    """Represents metadata about an economics data series. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/series.html)."""

    model_config = ConfigDict(extra="allow")

    id: str
    realtime_start: str
    realtime_end: str
    title: str
    observation_start: str
    observation_end: str
    frequency: str
    frequency_short: str
    units: str
    units_short: str
    seasonal_adjustment: str
    seasonal_adjustment_short: str
    last_updated: str
    popularity: int
    notes: Optional[str] = None
    _base_url: str = "https://fred.stlouisfed.org/series"

    def open_url(self):
        """Open the FRED webpage for the given series."""
        webbrowser.open(f"{self._base_url}/{self.id}", new=2)


def get_series_info(
    series_id: str, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> SeriesInfo:
    """Get an economic data series information by ID. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/series.html).

    Parameters
    ----------
    series_id : str
        Series id of interest.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``series/`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    SeriesInfo
        An instance of SeriesInfo.

    """
    params = _convert_pydantic_model_to_frozenset(
        SeriesApiParameters(series_id=series_id, **kwargs)
    )
    response = _get_request(
        api_key=api_key,
        endpoint="series",
        params=params,
    )
    return SeriesInfo(**response["seriess"][0])


def get_series_categories(
    series_id: str, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get the categories for an economic data series by ID. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/series_categories.html).

    Parameters
    ----------
    series_id : str
        Series id of interest.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``series/categories`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict
        Dictionary representing the json response.

    """
    params = _convert_pydantic_model_to_frozenset(
        SeriesApiParameters(series_id=series_id, **kwargs)
    )
    return _get_request(
        api_key=api_key,
        endpoint="series/categories",
        params=params,
    )


def get_series(
    series_id: str,
    api_key: ApiKeyType = None,
    return_format: ReturnFmtType = "pandas",
    **kwargs: KwargsType,
) -> JsonOrPdType:
    """Get the observations or data values for an economic data series by ID. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/series_observations.html).

    Parameters
    ----------
    series_id : str
        Series id of interest.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    return_format : Literal[json, pandas] | ReturnFormat, optional
        Define how to return the response. Must be either 'json' or 'pandas'. Defaults to 'pandas'.
    **kwargs : dict, optional
        Additional parameters to FRED API ``series/observations`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict | pd.DataFrame
        Either a dictionary representing the json response or a pandas dataframe.

    """
    return_format = ReturnFormat(return_format)

    params = _convert_pydantic_model_to_frozenset(
        SeriesApiParameters(series_id=series_id, **kwargs)
    )
    response = _get_request(
        api_key=api_key,
        endpoint="series/observations",
        params=params,
    )

    if return_format == ReturnFormat.pandas:
        pdf = _convert_to_pandas(response["observations"])
        return pdf
    return response["observations"]


def get_series_releases(
    series_id: str, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get the FRED release for an economic data series by ID. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/series_release.html).

    Parameters
    ----------
    series_id : str
        Series id of interest.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``series/releases`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict
        Dictionary representing the json response.

    """
    params = _convert_pydantic_model_to_frozenset(
        SeriesApiParameters(series_id=series_id, **kwargs)
    )
    return _get_request(
        endpoint="series/release",
        api_key=api_key,
        params=params,
    )


def get_series_tags(
    series_id: str, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get the FRED tags for an economic data series by ID. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/series_tags.html).

    Parameters
    ----------
    series_id : str
        Series id of interest.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``series/tags`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict
        Dictionary representing the json response.

    """
    params = _convert_pydantic_model_to_frozenset(
        SeriesApiParameters(series_id=series_id, **kwargs)
    )
    return _get_request(
        endpoint="series/tags",
        api_key=api_key,
        params=params,
    )


def get_series_updates(
    series_id: str, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get the FRED updates for an economic data series by ID. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/series_updates.html).

    Parameters
    ----------
    series_id : str
        Series id of interest.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``series/updates`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict
        Dictionary representing the json response.

    """
    params = _convert_pydantic_model_to_frozenset(
        SeriesApiParameters(series_id=series_id, **kwargs)
    )
    return _get_request(
        endpoint="series/updates",
        api_key=api_key,
        params=params,
    )


def get_series_vintagedates(
    series_id: str, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> List[str]:
    """Get the dates in history when a series' data values were revised or new data values were released.

    Vintage dates are the release dates for a series excluding release dates when the data did not change. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/series_vintagesdates.html).

    Parameters
    ----------
    series_id : str
        Series id of interest.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``series/vintagedates`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    List[str]
        List of strings representing the the available vintage dates

    """
    params = _convert_pydantic_model_to_frozenset(
        SeriesApiParameters(series_id=series_id, **kwargs)
    )
    response = _get_request(
        endpoint="series/vintagedates",
        api_key=api_key,
        params=params,
    )
    return response["vintage_dates"]


def get_series_all_releases(
    series_id: str,
    api_key: ApiKeyType = None,
    return_format: ReturnFmtType = "pandas",
    **kwargs: KwargsType,
) -> JsonOrPdType:
    """Get the observations or data values for all releases an economic data series by ID.

    Parameters
    ----------
    series_id : str
        Series id of interest.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    return_format : Literal["json", "pandas"] | ReturnFormat, optional
        In what format to return the response. Must be either 'json' or 'pandas'. Defaults to 'pandas'.
    **kwargs : dict, optional
        Additional parameters to FRED API ``series/observation`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict | pd.DataFrame
        Either a dictionary representing the json response or a pandas dataframe.

    """
    return_format = ReturnFormat(return_format)

    # sanitize the kwargs to ensure the user did not
    # in inadvertently supply values for realtime_start & realtime_end
    _ = kwargs.pop("realtime_start", None)
    _ = kwargs.pop("realtime_end", None)

    params = _convert_pydantic_model_to_dict(
        SeriesApiParameters(
            realtime_start=_earliest_realtime_start,
            realtime_end=_latest_realtime_end,
            **kwargs,
        )
    )

    return get_series(
        series_id=series_id,
        api_key=api_key,
        return_format=return_format,
        **params,
    )


def get_series_initial_release(
    series_id: str,
    api_key: ApiKeyType = None,
    return_format: ReturnFmtType = "pandas",
    **kwargs: KwargsType,
) -> JsonOrPdType:
    """Get the observations or data values for the initial release of an economic data series.

    Includes only the the initial release of the series and excludes all revisions.

    Parameters
    ----------
    series_id : str
        Series id of interest.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    return_format : Literal["json", "pandas"] | ReturnFormat, optional
        In what format to return the response. Must be either 'json' or 'pandas'. Defaults to 'pandas'.
    **kwargs : dict, optional
        Additional parameters to FRED API ``series/observation`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict | pd.DataFrame
        Either a dictionary representing the json response or a pandas dataframe.

    """
    return_format = ReturnFormat(return_format)

    # sanitize the kwargs to ensure the user did not
    # in inadvertently supply values for realtime_start & output_type
    _ = kwargs.pop("realtime_start", None)
    _ = kwargs.pop("output_type", None)

    params = _convert_pydantic_model_to_dict(
        SeriesApiParameters(
            realtime_start=_earliest_realtime_start, output_type=4, **kwargs
        )
    )

    return get_series(
        series_id=series_id,
        api_key=api_key,
        return_format=return_format,
        **params,
    )


def get_series_asof_date(
    series_id: str,
    date: str,
    api_key: ApiKeyType = None,
    return_format: ReturnFmtType = "pandas",
    **kwargs: KwargsType,
) -> JsonOrPdType:
    """Get the observations or data values for an economic data series made on or before a specific date.

    Retrieves the latest data known for the series as of the date provided. This includes any revisions to
    the data series made before or on the date, but excludes any revisions made after the date.

    Parameters
    ----------
    series_id : str
        Series id of interest.
    date : str
        Include only data revisions made on or before this date.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    return_format : Literal["json", "pandas"] | ReturnFormat, optional
        In what format to return the response. Must be either 'json' or 'pandas'. Defaults to 'pandas'.
    **kwargs : dict, optional
        Additional parameters to FRED API ``series/observation`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict | pd.DataFrame
        Either a dictionary representing the json response or a pandas dataframe.

    """
    return_format = ReturnFormat(return_format)

    # sanitize the kwargs to ensure the user did not
    # in inadvertently supply values for realtime_start & realtime_end
    _ = kwargs.pop("realtime_start", None)
    _ = kwargs.pop("realtime_end", None)

    params = _convert_pydantic_model_to_dict(
        SeriesApiParameters(
            realtime_start=_earliest_realtime_start, realtime_end=date, **kwargs
        )
    )

    return get_series(
        series_id=series_id,
        api_key=api_key,
        return_format=return_format,
        **params,
    )


def search_series(
    search_text: str,
    api_key: ApiKeyType = None,
    search_type: Literal["full_text", "series_id"] = "full_text",
    return_format: ReturnFmtType = "pandas",
    **kwargs: KwargsType,
) -> JsonOrPdType:
    """Get economic data series that match search text. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/series_search.html).

    Parameters
    ----------
    search_text : str
        The text to match against.
    api_key : str | None, optional, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    search_type : Literal["full_text", "series_id"]
        Defines which type of search to preform. One of the following strings: 'full_text', 'series_id'.
        [Parameter docs](https://fred.stlouisfed.org/docs/api/fred/series_search.html#search_type).
    return_format : : Literal["json", "pandas"] | ReturnFormat, optional
        In what format to return the response. Must be either 'json' or 'pandas'. Defaults to 'pandas'.
    **kwargs : dict, optional
        Additional parameters to FRED API ``series/observation`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict | pd.DataFrame
        Either a pandas dataframe or json. Defaults to pandas dataframe.

    """
    return_format = ReturnFormat(return_format)

    params = _convert_pydantic_model_to_frozenset(
        SeriesSearchParameters(
            search_text=search_text,
            search_type=search_type,
            **kwargs,
        )
    )

    response = _get_request(
        endpoint="series/search",
        api_key=api_key,
        params=params,
    )

    if return_format == ReturnFormat.pandas:
        return pd.DataFrame.from_dict(response["seriess"])
    return response


def search_series_tags(
    search_text: str,
    api_key: ApiKeyType = None,
    return_format: ReturnFmtType = "pandas",
    **kwargs: KwargsType,
) -> JsonOrPdType:
    """Get the FRED tags for a series search. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/series_search_related_tags.html).

    Parameters
    ----------
    search_text : str
        The text to match against.
    api_key : str | None, optional, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    return_format : : Literal["json", "pandas"] | ReturnFormat, optional
        In what format to return the response. Must be either 'json' or 'pandas'. Defaults to 'pandas'.
    **kwargs : dict, optional
        Additional parameters to FRED API ``series/observation`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict | pd.DataFrame
        Either a pandas dataframe or json. Defaults to pandas dataframe.

    """
    return_format = ReturnFormat(return_format)

    params = _convert_pydantic_model_to_dict(SeriesSearchParameters(**kwargs))
    fparams = frozenset(
        {
            "series_search_text": search_text,
            **params,
        }.items()
    )

    response = _get_request(
        endpoint="series/search/tags",
        api_key=api_key,
        params=fparams,
    )

    if return_format == ReturnFormat.pandas:
        return _convert_to_pandas(response["tags"])

    return response


def search_series_related_tags(
    search_text: str,
    tag_names: str,
    api_key: ApiKeyType = None,
    return_format: ReturnFmtType = "pandas",
    **kwargs,
) -> JsonOrPdType:
    """Get the related FRED tags for one or more FRED tags matching a series search. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/series_search_related_tags.html).

    Parameters
    ----------
    search_text : str
        The text to match against.
    tag_names : str
        A semicolon delimited list of tag names that series match all of.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    return_format : : Literal["json", "pandas"] | ReturnFormat, optional
        In what format to return the response. Must be either 'json' or 'pandas'. Defaults to 'pandas'.
    **kwargs : dict, optional
        Additional parameters to FRED API ``series/observation`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict | pd.DataFrame
        Either a pandas dataframe or json. Defaults to pandas dataframe.

    """
    return_format = ReturnFormat(return_format)

    params = _convert_pydantic_model_to_dict(SeriesSearchParameters(**kwargs))
    fparams = frozenset(
        {
            "series_search_text": search_text,
            "tag_names": tag_names,
            **params,
        }.items()
    )

    response = _get_request(
        endpoint="series/search/related_tags",
        api_key=api_key,
        params=fparams,
    )

    if return_format == ReturnFormat.pandas:
        return pd.DataFrame.from_dict(response["tags"])
    return response
