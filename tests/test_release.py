import os

import pytest

from pyfredapi.releases import (
    get_release,
    get_release_dates,
    get_release_related_tags,
    get_release_series,
    get_release_sources,
    get_release_tables,
    get_release_tags,
    get_releases,
    get_releases_dates,
)

from .conftest import get_request

base_params = {
    "api_key": os.environ.get("FRED_API_KEY", None),
    "file_type": "json",
    "release_id": 10,
}


@pytest.mark.vcr()
def test_get_releases():
    actual = get_releases()
    expected = get_request(endpoint="releases").json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_releases_dates():
    actual = get_releases_dates()
    expected = get_request(endpoint="releases/dates").json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_release():
    actual = get_release(release_id=base_params["release_id"])
    expected = get_request(
        endpoint="release",
        extra_params={"release_id": base_params["release_id"]},
    ).json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_release_dates():
    actual = get_release_dates(release_id=base_params["release_id"])
    expected = get_request(
        endpoint="release/dates",
        extra_params={"release_id": base_params["release_id"]},
    ).json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_release_series():
    actual = get_release_series(release_id=base_params["release_id"])
    expected = get_request(
        endpoint="release/series",
        extra_params={"release_id": base_params["release_id"]},
    ).json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_release_sources():
    actual = get_release_sources(release_id=base_params["release_id"])
    expected = get_request(
        endpoint="release/sources",
        extra_params={"release_id": base_params["release_id"]},
    ).json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_release_tags():
    actual = get_release_tags(release_id=base_params["release_id"])
    expected = get_request(
        endpoint="release/tags",
        extra_params={"release_id": base_params["release_id"]},
    ).json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_release_related_tags():
    actual = get_release_related_tags(
        release_id=base_params["release_id"], tag_names="sa;foreign"
    )
    expected = get_request(
        endpoint="release/related_tags",
        extra_params={
            "release_id": base_params["release_id"],
            "tag_names": "sa;foreign",
        },
    ).json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_release_tables():
    actual = get_release_tables(release_id=base_params["release_id"])
    expected = get_request(
        endpoint="release/tables",
        extra_params={"release_id": base_params["release_id"]},
    ).json()

    assert actual == expected
