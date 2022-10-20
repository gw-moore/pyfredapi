"""This module contains the FredRelease implementation."""

from typing import Literal, Optional

from pydantic import BaseModel, Extra, PositiveInt

from .base import FredBase, Json


class ReleaseApiParameters(BaseModel):
    """Represents the parameters accepted by the FRED Release endpoints."""

    release_id: Optional[PositiveInt] = None
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
    include_release_dates_with_no_data: Optional[bool] = None
    element_id: Optional[int] = None
    tag_names: Optional[str] = None

    class Config:
        extra = Extra.allow


class FredRelease(FredBase):
    """FRED API Release Release endpoints."""

    def get_releases(self, **kwargs) -> Json:
        """Get all releases of economic data. https://fred.stlouisfed.org/docs/api/fred/releases.html.

        Parameters
        ----------
        **kwargs : dict, optional
            Additional parameters to FRED API releases/ endpoint. Refer to the FRED documentation for a list of all possible parameters.

        Returns
        -------
        Dictionary representing the Json response
        """
        params = ReleaseApiParameters(**kwargs)
        return self._get(
            endpoint="releases",
            params=params.dict(exclude_none=True),
        )

    def get_releases_dates(self, **kwargs) -> Json:
        """Get release dates for all releases of economic data. https://fred.stlouisfed.org/docs/api/fred/releases_dates.html.

        Parameters
        ----------
        **kwargs : dict, optional
            Additional parameters to FRED API releases/ endpoint. Refer to the FRED documentation for a list of all possible parameters.

        Returns
        -------
        Dictionary representing the Json response
        """
        params = ReleaseApiParameters(**kwargs)
        return self._get(
            endpoint="releases/dates",
            params=params.dict(exclude_none=True),
        )

    def get_release(self, release_id: int, **kwargs) -> Json:
        """Get a release of economic data. https://fred.stlouisfed.org/docs/api/fred/release.html.

        Parameters
        ----------
        release_id : int
            Release id of interest.
        **kwargs : dict, optional
            Additional parameters to FRED API release/ endpoint. Refer to the FRED documentation for a list of all possible parameters.

        Returns
        -------
        Dictionary representing the Json response.
        """
        params = ReleaseApiParameters(release_id=release_id, **kwargs)
        return self._get(
            endpoint="release",
            params=params.dict(exclude_none=True),
        )

    def get_release_dates(self, release_id: int, **kwargs) -> Json:
        """Get release dates for a release of economic data. https://fred.stlouisfed.org/docs/api/fred/release_dates.html.

        Parameters
        ----------
        release_id : int
            Release id of interest.
        **kwargs : dict, optional
            Additional parameters to FRED API release/release_dates/ endpoint. Refer to the FRED documentation for a list of all possible parameters.

        Returns
        -------
        Dictionary representing the Json response.
        """
        params = ReleaseApiParameters(release_id=release_id, **kwargs)
        return self._get(
            endpoint="release/dates",
            params=params.dict(exclude_none=True),
        )

    def get_release_series(self, release_id: int, **kwargs) -> Json:
        """Get the series on a release of economic data. https://fred.stlouisfed.org/docs/api/fred/release_series.html.

        Parameters
        ----------
        release_id : int
            Release id of interest.
        **kwargs : dict, optional
            Additional parameters to FRED API release/release_series/ endpoint. Refer to the FRED documentation for a list of all possible parameters.

        Returns
        -------
        Dictionary representing the Json response.
        """
        params = ReleaseApiParameters(release_id=release_id, **kwargs)
        return self._get(
            endpoint="release/series",
            params=params.dict(exclude_none=True),
        )

    def get_release_sources(self, release_id: int, **kwargs) -> Json:
        """Get the sources for a release of economic data. https://fred.stlouisfed.org/docs/api/fred/release_sources.html.

        Parameters
        ----------
        release_id : int
            Release id of interest.
        **kwargs : dict, optional
            Additional parameters to FRED API release/release_sources/ endpoint. Refer to the FRED documentation for a list of all possible parameters.

        Returns
        -------
        Dictionary representing the Json response.
        """
        params = ReleaseApiParameters(release_id=release_id, **kwargs)
        return self._get(
            endpoint="release/sources",
            params=params.dict(exclude_none=True),
        )

    def get_release_tags(self, release_id: int, **kwargs) -> Json:
        """Get the FRED tags for a release. https://fred.stlouisfed.org/docs/api/fred/release_tags.html.

        Parameters
        ----------
        release_id : int
            Release id of interest.
        **kwargs : dict, optional
            Additional parameters to FRED API release/release_tags/ endpoint. Refer to the FRED documentation for a list of all possible parameters.

        Returns
        -------
        Dictionary representing the Json response.
        """
        params = ReleaseApiParameters(release_id=release_id, **kwargs)
        return self._get(
            endpoint="release/tags",
            params=params.dict(exclude_none=True),
        )

    def get_release_related_tags(
        self, release_id: int, tag_names: str, **kwargs
    ) -> Json:
        """Get the related FRED tags for one or more FRED tags within a release. https://fred.stlouisfed.org/docs/api/fred/release_related_tags.html.

        Parameters
        ----------
        release_id : int
            Release id of interest.
        tag_names : str
            A semicolon delimited list of tag names that series match all of. See the related request fred/release/tags.
        **kwargs : dict, optional
            Additional parameters to FRED API release/related_tags/ endpoint. Refer to the FRED documentation for a list of all possible parameters.

        Returns
        -------
        Dictionary representing the Json response.
        """
        params = ReleaseApiParameters(
            release_id=release_id, tag_names=tag_names, **kwargs
        )
        return self._get(
            endpoint="release/related_tags",
            params=params.dict(exclude_none=True),
        )

    def get_release_tables(self, release_id: int, **kwargs) -> Json:
        """Get release table trees for a given release. https://fred.stlouisfed.org/docs/api/fred/release_tables.html.

        Parameters
        ----------
        release_id : int
            Release id of interest.
        **kwargs : dict, optional
            Additional parameters to FRED API release/tables/ endpoint. Refer to the FRED documentation for a list of all possible parameters.

        Returns
        -------
        Dictionary representing the Json response.
        """
        params = ReleaseApiParameters(release_id=release_id, **kwargs)
        return self._get(
            endpoint="release/tables",
            params=params.dict(exclude_none=True),
        )
