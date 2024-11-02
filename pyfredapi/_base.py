"""The `_base` module contains the get request functions used in the pyfredapi modules.

The `_base` module is not intended to be used directly by the user. It is used by the other
functions in pyfredapi.
"""

from functools import lru_cache
from http import HTTPStatus
from os import environ
from typing import Union

import requests
from pydantic import BaseModel, ConfigDict

from .exceptions import APIKeyNotFound, FredAPIRequestError, InvalidAPIKey
from .utils._common_type_hints import JsonType


class BaseApiParameters(BaseModel):
    """Represents the parameters accepted by all FRED Series endpoints."""

    model_config = ConfigDict(extra="forbid")

    api_key: str
    file_type: str = "json"


@lru_cache
def _get_api_key(api_key: Union[str, None] = None) -> str:
    """Get FRED_API_KEY from the environment.

    api_key : str | None
        FRED API key. Defaults to None. If None, will check for FRED_API_KEY in the environment.

    Returns
    -------
    str
        The FRED API key.

    Raises
    ------
    APIKeyNotFound
        If the api_key is None and FRED_API_KEY is not in the environment.

    """
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
    params: Union[frozenset, None] = None,
    base_url: str = "https://api.stlouisfed.org/fred",
) -> JsonType:
    """Make a get request to a FRED web service endpoint and return the response as Json.

    Base get request that child class methods utilize.

    Parameters
    ----------
    endpoint : str
        The FRED API endpoint.
    api_key : str | None, optional
        FRED API key. Defaults to None. If None, will check for FRED_API_KEY in the environment.
    params : Dict[str, Any] | None, optional
        Dictionary of query parameters. Defaults to None.
    base_url : str, optional
        Base fred url. Defaults to https://api.stlouisfed.org/fred.

    Returns
    -------
    A dictionary representing the json response.

    Raises
    ------
    FredAPIRequestError
        If the request fails.

    """
    api_key = _get_api_key(api_key)
    _base_params = BaseApiParameters(api_key=api_key)

    if not params:
        params = frozenset({}.items())

    fparams = dict(params)

    try:
        response = requests.get(
            f"{base_url}/{endpoint}",
            params={**_base_params.model_dump(), **fparams},
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
