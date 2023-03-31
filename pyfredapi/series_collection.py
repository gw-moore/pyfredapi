"""The series_collection module contains the SeriesCollection implementation.

SeriesCollection is meant to make handling multiple series easier. Often users of the FRED API will want analyze multiple economic series. This can be done with `FredSeries` alone, but can be tedious and cumbersome.
`pyfredapi` offers the `SeriesCollection` class to streamline the process of collecting and munging the data for plotting and analysis.
"""

from dataclasses import dataclass
from typing import Callable, Dict, List, Union

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure
from rich.console import Console

from pyfredapi._base import _get_api_key
from pyfredapi.series import SeriesInfo, get_series, get_series_info

console = Console()


date_cols = ["date", "realtime_start", "realtime_end"]


@dataclass
class SeriesData:
    """Represents the response from ``series/observations`` endpoint.

    Parameters
    ----------
    info : SeriesInfo
        A series info object.
    data : pd.DataFrame
        Series data in a pandas dataframe.
    """

    info: SeriesInfo
    df: pd.DataFrame

    def plot(self) -> Figure:
        """Create a `plotly <https://plotly.com/python/>`_ time series plot.

        Raises
        ------
        ValueError
            If data format is not a pandas dataframe.

        Returns
        -------
        Figure
            A `plotly figure <https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html>`_.
        """
        if not isinstance(self.df, pd.DataFrame):
            raise ValueError(
                "Plots can only be created when data is returned as a pandas dataframe."
            )

        value_col = [c for c in self.df.columns.tolist() if c not in date_cols]

        def format_title(title, start_date: str, end_date: str, subtitle=None):
            title = f"{title}, {start_date} - {end_date}"
            if not subtitle:
                return title
            subtitle = f"<sup>{subtitle}</sup>"
            return f"{title}<br>{subtitle}"

        fig = px.line(
            data_frame=self.df,
            x="date",
            y=value_col,
            title=format_title(
                title=self.info.title,
                start_date=self.info.observation_start,
                end_date=self.info.observation_end,
                subtitle=f"{self.info.seasonal_adjustment}, {self.info.units}",
            ),
            color_discrete_sequence=px.colors.qualitative.Safe,
            labels=dict(
                value=f"{self.info.id}",
                date="Date",
                variable="Series",
            ),
        )

        fig.update_layout(showlegend=False)

        return fig


def _rename_series(
    series_data: SeriesData,
    rename: Union[Dict[str, str], Callable[[str], str], None] = None,
):
    """Rename series with a dictionary or title parsing function."""
    if not isinstance(rename, dict) and not callable(rename):
        raise TypeError(
            f"`Rename` argument must be a dictionary or function, not {type(rename)}."
        )

    if isinstance(rename, dict):
        series_name = rename.get(series_data.info.id, None)
    elif callable(rename):
        series_name = rename(series_data.info.title)

    if series_name is None or rename is None:
        series_name = series_data.info.id

    return series_name


