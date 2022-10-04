import os

import pytest

from pyfredapi.api.releases import FredRelease

from .conftest import base_request

base_params = {
    "api_key": os.environ.get("FRED_API_KEY", None),
    "file_type": "json",
    "release_id": 10,
}


@pytest.fixture()
def client():
    return FredRelease()


@pytest.mark.vcr()
def test_get_releases(client):
    actual = client.get_releases()
    expected = base_request(endpoint="releases").json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_releases_dates(client):
    actual = client.get_releases_dates()
    expected = base_request(endpoint="releases/dates").json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_release(client):
    actual = client.get_release(release_id=base_params["release_id"])
    expected = base_request(
        endpoint="release",
        extra_params={"release_id": base_params["release_id"]},
    ).json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_release_dates(client):
    actual = client.get_release_dates(release_id=base_params["release_id"])
    expected = base_request(
        endpoint="release/dates",
        extra_params={"release_id": base_params["release_id"]},
    ).json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_release_series(client):
    actual = client.get_release_series(release_id=base_params["release_id"])
    expected = base_request(
        endpoint="release/series",
        extra_params={"release_id": base_params["release_id"]},
    ).json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_release_sources(client):
    actual = client.get_release_sources(release_id=base_params["release_id"])
    expected = base_request(
        endpoint="release/sources",
        extra_params={"release_id": base_params["release_id"]},
    ).json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_release_tags(client):
    actual = client.get_release_tags(release_id=base_params["release_id"])
    expected = base_request(
        endpoint="release/tags",
        extra_params={"release_id": base_params["release_id"]},
    ).json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_release_related_tags(client):
    actual = client.get_release_related_tags(
        release_id=base_params["release_id"], tag_names="sa;foreign"
    )
    expected = base_request(
        endpoint="release/related_tags",
        extra_params={
            "release_id": base_params["release_id"],
            "tag_names": "sa;foreign",
        },
    ).json()

    assert actual == expected


@pytest.mark.vcr()
def test_get_release_tables(client):
    actual = client.get_release_tables(release_id=base_params["release_id"])
    expected = base_request(
        endpoint="release/tables",
        extra_params={"release_id": base_params["release_id"]},
    ).json()

    assert actual == expected
