"""The `releases` module provides functions to request data from the [FRED API Releases endpoints](https://fred.stlouisfed.org/docs/api/fred/#Releases)."""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, PositiveInt

from ._base import _get_request
from .utils import _convert_pydantic_model_to_frozenset
from .utils._common_type_hints import ApiKeyType, JsonType, KwargsType


class ReleaseApiParameters(BaseModel):
    """Represents the parameters accepted by the FRED Release endpoints."""

    model_config = ConfigDict(extra="allow")

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


def get_releases(api_key: ApiKeyType = None, **kwargs: KwargsType) -> JsonType:
    """Get all releases of economic data. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/releases.html).

    Parameters
    ----------
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``releases/`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    Dictionary representing the Json response

    """
    params = _convert_pydantic_model_to_frozenset(ReleaseApiParameters(**kwargs))
    return _get_request(
        endpoint="releases",
        api_key=api_key,
        params=params,
    )


def get_releases_dates(api_key: ApiKeyType = None, **kwargs: KwargsType) -> JsonType:
    """Get release dates for all releases of economic data. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/releases_dates.html).

    Parameters
    ----------
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``releases/dates`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    Dictionary representing the Json response

    """
    params = _convert_pydantic_model_to_frozenset(ReleaseApiParameters(**kwargs))
    return _get_request(
        endpoint="releases/dates",
        api_key=api_key,
        params=params,
    )


def get_release(
    release_id: int, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get a release of economic data. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/release.html).

    Parameters
    ----------
    release_id : int
        Release id of interest.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``release/`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    Dictionary representing the Json response.

    Example
    -------
    >>> release_info = get_release(release_id=53)

    """
    params = _convert_pydantic_model_to_frozenset(
        ReleaseApiParameters(release_id=release_id, **kwargs)
    )
    return _get_request(
        endpoint="release",
        api_key=api_key,
        params=params,
    )


def get_release_dates(
    release_id: int, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get release dates for a release of economic data. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/release_dates.html).

    Parameters
    ----------
    release_id : int
        Release id of interest.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``release/dates/`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    Dictionary representing the Json response.

    """
    params = _convert_pydantic_model_to_frozenset(
        ReleaseApiParameters(release_id=release_id, **kwargs)
    )
    return _get_request(
        endpoint="release/dates",
        api_key=api_key,
        params=params,
    )


def get_release_series(
    release_id: int, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get the series on a release of economic data. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/release_series.html).

    Parameters
    ----------
    release_id : int
        Release id of interest.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API release/release_series/ endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    Dictionary representing the Json response.

    """
    params = _convert_pydantic_model_to_frozenset(
        ReleaseApiParameters(release_id=release_id, **kwargs)
    )
    return _get_request(
        endpoint="release/series",
        api_key=api_key,
        params=params,
    )


def get_release_sources(
    release_id: int, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get the sources for a release of economic data. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/release_sources.html).

    Parameters
    ----------
    release_id : int
        Release id of interest.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``release/sources/`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    Dictionary representing the Json response.

    """
    params = _convert_pydantic_model_to_frozenset(
        ReleaseApiParameters(release_id=release_id, **kwargs)
    )
    return _get_request(
        endpoint="release/sources",
        api_key=api_key,
        params=params,
    )


def get_release_tags(
    release_id: int, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get the FRED tags for a release. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/release_tags.html).

    Parameters
    ----------
    release_id : int
        Release id of interest.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``release/tags/`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    Dictionary representing the Json response.

    """
    params = _convert_pydantic_model_to_frozenset(
        ReleaseApiParameters(release_id=release_id, **kwargs)
    )
    return _get_request(
        endpoint="release/tags",
        api_key=api_key,
        params=params,
    )


def get_release_related_tags(
    release_id: int, tag_names: str, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get the related FRED tags for one or more FRED tags within a release. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/release_related_tags.html).

    Parameters
    ----------
    release_id : int
        Release id of interest.
    tag_names : str
        A semicolon delimited list of tag names that series match all of. See the related request fred/release/tags.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``release/related_tags/`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    Dictionary representing the Json response.

    """
    params = _convert_pydantic_model_to_frozenset(
        ReleaseApiParameters(release_id=release_id, tag_names=tag_names, **kwargs)
    )
    return _get_request(
        endpoint="release/related_tags",
        api_key=api_key,
        params=params,
    )


def get_release_tables(
    release_id: int, api_key: ApiKeyType = None, **kwargs: KwargsType
) -> JsonType:
    """Get release table trees for a given release. [Endpoint documentation](https://fred.stlouisfed.org/docs/api/fred/release_tables.htm).

    Parameters
    ----------
    release_id : int
        Release id of interest.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    **kwargs : dict, optional
        Additional parameters to FRED API ``release/tables/`` endpoint. Refer to the FRED documentation for a list of all possible parameters.

    Returns
    -------
    Dictionary representing the Json response.

    """
    params = _convert_pydantic_model_to_frozenset(
        ReleaseApiParameters(release_id=release_id, **kwargs)
    )
    return _get_request(
        endpoint="release/tables",
        api_key=api_key,
        params=params,
    )