class SeriesCollection:
    """A collection of pyfredapi.SeriesData objects.

    Useful when you need to collect and manage multiple economic series. Provides methods
    for listing metadata, collecting data, and merging data together in long or wide formats.
    """

    def __init__(self, api_key: Union[str, None] = None):
        """Create instance of SeriesCollection.

        Parameters
        ----------
        api_key : str | None
            FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
        """
        if api_key is None:
            self.api_key = _get_api_key()
        self.data: Dict[str, SeriesData] = {}

    def rename_series(self, rename):
        """Rename series columns."""
        for series_id, series_data in self.data.items():
            series_name = _rename_series(series_data=series_data, rename=rename)

            orig_col_name = [
                c
                for c in self.data[series_id].df.columns.tolist()
                if c not in date_cols
            ].pop()

            self.data[series_id].df.rename(columns={orig_col_name: series_name}, inplace=True)  # type: ignore

    def add_series(
        self,
        series_ids: Union[str, List[str]],
        drop_realtime: bool = True,
        rename: Union[Dict[str, str], Callable[[str], str], None] = None,
        **kwargs,
    ) -> None:
        """Add series to class instance.

        A request to the FRED api will be made for the series. The data will
        be formatted as as pandas dataframe.

        After adding a series, you can access it via an attribute or
        in the responses dict.

        Parameters
        ----------
        series_ids : Union[str, List[str]]
            Series to add to collection.
        drop_realtime : bool
            Indicates if you want to drop the realtime columns.
        rename : Union[Dict[str, str], Callable[[str], str], None]
            Label to give series. Defaults to series ID.
        **kwargs : dict, optional
            Additional parameters to FRED API series/ endpoint. Refer to the FRED documentation for a list of all possible parameters.
        """
        if isinstance(series_ids, str):
            series_ids = [series_ids]

        for series_id in series_ids:
            if series_id in self.data:
                print(f"Already have {series_id}")
                continue

            print(f"Requesting series {series_id}...")

            df = get_series(series_id=series_id, api_key=self.api_key, **kwargs)
            assert isinstance(df, pd.DataFrame)  # noqa: S101

            series_data = SeriesData(info=get_series_info(series_id=series_id), df=df)

            if drop_realtime:
                series_data.df.drop(
                    ["realtime_start", "realtime_end"], inplace=True, axis=1
                )
            if rename:
                series_name = _rename_series(series_data, rename)
            else:
                series_name = series_data.info.id

            series_data.df.rename(columns={"value": series_name}, inplace=True)
            self.data[series_id] = series_data
            setattr(self, series_id, series_data)

    def drop_series(self, series_ids: Union[str, List[str]]) -> None:
        """Drop series from collection.

        Parameters
        ----------
        series_ids : Union[str, List[str]]
            Series ids to remove from collection.
        """
        if isinstance(series_ids, str):
            series_ids = [series_ids]

        for series_id in series_ids:
            try:
                del self.data[series_id]
            except KeyError:
                raise ValueError from KeyError(f"No series '{series_id}' in collection")

            delattr(self, series_id)
            print(f"Removed series {series_id}")

    def merge_long(self, col_name: Union[str, None] = None) -> pd.DataFrame:
        """Merge the series in the collection into a long pandas dataframe.

        Parameters
        ----------
        col_name : str | None
            Name to give columns holding the series id/label.

        Returns
        -------
        pd.DataFrame
            Long pandas dataframe.
        """
        if col_name is None:
            col_name = "series"

        long_df_prep = []
        for series in list(self.data.values()):
            series_name = [
                c for c in series.df.columns.tolist() if c not in date_cols
            ].pop()
            long_df = series.df.copy()
            long_df = long_df.rename(columns={series_name: "value"})
            long_df[col_name] = series_name
            long_df_prep.append(long_df)

        return pd.concat(long_df_prep, axis=0).reset_index(drop=True)

    def merge_wide(self) -> pd.DataFrame:
        """Merge the series in the collection into a wide pandas dataframe. Only works if all the series in the collection share the same date index.

        Returns
        -------
        pd.DataFrame
            Wide pandas dataframe.
        """
        wide_df_prep = [
            series.df.copy().set_index("date") for series in list(self.data.values())  # type: ignore
        ]
        wide_df = pd.concat(wide_df_prep, axis=1)
        return wide_df.reset_index()

    def merge_asof(
        self,
        base_series_id: str,
    ) -> pd.DataFrame:
        """Merge the series in the collection into a wide pandas dataframe based on nearest date.

        Uses pandas `merge_asof` methods to merge the data based on nearest date.

        Parameters
        ----------
        base_series_id: str
            Series ID of the series to serve of the basis for joining.

        Returns
        -------
        pd.DataFrame
            Wide pandas dataframe.
        """
        base_df = self.data[base_series_id].df.copy()
        for series_data in list(self.data.values()):
            if base_series_id == series_data.info.id:
                continue
            df = series_data.df.copy()
            base_df = pd.merge_asof(left=base_df, right=df, on="date")  # type: ignore

        return base_df  # type: ignore

    def list_series(self) -> None:
        """List the series' id and title."""
        for series_data in list(self.data.values()):
            console.print(f"{series_data.info.id}: {series_data.info.title}")

    def list_seasonality(self) -> None:
        """List the series' seasonality."""
        seasonal_adjustments = [
            series_data.info.seasonal_adjustment
            for series_data in list(self.data.values())
        ]
        distinct_seasonality = set(seasonal_adjustments)

        if len(distinct_seasonality) == 1:
            print(f"All series are {distinct_seasonality.pop()}")
            return

        for season in distinct_seasonality:
            console.rule(f"[bold red]Series that are {season}")
            for series_data in list(self.data.values()):
                if series_data.info.seasonal_adjustment == season:
                    console.print(f"{series_data.info.id}: {series_data.info.title}")

    def list_frequency(self) -> None:
        """List the series' frequency."""
        frequencies = [
            series_data.info.frequency for series_data in list(self.data.values())
        ]
        distinct_freq = set(frequencies)

        if len(distinct_freq) == 1:
            print(f"All series are {distinct_freq.pop()}")
            return

        for freq in distinct_freq:
            console.rule(f"[bold red]Series that are published {freq}")
            for series_data in list(self.data.values()):
                if series_data.info.frequency == freq:
                    console.print(f"{series_data.info.id}: {series_data.info.title}")

    def list_units(self) -> None:
        """List the series' measurement units."""
        units = [series_data.info.units for series_data in list(self.data.values())]
        distinct_units = set(units)

        if len(distinct_units) == 1:
            print(f"All series are that are measured in {distinct_units.pop()}")
            return

        for unit in distinct_units:
            console.rule(f"[bold red]Series that are measured in {unit}")
            for series_data in list(self.data.values()):
                if series_data.info.units == unit:
                    console.print(f"{series_data.info.id}: {series_data.info.title}")

    def list_end_date(self) -> None:
        """List the series' latest date."""
        end_dates = [
            series_data.info.observation_end for series_data in list(self.data.values())
        ]
        distinct_end_dates = set(end_dates)

        if len(distinct_end_dates) == 1:
            print(f"All series end on {distinct_end_dates.pop()}")
            return

        for date in distinct_end_dates:
            console.rule(f"[bold red]Series that end on {date}")
            for series_data in list(self.data.values()):
                if series_data.info.observation_end == date:
                    console.print(f"{series_data.info.id}: {series_data.info.title}")

    def list_start_date(self) -> None:
        """List the series' earliest date."""
        start_dates = [
            series_data.info.observation_start
            for series_data in list(self.data.values())
        ]
        distinct_start_dates = set(start_dates)

        if len(distinct_start_dates) == 1:
            print(f"All series start on {distinct_start_dates.pop()}")
            return

        for date in distinct_start_dates:
            console.rule(f"[bold red]Series that start on {date}")
            for series_data in list(self.data.values()):
                if series_data.info.observation_start == date:
                    console.print(f"{series_data.info.id}: {series_data.info.title}")

    def plot(self):
        """Make a basic plotly time series plot with all series in the collection."""
        raise NotImplementedError

    def extract_series(self):
        """Return a new instance of SeriesCollection, with a subset of data from this instance."""
        raise NotImplementedError
