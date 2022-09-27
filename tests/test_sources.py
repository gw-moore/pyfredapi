import pytest

from pyfredapi.api.sources import FredSources

# from .conftest import BASE_FRED_URL, base_params


@pytest.fixture()
def client():
    return FredSources()


def test_get_sources():
    ...


def test_get_source():
    ...


def test_get_source_release():
    ...
