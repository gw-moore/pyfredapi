import pytest

from pyfredapi.sources import get_source, get_source_release, get_sources

from .conftest import base_request


@pytest.mark.vcr()
def test_get_sources():
    actual = get_sources()
    expected = base_request(endpoint="sources").json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_source():
    actual = get_source(source_id=1)
    expected = base_request(endpoint="source", extra_params={"source_id": 1}).json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_source_release():
    actual = get_source_release(source_id=1)
    expected = base_request(
        endpoint="source/releases", extra_params={"source_id": 1}
    ).json()

    assert actual == expected
