from enum import Enum
from http import HTTPStatus
from os import environ
from typing import Any, Dict, Literal, Optional, Union

import pandas as pd
import requests
from pydantic import BaseModel, Extra

from .exceptions import APIKeyNotFoundError, FredAPIRequestError, InvalidAPIKey

Json = Dict[str, Any]
JsonOrPandas = Union[Dict, pd.DataFrame]


class BaseApiArgs(BaseModel):
    api_key: str
    file_type: str = "json"

    class Config:
        extra = Extra.forbid


RETURN_FORMAT = Literal["json", "pandas"]


class ReturnFormat(str, Enum):
    json = "json"
    pandas = "pandas"


class FredBase:
    """FredBase defines the common interface shared between FRED endpoint classes.

    Parameters
    ----------
    api_key : str | None
        FRED API key. Defaults to None. If None, will search for FRED_API_KEY in environment variables.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        if self.api_key is None:
            self.api_key = environ.get("FRED_API_KEY", None)

        if self.api_key is None:
            raise APIKeyNotFoundError()

        if not self.api_key.isalnum() or len(self.api_key) != 32:
            raise InvalidAPIKey()

        self.base_url = "https://api.stlouisfed.org/fred"
        self.base_params = BaseApiArgs(api_key=self.api_key).dict()

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Json:
        """Make a get request to a FRED web service endpoint and return the response as Json.

        Base get request that child class methods utilize.

        Parameters
        ----------
        endpoint : str
            The FRED endpoint to hit.
        params : Dict[str, str] | None
            Dictionary of query parameters. Defaults to None.

        Returns
        -------
        A dictionary representing json.
        """
        if not params:
            params = {}
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}", params={**self.base_params, **params}
            )
        except requests.exceptions.RequestException as e:
            raise FredAPIRequestError(
                message=f"Error invoking Fred API: {e}", status_code=None
            )
        if response.status_code != HTTPStatus.OK:
            raise FredAPIRequestError(
                message=response.json()["error_message"],
                status_code=response.status_code,
            )

        return response.json()
