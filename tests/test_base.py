import os
from unittest import mock

import pytest

from pyfredapi.api.base import FredBase, ReturnFormat
from pyfredapi.api.exceptions import (
    APIKeyNotFoundError,
    FredAPIRequestError,
    InvalidAPIKey,
)


def test_invalid_api_key_err():
    with pytest.raises(InvalidAPIKey):
        FredBase(api_key="foobar")


def test_api_key_not_found_err():
    with mock.patch.dict("os.environ", {}, clear=True):
        with pytest.raises(APIKeyNotFoundError):
            FredBase()


def test_api_key_property():
    assert FredBase()._api_key == os.environ.get("FRED_API_KEY")


def test_return_format():
    with pytest.raises(ValueError):
        ReturnFormat("foobar")


def test_fredapi_request_err():
    with pytest.raises(FredAPIRequestError):
        FredBase()._get(
            endpoint="not-a-real-endpoint",
        )
