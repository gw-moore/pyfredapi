import os
from typing import Dict, Optional

import pandas as pd
import pytest
import requests

from pyfredapi import FredCategory

base_params = {
    "api_key": os.environ.get("FRED_API_KEY", None),
    "file_type": "json",
    "category_id": 125,
}
BASE_FRED_URL = "https://api.stlouisfed.org/fred"


@pytest.fixture(autouse=True)
def client():
    return FredCategory()


def category_request(endpoint: str, extra_params: Optional[Dict[str, str]] = None):
    if extra_params is None:
        extra_params = {}

    return requests.get(
        f"{BASE_FRED_URL}/{endpoint}",
        params={**base_params, **extra_params},
    )


def test_get_category(client):
    resp = client.get_category(base_params["category_id"])
    assert resp is not None
    assert isinstance(resp, dict)
    assert isinstance(resp["categories"], list)
    assert category_request("category").json() == resp


def test_get_category_children(client):
    resp = client.get_category_children(base_params["category_id"])
    assert resp is not None
    assert isinstance(resp, dict)
    assert isinstance(resp["categories"], list)
    assert category_request("category/children").json() == resp


def test_get_category_related(client):
    resp = client.get_category_related(base_params["category_id"])
    assert resp is not None
    assert isinstance(resp, dict)
    assert isinstance(resp["categories"], list)
    assert category_request("category/related").json() == resp


@pytest.mark.parametrize("return_type", ["json", "pandas"])
def test_get_category_series(client, return_type):
    resp = client.get_category_series(
        category_id=base_params["category_id"],
        return_format=return_type,
    )
    actual = category_request("category/series").json()

    if return_type == "json":
        assert isinstance(resp, dict)
        assert "seriess" in resp
        assert actual == resp
    elif return_type == "pandas":
        assert isinstance(resp, pd.DataFrame)
        pd.testing.assert_frame_equal(pd.DataFrame.from_dict(actual["seriess"]), resp)


@pytest.mark.parametrize("return_type", ["json", "pandas"])
def test_get_category_tags(client, return_type):
    resp = client.get_category_tags(
        category_id=base_params["category_id"],
        return_format=return_type,
    )
    actual = category_request("category/tags").json()

    if return_type == "json":
        assert isinstance(resp, dict)
        assert "tags" in resp
        assert actual == resp
    elif return_type == "pandas":
        assert isinstance(resp, pd.DataFrame)
        pd.testing.assert_frame_equal(pd.DataFrame.from_dict(actual["tags"]), resp)


@pytest.mark.parametrize("return_type", ["json", "pandas"])
def test_get_category_related_tags(client, return_type):
    resp = client.get_category_related_tags(
        category_id=base_params["category_id"],
        return_format=return_type,
        **{"tag_names": "balance"},
    )

    actual = category_request(
        "category/related_tags", extra_params={"tag_names": "balance"}
    ).json()

    if return_type == "json":
        assert isinstance(resp, dict)
        assert "tags" in resp
        assert actual == resp
    elif return_type == "pandas":
        assert isinstance(resp, pd.DataFrame)
        pd.testing.assert_frame_equal(pd.DataFrame.from_dict(actual["tags"]), resp)
