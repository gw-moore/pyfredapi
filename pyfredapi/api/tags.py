"""This module contains the FredTags implementation."""


from typing import Literal, Optional

from pydantic import BaseModel, Extra, PositiveInt

from .base import FredBase, Json


class TagsApiParameters(BaseModel):
    """Represents the parameters accepted by the FRED Tags endpoints."""

    realtime_start: Optional[str] = None
    realtime_end: Optional[str] = None
    tag_names: Optional[str] = None
    tag_group_id: Optional[
        Literal["freq", "gen", "geo", "geot", "rls", "seas", "src", "cc"]
    ] = None
    search_text: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[PositiveInt] = None
    order_by: Optional[
        Literal["series_count", "popularity", "created", "name", "group_id"]
    ] = None
    sort_order: Optional[Literal["acs", "desc"]] = None
    exclude_tag_names: Optional[str] = None

    class Config:
        extra = Extra.allow


class FredTags(FredBase):
    def get_tags(self, **kwargs) -> Json:
        """Get FRED tags. https://fred.stlouisfed.org/docs/api/fred/tags.html.

        Parameters
        ----------
        **kwargs : dict, optional
            Additional parameters to FRED API tags/ endpoint. Refer to the FRED documentation for a list of all possible parameters.
        """
        params = TagsApiParameters(**kwargs)
        return self._get(
            endpoint="tags",
            params={**params.dict(exclude_none=True)},
        )

    def get_related_tags(self, tag_names: str, **kwargs) -> Json:
        """Get related FRED tags for one or more FRED tags. https://fred.stlouisfed.org/docs/api/fred/related_tags.html.

        Parameters
        ----------
        tag_names : str
            A semicolon delimited list of tag names that series match all of.
        **kwargs : dict, optional
            Additional parameters to FRED API related_tags/ endpoint. Refer to the FRED documentation for a list of all possible parameters.
        """
        params = TagsApiParameters(
            tag_names=tag_names,
            **kwargs,
        )
        return self._get(
            endpoint="related_tags",
            params={**params.dict(exclude_none=True)},
        )

    def get_series_matching_tags(self, tag_names: str, **kwargs):
        """Get the series matching all tags in the tag_names parameter. https://fred.stlouisfed.org/docs/api/fred/tags_series.html.

        Parameters
        ----------
        tag_names : str
            A semicolon delimited list of tag names that series match all of.
        **kwargs : dict, optional
            Additional parameters to FRED API tags/series endpoint. Refer to the FRED documentation for a list of all possible parameters.
        """
        params = TagsApiParameters(**kwargs)
        return self._get(
            endpoint="tags/series",
            params={
                "tag_names": tag_names,
                **params.dict(exclude_none=True),
            },
        )
