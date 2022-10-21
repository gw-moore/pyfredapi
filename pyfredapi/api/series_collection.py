"""This module contains the SeriesCollection implementation."""

from typing import Callable, Dict, List, Union

import pandas as pd
from rich.console import Console

from pyfredapi.api.series import FredSeries, SeriesData

console = Console()


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

    Parameters
    ----------
    client : FredSeries
        A FredSeries object.
    """

    def __init__(self, client: FredSeries):
        self.client = client
        self.data: Dict[str, SeriesData] = {}

    def rename_series(self, rename):
        """Rename series columns."""
        for series_id, series_data in self.data.items():
            series_name = _rename_series(series_data=series_data, rename=rename)

            orig_col_name = [
                c
                for c in self.data[series_id].data.columns.tolist()
                if c not in ["date", "realtime_start", "realtime_end"]
            ].pop()

            self.data[series_id].data.rename(columns={orig_col_name: series_name}, inplace=True)  # type: ignore

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
        series : Union[str, List[str]]
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
            series_data = self.client.get_series(series_id=series_id, **kwargs)
            if drop_realtime:
                series_data.data.drop(  # type: ignore
                    ["realtime_start", "realtime_end"], inplace=True, axis=1
                )
            if rename:
                series_name = _rename_series(series_data, rename)
            else:
                series_name = series_data.info.id

            series_data.data.rename(columns={"value": series_name}, inplace=True)  # type: ignore
            self.data[series_id] = series_data
            setattr(self, series_id, series_data)

    def drop_series(self, series_ids: Union[str, List[str]]) -> None:
        """Drop series from collection.

        Parameters
        ----------
        series : Union[str, List[str]]
            Series to remove from collection.
        """
        if isinstance(series_ids, str):
            series_ids = [series_ids]

        for series_id in series_ids:
            try:
                del self.data[series_id]
            except KeyError:
                raise ValueError(f"No series '{series_id}' in collection")

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
        Pandas dataframe.
        """
        if col_name is None:
            col_name = "series"

        long_df_prep = []
        for series in list(self.data.values()):
            series_name = [
                c
                for c in series.data.columns.tolist()  # type: ignore
                if c not in ["date", "realtime_start", "realtime_end"]
            ].pop()
            long_df = series.data.copy()
            long_df = long_df.rename(columns={series_name: "value"})  # type: ignore
            long_df[col_name] = series_name  # type: ignore
            long_df_prep.append(long_df)

        return pd.concat(long_df_prep, axis=0).reset_index(drop=True)  # type: ignore

    def merge_wide(self) -> pd.DataFrame:
        """Merge the series in the collection into a wide pandas dataframe. Only works if all the series in the collection share the same date index.

        Returns
        -------
        Pandas dataframe.
        """
        wide_df_prep = [
            series.data.copy().set_index("date") for series in list(self.data.values())  # type: ignore
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
        Pandas dataframe.
        """
        base_df = self.data[base_series_id].data.copy()
        for series_data in list(self.data.values()):
            if base_series_id == series_data.info.id:
                continue
            df = series_data.data.copy()
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
