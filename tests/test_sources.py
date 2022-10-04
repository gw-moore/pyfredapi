import pytest

from pyfredapi.api.sources import FredSources

from .conftest import base_request


@pytest.fixture()
def client():
    return FredSources()


@pytest.mark.vcr()
def test_get_sources(client):
    actual = client.get_sources()
    expected = base_request(endpoint="sources").json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_source(client):
    actual = client.get_source(source_id=1)
    expected = base_request(endpoint="source", extra_params={"source_id": 1}).json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_source_release(client):
    actual = client.get_source_release(source_id=1)
    expected = base_request(
        endpoint="source/releases", extra_params={"source_id": 1}
    ).json()

    assert actual == expected
