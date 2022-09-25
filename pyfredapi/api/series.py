import webbrowser
from typing import List, Literal, Optional, Union

import pandas as pd
from pydantic import BaseModel, Extra, PositiveInt

from .base import RETURN_FORMAT, FredBase, Json, JsonOrPandas, ReturnFormat


class SeriesArgs(BaseModel):
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

    class Config:
        extra = Extra.forbid


class SeriesSearchArgs(BaseModel):
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
    filter_variable: Optional[
        Literal["frequency", "units", "seasonal_adjustment"]
    ] = None
    filter_values: Optional[str] = None
    tag_names: Optional[str] = None
    exclude_tag_names: Optional[str] = None

    class Config:
        extra = Extra.forbid


class SeriesInfo(BaseModel):
    """Represents an economics data series information. https://fred.stlouisfed.org/docs/api/fred/series.html."""

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
    notes: str
    _base_url: str = "https://fred.stlouisfed.org/series"

    def open_url(self):
        """Open the FRED webpage for the given series."""
        webbrowser.open(f"{self._base_url}/{self.id}", new=2)


class FredSeries(FredBase):
    """FRED API series endpoints."""

    _earliest_realtime_start: str = "1776-07-04"
    _latest_realtime_end: str = "9999-12-31"

    def get_series_info(self, series_id: str, **kwargs) -> SeriesInfo:
        """Get an economic data series information by ID. https://fred.stlouisfed.org/docs/api/fred/series.html.

        Parameters
        ----------
        series_id : str
            Series id of interest.
        **kwargs : dict, optional
            Extra arguments to FRED API series/ endpoint. Refer the FRED documentation for a list of all possible arguments.

        Returns
        -------
        SeriesInfo object.
        """
        params = SeriesArgs(**kwargs)
        response = self._get(
            endpoint="series",
            params={
                "series_id": series_id,
                **params.dict(exclude_none=True),
            },
        )
        return SeriesInfo(**response["seriess"][0])

    def get_series_categories(self, series_id: str, **kwargs) -> Json:
        """Get the categories for an economic data series by ID. https://fred.stlouisfed.org/docs/api/fred/series_categories.html.

        Parameters
        ----------
        series_id : str
            Series id of interest.
        **kwargs : dict, optional
            Extra arguments to FRED API series/categories endpoint. Refer the FRED documentation for a list of all possible arguments.

        Returns
        -------
        Dictionary representing the json response.
        """
        params = SeriesArgs(**kwargs)
        return self._get(
            endpoint="series/categories",
            params={
                "series_id": series_id,
                **params.dict(exclude_none=True),
            },
        )

    def get_series_data(
        self,
        series_id: str,
        return_format: Union[RETURN_FORMAT, ReturnFormat] = "pandas",
        **kwargs,
    ) -> JsonOrPandas:
        """Get the observations or data values for an economic data series by ID. https://fred.stlouisfed.org/docs/api/fred/series_observations.html.

        Parameters
        ----------
        series_id : str
            Series id of interest.
        return_format : Literal["json", "pandas"] | ReturnFormat, optional
            Define how to return the response. Must be either 'json' or 'pandas'. Defaults to 'pandas'.
        **kwargs : dict, optional
            Extra arguments to FRED API series/observations endpoint. Refer the FRED documentation for a list of all possible arguments.

        Returns
        -------
        Either a pandas dataframe or json. Defaults to pandas dataframe.
        """
        return_format = ReturnFormat(return_format)

        params = SeriesArgs(**kwargs)
        response = self._get(
            endpoint="series/observations",
            params={
                "series_id": series_id,
                **params.dict(exclude_none=True),
            },
        )

        if return_format == ReturnFormat.pandas:
            return pd.DataFrame.from_dict(response["observations"])
        return response

    def get_series_releases(self, series_id: str, **kwargs) -> Json:
        """Get the FRED release for an economic data series by ID. https://fred.stlouisfed.org/docs/api/fred/series_release.html.

        Parameters
        ----------
        series_id : str
            Series id of interest.
        **kwargs : dict, optional
            Extra arguments to FRED API series/releases endpoint. Refer the FRED documentation for a list of all possible arguments.

        Returns
        -------
        Dictionary representing the json response.
        """
        params = SeriesArgs(**kwargs)
        return self._get(
            endpoint="series/releases",
            params={
                "series_id": series_id,
                **params.dict(exclude_none=True),
            },
        )

    def get_series_tags(self, series_id: str, **kwargs) -> Json:
        """Get the FRED tags for an economic data series by ID. https://fred.stlouisfed.org/docs/api/fred/series_tags.html.

        Parameters
        ----------
        series_id : str
            Series id of interest.
        **kwargs : dict, optional
            Extra arguments to FRED API series/tags endpoint. Refer the FRED documentation for a list of all possible arguments.

        Returns
        -------
        Dictionary representing the json response.
        """
        params = SeriesArgs(**kwargs)
        return self._get(
            endpoint="series/tags",
            params={
                "series_id": series_id,
                **params.dict(exclude_none=True),
            },
        )

    def get_series_updates(self, series_id: str, **kwargs) -> Json:
        """Get the FRED updates for an economic data series by ID. https://fred.stlouisfed.org/docs/api/fred/series_updates.html.

        Parameters
        ----------
        series_id : str
            Series id of interest.
        **kwargs : dict, optional
            Extra arguments to FRED API series/updates endpoint. Refer the FRED documentation for a list of all possible arguments.

        Returns
        -------
        Dictionary representing the json response.
        """
        params = SeriesArgs(**kwargs)
        return self._get(
            endpoint="series/updates",
            params={
                "series_id": series_id,
                **params.dict(exclude_none=True),
            },
        )

    def get_series_vintagedates(self, series_id: str, **kwargs) -> List[str]:
        """Get the dates in history when a series' data values were revised or new data values were released.

        Vintage dates are the release dates for a series excluding release dates when the data for the series did not change. https://fred.stlouisfed.org/docs/api/fred/series_vintagesdates.html.

        Parameters
        ----------
        series_id : str
            Series id of interest.
        **kwargs : dict, optional
            Extra arguments to FRED API series/vintagedates endpoint. Refer the FRED documentation for a list of all possible arguments.

        Returns
        -------
        List of strings representing the the available vintage dates
        """
        params = SeriesArgs(**kwargs)
        response = self._get(
            endpoint="series/vintagedates",
            params={
                "series_id": series_id,
                **params.dict(exclude_none=True),
            },
        )
        return response["vintage_dates"]

    def get_series_all_releases(
        self,
        series_id: str,
        return_format: Union[RETURN_FORMAT, ReturnFormat] = "pandas",
        **kwargs,
    ) -> JsonOrPandas:
        """Get the observations or data values for all releases an economic data series by ID.

        Parameters
        ----------
        series_id : str
            Series id of interest.
        return_format : Literal["json", "pandas"] | ReturnFormat, optional
            In what format to return the response. Must be either 'json' or 'pandas'. Defaults to 'pandas'.
        **kwargs : dict, optional
            Extra arguments to FRED API series/observation endpoint. Refer the FRED documentation for a list of all possible arguments.

        Returns
        -------
        Either a pandas dataframe or json. Defaults to pandas dataframe.
        """
        return_format = ReturnFormat(return_format)

        params = SeriesArgs(**kwargs)
        return self.get_series_data(
            series_id=series_id,
            return_format=return_format,
            **{
                "realtime_start": self._earliest_realtime_start,
                "realtime_end": self._latest_realtime_end,
                **params.dict(exclude_none=True),
            },
        )

    def get_series_initial_release(
        self,
        series_id: str,
        return_format: Union[RETURN_FORMAT, ReturnFormat],
        **kwargs,
    ) -> JsonOrPandas:
        """Get the observations or data values for the initial release of an economic data series.

        Includes only the the initial release of the series and excludes all revisions.

        Parameters
        ----------
        series_id : str
            Series id of interest.
        return_format : Literal["json", "pandas"] | ReturnFormat, optional
            In what format to return the response. Must be either 'json' or 'pandas'. Defaults to 'pandas'.
        **kwargs : dict, optional
            Extra arguments to FRED API series/observation endpoint. Refer the FRED documentation for a list of all possible arguments.

        Returns
        -------
        Either a pandas dataframe or json. Defaults to pandas dataframe.
        """
        return_format = ReturnFormat(return_format)

        # sanitize the kwargs to ensure the user did not
        # in inadvertently supply values for realtime_start & output_type
        _ = kwargs.pop("realtime_start")
        _ = kwargs.pop("output_type")

        params = SeriesArgs(**kwargs)
        return self.get_series_data(
            series_id=series_id,
            return_format=return_format,
            **{
                "realtime_start": self._earliest_realtime_start,
                "output_type": 4,
                **params.dict(exclude_none=True),
            },
        )

    def get_series_asof_date(
        self,
        series_id: str,
        date: str,
        return_format: Union[RETURN_FORMAT, ReturnFormat] = "pandas",
        **kwargs,
    ) -> JsonOrPandas:
        """Get the observations or data values for an economic data series made on or before a specific date.

        Retrieves the latest data known for the series as of the date provided. This includes any revisions to
        the data series made before or on the date, but excludes any revisions made after the date.

        Parameters
        ----------
        series_id : str
            Series id of interest.
        date: str
            Include only data revisions made on or before this date.
        return_format : : Literal["json", "pandas"] | ReturnFormat, optional
            In what format to return the response. Must be either 'json' or 'pandas'. Defaults to 'pandas'.
        **kwargs : dict, optional
            Extra arguments to FRED API series/observation endpoint. Refer the FRED documentation for a list of all possible arguments.

        Returns
        -------
        Either a pandas dataframe or json. Defaults to pandas dataframe.
        """
        return_format = ReturnFormat(return_format)

        params = SeriesArgs(**kwargs)
        return self.get_series_data(
            series_id=series_id,
            return_format=return_format,
            **{
                "realtime_start": self._earliest_realtime_start,
                "realtime_end": date,
                **params.dict(exclude_none=True),
            },
        )

    def search_series(
        self,
        search_text: str,
        search_type: Literal["full_text", "series_id"] = "full_text",
        return_format: Union[RETURN_FORMAT, ReturnFormat] = "pandas",
        **kwargs,
    ) -> JsonOrPandas:
        """Get economic data series that match search text. `FRED docs <https://fred.stlouisfed.org/docs/api/fred/series_search.html>`_.

        Parameters
        ----------
        search_text : str
            The word to match against.
        search_type : Literal[str]
            Defines which type of search to preform. One of the following strings: 'full_text', 'series_id'.
            `Parameter docs` <https://fred.stlouisfed.org/docs/api/fred/series_search.html#search_type>`_.
        return_format : : Literal["json", "pandas"] | ReturnFormat, optional
            In what format to return the response. Must be either 'json' or 'pandas'. Defaults to 'pandas'.
        **kwargs : dict, optional
            Extra arguments to FRED API series/observation endpoint. Refer the FRED documentation for a list of all possible arguments.

        Returns
        -------
        Either a pandas dataframe or json. Defaults to pandas dataframe.
        """
        return_format = ReturnFormat(return_format)

        params = SeriesSearchArgs(**kwargs)
        response = self._get(
            endpoint="series/search",
            params={
                "search_text": search_text,
                "search_type": search_type,
                **params.dict(exclude_none=True),
            },
        )

        if return_format == ReturnFormat.pandas:
            return pd.DataFrame.from_dict(response["seriess"])
        return response

    def search_series_tags(self):
        raise NotImplementedError

    def search_series_related_tags(self):
        raise NotImplementedError
