import os
from typing import Dict, Optional

import pandas as pd
import pytest
import requests

from pyfredapi.api.maps import FredMaps, GeoseriesData, GeoseriesInfo

BASE_FRED_URL = "https://api.stlouisfed.org/geofred/"

base_params = {
    "api_key": os.environ.get("FRED_API_KEY", None),
    "file_type": "json",
}


@pytest.fixture()
def client():
    return FredMaps()


def maps_request(endpoint: str, extra_params: Optional[Dict[str, str]] = None):
    if extra_params is None:
        extra_params = {}

    return requests.get(
        f"{BASE_FRED_URL}/{endpoint}",
        params={**base_params, **extra_params},
    )


@pytest.mark.vcr()
def test_get_geoseries_info(client):
    actual = client.get_geoseries_info(series_id="WIPCPI")
    response = maps_request("series/group", extra_params={"series_id": "WIPCPI"}).json()
    expected = GeoseriesInfo(**response["series_group"])
    assert isinstance(actual, GeoseriesInfo)
    assert expected == actual


@pytest.mark.vcr()
def test_get_shape_files(client):
    actual = client.get_shape_files(shape="bea")
    expected = maps_request("shapes/file", extra_params={"shape": "bea"}).json()
    assert isinstance(actual, dict)
    assert expected == actual


@pytest.mark.vcr()
@pytest.mark.parametrize("return_type", ["json", "pandas"])
def test_get_geoseries(client, return_type):
    actual = client.get_geoseries(
        series_id="WIPCPI",
        start_date="2019-01-01",
        end_date="2021-01-01",
        return_format=return_type,
    )
    assert isinstance(actual, GeoseriesData)
    assert isinstance(actual.info, GeoseriesInfo)

    expected = maps_request(
        "series/data",
        extra_params={
            "series_id": "WIPCPI",
            "start_date": "2019-01-01",
            "date": "2021-01-01",
            "return_format": "json",
        },
    ).json()

    if return_type == "json":
        assert isinstance(actual.data, dict)
        assert expected["meta"]["data"] == actual.data
    elif return_type == "pandas":
        dfs = []
        for date, data in expected["meta"]["data"].items():
            t = pd.DataFrame.from_dict(data)
            t["date"] = date
            t["date"] = pd.to_datetime(t["date"])
            dfs.append(t)

        assert isinstance(actual.data, pd.DataFrame)
        pd.testing.assert_frame_equal(pd.concat(dfs), actual.data)
