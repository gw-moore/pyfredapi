"""The _base module contains the base functions used pyfredapi modules."""

from functools import lru_cache
from http import HTTPStatus
from os import environ
from typing import Any, Dict, Optional, Union

import requests
from frozendict import frozendict
from pydantic import BaseModel, Extra

from .exceptions import APIKeyNotFound, FredAPIRequestError, InvalidAPIKey
from .utils._common_type_hints import JsonType


class BaseApiParameters(BaseModel):
    """Represents the parameters accepted by all FRED Series endpoints."""

    api_key: str
    file_type: str = "json"

    class Config:
        extra = Extra.forbid


@lru_cache
def _get_api_key(api_key: Optional[str] = None) -> str:
    """Get FRED_API_KEY from the environment."""
    if api_key is None:
        api_key = environ.get("FRED_API_KEY", None)

    if api_key is None:
        raise APIKeyNotFound()
    elif not api_key.isalnum() or len(api_key) != 32:
        raise InvalidAPIKey()

    return api_key


@lru_cache
def _get_request(
    endpoint: str,
    api_key: Union[str, None] = None,
    params: Optional[Dict[str, Any]] = None,
    base_url: str = "https://api.stlouisfed.org/fred",
) -> JsonType:
    """Make a get request to a FRED web service endpoint and return the response as Json.

    Base get request that child class methods utilize.

    Parameters
    ----------
    endpoint : str
        The FRED endpoint to hit.
    api_key : str | None
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in the environment.
    params : Dict[str, Any] | None
        Dictionary of query parameters. Defaults to None.
    base_url : str, optional
        Base fred url. Defaults to https://api.stlouisfed.org/fred.

    Returns
    -------
    A dictionary representing the json response.
    """
    api_key = _get_api_key(api_key)
    _base_params = BaseApiParameters(api_key=api_key)

    if not params:
        params = {}
    try:
        response = requests.get(
            f"{base_url}/{endpoint}",
            params=frozendict({**_base_params.dict(), **params}),
            timeout=30,
        )
    except requests.exceptions.RequestException as e:
        raise FredAPIRequestError(
            message=f"Error invoking Fred API: {e}", status_code=None
        ) from e
    if response.status_code != HTTPStatus.OK:
        raise FredAPIRequestError(
            message=response.json()["error_message"],
            status_code=response.status_code,
        )

    return response.json()
