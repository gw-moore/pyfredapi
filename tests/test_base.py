import os
from unittest import mock

import pytest

from pyfredapi._base import _get_api_key, _get_request
from pyfredapi.exceptions import APIKeyNotFound, FredAPIRequestError, InvalidAPIKey


def test_get_api_kay():
    assert _get_api_key() == os.environ.get("FRED_API_KEY")


def test_invalid_api_key_err():
    with pytest.raises(InvalidAPIKey):
        _get_api_key(api_key="foobar")


def test_api_key_not_found_err():
    _get_api_key.cache_clear()
    with mock.patch.dict(os.environ, {}, clear=True):
        with pytest.raises(APIKeyNotFound):
            _ = _get_api_key()


def test_fredapi_request_err():
    with pytest.raises(FredAPIRequestError):
        _get_request(endpoint="not-a-real-endpoint")
