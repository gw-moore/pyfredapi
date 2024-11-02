"""The `tags` module provides functions to request data from the [FRED API Tags endpoints](https://fred.stlouisfed.org/docs/api/fred/#Tags).

FRED tags are assigned to series. Tags define a characteristic about the series. Each tag is a unique character identifier. For example:

- Gross Domestic Product has the tag id 'gdp'
- Not Seasonally Adjusted has the tag id 'nsa'
- Monthly has the tag id `monthly`

Categories are organized in a hierarchical structure where parent categories contain children categories. All categories are children of the root category (category_id = 0).
"""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, PositiveInt

from ._base import _get_request
from .utils import _convert_pydantic_model_to_dict, _convert_pydantic_model_to_frozenset
from .utils._common_type_hints import ApiKeyType, JsonType, KwargsType


class TagsApiParameters(BaseModel):
    """Represents the parameters accepted by the FRED Tags endpoints."""

    model_config = ConfigDict(extra="allow")

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


def get_tags(api_key: ApiKeyType = None, **kwargs: KwargsType) -> JsonType:
    """Get FRED tags.[Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/tags.html).

    Parameters
    ----------
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``tags/`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict
        A dictionary representing the json response.

    """
    params = _convert_pydantic_model_to_frozenset(TagsApiParameters(**kwargs))
    return _get_request(
        endpoint="tags",
        api_key=api_key,
        params=params,
    )


def get_related_tags(
    tag_names: str, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get related FRED tags for one or more FRED tags. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/related_tags.html).

    Parameters
    ----------
    tag_names : str
        A semicolon delimited list of tag names that series match all of.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in the environment.
    **kwargs : dict, optional
        Additional parameters to FRED API ``related_tags/`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict
        A dictionary representing the json response.

    """
    params = _convert_pydantic_model_to_frozenset(
        TagsApiParameters(tag_names=tag_names, **kwargs)
    )
    return _get_request(
        endpoint="related_tags",
        api_key=api_key,
        params=params,
    )


def get_series_matching_tags(
    tag_names: str, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get the series matching all tags in the tag_names parameter. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/tags_series.html).

    Parameters
    ----------
    tag_names : str
        A semicolon delimited list of tag names that series match all of.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``tags/series`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    dict
        A dictionary representing the json response.

    """
    params = _convert_pydantic_model_to_dict(TagsApiParameters(**kwargs))
    fparams = frozenset(
        {
            "tag_names": tag_names,
            **params,
        }.items()
    )

    return _get_request(
        endpoint="tags/series",
        api_key=api_key,
        params=fparams,
    )
