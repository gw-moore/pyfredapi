import pytest

from pyfredapi.tags import get_related_tags, get_series_matching_tags, get_tags

from .conftest import get_request


@pytest.mark.vcr()
def test_get_tags():
    actual = get_tags()
    expected = get_request(endpoint="tags").json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_related_tags():
    actual = get_related_tags(tag_names="nation")
    expected = get_request(
        endpoint="related_tags", extra_params={"tag_names": "nation"}
    ).json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_tag_series():
    actual = get_series_matching_tags(tag_names="slovenia;food;oecd")
    expected = get_request(
        endpoint="tags/series", extra_params={"tag_names": "slovenia;food;oecd"}
    ).json()

    assert actual == expected
