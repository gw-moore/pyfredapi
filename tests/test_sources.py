import os

import pytest

from pyfredapi.api.sources import FredSources


@pytest.fixture(autouse=True)
def client():
    return FredSources()


base_params = {
    "api_key": os.environ.get("FRED_API_KEY", None),
    "file_type": "json",
}
BASE_FRED_URL = "https://api.stlouisfed.org/fred"


def test_get_sources():
    ...


def test_get_source():
    ...


def test_get_source_release():
    ...
