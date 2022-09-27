import os
from typing import Dict, Optional

import pandas as pd
import pytest
import requests

from pyfredapi import FredSeries
from pyfredapi.api.series import SeriesData, SeriesInfo
from pyfredapi.api.utils import _convert_to_pandas

from .conftest import BASE_FRED_URL

base_params = {
    "api_key": os.environ.get("FRED_API_KEY", None),
    "file_type": "json",
    "series_id": "GDP",
}


@pytest.fixture()
def client():
    return FredSeries()


def series_request(
    endpoint: str,
    extra_params: Optional[Dict[str, str]] = None,
    base_params: Dict[str, str] = base_params,
):
    if extra_params is None:
        extra_params = {}

    return requests.get(
        f"{BASE_FRED_URL}/{endpoint}",
        params={**base_params, **extra_params},
    )


@pytest.mark.vcr()
def test_get_series_info(client):
    actual = client.get_series_info(base_params["series_id"])
    assert isinstance(actual, SeriesInfo)


@pytest.mark.vcr()
def test_get_series_categories(client):
    actual = client.get_series_categories(series_id=base_params["series_id"])
    actual = series_request("series/categories").json()
    assert isinstance(actual, dict)
    assert actual == actual


@pytest.mark.vcr()
@pytest.mark.parametrize("return_type", ["json", "pandas"])
def test_get_series(client, return_type):
    actual = client.get_series(
        series_id=base_params["series_id"], return_format=return_type
    )
    assert isinstance(actual, SeriesData)
    assert isinstance(actual.info, SeriesInfo)

    expected = series_request("series/observations").json()["observations"]

    if return_type == "json":
        assert isinstance(actual.data, list)
        assert expected == actual.data
    elif return_type == "pandas":
        assert isinstance(actual.data, pd.DataFrame)
        pd.testing.assert_frame_equal(_convert_to_pandas(expected), actual.data)


@pytest.mark.vcr()
def test_get_series_releases(client):
    actual = client.get_series_releases(series_id=base_params["series_id"])
    expected = series_request("series/release").json()
    assert isinstance(actual, dict)
    assert expected == actual


@pytest.mark.vcr()
def test_get_series_tags(client):
    actual = client.get_series_tags(series_id=base_params["series_id"])
    expected = series_request("series/tags").json()
    assert isinstance(actual, dict)
    assert expected == actual


@pytest.mark.vcr()
def test_get_series_updates(client):
    actual = client.get_series_updates(series_id=base_params["series_id"])
    expected = series_request("series/updates").json()
    assert isinstance(actual, dict)
    assert expected == actual


@pytest.mark.vcr()
def test_get_series_vintagedates(client):
    actual = client.get_series_vintagedates(series_id=base_params["series_id"])
    expected = series_request("series/vintagedates").json()["vintage_dates"]
    assert isinstance(actual, list)
    assert expected == actual


@pytest.mark.vcr()
@pytest.mark.parametrize("return_type", ["json", "pandas"])
def test_get_series_all_releases(client, return_type):
    actual = client.get_series_all_releases(
        series_id=base_params["series_id"], return_format=return_type
    )
    assert isinstance(actual, SeriesData)
    assert isinstance(actual.info, SeriesInfo)

    expected = series_request(
        "series/observations",
        {
            "realtime_start": "1776-07-04",
            "realtime_end": "9999-12-31",
        },
    ).json()["observations"]

    if return_type == "json":
        assert isinstance(actual.data, list)
        assert expected == actual.data
    elif return_type == "pandas":
        assert isinstance(actual.data, pd.DataFrame)
        pd.testing.assert_frame_equal(_convert_to_pandas(expected), actual.data)


@pytest.mark.vcr()
@pytest.mark.parametrize("return_type", ["json", "pandas"])
def test_get_series_initial_release(client, return_type):
    actual = client.get_series_initial_release(
        series_id=base_params["series_id"], return_format=return_type
    )
    assert isinstance(actual, SeriesData)
    assert isinstance(actual.info, SeriesInfo)

    expected = series_request(
        "series/observations",
        {
            "realtime_start": "1776-07-04",
            "output_type": "4",
        },
    ).json()["observations"]

    if return_type == "json":
        assert isinstance(actual.data, list)
        assert expected == actual.data
    elif return_type == "pandas":
        assert isinstance(actual.data, pd.DataFrame)
        pd.testing.assert_frame_equal(_convert_to_pandas(expected), actual.data)


@pytest.mark.vcr()
@pytest.mark.parametrize("return_type", ["json", "pandas"])
def test_get_series_asof_date(client, return_type):
    actual = client.get_series_asof_date(
        series_id=base_params["series_id"], date="2019-01-01", return_format=return_type
    )
    assert isinstance(actual, SeriesData)
    assert isinstance(actual.info, SeriesInfo)

    expected = series_request(
        "series/observations",
        {
            "realtime_start": "1776-07-04",
            "realtime_end": "2019-01-01",
        },
    ).json()["observations"]

    if return_type == "json":
        assert isinstance(actual.data, list)
        assert expected == actual.data
    elif return_type == "pandas":
        assert isinstance(actual.data, pd.DataFrame)
        pd.testing.assert_frame_equal(_convert_to_pandas(expected), actual.data)


@pytest.mark.vcr()
@pytest.mark.parametrize("return_type", ["json", "pandas"])
def test_search_series(client, return_type):
    actual = client.search_series(
        search_text="monetary+service+index",
        return_format=return_type,
    )
    expected = series_request(
        "series/search",
        {"search_text": "monetary+service+index"},
    ).json()

    if return_type == "json":
        assert isinstance(actual, dict)
        assert "seriess" in actual
        assert expected == actual
    elif return_type == "pandas":
        assert isinstance(actual, pd.DataFrame)
        pd.testing.assert_frame_equal(_convert_to_pandas(expected["seriess"]), actual)


@pytest.mark.vcr()
@pytest.mark.parametrize("return_type", ["json", "pandas"])
def test_search_series_tags(client, return_type):
    search_text = "monetary+service+index"
    actual = client.search_series_tags(
        search_text=search_text,
        return_format=return_type,
    )
    expected = series_request(
        "series/search/tags",
        {"series_search_text": search_text},
        base_params={
            "api_key": os.environ.get("FRED_API_KEY", None),
            "file_type": "json",
        },
    ).json()

    if return_type == "json":
        assert isinstance(actual, dict)
        assert "tags" in actual
        assert expected == actual
    elif return_type == "pandas":
        assert isinstance(actual, pd.DataFrame)
        pd.testing.assert_frame_equal(_convert_to_pandas(expected["tags"]), actual)


@pytest.mark.vcr()
@pytest.mark.parametrize("return_type", ["json", "pandas"])
def test_search_series_related_tags(client, return_type):
    actual = client.search_series_related_tags(
        search_text="monetary+service+index",
        tag_names="30-year;frb",
        return_format=return_type,
    )
    expected = series_request(
        "series/search/related_tags",
        {
            "series_search_text": "monetary+service+index",
            "tag_names": "30-year;frb",
        },
    ).json()

    if return_type == "json":
        assert isinstance(actual, dict)
        assert "tags" in actual
        assert expected == actual
    elif return_type == "pandas":
        assert isinstance(actual, pd.DataFrame)
        pd.testing.assert_frame_equal(_convert_to_pandas(expected["tags"]), actual)
