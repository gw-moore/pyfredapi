import os
from unittest import mock

import pytest

from pyfredapi.api.base import FredBase, ReturnFormat
from pyfredapi.api.exceptions import (
    APIKeyNotFoundError,
    FredAPIRequestError,
    InvalidAPIKey,
)


def test_InvalidAPIKey():
    with pytest.raises(InvalidAPIKey):
        FredBase(api_key="foobar")


def test_APIKeyNotFoundError():
    with mock.patch.dict("os.environ", {}, clear=True):
        with pytest.raises(APIKeyNotFoundError):
            FredBase()


def test_api_key_property():
    assert FredBase()._api_key == os.environ.get("FRED_API_KEY")


def test_ReturnFormat():
    with pytest.raises(ValueError):
        ReturnFormat("foobar")


def test_FredAPIRequestError():
    with pytest.raises(FredAPIRequestError):
        FredBase()._get(
            endpoint="not-a-real-endpoint",
        )
