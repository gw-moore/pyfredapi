"""This module contains the FredMaps implementation."""


from typing import Any, Dict, List, Literal, Optional, Union

import pandas as pd
from pydantic import BaseModel, Extra

from .base import RETURN_FORMAT, FredBase, Json, ReturnFormat


class MapApiParameters(BaseModel):
    """Represents the parameters accepted by the FRED Maps endpoints."""

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

    class Config:
        extra = Extra.allow


class GeoseriesInfo(BaseModel):
    """Represents an economics data series information. https://fred.stlouisfed.org/docs/api/geofred/series_group.html."""

    title: str
    region_type: str
    series_group: str
    season: str
    units: str
    frequency: str
    min_date: str
    max_date: str

    class Config:
        extra = Extra.allow


class GeoseriesData(BaseModel):
    info: GeoseriesInfo
    data: Union[Dict[str, List[Dict[str, Any]]], pd.DataFrame]

    class Config:
        arbitrary_types_allowed = True


class FredMaps(FredBase):
    """Provides methods to request data from the FRED Maps API.

    The FRED Maps API is a web service that allows developers to write programs and build applications to harvest data and shape files of series available on the maps found
    in the FRED website hosted by the Economic Research Division of the Federal Reserve Bank of St. Louis. Not all series that are in FRED have geographical data.
    """

    # FredMaps requires an __init__ method because it needs to overwrite the base_url attribute in FredBase
    def __init__(self):
        super().__init__()
        self._base_url = "https://api.stlouisfed.org/geofred/"

    def get_geoseries_info(self, series_id: str) -> GeoseriesInfo:
        """Request the meta information for a given series_id. https://fred.stlouisfed.org/docs/api/geofred/series_group.html.

        Parameters
        ----------
        series_id : str
            Series id of interest.

        Returns
        -------
        An instance of GeoseriesInfo.
        """
        params = MapApiParameters(series_id=series_id)
        response = self._get(
            endpoint="series/group",
            params=params.dict(exclude_none=True),
        )
        return GeoseriesInfo(**response["series_group"])

    def get_shape_files(
        self,
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
    ) -> Json:
        """Request shape files from FRED in Well-known text (WKT) format.

        Parameters
        ----------
        shape : One of "bea", "msa", "frb", "necta", "state", "country", "county", "censusregion", "censusdivision"
            Define the shape of Well-known text (WKT) data.

        Returns
        -------
        Dictionary representing the json response.
        """
        params = MapApiParameters(shape=shape)
        return self._get(
            endpoint="shapes/file",
            params=params.dict(exclude_none=True),
        )

    def get_geoseries(
        self,
        series_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        return_format: Union[RETURN_FORMAT, ReturnFormat] = "pandas",
    ) -> GeoseriesData:
        """Request a cross section of regional data for a specified release date. If no date is specified, the most recent data available are returned.

        For example, you can request Per Capita Personal Income by State (series_id: WIPCPI) over a specific time period.
        https://fred.stlouisfed.org/docs/api/geofred/series_data.html.

        Parameters
        ----------
        series_id : str
            Series id of interest. Not all series that are in FRED have geographical data.
        start_date : str, optional
            Define start date. YYYY-MM-DD formatted string.
        end_date : str, optional
            Define the end date. YYYY-MM-DD formatted string.
        return_format : Literal["json", "pandas"] | ReturnFormat
            Define how to return the response. Must be either 'json' or 'pandas'. Defaults to 'pandas'.

        Returns
        -------
        GeoseriesData object containing the geoseries data and metadata.
        """
        params = MapApiParameters(
            series_id=series_id, date=end_date, start_date=start_date
        )
        response = self._get(
            endpoint="series/data",
            params=params.dict(exclude_none=True),
        )

        geoseries_info = self.get_geoseries_info(series_id=series_id)

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
