"""This module contains the FredSources implementation."""


from typing import Literal, Optional

from pydantic import BaseModel, Extra, PositiveInt

from .base import FredBase, Json


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


class FredSources(FredBase):
    def get_sources(self, **kwargs) -> Json:
        """Get all sources of economic data. https://fred.stlouisfed.org/docs/api/fred/sources.html.

        Parameters
        ----------
        **kwargs : dict, optional
            Additional parameters to FRED API sources/ endpoint. Refer to the FRED documentation for a list of all possible parameters.

        Returns
        -------
        Dictionary representing the Json response
        """
        params = SourceApiParameters(**kwargs)
        return self._get(
            endpoint="sources",
            params=params.dict(exclude_none=True),
        )

    def get_source(self, source_id: int, **kwargs) -> Json:
        """Get a source of economic data. https://fred.stlouisfed.org/docs/api/fred/source.html.

        Parameters
        ----------
        source_id : int
            Source id of interest.
        **kwargs : dict, optional
            Additional parameters to FRED API sources/ endpoint. Refer to the FRED documentation for a list of all possible parameters.

        Returns
        -------
        Dictionary representing the Json response
        """
        params = SourceApiParameters(source_id=source_id, **kwargs)
        return self._get(
            endpoint="source",
            params=params.dict(exclude_none=True),
        )

    def get_source_release(self, source_id: int, **kwargs):
        """Get the releases for a source. https://fred.stlouisfed.org/docs/api/fred/source.html.

        Parameters
        ----------
        source_id : int
            Source id of interest.
        **kwargs : dict, optional
            Additional parameters to FRED API sources/ endpoint. Refer to the FRED documentation for a list of all possible parameters.

        Returns
        -------
        Dictionary representing the Json response
        """
        params = SourceApiParameters(source_id=source_id, **kwargs)
        return self._get(
            endpoint="source/releases",
            params=params.dict(exclude_none=True),
        )
