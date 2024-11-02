"""The `maps` module provides functions to request data from the [FRED API Maps endpoints](https://fred.stlouisfed.org/docs/api/fred/#Maps).

The FRED Maps API is a web service that allows developers to write programs and build applications to harvest data and shape files of series available on the maps found
in the FRED website hosted by the Economic Research Division of the Federal Reserve Bank of St. Louis. Not all series that are in FRED have geographical data.
"""

from typing import Any, Dict, List, Literal, Optional, Union

import pandas as pd
from pydantic import BaseModel, ConfigDict

from ._base import _get_request
from .utils import _convert_pydantic_model_to_frozenset
from .utils._common_type_hints import ApiKeyType, JsonType, ReturnFmtType
from .utils.enums import ReturnFormat

_geo_fred_url = "https://api.stlouisfed.org/geofred/"


class MapApiParameters(BaseModel):
    """Represents the parameters accepted by the FRED Maps endpoints."""

    model_config = ConfigDict(extra="allow")

    shape: Optional[
        Literal[
            "bea",
            "msa",
            "frb",
            "necta",
            "state",
            "country",
            "county",
            "censusregion",
            "censusdivision",
        ]
    ] = None
    series_id: Optional[str] = None
    date: Optional[str] = None
    start_date: Optional[str] = None


class GeoseriesInfo(BaseModel):
    """Represents geo series information. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/geofred/series_group.html)."""

    model_config = ConfigDict(extra="allow")

    title: str
    region_type: str
    series_group: str
    season: str
    units: str
    frequency: str
    min_date: str
    max_date: str


class GeoseriesData(BaseModel):
    """Represents metadata about an economics data series. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/series.html)."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    info: GeoseriesInfo
    data: Union[Dict[str, List[Dict[str, Any]]], pd.DataFrame]


def get_geoseries_info(series_id: str, api_key: ApiKeyType = None) -> GeoseriesInfo:
    """Request the metadata for a given geo series id. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/geofred/series_group.html).

    Parameters
    ----------
    series_id : str
        Series id of interest.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.

    Returns
    -------
    GeoseriesInfo
        An instance of GeoseriesInfo.

    """
    params = _convert_pydantic_model_to_frozenset(MapApiParameters(series_id=series_id))
    response = _get_request(
        base_url=_geo_fred_url,
        endpoint="series/group",
        api_key=api_key,
        params=params,
    )
    return GeoseriesInfo(**response["series_group"])


def get_shape_files(
    shape: Literal[
        "bea",
        "msa",
        "frb",
        "necta",
        "state",
        "country",
        "county",
        "censusregion",
        "censusdivision",
    ],
    api_key: ApiKeyType = None,
) -> JsonType:
    """Request shape files from FRED in Well-known text (WKT) format.

    Parameters
    ----------
    shape : One of "bea", "msa", "frb", "necta", "state", "country", "county", "censusregion", "censusdivision"
        Define the shape of Well-known text (WKT) data.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.

    Returns
    -------
    dict
        Dictionary representing the json response.

    """
    params = _convert_pydantic_model_to_frozenset(MapApiParameters(shape=shape))
    return _get_request(
        base_url=_geo_fred_url,
        endpoint="shapes/file",
        api_key=api_key,
        params=params,
    )


def get_geoseries(
    series_id: str,
    api_key: ApiKeyType = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    return_format: ReturnFmtType = "pandas",
) -> GeoseriesData:
    """Request a cross section of regional data for a specified release date. If no date is specified, the most recent data available are returned.

    For example, you can request Per Capita Personal Income by State (series_id: WIPCPI) over a specific time period.
    [Endpoint documentation](https://fred.stlouisfed.org/docs/api/geofred/series_data.html).

    Parameters
    ----------
    series_id : str
        Series id of interest. Not all series that are in FRED have geographical data.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    start_date : str, optional
        Define start date. YYYY-MM-DD formatted string.
    end_date : str, optional
        Define the end date. YYYY-MM-DD formatted string.
    return_format : Literal[json, pandas] | ReturnFormat
        Define how to return the response. Must be either 'json' or 'pandas'. Defaults to 'pandas'.

    Returns
    -------
    GeoseriesData
        GeoseriesData object containing the geoseries data and metadata.

    """
    params = _convert_pydantic_model_to_frozenset(
        MapApiParameters(series_id=series_id, date=end_date, start_date=start_date)
    )
    response = _get_request(
        endpoint="series/data",
        api_key=api_key,
        params=params,
        base_url=_geo_fred_url,
    )

    geoseries_info = get_geoseries_info(series_id=series_id)

    if return_format == ReturnFormat.pandas:
        dfs = []
        for date, data in response["meta"]["data"].items():
            t = pd.DataFrame.from_dict(data)
            t["date"] = date
            t["date"] = pd.to_datetime(t["date"])
            dfs.append(t)

        return GeoseriesData(info=geoseries_info, data=pd.concat(dfs))
    else:
        return GeoseriesData(info=geoseries_info, data=response["meta"]["data"])
