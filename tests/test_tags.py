import pytest

from pyfredapi.api.tags import FredTags

from .conftest import base_request


@pytest.fixture()
def client():
    return FredTags()


@pytest.mark.vcr()
def test_get_tags(client):
    actual = client.get_tags()
    expected = base_request(endpoint="tags").json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_related_tags(client):
    actual = client.get_related_tags(tag_names="nation")
    expected = base_request(
        endpoint="related_tags", extra_params={"tag_names": "nation"}
    ).json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_tag_series(client):
    actual = client.get_series_matching_tags(tag_names="slovenia;food;oecd")
    expected = base_request(
        endpoint="tags/series", extra_params={"tag_names": "slovenia;food;oecd"}
    ).json()

    assert actual == expected
